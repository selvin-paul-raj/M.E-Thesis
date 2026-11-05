"""P0b: Table 5 (raw vs hybrid) at unit level, question-weighted (each unit's accuracy = mean over its questions; Memora question = mean of its checks).
Cluster bootstrap 10,000 (seed 0), exact sign-flip over units. Writes results/p0b_hybrid_unit.txt"""
import csv, collections, random, itertools, pathlib
R = pathlib.Path(__file__).resolve().parent.parent / "results"
Q = collections.defaultdict(list)
for r in csv.DictReader(open(R / "a10_hybrid_scores.csv")): Q[(r["dataset"], r["unit"], r["cond"], r["qid"])].append(int(r["correct"]))
U = collections.defaultdict(list)
for (d, u, c, q), v in Q.items(): U[(d, u, c)].append(sum(v) / len(v))
COL = {"conv-26", "conv-42", "conv-47", "business_executive", "management_consultant", "marketing_manager"}
out = []
units = sorted({(d, u) for d, u, c in U if (d, u, "raw") in U and (d, u, "hybrid") in U})
for nm, f in (("LoCoMo", lambda d, u: d == "locomo"), ("Memora", lambda d, u: d == "memora"), ("Pooled", lambda d, u: True),
              ("Collapsed units", lambda d, u: u in COL), ("Non-collapsed units", lambda d, u: u not in COL)):
    us = [x for x in units if f(*x)]
    P = [(U[(d, u, "raw")], U[(d, u, "hybrid")]) for d, u in us]
    acc = lambda PP, i: 100 * sum(sum(p[i]) for p in PP) / sum(len(p[i]) for p in PP)
    obs = acc(P, 1) - acc(P, 0); rng = random.Random(0)
    bs = sorted(acc(B, 1) - acc(B, 0) for B in ([rng.choice(P) for _ in P] for _ in range(10000)))
    dif = [100 * (sum(y) / len(y) - sum(x) / len(x)) for x, y in P]
    pp = sum(abs(sum(s * x for s, x in zip(sg, dif))) >= abs(sum(dif)) - 1e-9 for sg in itertools.product((1, -1), repeat=len(dif))) / 2 ** len(dif)
    out.append(f"{nm}: units={len(us)} n_q={sum(len(p[0]) for p in P)} raw={acc(P,0):.1f} hybrid={acc(P,1):.1f} diff={obs:+.1f} [{bs[250]:+.1f},{bs[9749]:+.1f}] perm_p={pp:.3f} wins={sum(x>1e-9 for x in dif)} losses={sum(x<-1e-9 for x in dif)}")
(R / "p0b_hybrid_unit.txt").write_text("\n".join(out) + "\n"); print("\n".join(out))
