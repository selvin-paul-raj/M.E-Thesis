"""Charts (PNG, 2x) following a light, minimal style. Bar labels use 3 decimals, rounded from the
unrounded values exactly as the report tables are, so a chart and its table always show the same number."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
BG, INK = "#e8e8ea", "#1d1d1f"; COLS = ["#b1bcd2", "#607868", "#dbb691", "#a79fb8", "#d9c489"]
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.facecolor": BG, "figure.facecolor": BG,
    "axes.edgecolor": INK + "80", "axes.labelcolor": INK + "80", "xtick.color": INK + "80", "ytick.color": INK + "80",
    "axes.spines.top": False, "axes.spines.right": False, "xtick.major.size": 0, "ytick.major.size": 0})
R = pd.read_csv("results/main_results.csv"); T = R[R.corpus == "ta"]
def val(s, r, m="MRR@10"): return float(T[(T.query_set == s) & (T.retriever == r)][m].iloc[0])
def fmt3(v): return f"{v:.3f}"
def style(ax, title, sub):
    ax.set_title(title, loc="left", fontsize=14, color=INK, pad=24, fontweight="bold")
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=10.5, color=INK + "99")
    ax.yaxis.grid(True, color=INK, alpha=.07); ax.set_axisbelow(True)
    for t in ax.get_yticklabels(): t.set_family("DejaVu Sans Mono")

# 1. MRR by query variant
sets = [("en", "English"), ("ta", "Tamil script"), ("cm", "Code-mixed"), ("rom", "Romanised")]
rets = ["BM25", "BM25-char3", "Dense-e5", "Hybrid-RRF"]
fig, ax = plt.subplots(figsize=(9, 4.8)); w = .2; x = np.arange(len(sets))
for k, r in enumerate(rets):
    v = [val(s, r) for s, _ in sets]
    b = ax.bar(x + (k - 1.5) * w, v, w * .92, color=COLS[k], label=r)
    for xi, vi in zip(x + (k - 1.5) * w, v): ax.text(xi, vi + .015, fmt3(vi), ha="center", fontsize=7.2, family="DejaVu Sans Mono", color=INK)
ax.set_xticks(x, [l for _, l in sets], fontsize=11.5, color=INK); ax.set_ylim(0, 1.05)
ax.legend(frameon=False, ncol=4, loc="upper right", fontsize=9.5, bbox_to_anchor=(1, 1.0))
style(ax, "Romanised Tamil queries break every retriever", "MRR@10 on a Tamil-script corpus of 500 docs, 2,154 queries per variant (no normalisation)")
fig.tight_layout(); fig.savefig("results/charts/fig1_mrr_by_variant.png", dpi=200); plt.close()

# 2. normalisation effect (Recall@10), two panels
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
for ax, base, lab in [(axes[0], "rom", "Romanised queries"), (axes[1], "cm", "Code-mixed queries")]:
    modes = [(base, "Raw"), (f"{base}_itrans", "ITRANS"), (f"{base}_rules", "Tanglish rules")]
    rr = ["Dense-e5", "BM25-char3", "Hybrid-RRF3"]
    for k, r in enumerate(rr):
        v = [val(s, r, "R@10") for s, _ in modes]; xs = np.arange(3) + (k - 1) * .26
        ax.bar(xs, v, .24, color=COLS[[2, 1, 3][k]], label=r)
        for xi, vi in zip(xs, v): ax.text(xi, vi + .015, fmt3(vi), ha="center", fontsize=7.2, family="DejaVu Sans Mono", color=INK)
    ax.set_xticks(np.arange(3), [l for _, l in modes], fontsize=10.5, color=INK); ax.set_ylim(0, 1.0)
    ax.set_title(lab, fontsize=11.5, color=INK, loc="left"); ax.yaxis.grid(True, color=INK, alpha=.07); ax.set_axisbelow(True)
axes[0].set_ylabel("Recall@10"); axes[0].legend(frameon=False, fontsize=9, loc="upper left")
fig.suptitle("Transliterating to Tamil script recovers most romanised queries", x=.06, ha="left", fontsize=14, fontweight="bold", color=INK)
fig.text(.06, .895, "Recall@10 on the Tamil-script corpus; normalisation adds ~0.3 ms per query", fontsize=10.5, color=INK + "99")
fig.tight_layout(rect=(0, 0, 1, .9)); fig.savefig("results/charts/fig2_normalisation.png", dpi=200); plt.close()

# 3. equal-weight hybrid fusion across scripts (zero-score BM25 documents excluded; v1 'naive' lists shown for contrast)
sets3 = [("ta", "Tamil script"), ("en", "English"), ("cm", "Code-mixed"), ("rom_rules", "Romanised\n+rules")]
fig, ax = plt.subplots(figsize=(10, 4.8)); x = np.arange(4); w = .2
SER = [("Dense-e5", COLS[2], "Dense alone"), ("Hybrid-RRF", COLS[0], "RRF (BM25 + dense)"),
       ("Hybrid-RRF3", COLS[3], "RRF3 (+ char 3-gram)"), ("Hybrid-RRF-naive", "#1d1d1f4d", "RRF, v1 naive lists")]
for k, (r, c, name) in enumerate(SER):
    v = [val(s, r) for s, _ in sets3]; xs = x + (k - 1.5) * w
    ax.bar(xs, v, w * .92, color=c, label=name)
    for xi, vi in zip(xs, v): ax.text(xi, vi + .015, fmt3(vi), ha="center", fontsize=7.2, family="DejaVu Sans Mono", color=INK)
ax.set_xticks(x, [l for _, l in sets3], fontsize=10.5, color=INK); ax.set_ylim(0, 1.1)
ax.legend(frameon=False, ncol=4, fontsize=9, loc="upper right")
style(ax, "Equal-weight fusion still drags dense retrieval down across scripts", "MRR@10, Tamil-script corpus. RRF k = 60; BM25 lists hold only documents with a positive score")
fig.tight_layout(); fig.savefig("results/charts/fig3_hybrid.png", dpi=200); plt.close()
print("ok")
