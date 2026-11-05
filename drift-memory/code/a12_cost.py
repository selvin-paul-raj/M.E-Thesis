"""A12: deployment cost. Reader context size (words) per method and environment, from the score CSVs (no model calls)."""
import csv, collections, statistics as S, pathlib
R = pathlib.Path(__file__).resolve().parents[1] / "results"
def agg(f, cond_col="cond", filt=lambda r: True, rename=lambda c: c, unit=None):
    d = collections.defaultdict(dict)
    for r in csv.DictReader(open(R / f)):
        if not filt(r) or not r.get("mem_words"): continue
        u = r[unit] if unit else ""
        d[rename(r[cond_col])][u] = int(float(r["mem_words"]))
    return {c: (S.mean(v.values()), max(v.values())) for c, v in d.items()}
out = []
for env, f, kw in [("LoCoMo", "a7_locomo_scores.csv", dict(unit="conv")),
                   ("Memora", "a5_scores_nemotron-3.5-lightning-30b-a3b.csv", dict(unit="persona")),
                   ("Memora", "a6_guard_scores.csv", dict(unit="persona")),
                   ("Both", "a8_retry_scores.csv", dict(unit="unit")),
                   ("LongMemEval", "a11_lme_scores.csv", dict(unit="qid"))]:
    try:
        for c, (m, mx) in agg(f, **kw).items(): out.append(f"{env:12s} {f:45s} {c:14s} mean_words={m:8.0f} max_words={mx:6d}")
    except Exception as e: out.append(f"{env} {f} ERR {e}")
(R / "a12_cost.txt").write_text("\n".join(out) + "\n"); print("\n".join(out))
