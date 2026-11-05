"""Question-clustered paired bootstrap (5,000 resamples, seed 0) for any scores CSV.
usage: boot.py CSV DATASETCOL UNITCOL QIDCOL CONDA CONDB [subset unit list]
Score = mean over all check rows; resampling unit = (dataset, unit, qid)."""
import csv, sys, random, collections
def boot(rows, a, b, ds, un, qi, units=None, n=5000):
    C = collections.defaultdict(lambda: {a: [], b: []})
    for r in rows:
        if r["cond"] in (a, b) and (units is None or r[un] in units):
            C[(r.get(ds, ""), r[un], r[qi])][r["cond"]].append(int(r["correct"]))
    keys = [k for k, v in C.items() if v[a] and v[b]]
    def score(ks, c):
        s = sum(sum(C[k][c]) for k in ks); m = sum(len(C[k][c]) for k in ks); return 100 * s / m
    sa, sb = score(keys, a), score(keys, b); d = sb - sa; rng = random.Random(0); ds_ = []
    for _ in range(n):
        ks = [rng.choice(keys) for _ in keys]; ds_.append(score(ks, b) - score(ks, a))
    ds_.sort(); lo, hi = ds_[int(.025 * n)], ds_[int(.975 * n)]
    p = min(1.0, 2 * min(sum(x <= 0 for x in ds_), sum(x >= 0 for x in ds_)) / n)
    return len(keys), sa, sb, d, lo, hi, p
if __name__ == "__main__":
    f, ds, un, qi, a, b = sys.argv[1:7]; units = set(sys.argv[7].split(",")) if len(sys.argv) > 7 else None
    rows = list(csv.DictReader(open(f)))
    nq, sa, sb, d, lo, hi, p = boot(rows, a, b, ds, un, qi, units)
    print(f"{f.split('/')[-1]} {b}-{a} subset={sys.argv[7] if units else 'all'}: n_q={nq} {a}={sa:.1f} {b}={sb:.1f} diff={d:+.1f} [{lo:+.1f},{hi:+.1f}] p={p:.3f}")
