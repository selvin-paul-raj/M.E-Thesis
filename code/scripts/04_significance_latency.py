"""End-to-end single-query latency (CPU, 2 threads). Significance tests: see 04a_significance.py."""
import sys, pathlib, time
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
# Significance tests moved to 04a_significance.py (adds the document-cluster bootstrap).
# single-query latency: normalise + encode + search, 200 random romanised queries, one at a time
from tanglish_rag.retrievers import BM25, Dense, word_tokens, char_ngrams, topk, topk_positive, rrf
from tanglish_rag.normalise import normalise
torch.set_num_threads(2)
corpus = pd.read_json("data/corpus.jsonl", lines=True); q = pd.read_json("data/queries.jsonl", lines=True)
texts = corpus.text_ta.tolist(); D = np.load("results/cache/multilingual-e5-small/docs_ta.npy")
bw, bc, enc = BM25(texts, word_tokens), BM25(texts, char_ngrams), Dense()
sample = q.query_ta_romanized.sample(200, random_state=1).tolist()
enc.encode_queries(sample[:8])  # warm-up
T = {k: [] for k in ("normalise", "bm25_word", "bm25_char3", "dense_encode", "dense_search", "rrf")}
for s in sample:
    t = time.perf_counter(); n = normalise(s, "rules"); T["normalise"].append(time.perf_counter() - t)
    t = time.perf_counter(); r1 = topk_positive(bw.scores(n)); T["bm25_word"].append(time.perf_counter() - t)
    t = time.perf_counter(); r2 = topk_positive(bc.scores(n)); T["bm25_char3"].append(time.perf_counter() - t)
    t = time.perf_counter(); e = enc.encode_queries([n], bs=1)[0]; T["dense_encode"].append(time.perf_counter() - t)
    t = time.perf_counter(); r3 = topk(D @ e); T["dense_search"].append(time.perf_counter() - t)
    t = time.perf_counter(); rrf([r1, r2, r3]); T["rrf"].append(time.perf_counter() - t)
lat = pd.DataFrame([{"stage": k, "median_ms": 1000 * np.median(v), "p95_ms": 1000 * np.quantile(v, .95)} for k, v in T.items()]).round(3)
lat.to_csv("results/latency_single_query.csv", index=False); print(lat.to_string())
