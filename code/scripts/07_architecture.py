"""Draw the system architecture diagram (results/charts/fig0_architecture.png)."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BG, INK = "#ffffff", "#1d1d1f"
fig, ax = plt.subplots(figsize=(13, 6.2)); fig.patch.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.2); ax.axis("off")
def box(x, y, w, h, title, body="", fc="#e8e8ea", dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=INK if not dashed else "#888",
                                lw=1.1, ls="--" if dashed else "-"))
    ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="top", fontsize=10.5, fontweight="bold", color=INK)
    if body: ax.text(x + w / 2, y + h - 0.55, body, ha="center", va="top", fontsize=8.6, color="#333", linespacing=1.35)
def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
# query path (top)
box(0.2, 3.6, 2.1, 1.9, "User query", "English\nTamil script\nRomanised Tamil\nCode-mixed (Tanglish)", "#b1bcd2")
box(2.7, 3.6, 2.3, 1.9, "Script & language ID", "per token:\nTamil script / English /\nromanised Tamil\n(wordfreq + particle list)")
box(5.4, 3.6, 2.4, 1.9, "Query normaliser", "romanised Tamil -> Tamil\nscript (ITRANS or\nTanglish rules);\nEnglish tokens kept", "#dbb691")
box(8.2, 3.3, 2.3, 2.5, "Retrievers", "BM25 (word)\nBM25 (char 3-gram)\nDense: multilingual-\ne5-small (384-d)", "#b9cdbd")
box(10.9, 3.6, 1.9, 1.9, "Fusion", "Reciprocal Rank\nFusion (k = 60);\nBM25 lists keep\nscore > 0 docs only\n-> top-10 docs")
# corpus path (bottom)
box(0.2, 0.5, 2.1, 1.9, "Tamil corpus", "500 news docs\n(nlpctx/tamil-\nenglish-retrieval)", "#b1bcd2")
box(2.7, 0.5, 2.3, 1.9, "Chunker", "whole-doc here\n(median 326 chars);\nTamil-aware chunker\nin Module 3", dashed=True)
box(5.4, 0.5, 2.4, 1.9, "Indexes", "BM25 word index\nBM25 char index\ndense vector matrix")
box(8.2, 0.5, 2.3, 1.9, "Evaluation", "Recall@1/5/10, MRR@10,\nnDCG@10, latency,\nbootstrap 95% CI", "#d9c489")
box(10.9, 0.5, 1.9, 1.9, "LLM generator", "answer from\nretrieved docs\n(Module 4)", dashed=True)
for a in [(2.3, 4.55, 2.7, 4.55), (5.0, 4.55, 5.4, 4.55), (7.8, 4.55, 8.2, 4.55), (10.5, 4.55, 10.9, 4.55),
          (2.3, 1.45, 2.7, 1.45), (5.0, 1.45, 5.4, 1.45), (6.6, 2.4, 8.6, 3.3), (11.85, 3.6, 11.85, 2.4), (10.9, 3.9, 10.5, 2.2)]:
    arrow(*a)
ax.text(0.2, 6.0, "Code-mixed RAG retrieval pipeline (Modules 1-2 built; dashed = later modules)", fontsize=13, fontweight="bold", color=INK)
fig.savefig("results/charts/fig0_architecture.png", dpi=200, bbox_inches="tight", facecolor=BG); print("ok")
