"""A9: analyses for the full paper, using existing outputs only (no new model calls).
Writes results/a9_analysis.txt and paper/fig_trajectories.pdf."""
import json, glob, csv, collections, pathlib
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = pathlib.Path(__file__).resolve().parent.parent / "results"; P = R.parent / "paper"
out = []; say = lambda *a: out.append(" ".join(str(x) for x in a))

streams = {}
for f in sorted(glob.glob(str(R / "a5_stream_memories/*.json"))):
    n = pathlib.Path(f).stem
    if n != "academic_researcher": streams["memora/" + n] = json.load(open(f))["words"]
for f in sorted(glob.glob(str(R / "a7_stream_memories/*_plain.json"))):
    streams["locomo/" + pathlib.Path(f).stem.replace("_plain", "")] = json.load(open(f))["words"]
nrw = sum(len(w) - 1 for w in streams.values())
say("Nemotron streams:", len(streams), "rewrites:", nrw)

def events(w, frac, floor):
    return [(i + 1, a, b) for i, (a, b) in enumerate(zip(w, w[1:])) if a >= floor and b <= frac * a]

say("\n## Threshold sensitivity (collapse = shrink to <= frac of old, old >= floor words)")
say("frac floor events rate% streams_hit")
for frac in (0.3, 0.4, 0.5, 0.6, 0.7):
    for floor in (200, 300, 500):
        ev = {k: events(w, frac, floor) for k, w in streams.items()}
        n = sum(len(v) for v in ev.values())
        say(frac, floor, n, f"{100*n/nrw:.1f}", sum(1 for v in ev.values() if v))
# shrink-ratio distribution
ratios = [b / a for w in streams.values() for a, b in zip(w, w[1:]) if a >= 300]
say("\nrewrites from >=300 words:", len(ratios), "ratio<=0.5:", sum(r <= .5 for r in ratios),
    "0.5-0.7:", sum(.5 < r <= .7 for r in ratios), "0.7-0.9:", sum(.7 < r <= .9 for r in ratios), ">0.9:", sum(r > .9 for r in ratios))

say("\n## Recovery of length after each collapse (default 0.5/300)")
rec = 0; tot = 0
for k, w in streams.items():
    for i, a, b in events(w, .5, 300):
        tot += 1; later = w[i + 1:]; back = next((j for j, x in enumerate(later, 1) if x >= a), None)
        rec += back is not None
        say(k, f"step {i}: {a}->{b}, regained >= {a} words", f"after {back} sessions" if back else "never", "| final", w[-1])
say(f"regained pre-collapse length: {rec}/{tot}")

say("\n## Guard cost")
acts = collections.Counter(); nguard = 0
for f in glob.glob(str(R / "a6_guard_memories/*.json")) + glob.glob(str(R / "a7_stream_memories/*_guard.json")):
    d = json.load(open(f)); nguard += len(d["words"]) - 1
    for e in d.get("events", []): acts[e["action"]] += 1
say("guard-append rewrites", nguard, "triggers", sum(acts.values()), dict(acts),
    f"extra calls {100*sum(acts.values())/nguard:.1f}%")
b = [e for f in glob.glob(str(R / "a8_retry_memories/*.json")) for e in json.load(open(f))["events"]]
say("guard-bounded triggers", len(b), "recovered (kept >= 0.5*old):", sum(e["kept"] >= .5 * e["old"] for e in b))

say("\n## Per-unit accuracy (%)")
def per(path, ucol):
    D = collections.defaultdict(lambda: [0, 0])
    for r in csv.DictReader(open(path)):
        D[(r[ucol], r["cond"])][0] += int(r["correct"]); D[(r[ucol], r["cond"])][1] += 1
    return D
M = per(R / "a5_scores_nemotron-3.5-lightning-30b-a3b.csv", "persona"); M.update(per(R / "a6_guard_scores.csv", "persona"))
L = per(R / "a7_locomo_scores.csv", "conv")
A = per(R / "a8_retry_scores.csv", "unit")
for D, ds in ((M, "memora"), (L, "locomo")):
    for u in sorted({u for u, _ in D}):
        if (u, "stream") not in D: continue
        sr = A.get((u, "stream_retry"), D[(u, "stream")])
        f = lambda c: f"{100*D[(u,c)][0]/D[(u,c)][1]:.1f}" if (u, c) in D else "-"
        ncol = len(events(streams.get(ds + "/" + u, []), .5, 300))
        say(ds, u, "k0", f("k0"), "stream", f("stream"), "g-app", f("stream_guard"), "g-bnd", f"{100*sr[0]/sr[1]:.1f}",
            "collapses", ncol, "final_words", streams.get(ds + "/" + u, ["?"])[-1])

say("\n## LoCoMo by category (correct/n)")
C = collections.defaultdict(lambda: [0, 0])
for r in csv.DictReader(open(R / "a7_locomo_scores.csv")):
    C[(r["category"], r["cond"])][0] += int(r["correct"]); C[(r["category"], r["cond"])][1] += 1
for c in sorted({c for c, _ in C}):
    say("cat", c, {k: f"{C[(c,k)][0]}/{C[(c,k)][1]}" for k in ("k0", "stream", "stream_guard")})

# figure: length trajectories for collapsed streams, plain vs bounded guard
ret = {pathlib.Path(f).stem.replace("memora_", "memora/").replace("locomo_", "locomo/"): json.load(open(f))["words"]
       for f in glob.glob(str(R / "a8_retry_memories/*.json"))}
keys = sorted(ret); fig, ax = plt.subplots(2, 3, figsize=(7.2, 3.6), sharex=False)
for a, k in zip(ax.flat, keys):
    w = streams[k]; a.plot(range(1, len(w) + 1), w, color="tab:red", lw=1.2, label="stream")
    g = ret[k]; a.plot(range(1, len(g) + 1), g, color="tab:blue", lw=1.2, ls="--", label="guard (bounded)")
    for i, _, _ in events(w, .5, 300): a.axvline(i + 1, color="tab:red", alpha=.25, lw=.8)
    a.set_title(k.replace("_", " "), fontsize=7); a.tick_params(labelsize=6)
ax[0, 0].legend(fontsize=6); fig.supxlabel("rewrite step", fontsize=7); fig.supylabel("memory words", fontsize=7)
fig.tight_layout(); fig.savefig(P / "fig_trajectories.pdf"); fig.savefig(R / "fig_trajectories.png", dpi=110)
open(R / "a9_analysis.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
