"""A3b: hard equal budget on Memora. Every arm's memory is forced to <= W words: up to 3 condense passes
(REWRITE, cap = W*0.85), then mechanical truncation to W words at a line boundary (keeps the first lines; the
log records how many words truncation removed). Arms: k0 (append-only notes = one Render-from-Raw pass),
k8 (fixed rewrites), stream. Same reader/judge as A2."""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
import pilot, memora_pilot as mp
RES = pilot.RES; W = 900

def fit(m):
    passes = 0
    while len(m.split()) > W and passes < 3:
        m = chat(mp.WRITER, [{"role": "user", "content": pilot.REWRITE.format(cap=int(W * .85), mem=m)}], max_tokens=3000)[0].strip(); passes += 1
    before = len(m.split()); out, n = [], 0
    for l in m.splitlines():
        k = len(l.split())
        if n + k > W: break
        out.append(l); n += k
    return "\n".join(out), passes, before - n

rows, log = [], []
for p in mp.PERSONAS:
    fixed = json.load(open(RES / "memora_memories" / f"{p}.json")); st = json.load(open(RES / "memora_stream_memories" / f"{p}.json"))
    qs = mp.questions(p)
    for arm, m0 in [("k0_W", fixed["0"]), ("k8_W", fixed["8"]), ("stream_W", st["mem"])]:
        m, passes, cut = fit(m0); log.append(f"{p} {arm}: {len(m0.split())} -> {len(m.split())} words, {passes} condense passes, {cut} truncated")
        preds = mp.answer(m, qs); g = mp.judge(qs, preds)
        for q, pr in zip(qs, preds):
            for e in q["evaluation"]["evaluation_questions"]:
                rows.append({"data": "memora", "unit": p, "cond": arm, "item": e["evaluation_question_id"], "qid": q["question_id"],
                             "type": e["evaluation_type"], "age": "", "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(m.split()), "budget": W})
with open(RES / "a3b_scores.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("\n".join(log))
for arm in ("k0_W", "k8_W", "stream_W"):
    r = [x for x in rows if x["cond"] == arm]
    def s(t=None): v = [x["correct"] for x in r if t is None or x["type"] == t]; return f"{100*sum(v)/len(v):.1f}"
    print(arm, "acc", s(), "presence", s("memory_presence"), "forget", s("forgetting_absence"))
