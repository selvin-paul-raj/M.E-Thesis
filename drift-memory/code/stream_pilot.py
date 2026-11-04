"""Option A, step 1: streaming arm on LoCoMo (does new content restart the decay?).

Rewrite-in-place memory (Mem0-style): after every session, memory = UPDATE(memory, session), 1,200-word cap.
A fact first stored in session s is rewritten (S - s) more times, so old evidence has been through
5-25 rewrites WITH new content arriving each time. Compared with the pilot's append-only notes (k=0)
and the fixed-content arm (k=8) on the same 30 questions, reader and judge.
"""
import json, csv, pathlib, sys, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
import pilot
from pilot import WRITER, CONVS, CAP_WORDS, sessions, select, read_batch, judge

ROOT = pathlib.Path(__file__).resolve().parents[1]; RES = ROOT / "results"
SD = RES / "stream_memories"; SD.mkdir(parents=True, exist_ok=True)
UPDATE = ("You maintain a long-term memory for a chat assistant. Update the MEMORY with the NEW SESSION: add new "
          "facts (with absolute dates; resolve relative dates using the session date), update or remove facts that "
          "changed, merge duplicates, keep it organised and concise, one fact per line starting with '- '. Keep the "
          "whole memory under {cap} words. Output only the full updated memory.\n\nMEMORY:\n{mem}\n\nNEW SESSION:\n{sess}")


def stream(c):
    f = SD / f"{c['sample_id']}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": []}
    ss = sessions(c["conversation"])
    for i, dt, turns in ss[st["done"]:]:
        sess = f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
        m, _ = chat(WRITER, [{"role": "user", "content": UPDATE.format(cap=CAP_WORDS, mem=st["mem"] or "(empty)", sess=sess)}], max_tokens=3000)
        st["mem"] = m.strip(); st["done"] += 1; st["words"].append(len(st["mem"].split()))
        f.write_text(json.dumps(st, indent=1))  # resumable
    return st


def run(sid, d):
    c = d[sid]; qs = select(c); st = stream(c)
    preds = read_batch(st["mem"], qs); g = judge(qs, preds)
    return [{"conv": sid, "cond": "stream_rewrite", "category": q["category"], "age": q["age"], "question": q["question"],
             "gold": q["answer"], "pred": p, "correct": s, "mem_words": st["words"][-1]} for q, p, s in zip(qs, preds, g)]


if __name__ == "__main__":
    d = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
    rows = []
    with cf.ThreadPoolExecutor(3) as ex:
        for r in ex.map(lambda s: run(s, d), CONVS): rows += r
    with open(RES / "stream_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    base = list(csv.DictReader(open(RES / "pilot_scores.csv")))
    def acc(rs): return 100 * sum(int(x["correct"]) for x in rs) / max(1, len(rs))
    out = ["| condition | all | age 5-9 | age 10+ |", "|---|---|---|---|"]
    for name, rs in [("append-only notes (k=0)", [x for x in base if x["cond"] == "k=0"]),
                     ("fixed-content k=8", [x for x in base if x["cond"] == "k=8"]),
                     ("streaming rewrite-in-place", rows),
                     ("raw BM25", [x for x in base if x["cond"] == "bm25_raw"])]:
        a = [x for x in rs if int(x["age"]) < 10]; b = [x for x in rs if int(x["age"]) >= 10]
        out.append(f"| {name} | {acc(rs):.1f} | {acc(a):.1f} (n={len(a)}) | {acc(b):.1f} (n={len(b)}) |")
    (RES / "stream_summary.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
