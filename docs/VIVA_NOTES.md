# Viva notes: Tanglish RAG, Modules 1–2

## The 1-minute explanation (say this out loud)

"Chatbots like ChatGPT can answer questions about your own documents using a method called RAG. First a *search step* finds the right document, then the AI writes an answer from it. If the search step picks the wrong document, the answer is wrong.

Most of us in Tamil Nadu don't type in Tamil script or perfect English. We type Tanglish, like 'scholarship ku last date enna?'. Search engines for romanised Hindi were studied at the FIRE workshops ten years ago, but nobody has tested the parts of a modern RAG search step (dense, keyword, fusion) on Tamil–English queries.

So I took 500 Tamil news documents and 2,154 questions. Each question exists in four forms: English, Tamil script, Tamil typed in English letters (romanised), and mixed Tanglish. I tested five search methods on all of them.

Result: Tamil-script questions get the right document as the top result about 90% of the time (MRR 0.92). Romanised Tamil questions almost completely fail (MRR 0.14). I wrote simple rules that convert romanised Tamil back into Tamil script, like 'zh' to ழ and 'th' to த. That brings it up to 0.68, and it costs less than a millisecond. I also found that the popular 'hybrid' search setting makes things worse across scripts. I first measured that loss as huge, then found a bug in my fusion code, fixed it, and the loss is smaller but still real: 0.79 down to 0.71.

Next I will collect 500 real Tanglish questions from students, test Tamil-aware document splitting, and then test the full answer quality."

## Key numbers to remember

| What | Number |
|---|---|
| Documents / queries per form | 500 / 2,154 |
| Tamil-script queries, best MRR@10 | 0.923 (BM25 char 3-gram) |
| English queries on Tamil docs, dense | 0.788 |
| Code-mixed queries, dense | 0.687 |
| Romanised queries, dense / best raw | 0.143 (Recall@10 0.29) / 0.178 (BM25 + dense fusion) |
| Romanised + my rules + char BM25 | 0.684 (Recall@10 0.81) |
| Romanised + ITRANS + char BM25 | 0.547 |
| Hybrid RRF on English queries (corrected) | 0.788 → 0.710 (RRF3: 0.305) |
| Same, old buggy 'naive' run | 0.788 → 0.187 (zero-score BM25 docs were fused) |
| Queries per source document | ~4.3 (cluster bootstrap: conclusions unchanged) |
| Normalisation cost | ~0.3 ms per query |
| Code-mixed queries with no Tamil word | 22% |

## Simple meanings of the terms

- **RAG:** retrieve documents, then generate an answer from them.
- **BM25:** classic keyword search. Counts shared words, gives rare words more weight.
- **Character 3-gram BM25:** the same, but matches 3-letter pieces of words, so small spelling differences still match.
- **Dense retrieval / embeddings:** a neural model turns text into a list of numbers (a vector); similar meanings get similar vectors. I used multilingual-e5-small (118M parameters, runs on CPU).
- **RRF (Reciprocal Rank Fusion):** merges two ranked lists by adding 1/(60 + rank) from each.
- **Recall@10:** in how many questions the right document appears in the top 10.
- **MRR@10:** average of 1/rank of the right document (rank 1 = 1.0, rank 2 = 0.5, missing = 0).
- **nDCG@10:** like MRR but with a gentler penalty, 1/log2(rank + 1).
- **Transliteration:** changing the script, not the language (romanised "enna" → என்ன).

## 10 likely viva questions with short answers

**1. What exactly is new in your work?**
No prior study evaluates RAG retrieval components (dense, lexical, fusion) for Tamil–English code-mixed and romanised queries. Transliteration-based mixed-script IR itself has a history at FIRE: the 2013–2016 Transliterated Search / MSIR tracks and Gupta et al. (SIGIR 2014) did retrieval for romanised Hindi (and Bengali), and Tamil appeared only in word-level language labelling. One FIRE 2015 team even used transliteration + character n-grams, so I don't claim that idea. What I add: the first component-level RAG baselines on Tamil (dense mE5, word and char BM25, RRF), on the nlpctx dataset, with significance tests; the finding that equal-weight fusion hurts across scripts; and an audit showing the dataset's code-mixed queries are mostly English.

**2. Why did romanised Tamil fail so badly, even for the multilingual model?**
The documents are in Tamil script, so BM25 has no shared words. The embedding model was trained mostly on native-script text, so it splits "mothalukku" into English-like pieces with no link to மோதலுக்கு. Code-mixed queries did better only because most of their words are English, and the model handles English well.

**3. Why did you write your own transliteration rules instead of using an existing tool?**
I did use one: ITRANS from indic-transliteration, as a baseline. ITRANS is a formal scheme for Sanskrit-style romanisation, so it gets Tanglish habits wrong (e.g. "enna" becomes ஏந்ந). My rules encode how people actually type (zh → ழ, initial n → ந, nn → ன்ன, tr → ற்ற); the full rule set is Table 4.1. They beat ITRANS on every retriever for romanised queries (0.684 vs 0.547 MRR with char BM25, p < 0.001). The obvious stronger baseline is IndicXlit, the neural model from AI4Bharat's Aksharantar paper (Madhani et al., EMNLP Findings 2023); it is the first Module 3 baseline, along with an LLM query rewriter. Rules have one advantage: 0.3 ms per query, no model.

**4. Did you tune the rules on the test data? Isn't that cheating?**
No. The rules came from Tamil spelling knowledge and were written before running the evaluation. But they were written by one person, so Module 3 will test them on a new, human-written query set.

**5. Why does hybrid RRF hurt? Everyone recommends it.**
RRF gives every list equal weight. When the query is English and the documents are Tamil, word BM25 matches nothing for 72% of queries and only stray words like "of" or "news" for the rest, yet RRF still trusts it, so it pushes the correct dense result down: MRR 0.788 → 0.710 (p < 0.001, also with the cluster bootstrap). With the char 3-gram list added it falls to 0.305.
*Be upfront about the bug:* my first run fed BM25's zero-score documents into RRF. rank-bm25 gives non-matching documents a score of exactly 0, and sorting those just lists documents 0–99 in index order, which RRF rewarded. That made the loss look like 0.788 → 0.187. I found it, filtered zero-score documents, reran every hybrid run, and kept the old numbers as "naive" in Table 5.6. The conclusion survives at its corrected size. Fusion does help when BM25 has real signal (raw romanised: 0.143 → 0.178). So: route or weight by script, and never fuse zero-score results.

**6. Your queries are LLM-generated. How do you know results hold for real users?**
I don't yet, and the report says so. My audit found that 22% of the "code-mixed" queries contain no Tamil word at all and 13% are identical to the English query. That's why Module 3 collects about 500 real Tanglish questions from students.

**7. Why only 500 documents and a small model?**
To run everything on a 2-core CPU, reproducibly, like a student laptop. 2,154 queries per form is enough for tight confidence intervals (about ±0.01 to ±0.02 MRR). Larger models (BGE-M3, LaBSE) and a larger corpus come in Module 3.

**8. How do you know the improvements are not luck?**
Every query exists in all forms, so comparisons are paired on the same 2,154 questions. I used a paired bootstrap test (2,000 resamples) and bootstrap 95% confidence intervals. Queries are clustered (about 4.3 per document), so I also ran a cluster bootstrap that resamples whole documents: intervals get about 1.6× wider, and every conclusion holds. The rules' gains have p < 0.001 in both. The tiny code-mixed dense change (0.687 → 0.692) has p = 0.45 (cluster 0.57), so I report it as no effect.

**9. Where is chunking, since it is in your title?**
These news documents are short (median 326 characters), so each one is already a single chunk; chunking would change nothing here. Module 3 uses longer documents (circulars, notices) and compares a Tamil-aware chunker with ChunkLab's chunkers.

**10. How does this connect to your ChunkLab project?**
ChunkLab is my RAG playground with chunkers, dense/sparse embeddings, BM25/dense/hybrid RRF retrievers, re-rankers and IR metrics. I reused its retriever design and metric definitions (RRF k = 60, Recall/MRR/nDCG) as small standalone functions, and Module 3 will plug in its chunkers.

## If you are asked "what would you do differently?"

Write a unit test for the fusion input from day one (that would have caught the zero-score bug), gate fusion by script (dense alone for English and code-mixed, rules + char BM25 for romanised), keep Indian named entities out of the transliterator (it turned 'Talaq' and 'Rajya' into Tamil script but kept 'Sabha' in English), and collect real Tanglish queries before tuning anything.

## Extra questions you may get

**Why does char 3-gram BM25 beat word BM25 even on Tamil script (0.923 vs 0.811)?** Tamil is agglutinative: மோதல், மோதலுக்கு, மோதலில் are one word with different suffixes. I used no stemmer, so word BM25 treats them as different words; char 3-grams share the stem's pieces, which works like a rough stemmer.

**What are the limitations?** LLM-generated queries; one relevant document per query; a small dense model; rules by one author; the language ID splits Indian names across scripts; queries cluster within documents (handled by the cluster bootstrap).
