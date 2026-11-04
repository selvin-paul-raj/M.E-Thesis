"""A3: equal-budget control. Is the streaming advantage just memory length?
Streaming memory is condensed once (REWRITE, cap = that dataset's fixed k=8 memory length) and re-scored.
Memora: qwen3.8-27b writer/reader; LoCoMo: gpt-oss-20b; judge gpt-oss-120b (as in A1/A2)."""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
import pilot, memora_pilot as mp
RES = pilot.RES
rows = []
# Memora
for p in mp.PERSONAS:
    st = json.load(open(RES / "memora_stream_memories" / f"{p}.json")); W = len(json.load(open(RES / "memora_memories" / f"{p}.json"))["8"].split())
    m = chat(mp.WRITER, [{"role": "user", "content": pilot.REWRITE.format(cap=W, mem=st["mem"])}], max_tokens=3000)[0].strip()
    qs = mp.questions(p); preds = mp.answer(m, qs); g = mp.judge(qs, preds)
    for q, pr in zip(qs, preds):
        for e in q["evaluation"]["evaluation_questions"]:
            rows.append({"data": "memora", "unit": p, "cond": "stream_eq", "item": e["evaluation_question_id"], "type": e["evaluation_type"],
                         "age": "", "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(m.split()), "budget": W})
# LoCoMo
d = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
for sid in pilot.CONVS:
    st = json.load(open(RES / "stream_memories" / f"{sid}.json")); W = len(json.load(open(RES / "pilot_memories" / f"{sid}.json"))["8"].split())
    m = st["mem"] if len(st["mem"].split()) <= W else chat(pilot.WRITER, [{"role": "user", "content": pilot.REWRITE.format(cap=W, mem=st["mem"])}], max_tokens=3000)[0].strip()
    qs = pilot.select(d[sid]); preds = pilot.read_batch(m, qs); g = pilot.judge(qs, preds)
    for q, s in zip(qs, g):
        rows.append({"data": "locomo", "unit": sid, "cond": "stream_eq", "item": q["question"], "type": "", "age": q["age"],
                     "correct": int(s), "mem_words": len(m.split()), "budget": W})
with open(RES / "a3_scores.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for ds in ("memora", "locomo"):
    r = [x["correct"] for x in rows if x["data"] == ds]; print(ds, "stream_eq", f"{100*sum(r)/len(r):.1f}", len(r),
          {x["unit"]: (x["mem_words"], x["budget"]) for x in rows if x["data"] == ds})
