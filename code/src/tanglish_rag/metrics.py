"""IR metrics for single-relevant-document queries (same definitions as ChunkLab's retrieval_metrics)."""
from __future__ import annotations
import math
import numpy as np

def rank_of(ranked: list[str], gold: str) -> int | None:
    try:
        return ranked.index(gold) + 1
    except ValueError:
        return None

def per_query(ranked: list[str], gold: str) -> dict:
    r = rank_of(ranked[:10], gold)
    return {
        "R@1": float(r is not None and r <= 1),
        "R@5": float(r is not None and r <= 5),
        "R@10": float(r is not None and r <= 10),
        "MRR@10": 1.0 / r if r else 0.0,
        "nDCG@10": 1.0 / math.log2(r + 1) if r else 0.0,  # one relevant doc -> IDCG = 1
        "rank": r if r else -1,
    }

def bootstrap_ci(values, n_boot: int = 1000, seed: int = 0, alpha: float = 0.05):
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(n_boot, len(v)))
    means = v[idx].mean(axis=1)
    return float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))

def paired_bootstrap_p(a, b, n_boot: int = 2000, seed: int = 0) -> float:
    """Two-sided paired bootstrap p-value for mean(b) - mean(a) != 0."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    obs = d.mean()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    boots = (d - obs)[idx].mean(axis=1)  # null-centred
    return float((np.abs(boots) >= abs(obs)).mean())
