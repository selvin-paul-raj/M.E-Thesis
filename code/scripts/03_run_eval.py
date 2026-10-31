"""Evaluate BM25 (word), BM25 (char 3-gram), dense e5-small and hybrid RRF for every query set.
Writes results/per_query.csv, results/main_results.csv (with bootstrap 95% CIs), results/latency.csv."""
import sys, pathlib, time, json
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from tanglish_rag.retrievers import BM25, char_ngrams, word_tokens, topk, topk_positive, rrf
from tanglish_rag.metrics import per_query, bootstrap_ci

MODEL = "multilingual-e5-small"
ONLY = sys.argv[1:]  # optional run filter like ta:rom en:cm (lets long runs be split)
cache = pathlib.Path("results/cache") / MODEL
corpus = pd.read_json("data/corpus.jsonl", lines=True); q = pd.read_json("data/queries.jsonl", lines=True)
doc_ids = corpus.doc_id.tolist()
COL = {"en": "query_en", "ta": "query_ta", "rom": "query_ta_romanized", "cm": "query_ta_codemix",
       "rom_itrans": "rom_itrans", "rom_rules": "rom_rules", "cm_itrans": "cm_itrans", "cm_rules": "cm_rules"}
RUNS = [("ta", s) for s in COL] + [("en", s) for s in ("en", "ta", "rom", "cm")]
lat = []
bm = {}
for corp in ("ta", "en"):
    texts = corpus[f"text_{corp}"].tolist()
    bm[(corp, "word")] = BM25(texts, word_tokens); bm[(corp, "char")] = BM25(texts, char_ngrams)
outdir = pathlib.Path("results/per_query"); outdir.mkdir(parents=True, exist_ok=True)
for corp, qs in RUNS:
    if ONLY and f"{corp}:{qs}" not in ONLY: continue
    if (outdir / f"{corp}_{qs}.csv").exists() and not ONLY: continue
    rows = []
    D = np.load(cache / f"docs_{corp}.npy"); Q = np.load(cache / f"{qs}.npy")
    texts = q[COL[qs]].tolist(); t_b = t_c = t_d = 0.0
    for i, (qtext, gold) in enumerate(zip(texts, q.doc_id)):
        t = time.perf_counter(); s_bw = bm[(corp, "word")].scores(qtext); r_bw = topk_positive(s_bw); t_b += time.perf_counter() - t
        t = time.perf_counter(); s_bc = bm[(corp, "char")].scores(qtext); r_bc = topk_positive(s_bc); t_c += time.perf_counter() - t
        t = time.perf_counter(); r_d = topk(D @ Q[i]); t_d += time.perf_counter() - t
        # v1 ("naive") fed the full top-100 BM25 lists, including zero-score documents in index order
        n_bw, n_bc = topk(s_bw), topk(s_bc)
        ranked = {"BM25": r_bw, "BM25-char3": r_bc, "Dense-e5": r_d,
                  "Hybrid-RRF": rrf([r_bw, r_d]), "Hybrid-RRF3": rrf([r_bw, r_bc, r_d]),
                  "Hybrid-RRF-naive": rrf([n_bw, r_d]), "Hybrid-RRF3-naive": rrf([n_bw, n_bc, r_d])}
        nz_w, nz_c = int((s_bw > 0).sum()), int((s_bc > 0).sum())
        for name, idx in ranked.items():
            m = per_query([doc_ids[j] for j in idx[:10]], gold)
            rows.append({"corpus": corp, "query_set": qs, "retriever": name, "qid": q.qid[i], **m,
                         "bm25_word_matches": nz_w, "bm25_char_matches": nz_c})
    n = len(texts)
    lat.append({"corpus": corp, "query_set": qs, "bm25_ms": 1000 * t_b / n, "bm25char_ms": 1000 * t_c / n,
                "dense_search_ms": 1000 * t_d / n})
    pd.DataFrame(rows).to_csv(outdir / f"{corp}_{qs}.csv", index=False)
    pd.DataFrame(lat[-1:]).to_csv(outdir / f"lat_{corp}_{qs}.csv", index=False)
    print(corp, qs, "done", flush=True)
if ONLY: sys.exit(0)
pq = pd.concat([pd.read_csv(f) for f in sorted(outdir.glob("[te]*_*.csv"))]); pq.to_csv("results/per_query.csv", index=False)
lat = pd.concat([pd.read_csv(f) for f in sorted(outdir.glob("lat_*.csv"))]).to_dict("records")
agg = []
for (c, s, r), g in pq.groupby(["corpus", "query_set", "retriever"], sort=False):
    d = {"corpus": c, "query_set": s, "retriever": r, "n": len(g)}
    for m in ("R@1", "R@5", "R@10", "MRR@10", "nDCG@10"):
        d[m] = g[m].mean()  # stored unrounded; tables round at display time
    lo, hi = bootstrap_ci(g["MRR@10"].values); d["MRR@10_CI95"] = f"[{lo:.3f}, {hi:.3f}]"
    agg.append(d)
pd.DataFrame(agg).to_csv("results/main_results.csv", index=False, float_format="%.6f")
pd.DataFrame(lat).round(3).to_csv("results/latency_search.csv", index=False)
print(pd.DataFrame(agg).round(3).to_string())
