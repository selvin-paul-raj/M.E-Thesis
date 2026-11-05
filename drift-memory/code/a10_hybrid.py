"""A10: Guarded memory + raw evidence (the paper's proposed full system, "CollapseGuard+Raw").
Reader sees the bounded-guard consolidated memory (A8 memory where the guard fired, otherwise the plain stream memory,
which is then identical) plus the top-k BM25 raw turns from the original sessions for that question.
Arms: raw (BM25 top-k only) and hybrid (guard memory + BM25 top-k). One reader call per question; the same Nemotron
reader and gpt-oss-120b judge, with the same questions as A5-A8.
usage: a10_hybrid.py memora p1,p2 | a10_hybrid.py locomo conv-26,...
Output: results/a10_hybrid_scores.csv (dataset,unit,cond,qid,correct)"""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"
DS, UNITS = sys.argv[1], sys.argv[2].split(",")
HDR = "CONSOLIDATED MEMORY:\n{mem}\n\nRAW EVIDENCE (original messages retrieved for this question):\n{raw}"
if DS == "memora":
    import memora_pilot as mp; mp.WRITER = mp.READER = WR; RES = mp.RES
else:
    import pilot; pilot.WRITER = pilot.READER = WR; RES = pilot.RES
    D = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
OUT = RES / "a10_hybrid_scores.csv"
done = {(r["dataset"], r["unit"]) for r in csv.DictReader(open(OUT))} if OUT.exists() else set()

from groq_client import chat
def read1(ctx, q):
    """Single-question read; the reader often answers in plain text for one question, so fall back to the text."""
    if DS == "memora":
        prompt = mp.READ.format(date=q["question_date"], ctx=ctx, qs="1. " + q["question"]); mt = 3000
    else:
        prompt = pilot.READ.format(ctx=ctx, qs="1. " + q["question"]); mt = 1200
    t, _ = chat(WR, [{"role": "user", "content": prompt}], max_tokens=mt)
    a = pilot_jparse(t)
    return str(a.get("1")) if a.get("1") else (t.strip() or "unknown")
import re
def pilot_jparse(t):
    m = re.search(r"\{.*\}", t, re.S)
    try: return json.loads(m.group(0)) if m else {}
    except Exception: return {}

def guard_mem(u):
    g = RES / "a8_retry_memories" / f"{DS}_{u}.json"
    if g.exists(): return json.load(open(g))["mem"]
    f = RES / ("a5_stream_memories" if DS == "memora" else "a7_stream_memories") / (f"{u}.json" if DS == "memora" else f"{u}_plain.json")
    return json.load(open(f))["mem"]

for u in UNITS:
    if (DS, u) in done: continue
    mem = guard_mem(u); rows = []
    if DS == "memora":
        qs = mp.questions(u)
        for cond in ("raw", "hybrid"):
            preds = []
            for q in qs:
                raw = mp.bm25_ctx(u, q)
                preds.append(read1(raw if cond == "raw" else HDR.format(mem=mem, raw=raw), q))
            g = mp.judge(qs, preds)
            for q in qs:
                for e in q["evaluation"]["evaluation_questions"]:
                    rows.append({"dataset": DS, "unit": u, "cond": cond, "qid": q["question_id"], "correct": int(g[e["evaluation_question_id"]])})
    else:
        c = D[u]; qs = pilot.select(c)
        for cond in ("raw", "hybrid"):
            preds = []
            for q in qs:
                raw = pilot.bm25_ctx(c, q)
                preds.append(read1(raw if cond == "raw" else HDR.format(mem=mem, raw=raw), q))
            sc = pilot.judge(qs, preds)
            for q, s in zip(qs, sc):
                rows.append({"dataset": DS, "unit": u, "cond": cond, "qid": q["question"][:80], "correct": s})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(DS, u, {c: round(100 * sum(r["correct"] for r in rows if r["cond"] == c) / sum(1 for r in rows if r["cond"] == c), 1) for c in ("raw", "hybrid")}, flush=True)
