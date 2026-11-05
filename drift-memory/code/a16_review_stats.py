"""A16: reviewer-requested analyses on existing outputs (no model calls).
(1) unit-level inference: per-unit accuracy, cluster bootstrap over units (5,000, seed 0), exact sign-flip permutation and sign test;
(2) stream-level collapse rates with Clopper-Pearson intervals;
(3) collapse vs the writer's 1,200-word cap: collapse rate by pre-rewrite length bin, for the 30B writer (Memora, LoCoMo, LongMemEval) and the 550B writer.
Writes results/a16_review_stats.txt"""
import csv, json, glob, pathlib, random, itertools, collections, math
from math import comb
def _cdf(k, n, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))
class _BT:
    def __init__(s, k, n):
        pk = comb(n, k) * .5**n; s.pvalue = min(1.0, sum(comb(n, i) * .5**n for i in range(n + 1) if comb(n, i) * .5**n <= pk + 1e-12))
binomtest = _BT
def _solve(f, t):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if f(m) > t: lo = m
        else: hi = m
    return (lo + hi) / 2
R = pathlib.Path(__file__).resolve().parent.parent / "results"
out = []; say = lambda *a: out.append(" ".join(str(x) for x in a))

def per_unit(path, ucol, dscol=None, ds=None):
    D = collections.defaultdict(lambda: [0, 0])
    for r in csv.DictReader(open(R / path)):
        d = r.get(dscol, ds) if dscol else ds
        D[(d, r[ucol], r["cond"])][0] += int(r["correct"]); D[(d, r[ucol], r["cond"])][1] += 1
    return D
U = {}
U.update(per_unit("a5_scores_nemotron-3.5-lightning-30b-a3b.csv", "persona", ds="memora"))
U.update(per_unit("a6_guard_scores.csv", "persona", ds="memora"))
U.update(per_unit("a7_locomo_scores.csv", "conv", ds="locomo"))
U.update(per_unit("a8_retry_scores.csv", "unit", "dataset"))
U.update(per_unit("a15_escalate_scores.csv", "unit", "dataset"))
U.update(per_unit("a13_ultra_scores.csv", "unit", "dataset"))
units = sorted({(d, u) for d, u, c in U if c == "stream" and u != "academic_researcher"})
def get(d, u, c, fill=None):
    if (d, u, c) in U: return U[(d, u, c)]
    if fill and (d, u, fill) in U: return U[(d, u, fill)]  # bounded guard / escalation never fire on non-collapsed streams
    return None

def test(name, us, a, b, fa=None, fb=None):
    pairs = [(get(d, u, a, fa), get(d, u, b, fb)) for d, u in us]
    pairs = [(x, y) for x, y in pairs if x and y]
    n = len(pairs)
    acc = lambda P, i: 100 * sum(p[i][0] for p in P) / sum(p[i][1] for p in P)
    diffs = [100 * (y[0] / y[1] - x[0] / x[1]) for x, y in pairs]
    obs = acc(pairs, 1) - acc(pairs, 0)
    rng = random.Random(0); bs = []
    for _ in range(5000):
        P = [rng.choice(pairs) for _ in pairs]; bs.append(acc(P, 1) - acc(P, 0))
    bs.sort(); lo, hi = bs[125], bs[4874]
    m = sum(diffs) / n; nz = [x for x in diffs if abs(x) > 1e-9]
    perm = [abs(sum(s * x for s, x in zip(sg, diffs)) / n) >= abs(m) - 1e-9 for sg in itertools.product((1, -1), repeat=n)] if n <= 20 else []
    pp = sum(perm) / len(perm) if perm else float("nan")
    wins = sum(x > 0 for x in nz); st = binomtest(wins, len(nz)).pvalue if nz else 1.0
    say(f"{name}: units={n} {a}={acc(pairs,0):.1f} {b}={acc(pairs,1):.1f} diff={obs:+.1f} unit-bootstrap[{lo:+.1f},{hi:+.1f}]"
        f" mean-unit-diff={m:+.1f} perm_p={pp:.3f} wins={wins}/{len(nz)} (ties {n-len(nz)}) sign_p={st:.3f}")

say("A16 unit-level inference. Resampling unit = conversation (LoCoMo) or persona (Memora).")
mem = [x for x in units if x[0] == "memora"]; loc = [x for x in units if x[0] == "locomo"]
COL = [("locomo", "conv-26"), ("locomo", "conv-42"), ("locomo", "conv-47"),
       ("memora", "business_executive"), ("memora", "management_consultant"), ("memora", "marketing_manager")]
for nm, us in (("Memora 9", mem), ("LoCoMo 10", loc), ("Pooled 19", units), ("Collapsed 6", COL)):
    test(nm + " retry-stream", us, "stream", "stream_retry", fb="stream")
    test(nm + " guard_append-stream", us, "stream", "stream_guard")
    test(nm + " stream-k0", us, "k0", "stream")
    test(nm + " retry-k0", us, "k0", "stream_retry", fb="stream")
    if all((d, u, "k2") in U for d, u in us): test(nm + " k2-k0", us, "k0", "k2")
test("Collapsed 6 escalate-stream", COL, "stream", "escalate")
test("Collapsed 6 escalate-retry", COL, "stream_retry", "escalate")
say("\nPer collapsed unit (acc %): unit k0 stream retry append escalate")
for d, u in COL:
    f = lambda c: f"{100*U[(d,u,c)][0]/U[(d,u,c)][1]:.1f}" if (d, u, c) in U else "-"
    say(d, u, f("k0"), f("stream"), f("stream_retry"), f("stream_guard"), f("escalate"))

def cp(k, n):
    lo = 0 if k == 0 else _solve(lambda p: _cdf(k - 1, n, p), 0.975)
    hi = 1 if k == n else _solve(lambda p: _cdf(k, n, p), 0.025)
    return lo * 100, hi * 100
def events(w, frac=.5, floor=300): return [(a, b) for a, b in zip(w, w[1:]) if a >= floor and b <= frac * a]
S = {}
for f in glob.glob(str(R / "a5_stream_memories/*.json")):
    n = pathlib.Path(f).stem
    if n != "academic_researcher": S["30B/memora/" + n] = json.load(open(f))["words"]
for f in glob.glob(str(R / "a7_stream_memories/*_plain.json")): S["30B/locomo/" + pathlib.Path(f).stem] = json.load(open(f))["words"]
LQ = {r["qid"] for r in csv.DictReader(open(R / "a11_lme_scores.csv"))}
UQ = {(r["dataset"], r["unit"]) for r in csv.DictReader(open(R / "a13_ultra_scores.csv"))}
for f in glob.glob(str(R / "a11_memories/*_plain.json")):
    if pathlib.Path(f).stem.replace("_plain", "") in LQ: S["30B/lme/" + pathlib.Path(f).stem] = json.load(open(f))["words"]
for f in glob.glob(str(R / "a13_ultra_memories/*.json")):
    d = json.load(open(f))
    st = pathlib.Path(f).stem; ds_, un_ = st.split("_", 1)[0], st.split("_", 1)[1].replace("_ultra_stream", "")
    if "words" in d and st.endswith("ultra_stream") and (ds_, un_) in UQ: S["550B/x/" + pathlib.Path(f).stem] = d["words"]
say("\n## Stream-level collapse rates (rho=0.5, floor 300), Clopper-Pearson 95%")
for grp in ("30B/memora", "30B/locomo", "30B/lme", "30B/", "550B/"):
    ks = [k for k in S if k.startswith(grp)]
    hit = sum(1 for k in ks if events(S[k])); nrw = sum(len(S[k]) - 1 for k in ks); ne = sum(len(events(S[k])) for k in ks)
    lo, hi = cp(hit, len(ks)); say(f"{grp}: streams hit {hit}/{len(ks)} [{lo:.0f},{hi:.0f}]%  events {ne}/{nrw} rewrites")

say("\n## Collapse vs the 1,200-word cap: rewrites by pre-rewrite length (old), rho=0.5")
say("writer bin rewrites collapses rate%")
for w in ("30B", "550B"):
    pairs = [(a, b) for k, v in S.items() if k.startswith(w) for a, b in zip(v, v[1:]) if a >= 300]
    for lo_, hi_ in ((300, 600), (600, 900), (900, 1200), (1200, 1500), (1500, 99999)):
        P = [(a, b) for a, b in pairs if lo_ <= a < hi_]; c = sum(b <= .5 * a for a, b in P)
        say(w, f"{lo_}-{hi_ if hi_<99999 else 'inf'}", len(P), c, f"{100*c/len(P):.1f}" if P else "-")
    ev = [a for a, b in pairs if b <= .5 * a]
    if ev: say(w, "pre-collapse old length: min", min(ev), "median", sorted(ev)[len(ev) // 2], "max", max(ev),
               "share >=1000:", f"{sum(a>=1000 for a in ev)}/{len(ev)}")
(R / "a16_review_stats.txt").write_text("\n".join(out) + "\n"); print("\n".join(out))
