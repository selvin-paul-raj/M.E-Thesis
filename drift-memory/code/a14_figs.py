"""Figure: (a) collapse-threshold sensitivity, (b) distribution of per-rewrite length ratios (rewrites from >=300 words).
Reads results/a9_analysis.txt and the Nemotron stream memory files used in A9 (no model calls)."""
import re, json, glob, pathlib, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = pathlib.Path(__file__).resolve().parents[1] / "results"; P = R.parent / "paper"
rows = re.findall(r"^(0\.\d) (\d+) (\d+) ([\d.]+) (\d+)$", (R / "a9_analysis.txt").read_text(), re.M)
fig, ax = plt.subplots(1, 2, figsize=(7, 2.6))
for fl in ("200", "300", "500"):
    xs = [float(r[0]) for r in rows if r[1] == fl]; ys = [float(r[3]) for r in rows if r[1] == fl]
    ax[0].plot(xs, ys, marker="o", label=f"floor {fl} w")
ax[0].set_xlabel("collapse threshold (new/old $\\leq$)"); ax[0].set_ylabel("% of rewrites"); ax[0].legend(fontsize=7); ax[0].set_title("(a) threshold sensitivity", fontsize=9)
ratios = []
for f in glob.glob(str(R / "a7_stream_memories/*_plain.json")) + [g for g in glob.glob(str(R / "a5_stream_memories/*.json")) if "academic_researcher" not in g]:
    w = json.load(open(f)).get("words", [])
    ratios += [b / a for a, b in zip(w, w[1:]) if a >= 300]
ax[1].hist([min(r, 2) for r in ratios], bins=40, color="gray"); ax[1].axvline(0.5, color="red", ls="--", lw=1)
ax[1].set_yscale("log"); ax[1].set_xlabel("new/old length (capped at 2)"); ax[1].set_ylabel("rewrites (log)"); ax[1].set_title(f"(b) length ratios, n={len(ratios)}", fontsize=9)
plt.tight_layout(); plt.savefig(P / "fig_threshold.pdf"); plt.savefig(R / "fig_threshold.png", dpi=150); print(len(ratios))
