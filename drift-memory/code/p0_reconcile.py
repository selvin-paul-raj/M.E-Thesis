"""P0 (brief v2): reconcile counts and add missing tests from saved outputs only (no model calls).
a) rewrite denominators per benchmark and length bins per benchmark; b) pooled weighting; c) batch size / rewrites per stream;
d) detector precision/recall vs fact-loss events (from a18 output); e) LoCoMo stream-k0 gap decomposition;
f) exact McNemar on LongMemEval stream vs guard; g) TOST for Memora k2 vs k0.
Writes results/p0_reconcile.txt"""
import csv, json, glob, pathlib, collections, random, re
from math import comb
R = pathlib.Path(__file__).resolve().parent.parent / "results"
out = []; say = lambda *a: out.append(" ".join(str(x) for x in a))
ev = lambda a, b: a >= 300 and b <= 0.5 * a

# ---- a, c: streams
S = {}
for f in glob.glob(str(R / "a5_stream_memories/*.json")):
    n = pathlib.Path(f).stem
    if n != "academic_researcher": S[("Memora", n)] = json.load(open(f))["words"]
for f in glob.glob(str(R / "a7_stream_memories/*_plain.json")): S[("LoCoMo", pathlib.Path(f).stem.replace("_plain", ""))] = json.load(open(f))["words"]
LQ = {r["qid"] for r in csv.DictReader(open(R / "a11_lme_scores.csv"))}
for f in glob.glob(str(R / "a11_memories/*_plain.json")):
    q = pathlib.Path(f).stem.replace("_plain", "")
    if q in LQ: S[("LongMemEval", q)] = json.load(open(f))["words"]
BATCH = {"LoCoMo": "1 session per rewrite (stream_pilot.py)", "Memora": "10 sessions per rewrite (memora_stream.py)",
         "LongMemEval": "5 sessions per rewrite (a11_longmemeval.py BATCH=5)"}
say("## a/c. 30B plain streams: writer calls, transitions, eligible transitions (old>=300), collapses")
say("benchmark | batching | streams | writer calls (incl. first from empty) | rewrites per stream min/median/max | transitions (old->new) | eligible (old>=300) | collapses | streams hit")
T = collections.Counter()
for b in ("LoCoMo", "Memora", "LongMemEval"):
    ks = [k for k in S if k[0] == b]; L = [len(S[k]) for k in ks]
    tr = sum(len(S[k]) - 1 for k in ks); el = sum(1 for k in ks for a, c in zip(S[k], S[k][1:]) if a >= 300)
    co = sum(1 for k in ks for a, c in zip(S[k], S[k][1:]) if ev(a, c)); hit = sum(1 for k in ks if any(ev(a, c) for a, c in zip(S[k], S[k][1:])))
    T.update(calls=sum(L), tr=tr, el=el, co=co, streams=len(ks), hit=hit)
    say(b, "|", BATCH[b], "|", len(ks), "|", sum(L), "|", min(L), sorted(L)[len(L)//2], max(L), "|", tr, "|", el, "|", co, "|", hit)
say("all 30B |", "|", T["streams"], "|", T["calls"], "|", "|", T["tr"], "|", T["el"], "|", T["co"], "|", T["hit"])
say("NOTE: the v7 figure '552 rewrites from >=300 words' is wrong: 552 is all transitions; eligible (old>=300) is", T["el"],
    "; collapses", T["co"], "= LoCoMo+Memora", sum(1 for k in S if k[0] != "LongMemEval" for a, c in zip(S[k], S[k][1:]) if ev(a, c)),
    "+ LongMemEval", sum(1 for k in S if k[0] == "LongMemEval" for a, c in zip(S[k], S[k][1:]) if ev(a, c)))
say("\n## a. Collapse rate by pre-rewrite length bin, per benchmark (30B)")
for b in ("LoCoMo", "Memora", "LongMemEval", "all"):
    P = [(a, c) for k in S if b in ("all", k[0]) for a, c in zip(S[k], S[k][1:]) if a >= 300]
    row = []
    for lo, hi in ((300, 600), (600, 900), (900, 1200), (1200, 1500), (1500, 10**6)):
        Q = [(a, c) for a, c in P if lo <= a < hi]; n_ = sum(ev(a, c) for a, c in Q)
        row.append(f"{lo}-{hi if hi < 10**6 else 'inf'}: {n_}/{len(Q)}" + (f" ({100*n_/len(Q):.1f}%)" if Q else ""))
    say(b, "; ".join(row))

# ---- b: pooled weighting
def load(path, ucol, ds, conds):
    rows = []
    for r in csv.DictReader(open(R / path)):
        if r["cond"] in conds and r[ucol] != "academic_researcher": rows.append((ds, r[ucol], r["cond"], r["qid"], int(r["correct"])))
    return rows
rows = load("a5_scores_nemotron-3.5-lightning-30b-a3b.csv", "persona", "memora", {"k0", "stream"}) + \
       load("a8_retry_scores.csv", "unit", None, {"stream_retry"}) + load("a6_guard_scores.csv", "persona", "memora", {"stream_guard"}) + \
       load("a7_locomo_scores.csv", "conv", "locomo", {"k0", "stream", "stream_guard"})
rows = [(d if d else ("memora" if not u.startswith("conv") else "locomo"), u, c, q, x) for d, u, c, q, x in rows]
# bounded guard identical to stream on units where it never fired: fill
have = {(d, u) for d, u, c, q, x in rows if c == "stream_retry"}
rows += [(d, u, "stream_retry", q, x) for d, u, c, q, x in list(rows) if c == "stream" and (d, u) not in have]
say("\n## b. Pooled accuracy under three weightings (LoCoMo 10 convs x 10 q; Memora 9 personas, rubric checks)")
for c in ("k0", "stream", "stream_guard", "stream_retry"):
    R_ = [r for r in rows if r[2] == c]
    item = 100 * sum(r[4] for r in R_) / len(R_)
    q = collections.defaultdict(list)
    for d, u, _, qid, x in R_: q[(d, u, qid)].append(x)
    qa = 100 * sum(sum(v) / len(v) for v in q.values()) / len(q)
    un = collections.defaultdict(list)
    for d, u, _, qid, x in R_: un[(d, u)].append(x)
    ua = 100 * sum(sum(v) / len(v) for v in un.values()) / len(un)
    nm = sum(1 for r in R_ if r[0] == "memora")
    say(f"{c}: item-weighted (v7 'Pooled', {len(R_)} items = {len(R_)-nm} LoCoMo questions + {nm} Memora checks) {item:.1f}; "
        f"question-weighted ({len(q)} questions, Memora question = mean of its checks) {qa:.1f}; unit-weighted ({len(un)} units) {ua:.1f}")

# ---- d
a18 = (R / "a18_fact_survival.txt").read_text()
say("\n## d. Length detector vs fact-loss events (from a18_fact_survival.txt; lexical line survival, 280 eligible rewrites of 19 plain LoCoMo+Memora streams)")
for line in a18.splitlines():
    if line.startswith("fact-loss ="): say(line)
say("Definition: a fact-loss event is an eligible rewrite (old>=300 words) whose line survival is below 0.5 (sensitivity: 0.7).")

# ---- e
say("\n## e. LoCoMo stream - k0 decomposition (100 q, 10 convs)")
COLL = {"conv-26", "conv-42", "conv-47"}
lc = [r for r in rows if r[0] == "locomo" and r[2] in ("k0", "stream")]
def tot(cs, conds): return sum(r[4] for r in lc if r[2] == conds and r[1] in cs)
allc = {r[1] for r in lc}; oth = allc - COLL
d_all = tot(allc, "stream") - tot(allc, "k0"); d_c = tot(COLL, "stream") - tot(COLL, "k0"); d_o = tot(oth, "stream") - tot(oth, "k0")
say(f"total gap {d_all:+d} questions of 100 ({d_all:+d} pt); collapsed 3 convs {d_c:+d} pt; other 7 convs {d_o:+d} pt")

# ---- f
say("\n## f. LongMemEval stream vs bounded guard, exact McNemar (23 instances, 1 question each)")
L = collections.defaultdict(dict)
for r in csv.DictReader(open(R / "a11_lme_scores.csv")): L[r["qid"]][r["cond"]] = int(r["correct"])
pr = [(v["stream"], v["guard"]) for v in L.values() if "stream" in v and "guard" in v]
b_ = sum(1 for s, g in pr if s == 1 and g == 0); c_ = sum(1 for s, g in pr if s == 0 and g == 1); n = b_ + c_
p = min(1.0, 2 * sum(comb(n, i) for i in range(0, min(b_, c_) + 1)) / 2 ** n) if n else 1.0
say(f"n={len(pr)} stream correct {sum(s for s,g in pr)}, guard correct {sum(g for s,g in pr)}; discordant: stream-only {b_}, guard-only {c_}; exact McNemar p={p:.3f}")

# ---- g
say("\n## g. TOST Memora k2 vs k0 (margin 5 pt), from contrasts.csv")
for r in csv.DictReader(open(R / "contrasts.csv")):
    if r["contrast"] == "Memora 9 k2-k0":
        say(f"diff {r['diff_pooled']}; 95% CI [{r['ci95_lo']}, {r['ci95_hi']}]; 90% CI [{r['ci90_lo']}, {r['ci90_hi']}] inside +/-5 -> equivalent at alpha .05 (two one-sided tests): {r['tost_equiv_5pt']}")
(R / "p0_reconcile.txt").write_text("\n".join(out) + "\n"); print("\n".join(out))

# ---- extra: guard trigger denominators, 550B transitions, TOST p
say("\n## extra. Guard triggers and denominators")
lq = LQ
gt = [json.load(open(f)) for f in glob.glob(str(R / "a11_memories/*_guard.json")) if pathlib.Path(f).stem.replace("_guard", "") in lq]
say(f"LongMemEval bounded guard: {len(gt)} streams, triggers {sum(len(d['events']) for d in gt)}, transitions {sum(len(d['words'])-1 for d in gt)}, writer calls {sum(len(d['words']) for d in gt)}")
rt = [json.load(open(f)) for f in glob.glob(str(R / "a8_retry_memories/*.json"))]
say(f"LoCoMo+Memora bounded guard (units where it diverged from stream): {len(rt)} streams, triggers {sum(len(d['events']) for d in rt)}, transitions {sum(len(d['words'])-1 for d in rt)}")
U5 = {(r["dataset"], r["unit"]) for r in csv.DictReader(open(R / "a13_ultra_scores.csv"))}
u5 = []
for f in glob.glob(str(R / "a13_ultra_memories/*ultra_stream.json")):
    st = pathlib.Path(f).stem; ds_, un_ = st.split("_", 1)[0], st.split("_", 1)[1].replace("_ultra_stream", "")
    if (ds_, un_) in U5: u5.append(json.load(open(f))["words"])
say(f"550B plain: {len(u5)} streams, writer calls {sum(map(len,u5))}, transitions {sum(len(w)-1 for w in u5)}, eligible {sum(1 for w in u5 for a,b in zip(w,w[1:]) if a>=300)}, collapses {sum(1 for w in u5 for a,b in zip(w,w[1:]) if ev(a,b))}")
# TOST p from unit bootstrap of Memora k2-k0 (same resampling as stats_cluster: 10,000, seed 0)
D = collections.defaultdict(lambda: [0, 0])
for r in csv.DictReader(open(R / "a5_scores_nemotron-3.5-lightning-30b-a3b.csv")):
    if r["persona"] != "academic_researcher" and r["cond"] in ("k0", "k2"): D[(r["persona"], r["cond"])][0] += int(r["correct"]); D[(r["persona"], r["cond"])][1] += 1
ps = sorted({p for p, c in D}); pairs = [(D[(p, "k0")], D[(p, "k2")]) for p in ps]
acc = lambda P, i: 100 * sum(x[i][0] for x in P) / sum(x[i][1] for x in P)
rng = random.Random(0); bs = sorted(acc(P, 1) - acc(P, 0) for P in ([rng.choice(pairs) for _ in pairs] for _ in range(10000)))
p_lo = sum(b <= -5 for b in bs) / len(bs); p_hi = sum(b >= 5 for b in bs) / len(bs)
say(f"TOST (bootstrap) Memora k2-k0, margin 5: p_lower={p_lo:.4f} p_upper={p_hi:.4f} -> TOST p={max(p_lo,p_hi):.4f}; 90% CI [{bs[500]:.1f}, {bs[9499]:.1f}]")
(R / "p0_reconcile.txt").write_text("\n".join(out) + "\n")

# ---- b2: pooled contrasts under question weighting (Memora question = mean of its checks), unit clusters
import itertools
say("\n## b2. Pooled 19-unit contrasts, question-weighted (each unit's accuracy = mean over its questions; pooled = mean over all 190 questions)")
Q = collections.defaultdict(lambda: collections.defaultdict(list))
for d, u, c, qid, x in rows: Q[(d, u, c)][qid].append(x)
def uq(d, u, c): v = Q[(d, u, c)]; return [sum(x) / len(x) for x in v.values()]
UN = sorted({(d, u) for d, u, c, q, x in rows})
for a, b in (("stream", "stream_retry"), ("stream", "stream_guard"), ("k0", "stream"), ("k0", "stream_retry")):
    P = [(uq(d, u, a), uq(d, u, b)) for d, u in UN]
    f = lambda PP: 100 * (sum(sum(y) for x, y in PP) / sum(len(y) for x, y in PP) - sum(sum(x) for x, y in PP) / sum(len(x) for x, y in PP))
    obs = f(P); rng = random.Random(0); bs = sorted(f([rng.choice(P) for _ in P]) for _ in range(10000))
    dif = [100 * (sum(y) / len(y) - sum(x) / len(x)) for x, y in P]; m = sum(dif) / len(dif)
    pp = sum(abs(sum(s * x for s, x in zip(sg, dif))) >= abs(sum(dif)) - 1e-9 for sg in itertools.product((1, -1), repeat=len(dif))) / 2 ** len(dif)
    say(f"{b}-{a}: diff {obs:+.1f} [{bs[250]:+.1f}, {bs[9749]:+.1f}] perm p={pp:.4f} wins {sum(x>1e-9 for x in dif)} losses {sum(x<-1e-9 for x in dif)}")
(R / "p0_reconcile.txt").write_text("\n".join(out) + "\n")
