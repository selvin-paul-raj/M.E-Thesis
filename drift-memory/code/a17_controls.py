"""A17: guard controls and cap ablation requested in review (30B writer and reader, same data, judge, reads as A8).
MODE preserve : every rewrite carries a fixed keep-facts instruction; no detection, no retry.
MODE floor    : on collapse (>=50% shrink from >=300 words) keep the OLD memory unchanged; no retry.
MODE nocap    : plain stream with the "Keep the whole memory under N words." sentence removed; no guard.
usage: a17_controls.py MODE memora|locomo unit1,...   Output: results/a17_controls_scores.csv (cond = MODE)
Based on A8: bounded collapse guard ("retry-only"), answering the length confound of A6/A7's fallback-append.
Rule: if a rewrite shrinks memory by >=50% from >=300 words, retry once with the keep-facts prompt and keep the
LONGER of the two attempts. Never append, so memory stays at the writer's own length (about the 1,200-word cap).
Same writer/reader (Nemotron), judge, prompts and questions as A5/A6 (Memora) and A7 (LoCoMo); unchanged steps hit cache.
usage: a8_retry_only.py memora persona1,...  |  a8_retry_only.py locomo conv-26,...
Output: results/a8_retry_scores.csv (dataset, unit, cond=stream_retry, qid, correct, mem_words)"""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
from stream_pilot import UPDATE
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"
KEEP = ("IMPORTANT: the current memory has {n} words. Your last attempt shrank it to {m} words and lost facts. "
        "Keep every existing fact unless {what} explicitly contradicts or retires it; merge new facts in.\n\n")
MODE, DS, UNITS = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
PRES = "IMPORTANT: keep every existing fact unless {what} explicitly contradicts or retires it; merge new facts in.\n\n"
NOCAP = UPDATE.replace(" Keep the whole memory under {cap} words.", "")
assert NOCAP != UPDATE

def collapsed(old, new): return old >= 300 and new <= 0.5 * old

def step(mem, sess, cap, what):
    if MODE == "nocap": prompt = NOCAP.format(mem=mem or "(empty)", sess=sess)
    else: prompt = UPDATE.format(cap=cap, mem=mem or "(empty)", sess=sess)
    if MODE == "preserve": prompt = PRES.format(what=what) + prompt
    m, _ = chat(WR, [{"role": "user", "content": prompt}], max_tokens=4000 if MODE == "nocap" else 3000); m = m.strip()
    old, new = len(mem.split()), len(m.split())
    if collapsed(old, new):
        if MODE == "floor": m = mem
        return m, {"old": old, "new": new, "kept": len(m.split())}
    return m, None

if DS == "memora":
    import memora_pilot as mp
    mp.WRITER = mp.READER = WR
    batches = lambda u: [("\n\n".join(f"[Session {sid}, {dt}]\n{txt}" for sid, dt, txt in ss[i:i + 10]))
                         for ss in [mp.sessions(u)] for i in range(0, len(ss), 10)]
    cap, what, res = mp.CAP_WORDS, "a new session", mp.RES
else:
    import pilot
    pilot.WRITER = pilot.READER = WR
    D = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
    batches = lambda u: [f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
                         for i, dt, turns in pilot.sessions(D[u]["conversation"])]
    cap, what, res = pilot.CAP_WORDS, "the new session", pilot.RES
SD = res / "a17_controls_memories"; SD.mkdir(exist_ok=True)
OUT = res / "a17_controls_scores.csv"
done = {(r["cond"], r["dataset"], r["unit"]) for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
for u in UNITS:
    if (MODE, DS, u) in done: continue
    f = SD / f"{MODE}_{DS}_{u}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": [], "events": []}
    bs = batches(u)
    for k in range(st["done"], len(bs)):
        m, ev = step(st["mem"], bs[k], cap, what)
        if ev: ev["step"] = k; st["events"].append(ev)
        st["mem"] = m; st["done"] = k + 1; st["words"].append(len(m.split())); f.write_text(json.dumps(st, indent=1))
    rows = []
    if DS == "memora":
        qs = mp.questions(u); preds = mp.answer(st["mem"], qs); g = mp.judge(qs, preds)
        for q in qs:
            for e in q["evaluation"]["evaluation_questions"]:
                rows.append({"dataset": DS, "unit": u, "cond": MODE, "qid": q["question_id"],
                             "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(st["mem"].split())})
    else:
        qs = pilot.select(D[u]); preds = pilot.read_batch(st["mem"], qs); sc = pilot.judge(qs, preds)
        for q, s in zip(qs, sc):
            rows.append({"dataset": DS, "unit": u, "cond": MODE, "qid": q["question"][:80], "correct": s,
                         "mem_words": len(st["mem"].split())})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(MODE, DS, u, f"{100*sum(r['correct'] for r in rows)/len(rows):.1f}", "words", len(st["mem"].split()), st["events"], flush=True)
