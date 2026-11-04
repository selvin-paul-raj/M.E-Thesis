"""DriftBench pilot (S2-S5): does rewrite-in-place memory drift on fixed content?

Fixed-content arm: the conversation is written into notes once (k=0), then the
memory is re-consolidated k times with NO new content (k=1..8, 1,200-word cap).
We score old-evidence LoCoMo questions at k = 0,1,2,4,8, a raw BM25S baseline
(the ceiling), and fact survival (share of k=0 facts still stated at k).
Every LLM call is cached, so rerunning this script is free.
"""
import json, random, re, csv, pathlib, sys, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "locomo10.json"
RES = ROOT / "results"; MEMD = RES / "pilot_memories"; MEMD.mkdir(parents=True, exist_ok=True)
WRITER = READER = "openai/gpt-oss-20b"
JUDGE = "openai/gpt-oss-120b"
CONVS = ["conv-26", "conv-30", "conv-49"]   # three shortest-ish dialogues
PER_CONV = 10; MIN_AGE = 5; KS = [0, 1, 2, 4, 8]; CAP_WORDS = 1200; SEED = 13


def sessions(conv):
    n = sorted(int(m.group(1)) for k in conv if (m := re.match(r"session_(\d+)$", k)))
    return [(i, conv.get(f"session_{i}_date_time", ""), conv[f"session_{i}"]) for i in n]


def select(c):
    conv = c["conversation"]; ns = max(i for i, _, _ in sessions(conv))
    pool = []
    for q in c["qa"]:
        if q.get("category") == 5 or "answer" not in q:
            continue
        ev = [int(m.group(1)) for e in q["evidence"] if (m := re.match(r"D(\d+):", e))]
        if ev and ns - max(ev) >= MIN_AGE:
            pool.append({**q, "answer": str(q["answer"]), "age": ns - max(ev), "conv": c["sample_id"]})
    rng = random.Random(SEED); rng.shuffle(pool)
    # stratify by category so one type does not dominate
    bycat = {}
    for q in pool: bycat.setdefault(q["category"], []).append(q)
    out, cats = [], sorted(bycat)
    while len(out) < PER_CONV and any(bycat.values()):
        for ct in cats:
            if bycat[ct] and len(out) < PER_CONV: out.append(bycat[ct].pop())
    return out


EXTRACT = ("You maintain a long-term memory for a chat assistant. Below are new dialogue sessions "
           "(with dates). Write concise memory notes: one fact per line, starting with '- ', covering "
           "people, events (with absolute dates), preferences, plans, relationships. Resolve relative "
           "dates like 'yesterday' using the session date. Output only the notes.\n\n{chunk}")
REWRITE = ("You maintain a long-term memory for a chat assistant. Consolidate the memory below: merge "
           "duplicates, resolve conflicts, keep it organised and concise, one fact per line starting "
           "with '- '. Keep it under {cap} words. Output only the rewritten memory.\n\nMEMORY:\n{mem}")


def build_memories(c):
    sid = c["sample_id"]; f = MEMD / f"{sid}.json"
    if f.exists():
        return json.loads(f.read_text())
    chunks, cur = [], ""
    for i, dt, turns in sessions(c["conversation"]):
        s = f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns) + "\n\n"
        if len(cur.split()) + len(s.split()) > 3000 and cur:
            chunks.append(cur); cur = ""
        cur += s
    chunks.append(cur)
    notes = []
    for ch in chunks:
        t, _ = chat(WRITER, [{"role": "user", "content": EXTRACT.format(chunk=ch)}], max_tokens=2000)
        notes.append(t.strip())
    mems = {"0": "\n".join(notes)}
    m = mems["0"]
    for k in range(1, max(KS) + 1):
        m, _ = chat(WRITER, [{"role": "user", "content": REWRITE.format(cap=CAP_WORDS, mem=m)}], max_tokens=3000)
        m = m.strip(); mems[str(k)] = m
    f.write_text(json.dumps(mems, indent=1))
    return mems


READ = ("Answer each question using ONLY the context. Be short (a few words or a date). If the context "
        "does not contain the answer, write 'unknown'. Reply as JSON: {{\"1\": \"...\", ...}}.\n\n"
        "CONTEXT:\n{ctx}\n\nQUESTIONS:\n{qs}")
JUDGE_P = ("Grade each predicted answer against the gold answer. 1 if it conveys the same information "
           "(dates may differ in format), else 0. Reply as JSON: {{\"1\": 0 or 1, ...}}.\n\n{items}")


def jparse(t):
    m = re.search(r"\{.*\}", t, re.S)
    try: return json.loads(m.group(0)) if m else {}
    except Exception: return {}


def read_batch(ctx, qs):
    qtxt = "\n".join(f"{i+1}. {q['question']}" for i, q in enumerate(qs))
    t, _ = chat(READER, [{"role": "user", "content": READ.format(ctx=ctx, qs=qtxt)}], max_tokens=1200)
    a = jparse(t); return [str(a.get(str(i + 1), "unknown")) for i in range(len(qs))]


def judge(qs, preds):
    items = "\n".join(f"{i+1}. Q: {q['question']}\n   gold: {q['answer']}\n   pred: {p}" for i, (q, p) in enumerate(zip(qs, preds)))
    t, _ = chat(JUDGE, [{"role": "user", "content": JUDGE_P.format(items=items)}], max_tokens=2000)
    g = jparse(t); return [int(g.get(str(i + 1), 0) or 0) for i in range(len(qs))]


def bm25_ctx(c, q, topk=10):
    import bm25s
    turns = [(dt, t) for i, dt, ts in sessions(c["conversation"]) for t in ts]
    corpus = [f"[{dt}] {t['speaker']}: {t['text']}" for dt, t in turns]
    ret = bm25s.BM25(); ret.index(bm25s.tokenize(corpus, show_progress=False), show_progress=False)
    idx, _ = ret.retrieve(bm25s.tokenize([q["question"]], show_progress=False), k=topk, show_progress=False)
    return "\n".join(corpus[j] for j in idx[0])


SURV = ("For each numbered fact, answer 1 if the MEMORY states or clearly implies it, else 0. Reply as JSON "
        "{{\"1\": 0 or 1, ...}}.\n\nMEMORY:\n{mem}\n\nFACTS:\n{facts}")


def survival(mems, n=40):
    facts = [l[2:].strip() for l in mems["0"].splitlines() if l.startswith("- ")]
    rng = random.Random(SEED); facts = rng.sample(facts, min(n, len(facts)))
    ftxt = "\n".join(f"{i+1}. {f}" for i, f in enumerate(facts))
    out = {}
    for k in KS[1:]:
        t, _ = chat(JUDGE, [{"role": "user", "content": SURV.format(mem=mems[str(k)], facts=ftxt)}], max_tokens=2500)
        g = jparse(t)
        if not g: raise RuntimeError("survival judge returned no JSON")
        out[k] = sum(int(g.get(str(i + 1), 0) or 0) for i in range(len(facts))) / len(facts)
    out[0] = 1.0
    return out


def run_conv(c):
    qs = select(c); mems = build_memories(c)
    rows = []
    for k in KS:
        preds = read_batch(mems[str(k)], qs); g = judge(qs, preds)
        for q, p, s in zip(qs, preds, g):
            rows.append({"conv": c["sample_id"], "cond": f"k={k}", "k": k, "category": q["category"], "age": q["age"],
                         "question": q["question"], "gold": q["answer"], "pred": p, "correct": s,
                         "mem_words": len(mems[str(k)].split())})
    preds = [read_batch(bm25_ctx(c, q), [q])[0] for q in qs]; g = judge(qs, preds)
    for q, p, s in zip(qs, preds, g):
        rows.append({"conv": c["sample_id"], "cond": "bm25_raw", "k": -1, "category": q["category"], "age": q["age"],
                     "question": q["question"], "gold": q["answer"], "pred": p, "correct": s, "mem_words": ""})
    return qs, rows, survival(mems)


if __name__ == "__main__":
    d = {c["sample_id"]: c for c in json.load(open(DATA))}
    allq, allrows, surv = [], [], {}
    with cf.ThreadPoolExecutor(3) as ex:
        for qs, rows, s in ex.map(lambda sid: run_conv(d[sid]), CONVS):
            allq += qs; allrows += rows; surv[qs[0]["conv"]] = s
    with open(RES / "pilot_questions.jsonl", "w") as f:
        for q in allq: f.write(json.dumps({k: q[k] for k in ("conv", "question", "answer", "evidence", "category", "age")}) + "\n")
    with open(RES / "pilot_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(allrows[0])); w.writeheader(); w.writerows(allrows)
    json.dump(surv, open(RES / "pilot_survival.json", "w"), indent=1)
    print("done", len(allq), "questions,", len(allrows), "rows")
