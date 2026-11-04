"""A5: scale-up for power. All 10 Memora weekly personas, one writer/reader (gpt-oss-20b; NVIDIA NIM fallback
on Groq daily cap), judge gpt-oss-120b. Arms: k0 (append-only notes), k2 (fixed rewrites; plateau reached by k=2
in pilots), stream (10-session batches). Resumable per persona; scores appended to results/a5_scores.csv."""
import json, csv, pathlib, sys, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import memora_pilot as mp, memora_stream as ms
# usage: a5_scale.py WRITER persona1,persona2,...  (one writer per persona; arms compared within persona)
WR = sys.argv[1] if len(sys.argv) > 1 else "openai/gpt-oss-20b"
mp.WRITER = mp.READER = WR; mp.KS = [0, 1, 2]
mp.MEMD = mp.RES / "a5_memories"; mp.MEMD.mkdir(exist_ok=True)
ms.SD = mp.RES / "a5_stream_memories"; ms.SD.mkdir(exist_ok=True)
OUT = mp.RES / f"a5_scores_{WR.split('/')[-1]}.csv"
PERS = sys.argv[2].split(",") if len(sys.argv) > 2 else sorted(p.name for p in mp.MD.iterdir() if p.is_dir())
import glob
done = {r["persona"] for f in glob.glob(str(mp.RES / "a5_scores_*.csv")) for r in csv.DictReader(open(f))}
for p in PERS:
    if p in done: continue
    qs = mp.questions(p); mems = mp.build(p); st = ms.stream(p); rows = []
    for arm, m in [("k0", mems["0"]), ("k2", mems["2"]), ("stream", st["mem"])]:
        preds = mp.answer(m, qs); g = mp.judge(qs, preds)
        for q, pr in zip(qs, preds):
            for e in q["evaluation"]["evaluation_questions"]:
                rows.append({"persona": p, "writer": WR, "cond": arm, "qid": q["question_id"], "task": q["task"], "type": e["evaluation_type"],
                             "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(m.split())})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(p, {a: f"{100*sum(r['correct'] for r in rows if r['cond']==a)/sum(1 for r in rows if r['cond']==a):.1f}" for a in ("k0","k2","stream")}, flush=True)
