"""Unit-level (conversation) contrast for A13: 550B-writer plain stream vs 30B-writer plain stream on LoCoMo, reader fixed.
10,000 cluster bootstrap (seed 0) + exact sign-flip permutation. Output: results/a13_unit_stats.txt"""
import csv, random, itertools, collections, pathlib
R = pathlib.Path(__file__).resolve().parent.parent / "results"
a = collections.defaultdict(lambda: collections.defaultdict(list))
for r in csv.DictReader(open(R / "a13_ultra_scores.csv")):
    if r["dataset"] == "locomo" and r["cond"] == "ultra_stream": a[r["unit"]]["u"].append(int(r["correct"]))
for r in csv.DictReader(open(R / "a7_locomo_scores.csv")):
    if r["cond"] == "stream" and r["conv"] in a: a[r["conv"]]["s"].append(int(r["correct"]))
d = [100 * (sum(v["u"]) / len(v["u"]) - sum(v["s"]) / len(v["s"])) for v in a.values()]
random.seed(0); m = sum(d) / len(d)
bs = sorted(sum(random.choice(d) for _ in d) / len(d) for _ in range(10000))
perm = sum(abs(sum(x * y for x, y in zip(s, d))) >= abs(sum(d)) - 1e-9 for s in itertools.product([1, -1], repeat=len(d))) / 2 ** len(d)
out = (f"LoCoMo units={len(d)} ultra_stream-stream30B diff={m:+.1f} unit-bootstrap[{bs[250]:+.1f},{bs[9749]:+.1f}] "
       f"perm_p={perm:.4f} wins={sum(x>0 for x in d)} losses={sum(x<0 for x in d)}")
print(out); (R / "a13_unit_stats.txt").write_text(out + "\n")
