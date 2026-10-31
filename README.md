# Code-Mixed Retrieval-Augmented Generation for Tamil–English (Tanglish) Queries

**M.E. CSE Thesis — Selvin PaulRaj K, Kings Engineering College (2025–2027)**

*An empirical study of retrieval, query normalisation and rank fusion for Tamil–English code-mixed and romanised queries in RAG.*

People type Tamil in English letters and mix it with English (for example, *"scholarship ku last date enna?"*). RAG systems are built and tested on English. This project measures how retrieval breaks on Tanglish queries and how a lightweight normaliser fixes it.

## Status: Modules 1 & 2 complete (review: 2 Nov 2026)

| Folder | Contents |
|---|---|
| `report/` | Module 1–2 report (PDF, DOCX) and `FULL_REPORT_FOR_REVIEW.md` (plain text for review) |
| `slides/` | Review slides (PPTX, PDF) |
| `code/` | Pipeline: data prep, BM25 / char-3gram BM25 / multilingual-e5 / RRF, normaliser, metrics, significance tests, results |
| `docs/` | Viva notes, future directions |
| `archive/ava/` | Earlier AVA (Agree, Verify, or Abstain) topic material, kept for reference |

## Key results (MRR@10, 500 Tamil documents, 2,154 queries per form)
- Raw romanised Tanglish queries collapse: best MRR@10 is **0.178**
- With the Tanglish→Tamil rule normaliser and character 3-gram BM25: **0.684** (Recall@10 0.812), at about 0.3 ms per query
- Naive hybrid fusion (RRF) hurts across scripts: English drops from 0.788 to 0.710 (after fixing a zero-score tie bug that had shown 0.187)
- 22% of the dataset's "code-mixed" queries contain no Tamil word, so real human Tanglish queries are needed (Module 3)

Dataset: [`nlpctx/tamil-english-retrieval`](https://huggingface.co/datasets/nlpctx/tamil-english-retrieval) (Apache-2.0). Built on ideas from [ChunkLab](https://github.com/selvin-paul-raj/chunklab).

## Run
```bash
cd code && pip install -r requirements.txt
# see code/README.md for the script order
```

See `docs/FUTURE_DIRECTIONS.md` for Modules 3–5.
