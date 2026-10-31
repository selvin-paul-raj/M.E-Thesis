# Tanglish RAG retrieval study (M.E. CSE project, Modules 1–2)

**Code-Mixed Retrieval-Augmented Generation: An Empirical Study of Chunking, Embedding and Query Normalisation for Tamil–English (Tanglish) Queries**
Selvin PaulRaj K · M.E. CSE 2025–2027 · Kings Engineering College, Chennai

This code evaluates RAG retrieval for the same 2,154 information needs written in four forms (English, Tamil script, romanised Tamil, code-mixed Tanglish), with five retrievers and two query-normalisation modes. Everything runs on a CPU (tested on 2 cores, 7 GB RAM, no GPU).

## Layout

```
src/tanglish_rag/
  data.py        load nlpctx/tamil-english-retrieval, seeded 500-doc subset
  normalise.py   token language ID + romanised Tamil -> Tamil script (ITRANS or Tanglish rules)
  retrievers.py  BM25 (word), BM25 (char 3-gram), dense multilingual-e5-small, RRF fusion
  metrics.py     Recall@k, MRR@10, nDCG@10, bootstrap CI, paired bootstrap test
scripts/
  01_prepare_data.py         download data, sample 500 docs (seed 42), build 8 query sets
  02_encode_dense.py         encode corpora + query sets (cached to results/cache/)
  03_run_eval.py             60 runs -> results/per_query.csv, main_results.csv
  04a_significance.py        paired tests: query-level and document-cluster bootstrap
  04_significance_latency.py single-query latency
  05_examples_analysis.py    query audit + example outputs
  06_make_charts.py          report charts;  07_architecture.py  architecture diagram
  08_slide_charts.py         square chart versions for the slides
data/       corpus.jsonl (500 docs), queries.jsonl (2,154 queries, 8 forms)
results/    CSVs, examples.json, charts/
```

## Run

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python scripts/01_prepare_data.py 500
python scripts/02_encode_dense.py intfloat/multilingual-e5-small     # ~5 min on 2 cores
python scripts/03_run_eval.py                                        # can be split: ta:rom ta:cm ...
python scripts/04a_significance.py
python scripts/04_significance_latency.py
python scripts/05_examples_analysis.py
python scripts/06_make_charts.py && python scripts/07_architecture.py
```

Run from this folder. `03_run_eval.py` accepts run filters (for example `ta:rom en:cm`) so a long run can be split; running it with no arguments aggregates whatever is in `results/per_query/`.

## Main results (Tamil corpus, MRR@10, n = 2,154 per form)

| Query form | BM25 | BM25 char-3 | Dense mE5-small | Hybrid RRF | Hybrid RRF3 |
|---|---|---|---|---|---|
| Tamil script | 0.811 | **0.923** | 0.903 | 0.895 | 0.911 |
| English | 0.067 | 0.062 | **0.788** | 0.710 | 0.305 |
| Code-mixed | 0.069 | 0.063 | **0.687** | 0.637 | 0.278 |
| Romanised | 0.056 | 0.058 | 0.143 | **0.178** | 0.113 |
| Romanised + ITRANS | 0.210 | **0.547** | 0.328 | 0.386 | 0.506 |
| Romanised + Tanglish rules | 0.333 | **0.684** | 0.535 | 0.537 | 0.627 |
| Code-mixed + Tanglish rules | 0.111 | 0.238 | **0.692** | 0.568 | 0.420 |

**Fusion fix (31 Oct 2026).** rank-bm25 scores non-matching documents exactly 0. The first version passed the whole top-100 BM25 list to RRF, so for zero-overlap queries documents 0–99 (index order) were fused as if relevant. `topk_positive` now drops zero-score documents from every BM25 list. The old behaviour is kept as `Hybrid-RRF-naive` / `Hybrid-RRF3-naive` for comparison (e.g. English queries: naive RRF 0.187, fixed 0.710). The v1 results are in `results/v1_before_rrf_fix/`. `main_results.csv` now stores unrounded values; round only for display.

Full tables with Recall@1/5/10, nDCG@10 and 95% CIs: `results/main_results.csv`.

## Relation to ChunkLab

The retriever and metric design follows github.com/selvin-paul-raj/chunklab (BM25, dense, hybrid RRF with k = 60; P/R/MRR/nDCG definitions in `modules/evaluation`). It is reimplemented here as plain functions so the experiment runs without the Streamlit app. ChunkLab's chunkers are used in Module 3, where documents are long enough to need chunking.

## Data licence

nlpctx/tamil-english-retrieval is Apache-2.0 (Tamil text from the Mozhi corpus / IndicCorpV2; English by IndicTrans2). All queries in it are LLM-generated.
