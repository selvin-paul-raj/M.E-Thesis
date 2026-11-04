"""A2: streaming rewrite-in-place on Memora (2 personas). Memory = UPDATE(memory, batch of 10 sessions),
1,200-word cap, same writer/reader (qwen3.8-27b) and judge as memora_pilot.py. Batching 10 sessions per update
(~11 updates per persona) keeps the run inside the Groq free-tier daily token cap. Resumable."""
import json, csv, pathlib, sys, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import memora_pilot as mp
from groq_client import chat
from stream_pilot import UPDATE
SD = mp.RES / "memora_stream_memories"; SD.mkdir(exist_ok=True)
B = 10

def stream(p):
    f = SD / f"{p}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": []}
    ss = mp.sessions(p)
    for i in range(st["done"], len(ss), B):
        sess = "\n\n".join(f"[Session {sid}, {dt}]\n{txt}" for sid, dt, txt in ss[i:i + B])
        m, _ = chat(mp.WRITER, [{"role": "user", "content": UPDATE.format(cap=mp.CAP_WORDS, mem=st["mem"] or "(empty)", sess=sess)}], max_tokens=3000)
        st["mem"] = m.strip(); st["done"] = min(i + B, len(ss)); st["words"].append(len(st["mem"].split()))
        f.write_text(json.dumps(st, indent=1))
    return st

def run(p):
    qs = mp.questions(p); st = stream(p); preds = mp.answer(st["mem"], qs); g = mp.judge(qs, preds); rows = []
    for q, pr in zip(qs, preds):
        for e in q["evaluation"]["evaluation_questions"]:
            rows.append({"persona": p, "cond": "stream", "task": q["task"], "qid": q["question_id"], "type": e["evaluation_type"],
                         "correct": int(g[e["evaluation_question_id"]]), "pred": pr[:300], "mem_words": st["words"][-1]})
    return rows

if __name__ == "__main__":
    rows = []
    with cf.ThreadPoolExecutor(2) as ex:
        for r in ex.map(run, mp.PERSONAS): rows += r
    with open(mp.RES / "memora_stream_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    base = list(csv.DictReader(open(mp.RES / "memora_scores.csv")))
    def s(rs, t=None):
        r = [int(x["correct"]) for x in rs if t is None or x["type"] == t]; return f"{100*sum(r)/max(1,len(r)):.1f}"
    out = ["| condition | check acc | presence | forgetting |", "|---|---|---|---|"]
    for name, rs in [("k=0", [x for x in base if x["cond"] == "k=0"]), ("k=8", [x for x in base if x["cond"] == "k=8"]),
                     ("streaming", rows), ("bm25_raw", [x for x in base if x["cond"] == "bm25_raw"])]:
        out.append(f"| {name} | {s(rs)} | {s(rs,'memory_presence')} | {s(rs,'forgetting_absence')} |")
    (mp.RES / "memora_stream_summary.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
