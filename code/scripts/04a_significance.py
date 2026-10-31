"""Paired significance tests (query-level and document-cluster bootstrap) + cluster-bootstrap CIs.
Queries are clustered within source documents (2,154 queries over 500 docs, ~4.3 per doc), so the
cluster bootstrap resamples whole documents with all their queries: a stricter test than resampling queries."""
import sys, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from tanglish_rag.metrics import paired_bootstrap_p
pq = pd.read_csv("results/per_query.csv")
q = pd.read_json("data/queries.jsonl", lines=True)[["qid", "doc_id"]].sort_values("qid")
doc_codes = pd.factorize(q.doc_id)[0]; ND = doc_codes.max() + 1
def col(c, s, r): return pq[(pq.corpus == c) & (pq.query_set == s) & (pq.retriever == r)].sort_values("qid")["MRR@10"].values
def cluster_boot(v, n_boot=2000, seed=0):
    """Bootstrap means of v resampling documents (clusters). Returns array of n_boot means."""
    sums = np.bincount(doc_codes, weights=v, minlength=ND); cnt = np.bincount(doc_codes, minlength=ND)
    idx = np.random.default_rng(seed).integers(0, ND, size=(n_boot, ND))
    return sums[idx].sum(1) / cnt[idx].sum(1)
def cluster_p(a, b, n_boot=2000, seed=0):
    d = b - a; obs = d.mean(); boots = cluster_boot(d - obs, n_boot, seed)
    return float((np.abs(boots) >= abs(obs)).mean())
COMP = [("rom", "rom_rules", "Dense-e5"), ("rom", "rom_rules", "BM25-char3"), ("rom", "rom_rules", "Hybrid-RRF3"),
        ("rom_itrans", "rom_rules", "Dense-e5"), ("rom_itrans", "rom_rules", "BM25-char3"),
        ("cm", "cm_rules", "Dense-e5"), ("cm", "cm_rules", "BM25"), ("cm", "cm_rules", "Hybrid-RRF3")]
out = []
def add(kind, a_set, b_set, ra, rb):
    x, y = col("ta", a_set, ra), col("ta", b_set, rb); d = y - x
    lo, hi = np.quantile(cluster_boot(d), [.025, .975])
    out.append({"kind": kind, "from": a_set, "to": b_set, "retriever_from": ra, "retriever_to": rb,
                "MRR_from": x.mean(), "MRR_to": y.mean(), "delta": d.mean(),
                "p_paired_bootstrap": paired_bootstrap_p(x, y), "p_cluster_bootstrap": cluster_p(x, y),
                "delta_CI95_cluster": f"[{lo:+.3f}, {hi:+.3f}]"})
for a, b, r in COMP: add("normalisation", a, b, r, r)
for s in ("ta", "en", "cm", "rom", "rom_rules"):
    add("fusion", s, s, "Dense-e5", "Hybrid-RRF")
    add("fusion-naive", s, s, "Dense-e5", "Hybrid-RRF-naive")
add("fusion", "rom_rules", "rom_rules", "BM25-char3", "Hybrid-RRF3")
sig = pd.DataFrame(out); sig.to_csv("results/significance.csv", index=False, float_format="%.6f"); print(sig.round(4).to_string())
# cluster-bootstrap 95% CIs of MRR@10 for every Tamil-corpus run, beside the query-level CI
rows = []
for (c, s, r), g in pq[pq.corpus == "ta"].groupby(["corpus", "query_set", "retriever"]):
    v = g.sort_values("qid")["MRR@10"].values; lo, hi = np.quantile(cluster_boot(v, 1000), [.025, .975])
    rows.append({"corpus": c, "query_set": s, "retriever": r, "MRR@10": v.mean(), "CI95_cluster": f"[{lo:.3f}, {hi:.3f}]"})
pd.DataFrame(rows).to_csv("results/cluster_ci.csv", index=False, float_format="%.6f")
