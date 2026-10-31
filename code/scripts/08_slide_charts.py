"""Square, large-type versions of the charts and a vertical architecture diagram for the slide deck."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BG, INK = "#e8e8ea", "#1d1d1f"; COLS = ["#b1bcd2", "#607868", "#dbb691", "#a79fb8"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "axes.facecolor": BG, "figure.facecolor": BG,
    "axes.edgecolor": INK + "80", "xtick.color": INK, "ytick.color": INK + "99", "axes.spines.top": False,
    "axes.spines.right": False, "xtick.major.size": 0, "ytick.major.size": 0})
R = pd.read_csv("results/main_results.csv"); T = R[R.corpus == "ta"]
def val(s, r, m="MRR@10"): return float(T[(T.query_set == s) & (T.retriever == r)][m].iloc[0])
def bars(ax, groups, series, metric, ylabel):
    n = len(series); w = 0.8 / n; x = np.arange(len(groups))
    for k, (r, c, lab) in enumerate(series):
        v = [val(s, r, metric) for s, _ in groups]; xs = x + (k - (n - 1) / 2) * w
        ax.bar(xs, v, w * .92, color=c, label=lab)
        for xi, vi in zip(xs, v): ax.text(xi, vi + .015, f"{vi:.3f}", ha="center", fontsize=(7 if n > 3 else 10.5), color=INK, family="DejaVu Sans Mono")
    ax.set_xticks(x, [l for _, l in groups], fontsize=15); ax.set_ylim(0, 1.12); ax.set_yticks([0, .25, .5, .75, 1])
    ax.yaxis.grid(True, color=INK, alpha=.08); ax.set_axisbelow(True); ax.set_ylabel(ylabel, color=INK + "99")
    ax.legend(frameon=False, fontsize=13, loc="upper center", ncol=2, bbox_to_anchor=(.5, 1.0))
out = "results/charts/slides/"; import os; os.makedirs(out, exist_ok=True)
fig, ax = plt.subplots(figsize=(8, 8))
bars(ax, [("ta", "Tamil\nscript"), ("en", "English"), ("cm", "Code-\nmixed"), ("rom", "Romanised")],
     [("BM25", COLS[0], "BM25"), ("BM25-char3", COLS[1], "BM25 char 3-gram"), ("Dense-e5", COLS[2], "Dense mE5-small"), ("Hybrid-RRF", COLS[3], "Hybrid RRF")], "MRR@10", "MRR@10")
fig.tight_layout(); fig.savefig(out + "s_fig1.png", dpi=170); plt.close()
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=False)
for ax, b, lab in [(axes[0], "rom", "Romanised queries"), (axes[1], "cm", "Code-mixed queries")]:
    bars(ax, [(b, "Raw"), (f"{b}_itrans", "ITRANS"), (f"{b}_rules", "Tanglish rules")],
         [("Dense-e5", COLS[2], "Dense"), ("BM25-char3", COLS[1], "BM25 char 3-gram"), ("Hybrid-RRF3", COLS[3], "Hybrid RRF3")], "R@10", "Recall@10")
    ax.set_title(lab, loc="left", fontsize=15, color=INK); ax.set_ylim(0, 1.25)
    if b == "cm": ax.get_legend().remove()
fig.tight_layout(); fig.savefig(out + "s_fig2.png", dpi=170); plt.close()
fig, ax = plt.subplots(figsize=(8, 8))
bars(ax, [("ta", "Tamil\nscript"), ("en", "English"), ("cm", "Code-\nmixed"), ("rom_rules", "Romanised\n+ rules")],
     [("Dense-e5", COLS[2], "Dense alone"), ("Hybrid-RRF", COLS[0], "RRF (BM25 + dense)"), ("Hybrid-RRF3", COLS[3], "RRF3 (+ char 3-gram)"), ("Hybrid-RRF-naive", "#1d1d1f4d", "RRF, v1 naive lists")], "MRR@10", "MRR@10")
fig.tight_layout(); fig.savefig(out + "s_fig3.png", dpi=170); plt.close()
# vertical architecture
fig, ax = plt.subplots(figsize=(8, 8)); fig.patch.set_facecolor("white"); ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.axis("off")
def box(x, y, w, h, t, b, fc="#e8e8ea", dash=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec="#888" if dash else INK, lw=1.2, ls="--" if dash else "-"))
    ax.text(x + w / 2, y + h - .17, t, ha="center", va="top", fontsize=13, fontweight="bold", color=INK)
    ax.text(x + w / 2, y + h - .5, b, ha="center", va="top", fontsize=10.5, color="#333", linespacing=1.25)
def arr(x1, y1, x2, y2): ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
W, H = 3.6, 1.25; ys = [6.6, 5.05, 3.5, 1.95, 0.4]
for (t, b, fc, d), y in zip([("User query", "English · Tamil script\nromanised · code-mixed", "#b1bcd2", 0), ("Script & language ID", "per token: Tamil / English /\nromanised Tamil", "#e8e8ea", 0),
        ("Query normaliser", "romanised Tamil → Tamil script\n(ITRANS or Tanglish rules)", "#dbb691", 0), ("Retrievers", "BM25 word · BM25 char 3-gram\ndense mE5-small", "#b9cdbd", 0),
        ("RRF fusion → top-10", "k = 60 over top-100 lists", "#e8e8ea", 0)], ys):
    box(0.1, y, W, H, t, b, fc, d)
for (t, b, fc, d), y in zip([("Tamil corpus", "500 news documents\n(nlpctx dataset)", "#b1bcd2", 0), ("Chunker", "whole document now;\nTamil-aware in Module 3", "#e8e8ea", 1),
        ("Indexes", "BM25 word · BM25 char\ndense vectors", "#e8e8ea", 0), ("Evaluation", "Recall@k · MRR@10 · nDCG@10\nlatency · bootstrap CI", "#d9c489", 0),
        ("LLM generator", "answer from top-10\n(Module 4)", "#e8e8ea", 1)], ys):
    box(4.3, y, W, H, t, b, fc, d)
for a, b in zip(ys[:-1], ys[1:]):
    arr(0.1 + W / 2, a, 0.1 + W / 2, b + H)
for a, b in zip(ys[:2], ys[1:3]): arr(4.3 + W / 2, a, 4.3 + W / 2, b + H)
arr(4.3, ys[2] + H / 2, 0.1 + W, ys[3] + H / 2)
arr(0.1 + W, ys[4] + H / 2, 4.3, ys[3] + H / 2); arr(0.1 + W, ys[4] + H * .3, 4.3, ys[4] + H * .4)
fig.savefig(out + "s_arch.png", dpi=170, bbox_inches="tight", facecolor="white"); plt.close(); print("ok")
