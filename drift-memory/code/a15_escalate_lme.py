"""A15 (escalation guard) on LongMemEval-S: identical to A11, but when the 30B writer's rewrite collapses, the SAME rewrite prompt
is re-issued once to nvidia/nemotron-3-ultra-550b-a55b and its output is kept (no keep-facts prefix). Arm: escalate.
Reuses A11 plain-stream cache up to the first collapse. Output: results/a15_lme_scores.csv
Original A11 doc follows.
A11: third environment, LongMemEval-S (cleaned; xiaowu0162/longmemeval-cleaned), with ~48 sessions per instance.
30 instances, stratified by type (seed 13, abstention items excluded): multi-session 8, knowledge-update 8,
temporal-reasoning 8, single-session-user 6. Sessions are fed in batches of 5 (about 10 rewrites per instance);
assistant turns are truncated to 300 characters.
Arms: stream (plain rewrite), guard (bounded collapse guard, rule fixed in A8), raw (BM25 top-10 turns), hybrid (guard + raw).
Writer/reader Nemotron (thinking off), judge gpt-oss-120b. Output: results/a11_lme_scores.csv
usage: a11_longmemeval.py select | a11_longmemeval.py run qid1,qid2,..."""
import json, csv, pathlib, sys, random, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
from stream_pilot import UPDATE
import pilot
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"; BIG = "nvidia/nemotron-3-ultra-550b-a55b"; JUDGE = "openai/gpt-oss-120b"; CAP = 1200; BATCH = 5
ROOT = pathlib.Path(__file__).resolve().parents[1]; RES = ROOT / "results"; DATA = ROOT / "data" / ("lme_s.json" if sys.argv[1] == "select" else "lme_s30.json")
SD = RES / "a15_memories"; SD.mkdir(exist_ok=True); OUT = RES / "a15_lme_scores.csv"; SEL = RES / "a11_selected.json"
KEEP = ("IMPORTANT: the current memory has {n} words. Your last attempt shrank it to {m} words and lost facts. "
        "Keep every existing fact unless the new session explicitly contradicts or retires it; merge new facts in.\n\n")
READ = ("Answer the question using ONLY the context. Today is {date}. Be short. If the context does not contain the "
        "answer, write 'unknown'. Reply as JSON: {{\"1\": \"...\"}}.\n\nCONTEXT:\n{ctx}\n\nQUESTION:\n1. {q}")
HDR = "CONSOLIDATED MEMORY:\n{mem}\n\nRAW EVIDENCE (original messages retrieved for this question):\n{raw}"

def jparse(t):
    m = re.search(r"\{.*\}", t, re.S)
    try: return json.loads(m.group(0)) if m else {}
    except Exception: return {}

def turn_txt(t): return f"{t['role']}: " + (t["content"] if t["role"] == "user" else t["content"][:300])

def batches(x):
    ss = [f"[Session {i+1}, {d}]\n" + "\n".join(turn_txt(t) for t in s) for i, (d, s) in enumerate(zip(x["haystack_dates"], x["haystack_sessions"]))]
    return ["\n\n".join(ss[i:i + BATCH]) for i in range(0, len(ss), BATCH)]

def collapsed(o, n): return o >= 300 and n <= 0.5 * o

def run_stream(x, guard):
    f = SD / f"{x['question_id']}_{'guard' if guard else 'plain'}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": [], "events": []}
    bs = batches(x)
    for k in range(st["done"], len(bs)):
        prompt = UPDATE.format(cap=CAP, mem=st["mem"] or "(empty)", sess=bs[k])
        m, _ = chat(WR, [{"role": "user", "content": prompt}], max_tokens=3000); m = m.strip()
        o, n = len(st["mem"].split()), len(m.split())
        if collapsed(o, n):
            ev = {"step": k, "old": o, "new": n}
            if guard:
                m2, _ = chat(BIG, [{"role": "user", "content": prompt}], max_tokens=3000); m = m2.strip()
                ev["kept"] = len(m.split())
            st["events"].append(ev)
        st["mem"] = m; st["done"] = k + 1; st["words"].append(len(m.split())); f.write_text(json.dumps(st, indent=1))
    return st

def bm25(x, topk=10):
    import bm25s
    corpus = [f"[{d}] {turn_txt(t)}" for d, s in zip(x["haystack_dates"], x["haystack_sessions"]) for t in s]
    r = bm25s.BM25(); r.index(bm25s.tokenize(corpus, show_progress=False), show_progress=False)
    idx, _ = r.retrieve(bm25s.tokenize([x["question"]], show_progress=False), k=topk, show_progress=False)
    return "\n".join(corpus[j] for j in idx[0])

def read(ctx, x):
    t, _ = chat(WR, [{"role": "user", "content": READ.format(date=x["question_date"], ctx=ctx, q=x["question"])}], max_tokens=800)
    a = jparse(t); return str(a.get("1")) if a.get("1") else (t.strip() or "unknown")

def judge(x, pred):
    items = f"1. Q: {x['question']}\n   gold: {x['answer']}\n   pred: {pred}"
    t, _ = chat(JUDGE, [{"role": "user", "content": pilot.JUDGE_P.format(items=items)}], max_tokens=800)
    return int(jparse(t).get("1", 0) or 0)

if sys.argv[1] == "select":
    D = [x for x in json.load(open(DATA)) if not x["question_id"].endswith("_abs")]
    rng = random.Random(13); sel = []
    for typ, n in (("multi-session", 8), ("knowledge-update", 8), ("temporal-reasoning", 8), ("single-session-user", 6)):
        pool = [x["question_id"] for x in D if x["question_type"] == typ]; rng.shuffle(pool); sel += pool[:n]
    SEL.write_text(json.dumps(sel)); print(len(sel), ",".join(sel)); sys.exit()

D = {x["question_id"]: x for x in json.load(open(DATA))}
done = {r["qid"] for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
for q in sys.argv[2].split(","):
    if q in done: continue
    x = D[q]; g = run_stream(x, True)
    ctxs = {"escalate": g["mem"]}
    rows = []
    for c, ctx in ctxs.items():
        p = read(ctx, x)
        rows.append({"qid": q, "type": x["question_type"], "cond": c, "correct": judge(x, p),
                     "mem_words": len(ctx.split()), "collapses": len(g["events"]), "pred": p[:200]})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(q, x["question_type"], {r["cond"]: r["correct"] for r in rows}, "escalations", len(g["events"]), "words", g["words"][-1], flush=True)
