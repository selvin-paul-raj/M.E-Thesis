"""P1 trajectory replicates (PREREGISTRATION.md, committed 81a87b2 before any run).
19 units (LoCoMo 10 convs, Memora 9 personas) x arms {stream, guard} x seeds, writer temperature 0.7 (top_p 1.0, API seed).
guard = A8 bounded rule (collapse: new <= .5*old with old >= 300 -> one keep-facts retry, keep the longer). Reader/judge at temperature 0.
Same prompts, sessions, batching (LoCoMo 1, Memora 10 sessions per rewrite), questions as A7/A5/A8. Calls cached (seed in key);
guard shares the stream's cached calls until its first trigger. Resumable per (unit, arm, seed); endpoint errors -> results/p1_errors.log.
usage: p1_seeds.py SEED [SEED...]     (rounds: run seed 1 for all units, then 2, then 3)
Output: results/p1_scores.csv (dataset, unit, arm, seed, qid, check_id, correct, mem_words), results/p1_memories/*.json"""
import json, csv, pathlib, sys, time, traceback, threading, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from groq_client import chat
from stream_pilot import UPDATE
import pilot, memora_pilot as mp
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"; T = 0.7
pilot.WRITER = pilot.READER = WR; mp.WRITER = mp.READER = WR
KEEP = ("IMPORTANT: the current memory has {n} words. Your last attempt shrank it to {m} words and lost facts. "
        "Keep every existing fact unless {what} explicitly contradicts or retires it; merge new facts in.\n\n")
LOC = ["conv-26", "conv-30", "conv-41", "conv-42", "conv-43", "conv-44", "conv-47", "conv-48", "conv-49", "conv-50"]
MEM = ["business_executive", "content_writer", "creative_designer", "financial_analyst", "management_consultant",
       "marketing_manager", "sales_manager", "software_engineer", "startup_founder"]
R = pilot.RES; SD = R / "p1_memories"; SD.mkdir(exist_ok=True); OUT = R / "p1_scores.csv"; ERR = R / "p1_errors.log"
D = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
lock = threading.Lock()
def batches(ds, u):
    if ds == "memora":
        ss = mp.sessions(u)
        return [("\n\n".join(f"[Session {sid}, {dt}]\n{txt}" for sid, dt, txt in ss[i:i + 10])) for i in range(0, len(ss), 10)], mp.CAP_WORDS, "a new session"
    return [f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
            for i, dt, turns in pilot.sessions(D[u]["conversation"])], pilot.CAP_WORDS, "the new session"
def collapsed(old, new): return old >= 300 and new <= 0.5 * old
def step(mem, sess, cap, what, arm, seed):
    prompt = UPDATE.format(cap=cap, mem=mem or "(empty)", sess=sess)
    m = chat(WR, [{"role": "user", "content": prompt}], max_tokens=3000, temperature=T, seed=seed)[0].strip()
    old, new = len(mem.split()), len(m.split()); ev = None
    if collapsed(old, new):
        ev = {"old": old, "new": new, "kept": new}
        if arm == "guard":
            m2 = chat(WR, [{"role": "user", "content": KEEP.format(n=old, m=new, what=what) + prompt}], max_tokens=3000, temperature=T, seed=seed)[0].strip()
            if len(m2.split()) > new: m = m2
            ev["kept"] = len(m.split())
    return m, ev
def done_set():
    return {(r["dataset"], r["unit"], r["arm"], r["seed"]) for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
def run(ds, u, arm, seed):
    if (ds, u, arm, str(seed)) in done_set(): return
    f = SD / f"{ds}_{u}_{arm}_s{seed}.json"
    st = json.loads(f.read_text()) if f.exists() else {"mem": "", "done": 0, "words": [], "events": [], "temperature": T, "seed": seed, "writer": WR}
    bs, cap, what = batches(ds, u)
    for k in range(st["done"], len(bs)):
        m, ev = step(st["mem"], bs[k], cap, what, arm, seed)
        if ev: ev["step"] = k; st["events"].append(ev)
        st["mem"] = m; st["done"] = k + 1; st["words"].append(len(m.split())); f.write_text(json.dumps(st, indent=1))
    rows = []
    if ds == "memora":
        qs = mp.questions(u); preds = mp.answer(st["mem"], qs); g = mp.judge(qs, preds)
        for q in qs:
            for e in q["evaluation"]["evaluation_questions"]:
                rows.append({"dataset": ds, "unit": u, "arm": arm, "seed": seed, "qid": q["question_id"], "check_id": e["evaluation_question_id"],
                             "correct": int(g[e["evaluation_question_id"]]), "mem_words": len(st["mem"].split())})
    else:
        qs = pilot.select(D[u]); preds = pilot.read_batch(st["mem"], qs); sc = pilot.judge(qs, preds)
        for q, s in zip(qs, sc):
            rows.append({"dataset": ds, "unit": u, "arm": arm, "seed": seed, "qid": q["question"][:80], "check_id": "",
                         "correct": s, "mem_words": len(st["mem"].split())})
    with lock:
        new = not OUT.exists()
        with open(OUT, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            if new: w.writeheader()
            w.writerows(rows)
    print(time.strftime("%H:%M"), ds, u, arm, "s", seed, f"{100*sum(r['correct'] for r in rows)/len(rows):.1f}",
          "words", st["words"][-1], "collapses", len(st["events"]), flush=True)
def safe(job):
    for attempt in range(4):
        try: return run(*job)
        except Exception as e:
            with lock, open(ERR, "a") as fh:
                fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {job} attempt {attempt+1}: {type(e).__name__}: {str(e)[:300]}\n")
            time.sleep(60 * (attempt + 1))
    with lock, open(ERR, "a") as fh: fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {job} GAVE UP (resumable)\n")
for seed in map(int, sys.argv[1:]):
    # stream first, so the guard reuses its cached calls until its first trigger
    for arm in ("stream", "guard"):
        jobs = [("locomo", u, arm, seed) for u in LOC] + [("memora", u, arm, seed) for u in MEM]
        with cf.ThreadPoolExecutor(4) as ex: list(ex.map(safe, jobs))
    print("ROUND DONE seed", seed, flush=True)
