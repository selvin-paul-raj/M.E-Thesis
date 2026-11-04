"""A6: collapse guard for streaming memory (mitigation). Same as the A5 stream arm (Nemotron writer/reader,
10-session batches, 1,200-word cap, gpt-oss-120b judge), but each rewrite is checked: if memory shrinks by >=50%
from >=300 words, retry once with a keep-facts instruction; if it still collapses, keep the previous memory and
append the new rewrite under 'Recent updates'. With no collapse the guarded run is identical to stream (same prompt,
cached). usage: a5_guard.py persona1,persona2,...  Output: results/a6_guard_scores.csv"""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import memora_pilot as mp
from groq_client import chat
from stream_pilot import UPDATE
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"
mp.WRITER = mp.READER = WR
GD = mp.RES / "a6_guard_memories"; GD.mkdir(exist_ok=True)
OUT = mp.RES / "a6_guard_scores.csv"
B = 10
KEEP = ("IMPORTANT: the current memory has {n} words. Your last attempt shrank it to {m} words and lost facts. "
        "Keep every existing fact unless a new session explicitly contradicts or retires it; merge new facts in.\n\n")

def collapsed(old, new): return old >= 300 and new <= 0.5 * old

def stream_guard(p):
    f = GD / f"{p}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": [], "events": []}
    ss = mp.sessions(p)
    for i in range(st["done"], len(ss), B):
        sess = "\n\n".join(f"[Session {sid}, {dt}]\n{txt}" for sid, dt, txt in ss[i:i + B])
        prompt = UPDATE.format(cap=mp.CAP_WORDS, mem=st["mem"] or "(empty)", sess=sess)
        m, _ = chat(WR, [{"role": "user", "content": prompt}], max_tokens=3000); m = m.strip()
        old, new = len(st["mem"].split()), len(m.split())
        if collapsed(old, new):
            m2, _ = chat(WR, [{"role": "user", "content": KEEP.format(n=old, m=new) + prompt}], max_tokens=3000); m2 = m2.strip()
            n2 = len(m2.split())
            if collapsed(old, n2):
                m = st["mem"] + "\n\nRecent updates:\n" + m; act = "fallback_append"
            else:
                m = m2; act = "retry_ok"
            st["events"].append({"step": len(st["words"]), "old": old, "new": new, "retry": n2, "action": act})
        st["mem"] = m; st["done"] = min(i + B, len(ss)); st["words"].append(len(m.split()))
        f.write_text(json.dumps(st, indent=1))
    return st

done = {r["persona"] for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
for p in sys.argv[1].split(","):
    if p in done: continue
    qs = mp.questions(p); st = stream_guard(p); preds = mp.answer(st["mem"], qs); g = mp.judge(qs, preds); rows = []
    for q, pr in zip(qs, preds):
        for e in q["evaluation"]["evaluation_questions"]:
            rows.append({"persona": p, "writer": WR, "cond": "stream_guard", "qid": q["question_id"], "task": q["task"],
                         "type": e["evaluation_type"], "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(st["mem"].split())})
    new = not OUT.exists()
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        if new: w.writeheader()
        w.writerows(rows)
    print(p, f"{100*sum(r['correct'] for r in rows)/len(rows):.1f}", st["events"], flush=True)
