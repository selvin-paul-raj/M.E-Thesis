"""S5: apply the PLAN.md kill-switch thresholds to the pilot and plot."""
import csv, json, pathlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]; RES = ROOT / "results"
rows = list(csv.DictReader(open(RES / "pilot_scores.csv")))
surv = json.load(open(RES / "pilot_survival.json"))
KS = [0, 1, 2, 4, 8]
acc = {}
for c in [f"k={k}" for k in KS] + ["bm25_raw"]:
    r = [int(x["correct"]) for x in rows if x["cond"] == c]
    acc[c] = 100 * sum(r) / len(r)
words = {k: sum(int(x["mem_words"]) for x in rows if x["cond"] == f"k={k}") / max(1, sum(1 for x in rows if x["cond"] == f"k={k}")) for k in KS}
fs = {k: sum(v[str(k)] for v in surv.values()) / len(surv) * 100 for k in KS}
a1, a4, a8 = acc["k=1"], acc["k=4"], acc["k=8"]
drop = a1 - a8
mono = all(fs[KS[i]] >= fs[KS[i + 1]] - 1e-9 for i in range(1, len(KS) - 1))
if drop >= 10 and mono: verdict = "FALLING -> continue (drift paper as planned)"
elif drop >= 3: verdict = "PLATEAU -> continue with equilibrium framing" if (a1 - a4) >= 0.6 * drop else "PLATEAU/SLOW DECLINE -> continue, check more k"
else: verdict = "FLAT -> rerun on 30 Memora questions before deciding"

n = sum(1 for x in rows if x["cond"] == "k=1")
lines = [f"# Pilot verdict (S5)", "", f"Questions: {n} (LoCoMo conv-26/30/49, evidence >= 5 sessions old, category 5 excluded).",
         "Writer/reader gpt-oss-20b; judge gpt-oss-120b. Memory cap 1,200 words for k>=1.", "",
         "| condition | accuracy % | memory words | fact survival % |", "|---|---|---|---|"]
for k in KS: lines.append(f"| k={k} | {acc[f'k={k}']:.1f} | {words[k]:.0f} | {fs[k]:.1f} |")
lines.append(f"| raw BM25 top-10 | {acc['bm25_raw']:.1f} | - | - |")
lines += ["", f"Drop k=1 -> k=8: {drop:.1f} pts; fact survival monotone (k>=1): {mono}.", f"**Verdict: {verdict}**", "",
          "Caveats: n=30 (one question = 3.3 pts); answer keys not hand-checked yet; single seed; fact survival judged by LLM, not NLI."]
(ROOT / "notes").mkdir(exist_ok=True)
(ROOT / "notes" / "pilot_verdict.md").write_text("\n".join(lines) + "\n")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
ax[0].plot(KS, [acc[f"k={k}"] for k in KS], "o-", label="rewrite-in-place memory")
ax[0].axhline(acc["bm25_raw"], ls="--", c="gray", label="raw BM25 (ceiling)")
ax[0].set_xlabel("consolidation rounds k (no new content)"); ax[0].set_ylabel("QA accuracy %"); ax[0].set_xticks(KS); ax[0].legend(fontsize=8)
ax[1].plot(KS, [fs[k] for k in KS], "s-", c="C3"); ax[1].set_xlabel("k"); ax[1].set_ylabel("fact survival %"); ax[1].set_xticks(KS); ax[1].set_ylim(0, 105); ax[0].set_ylim(0, 60)
fig.suptitle("DriftBench pilot: LoCoMo, 30 old-evidence questions"); fig.tight_layout()
fig.savefig(RES / "pilot_curve.png", dpi=150)
print("\n".join(lines))
