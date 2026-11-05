"""A18: fact (line) survival per rewrite and token cost, replaying the 30B plain streams (Memora 9, LoCoMo 10) from cache only.
A memory line of the old memory "survives" if some line of the new memory contains >= 60% of its content tokens
(lowercased words of >= 3 letters and all numbers). This is a lexical proxy for fact retention, not a semantic judgement.
Reports survival for collapsed vs other rewrites, and precision/recall of the length detector (ratio <= 0.5, old >= 300)
against "fact-loss" rewrites (survival < 0.5). Also reports prompt/completion tokens per rewrite from cached usage.
No model calls: a cache miss raises. Writes results/a18_fact_survival.txt"""
import json, re, pathlib, sys, statistics as st
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import groq_client
from stream_pilot import UPDATE
WR = "nvidia/nemotron-3.5-lightning-30b-a3b"
_orig = groq_client.urllib.request.urlopen
def _no_net(*a, **k): raise RuntimeError("cache miss")
groq_client.urllib.request.urlopen = _no_net
from groq_client import chat
import memora_pilot as mp, pilot
R = pathlib.Path(__file__).resolve().parent.parent / "results"
TOK = re.compile(r"[a-z]{3,}|\d+")
def toks(s): return set(TOK.findall(s.lower()))
def lines(m): return [l for l in m.splitlines() if len(toks(l)) >= 2]
def survival(old, new):
    O = lines(old); N = [toks(l) for l in lines(new)]
    if not O: return None
    keep = sum(1 for l in O if (t := toks(l)) and max((len(t & n) / len(t) for n in N), default=0) >= .6)
    return keep / len(O)

units = []
for p in sorted({l.split(",")[0] for l in open(R / "a5_scores_nemotron-3.5-lightning-30b-a3b.csv").read().splitlines()[1:]}):
    ss = mp.sessions(p); units.append(("memora", p, ["\n\n".join(f"[Session {sid}, {dt}]\n{txt}" for sid, dt, txt in ss[i:i + 10]) for i in range(0, len(ss), 10)], mp.CAP_WORDS))
D = {c["sample_id"]: c for c in json.load(open(pilot.DATA))}
for c in sorted({l.split(",")[0] for l in open(R / "a7_locomo_scores.csv").read().splitlines()[1:]}):
    units.append(("locomo", c, [f"[Session {i}, {dt}]\n" + "\n".join(f"{t['speaker']}: {t['text']}" for t in turns) for i, dt, turns in pilot.sessions(D[c]["conversation"])], pilot.CAP_WORDS))
rows = []; pt = []; ct = []; miss = 0
for ds, u, bs, cap in units:
    mem = ""
    for k, s in enumerate(bs):
        try: m, us = chat(WR, [{"role": "user", "content": UPDATE.format(cap=cap, mem=mem or "(empty)", sess=s)}], max_tokens=3000)
        except RuntimeError: miss += 1; break
        m = m.strip(); pt.append(us.get("prompt_tokens", 0)); ct.append(us.get("completion_tokens", 0))
        o, n = len(mem.split()), len(m.split())
        if o >= 300: rows.append((ds, u, k, o, n, survival(mem, m)))
        mem = m
out = [f"A18 replayed {len(units)} streams, cache misses (stream truncated) {miss}; rewrites from >=300 words: {len(rows)}"]
col = [r for r in rows if r[4] <= .5 * r[3]]; oth = [r for r in rows if r[4] > .5 * r[3]]
f = lambda R_: f"n={len(R_)} mean={100*st.mean(r[5] for r in R_):.1f}% median={100*st.median(r[5] for r in R_):.1f}% min={100*min(r[5] for r in R_):.1f}%"
out += ["line survival, collapsed rewrites: " + f(col), "line survival, other rewrites:     " + f(oth)]
for thr in (.5, .7):
    loss = [r for r in rows if r[5] < thr]; tp = sum(1 for r in col if r[5] < thr)
    out.append(f"fact-loss = survival<{thr}: {len(loss)} rewrites; detector flags {len(col)}, precision {tp}/{len(col)}, recall {tp}/{len(loss)}")
out.append("missed fact-loss rewrites (survival<0.5, not flagged): " + "; ".join(f"{d}/{u} step{k} {o}->{n} surv {100*s:.0f}%" for d, u, k, o, n, s in oth if s < .5))
out.append("collapsed: " + "; ".join(f"{d}/{u} step{k} {o}->{n} surv {100*s:.0f}%" for d, u, k, o, n, s in col))
out.append(f"tokens per rewrite (30B writer, cached usage, n={len(pt)}): prompt mean {st.mean(pt):.0f} (max {max(pt)}), completion mean {st.mean(ct):.0f} (max {max(ct)})")
(R / "a18_fact_survival.txt").write_text("\n".join(out) + "\n"); print("\n".join(out))
