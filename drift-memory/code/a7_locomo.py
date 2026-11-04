"""A7: held-out replication of the collapse guard on LoCoMo (all 10 conversations, 10 questions each, evidence age >=5).
Writer/reader nvidia/nemotron-3.5-lightning-30b-a3b, judge gpt-oss-120b. Arms: k0 (append-only extracted notes),
stream (rewrite after every session, 1,200-word cap), stream_guard (same, with the A6 collapse guard: >=50% shrink from
>=300 words -> retry with keep-facts prompt, else keep old + append). Guard rule fixed before this run (A6, 2026-11-04).
usage: a7_locomo.py conv-26,conv-30,...   Output: results/a7_locomo_scores.csv"""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pilot
from groq_client import chat
from stream_pilot import UPDATE
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"
pilot.WRITER = pilot.READER = WR; pilot.KS = [0]
pilot.MEMD = pilot.RES / "a7_k0_memories"; pilot.MEMD.mkdir(exist_ok=True)
SD = pilot.RES / "a7_stream_memories"; SD.mkdir(exist_ok=True)
OUT = pilot.RES / "a7_locomo_scores.csv"
KEEP = ("IMPORTANT: the current memory has {n} words. Your last attempt shrank it to {m} words and lost facts. "
        "Keep every existing fact unless the new session explicitly contradicts or retires it; merge new facts in.\n\n")

def collapsed(old, new): return old >= 300 and new <= 0.5 * old

def stream(c, guard):
    f = SD / f"{c['sample_id']}_{'guard' if guard else 'plain'}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": [], "events": []}
    ss = pilot.sessions(c["conversation"])
    for i, dt, turns in ss[st["done"]:]:
        sess = f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
        prompt = UPDATE.format(cap=pilot.CAP_WORDS, mem=st["mem"] or "(empty)", sess=sess)
        m, _ = chat(WR, [{"role": "user", "content": prompt}], max_tokens=3000); m = m.strip()
        old, new = len(st["mem"].split()), len(m.split())
        if collapsed(old, new):
            ev = {"step": st["done"], "old": old, "new": new}
            if guard:
                m2, _ = chat(WR, [{"role": "user", "content": KEEP.format(n=old, m=new) + prompt}], max_tokens=3000); m2 = m2.strip()
                ev["retry"] = len(m2.split())
                if collapsed(old, ev["retry"]): m = st["mem"] + "\n\nRecent updates:\n" + m; ev["action"] = "fallback_append"
                else: m = m2; ev["action"] = "retry_ok"
            st["events"].append(ev)
        st["mem"] = m; st["done"] += 1; st["words"].append(len(m.split()))
        f.write_text(json.dumps(st, indent=1))
    return st

d = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
done = {r["conv"] for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
for sid in sys.argv[1].split(","):
    if sid in done: continue
    c = d[sid]; qs = pilot.select(c); rows = []
    arms = [("k0", pilot.build_memories(c)["0"], [])]
    for g in (False, True):
        st = stream(c, g); arms.append(("stream_guard" if g else "stream", st["mem"], st["events"]))
    for arm, mem, evs in arms:
        preds = pilot.read_batch(mem, qs); sc = pilot.judge(qs, preds)
        for q, p, s in zip(qs, preds, sc):
            rows.append({"conv": sid, "cond": arm, "qid": q["question"][:80], "category": q["category"], "age": q["age"],
                         "correct": s, "mem_words": len(mem.split()), "collapses": len(evs)})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(sid, {a: sum(r["correct"] for r in rows if r["cond"] == a) for a in ("k0", "stream", "stream_guard")},
          {a: next(r["mem_words"] for r in rows if r["cond"] == a) for a in ("k0", "stream", "stream_guard")},
          "collapses", next(r["collapses"] for r in rows if r["cond"] == "stream"), flush=True)
