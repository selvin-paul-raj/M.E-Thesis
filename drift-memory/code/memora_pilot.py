"""S5b: kill-switch rerun on Memora (arXiv 2604.20006; data Apache-2.0, github.com/geniesinc/Memora).

Same fixed-content arm as pilot.py (k = 0,1,2,4,8 rewrites, no new content) plus raw BM25.
Input: the share_memory turns (the turns Memora marks as carrying memory) of 3 weekly personas.
Questions: remembering + reasoning (5 + 5 per persona = 30). Scoring follows Memora's rubric:
gpt-oss-120b answers each yes/no sub-question against the free-form answer;
presence = share of memory_presence items met, forget = share of forgetting_absence items met,
score = sub-question accuracy (FAMA-like; exact FAMA weights per Memora evals/README not used).
"""
import json, glob, csv, pathlib, sys, random, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
from pilot import EXTRACT, REWRITE, jparse, JUDGE, KS, CAP_WORDS, SEED
# gpt-oss-20b hit its 200K tokens/day free-tier cap during the LoCoMo pilot (2026-11-04), so the Memora
# arm uses the plan's second writer for both writing and reading. Judge unchanged (gpt-oss-120b).
WRITER = READER = "qwen/qwen3.8-27b"

ROOT = pathlib.Path(__file__).resolve().parents[1]
MD = ROOT / "data" / "memora" / "data" / "weekly"
RES = ROOT / "results"; MEMD = RES / "memora_memories"; MEMD.mkdir(parents=True, exist_ok=True)
PERSONAS = ["software_engineer", "academic_researcher"]  # 2 of 3: Groq free-tier tokens/day cap (2026-11-04)


def sessions(p):
    out = []
    for f in sorted(glob.glob(str(MD / p / "conversations" / "*.json"))):
        s = json.load(open(f))
        if any(t.get("share_memory") for t in s["conversation"]):
            txt = "\n".join(f"User: {t['message']}" for t in s["conversation"] if t.get("share_memory"))
            out.append((s["session_id"], s["date"], txt))
    return out


def rewrite(mem, max_words=2000):
    """One consolidation round. Memories above max_words are rewritten in line-aligned sections
    (free-tier requests are capped near 8K tokens); each section gets a share of the 1,200-word cap.
    A memory under max_words is one section, i.e. identical to pilot.py."""
    lines = [l for l in mem.splitlines() if l.strip()]
    secs, cur = [], []
    for l in lines:
        if cur and len(" ".join(cur + [l]).split()) > max_words: secs.append(cur); cur = []
        cur.append(l)
    if cur: secs.append(cur)
    total = max(1, len(mem.split())); out = []
    for sec in secs:
        txt = "\n".join(sec); cap = max(150, round(CAP_WORDS * len(txt.split()) / total)) if len(secs) > 1 else CAP_WORDS
        out.append(chat(WRITER, [{"role": "user", "content": REWRITE.format(cap=cap, mem=txt)}], max_tokens=3000)[0].strip())
    return "\n".join(out)


def build(p):
    f = MEMD / f"{p}.json"
    if f.exists(): return json.loads(f.read_text())
    chunks, cur = [], ""
    for sid, dt, txt in sessions(p):
        s = f"[Session {sid}, {dt}]\n{txt}\n\n"
        if len(cur.split()) + len(s.split()) > 2000 and cur: chunks.append(cur); cur = ""
        cur += s
    chunks.append(cur)
    notes = [chat(WRITER, [{"role": "user", "content": EXTRACT.format(chunk=c)}], max_tokens=2000)[0].strip() for c in chunks]
    mems = {"0": "\n".join(notes)}; m = mems["0"]
    for k in range(1, max(KS) + 1):
        m = rewrite(m); mems[str(k)] = m
    f.write_text(json.dumps(mems, indent=1)); return mems


def questions(p):
    q = json.load(open(MD / p / f"evaluation_questions_{p}.json"))["questions"]
    return [{**x, "task": t, "persona": p} for t in ("remembering", "reasoning") for x in q[t]]


READ = ("You are the user's long-term assistant. Today is {date}. Using ONLY the memory below, answer each "
        "question fully but concisely (list every relevant item; leave out things the user cancelled, "
        "finished, or replaced). Reply as JSON {{\"1\": \"...\", ...}}.\n\nMEMORY:\n{ctx}\n\nQUESTIONS:\n{qs}")


def answer(ctx, qs):
    qtxt = "\n".join(f"{i+1}. {q['question']}" for i, q in enumerate(qs))
    t, _ = chat(READER, [{"role": "user", "content": READ.format(date=qs[0]["question_date"], ctx=ctx, qs=qtxt)}], max_tokens=3000)
    a = jparse(t); return [str(a.get(str(i + 1), "")) for i in range(len(qs))]


JUDGE_P = ("For each RESPONSE, answer its yes/no checks strictly from what the response says. Reply as JSON "
           "{{\"<check id>\": \"yes\" or \"no\", ...}}.\n\n{items}")


def judge(qs, preds):
    items, ids = [], []
    for q, p in zip(qs, preds):
        ev = q["evaluation"]["evaluation_questions"]
        items.append(f"RESPONSE to '{q['question']}':\n{p}\nCHECKS:\n" + "\n".join(f"[{e['evaluation_question_id']}] {e['evaluation_question']}" for e in ev))
        ids += ev
    t, _ = chat(JUDGE, [{"role": "user", "content": JUDGE_P.format(items="\n\n".join(items))}], max_tokens=4000)
    g = jparse(t)
    if not g: raise RuntimeError("judge returned no JSON")
    return {e["evaluation_question_id"]: (str(g.get(e["evaluation_question_id"], "")).lower().startswith(e["expected_answer"])) for e in ids}


def bm25_ctx(p, q, topk=15):
    import bm25s
    corpus = [f"[{dt}] {line}" for sid, dt, txt in sessions(p) for line in txt.splitlines()]
    r = bm25s.BM25(); r.index(bm25s.tokenize(corpus, show_progress=False), show_progress=False)
    idx, _ = r.retrieve(bm25s.tokenize([q["question"]], show_progress=False), k=topk, show_progress=False)
    return "\n".join(corpus[j] for j in idx[0])


def run(p):
    qs = questions(p); mems = build(p); rows = []
    conds = [(f"k={k}", lambda k=k: answer(mems[str(k)], qs)) for k in KS]
    conds.append(("bm25_raw", lambda: [answer(bm25_ctx(p, q), [q])[0] for q in qs]))
    for name, fn in conds:
        preds = fn(); g = judge(qs, preds)
        for q, pr in zip(qs, preds):
            for e in q["evaluation"]["evaluation_questions"]:
                rows.append({"persona": p, "cond": name, "task": q["task"], "qid": q["question_id"], "type": e["evaluation_type"],
                             "correct": int(g[e["evaluation_question_id"]]), "pred": pr[:300],
                             "mem_words": len(mems[name[2:]].split()) if name.startswith("k=") else ""})
    return rows


if __name__ == "__main__":
    rows = []
    with cf.ThreadPoolExecutor(3) as ex:
        for r in ex.map(run, PERSONAS): rows += r
    with open(RES / "memora_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("rows", len(rows))
    for c in [f"k={k}" for k in KS] + ["bm25_raw"]:
        r = [x for x in rows if x["cond"] == c]
        pres = [x["correct"] for x in r if x["type"] == "memory_presence"]; fg = [x["correct"] for x in r if x["type"] == "forgetting_absence"]
        print(c, f"acc {100*sum(x['correct'] for x in r)/len(r):.1f}", f"presence {100*sum(pres)/max(1,len(pres)):.1f}",
              f"forget {100*sum(fg)/max(1,len(fg)):.1f}", f"n={len(r)}")
