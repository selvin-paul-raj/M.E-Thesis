"""A20 (judge validation, brief section 3.2 items 3-4): re-judge every main-table answer with a judge from another family
(mistralai/mistral-large-4-1t-a52b on NVIDIA), same judge prompt as the original gpt-oss-120b judge.
Reader answers are reconstructed from the saved memories through the response cache (reader = Nemotron-3.5-Lightning,
identical prompts => cache hits; a miss is a fresh call and is counted). Also writes reader predictions for the
deterministic check and the human audit sample.
Arms: Memora (9 personas) k0, k2, stream, stream_guard (append), stream_retry (bounded);
      LoCoMo (10 convs) k0, stream, stream_guard, stream_retry.
usage: a20_second_judge.py memora|locomo unit1,...   Output: results/a20_judge2_scores.csv, results/a20_preds.jsonl"""
import json, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import groq_client
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"; J2 = "mistralai/mistral-large-4-1t-a52b"
groq_client._FALLBACK.add(J2); groq_client.TPM = 10**9  # route via NVIDIA endpoint, no Groq throttle
DS, UNITS = sys.argv[1], sys.argv[2].split(",")
R = pathlib.Path(__file__).resolve().parent.parent / "results"
OUT = R / "a20_judge2_scores.csv"; PR = R / "a20_preds.jsonl"
done = {(r["dataset"], r["unit"], r["cond"]) for r in csv.DictReader(open(OUT))} if OUT.exists() else set()
L = lambda p: json.load(open(R / p))
rows = []
if DS == "memora":
    import memora_pilot as mp
    mp.WRITER = mp.READER = WR
    for u in UNITS:
        km = L(f"a5_memories/{u}.json")
        arms = [("k0", km["0"]), ("k2", km["2"]), ("stream", L(f"a5_stream_memories/{u}.json")["mem"]),
                ("stream_guard", L(f"a6_guard_memories/{u}.json")["mem"])]
        f = R / f"a8_retry_memories/memora_{u}.json"
        arms.append(("stream_retry", json.load(open(f))["mem"] if f.exists() else arms[2][1]))
        qs = mp.questions(u)
        for cond, mem in arms:
            if ("memora", u, cond) in done: continue
            preds = mp.answer(mem, qs)
            mp.JUDGE = J2; g = mp.judge(qs, preds); mp.JUDGE = "openai/gpt-oss-120b"
            out = []
            for q, p in zip(qs, preds if isinstance(preds, list) else [preds[q["question_id"]] for q in qs]):
                for e in q["evaluation"]["evaluation_questions"]:
                    out.append({"dataset": DS, "unit": u, "cond": cond, "qid": q["question_id"], "correct": int(g[e["evaluation_question_id"]])})
                with open(PR, "a") as fh: fh.write(json.dumps({"dataset": DS, "unit": u, "cond": cond, "qid": q["question_id"], "pred": p}) + "\n")
            new = not OUT.exists()
            with open(OUT, "a", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(out[0])); new and w.writeheader(); w.writerows(out)
            print(DS, u, cond, f"{100*sum(r['correct'] for r in out)/len(out):.1f}", flush=True)
else:
    import pilot
    pilot.WRITER = pilot.READER = WR
    D = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
    for u in UNITS:
        arms = [("k0", L(f"a7_k0_memories/{u}.json")["0"]), ("stream", L(f"a7_stream_memories/{u}_plain.json")["mem"]),
                ("stream_guard", L(f"a7_stream_memories/{u}_guard.json")["mem"])]
        f = R / f"a8_retry_memories/locomo_{u}.json"
        arms.append(("stream_retry", json.load(open(f))["mem"] if f.exists() else arms[1][1]))
        qs = pilot.select(D[u])
        for cond, mem in arms:
            if ("locomo", u, cond) in done: continue
            preds = pilot.read_batch(mem, qs)
            pilot.JUDGE = J2; sc = pilot.judge(qs, preds); pilot.JUDGE = "openai/gpt-oss-120b"
            out = [{"dataset": DS, "unit": u, "cond": cond, "qid": q["question"][:80], "correct": int(s)} for q, s in zip(qs, sc)]
            with open(PR, "a") as fh:
                for q, p in zip(qs, preds):
                    fh.write(json.dumps({"dataset": DS, "unit": u, "cond": cond, "qid": q["question"][:80], "question": q["question"],
                                         "gold": str(q.get("answer", "")), "pred": p}) + "\n")
            new = not OUT.exists()
            with open(OUT, "a", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(out[0])); new and w.writeheader(); w.writerows(out)
            print(DS, u, cond, f"{100*sum(r['correct'] for r in out)/len(out):.1f}", flush=True)
