"""Paired stats across arms: accuracy, 95% bootstrap CI of the difference (10k resamples, clustered by item),
exact McNemar p. Items aligned by position within (unit, cond), which all scripts write in the same order."""
import csv, random, math, pathlib, collections
R = pathlib.Path(__file__).resolve().parents[1] / "results"
def load(fn, unit, dsf=None):
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    p = R / fn
    if not p.exists(): return out
    for x in csv.DictReader(open(p)):
        if dsf and x.get("data") != dsf: continue
        out[x["cond"]][x[unit]].append(int(x["correct"]))
        G.setdefault((fn, x["cond"], x[unit]), []).append(x.get("qid") or x.get("question") or x.get("item"))
    return out
G = {}
def groups(units, d, cond):
    for (fn, c, u), g in G.items():
        pass
    return None
def vec(d, cond, units): return [v for u in units for v in d[cond][u]]
def mcnemar(a, b):
    n01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1); n10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0); n = n01 + n10
    if n == 0: return 1.0, n01, n10
    k = min(n01, n10); p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, p), n01, n10
def boot(a, b, B=10000, seed=13, cl=None):
    """cl: cluster label per item (question); resample whole questions when given."""
    rnd = random.Random(seed); n = len(a); diffs = []
    cl = cl or list(range(n)); bucket = collections.defaultdict(list)
    for i, c in enumerate(cl): bucket[c].append(i)
    keys = list(bucket)
    for _ in range(B):
        idx = [i for _ in keys for i in bucket[keys[rnd.randrange(len(keys))]]]
        diffs.append(sum(b[i] - a[i] for i in idx) / len(idx) * 100)
    diffs.sort(); return diffs[int(.025 * B)], diffs[int(.975 * B)]
out = []
for name, parts in [("Memora (103 checks)", [("memora_scores.csv", "persona", None), ("memora_stream_scores.csv", "persona", None), ("a3_scores.csv", "unit", "memora"), ("a3b_scores.csv", "unit", "memora")]),
                    ("LoCoMo (30 q)", [("pilot_scores.csv", "conv", None), ("stream_scores.csv", "conv", None), ("a3_scores.csv", "unit", "locomo")])]:
    d = collections.defaultdict(dict)
    for fn, unit, ds in parts:
        for c, v in load(fn, unit, ds).items(): d[c].update(v)
    units = sorted(next(iter(d.values())).keys())
    conds = [c for c in ["k=0", "k=1", "k=8", "bm25_raw", "stream_rewrite", "stream", "stream_eq"] if c in d and all(u in d[c] for u in units)]
    out += [f"\n### {name}", "| arm | acc | vs k=8: diff [95% CI, clustered by question] | McNemar p |", "|---|---|---|---|"]
    base = vec(d, "k=8", units)
    cl = None
    for (fn, c, u) in G:
        if c == "k=8" and fn in [x[0] for x in parts]:
            cl = [f"{uu}|{q}" for uu in units for (f2, c2, u2), qs in G.items() if c2 == "k=8" and u2 == uu and f2 == fn for q in qs]; break
    for c in conds:
        v = vec(d, c, units)
        if len(v) != len(base): out.append(f"| {c} | length mismatch {len(v)} vs {len(base)} | | |"); continue
        acc = 100 * sum(v) / len(v)
        if c == "k=8": out.append(f"| {c} | {acc:.1f} | — | — |"); continue
        lo, hi = boot(base, v, cl=cl if cl and len(cl) == len(base) else None); p, _, _ = mcnemar(base, v)
        out.append(f"| {c} | {acc:.1f} | {acc - 100*sum(base)/len(base):+.1f} [{lo:+.1f}, {hi:+.1f}] | {p:.3f} |")
(R / "stats_summary.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
