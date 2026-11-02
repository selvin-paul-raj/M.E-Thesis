# Viva notes: Tanglish RAG, Modules 1–2 (review 2 November 2026)

Selvin PaulRaj K · M.E. CSE · Kings Engineering College, Chennai

## The 1-minute pitch (say this out loud)

"In Tamil Nadu people ask questions in Tanglish, like *scholarship ku last date enna?* The documents that answer them are bilingual and not translations of each other: a Government Order may exist only in Tamil, a college circular only in English. RAG chatbots first *search* for the right document and then let an LLM answer from it, but they are built and tested in English.

I measured what each part of the RAG search step does when the same question is typed in four forms: English, Tamil script, romanised Tamil and code-mixed Tanglish. On 500 Tamil news documents and 2,154 questions, Tamil-script questions find the right document almost every time (MRR@10 0.92). Romanised Tamil almost completely fails (0.14). A small set of Tanglish rules that converts romanised Tamil back to Tamil script, plus character 3-gram BM25, brings it to 0.68 for 0.3 ms per query. I also showed that the popular hybrid BM25 + dense setting makes cross-script search worse (0.79 → 0.71).

Next, Module 3 builds the first human-written Tanglish benchmark over real bilingual Tamil Nadu documents and tests whether a mixed Tamil + English index is biased against Tamil documents."

## Key numbers

| What | Number |
|---|---|
| Documents / queries per form / query sets | 500 / 2,154 / 8 |
| Tamil-script queries, best (char 3-gram BM25) | MRR@10 0.923 |
| Romanised, dense / best raw (RRF) | 0.143 (Recall@10 0.294) / 0.178 |
| Romanised + Tanglish rules + char 3-gram BM25 | 0.684, Recall@10 0.812 (p < 0.001, also cluster bootstrap) |
| Rules vs ITRANS (char 3-gram) | 0.684 vs 0.547 |
| Best Recall@10 for romanised (rules + RRF3) | 0.842 |
| Code-mixed dense, raw → rules | 0.687 → 0.692 (p = 0.45, not significant) |
| English queries: dense → RRF (corrected) | 0.788 → 0.710 (naive bug version 0.187) |
| English corpus, romanised best (RRF3) | 0.557 |
| Code-mixed queries with no Tamil word / identical to English | 22.0% / 13.3% |
| Latency: normaliser / char BM25 / dense encode / full pipeline | 0.34 / 4.9 / 32 / 38 ms |

## Likely questions with short answers

**1. In one sentence, what is your project?**
I measure what each part of a RAG search pipeline does when Tamil questions are typed in English letters over a bilingual Tamil + English document base, and I build cheap fixes and a human benchmark for it.

**2. Why not just use ChatGPT?**
ChatGPT reads Tanglish well in a chat, but a help desk must answer from thousands of G.O.s and circulars, far more than fit in a prompt, so the LLM depends on a retrieval step to pick a few documents. That step collapses on romanised Tamil (dense MRR@10 0.143), so the LLM never sees the right evidence and either guesses or abstains. Translate-to-English pipelines never search Tamil-only documents. Sending every citizen query to a paid API also raises cost and privacy issues. I use LLMs where they fit: an LLM query rewriter is a Module 3 baseline and an LLM is the Module 4 generator.

**3. Isn't Tanglish too niche?**
Tamil has more than 80 million speakers and most type in Latin letters on phones. Tanglish is the M.E. entry point, not the end point: the same problem (an Indian language typed in Roman script, mixed with English, over native-script and English documents) applies to Hinglish, Manglish and Telugu–English. Hira et al. (EMNLP 2026) already show the bias for romanised Hindi, Bengali, Marathi and Urdu. The PhD extends the benchmark and methods to other Indic languages, which fits IndiaAI and Bhashini.

**4. What exactly is new?**
The first component-level study of RAG retrieval (dense, lexical, fusion) and query normalisation for romanised and code-mixed Tamil–English queries, measured on the same information needs in four forms; the cross-script fusion finding; the dataset audit; and (Module 3) the first human Tanglish retrieval benchmark over non-parallel bilingual Tamil Nadu documents.

**5. What do you NOT claim?**
Mixed-script IR with transliteration, rule normalisation and character n-grams was done at FIRE 2013–2016 for Hindi and Bengali; I say that openly. I don't claim to be first to show language bias in mixed indices (Hira et al.; Amiraz et al.), the first Tanglish embedder (Morgan-Tanglish-v7) or the first Tamil–English CLIR (Thenmozhi and Aravindan 2018).

**6. Closest papers and how you differ**

- **Hira, Mire, Sap (EMNLP 2026):** English anchoring for romanised Hindi/Bengali/Marathi/Urdu code-switched RAG. Their documents are machine-translated *parallel* copies (every answer exists in every language), no Tamil, dense retrievers only. Mine: Tamil, native *non-parallel* documents where the answer is in one language, lexical remedies.
- **Amiraz et al. (ArabicNLP 2025):** cross-lingual cost in non-parallel Arabic–English RAG and a balanced per-language fix. Native script only, no Tamil. Their balanced retrieval becomes my Module 3 baseline.
- **Chari, Ounis, MacAvaney (SIGIR 2025):** script gap for Latinised queries in dense IR, closed by mixed fine-tuning. No Indic language.
- **FIRE MSIR (2013–16), Gupta et al. (SIGIR 2014):** Hindi/Bengali mixed-script retrieval; Tamil only in word labelling; pre-dense, no RAG.
- **SchemeAI (IJARSCT 2026):** the existing Tamil Nadu scheme chatbot: English MiniLM + FAISS over an English CSV, output translated to Tamil, no metrics. My "existing system" and a Module 3 baseline.

**7. Why does romanised Tamil fail so badly?**
BM25 shares no characters with Tamil-script documents, and the embedder was trained mostly on native-script text, so it splits romanised words into English-like pieces. Verma et al. (ACL 2026) show romanised text aligns with neither the native script nor English.

**8. Why your own rules instead of a tool?**
I did use a tool, ITRANS, as the baseline; it is a Sanskrit-style scheme (e→ஏ, n→ந everywhere). My rules encode how people type (zh→ழ, nn→ன்ன, tr→ற்ற) and beat ITRANS on every retriever (0.684 vs 0.547, p < 0.001). IndicXlit and an LLM rewriter are the Module 3 baselines. The rules were written before the evaluation and never tuned on test data.

**9. Why does char 3-gram BM25 beat word BM25 even on Tamil script (0.923 vs 0.811)?**
Tamil is agglutinative (மோதல், மோதலுக்கு, மோதலில்). Without a stemmer word BM25 treats these as different words; 3-grams share the stem and also tolerate transliteration spelling errors.

**10. Everyone recommends hybrid search. Why does it hurt?**
RRF gives every list equal weight. For English queries on Tamil documents, word BM25 matched nothing for 72% of queries and only stray words (of, news) for the rest, yet RRF trusted it: 0.788 → 0.710 (p < 0.001, also cluster). This matches the "fusion tax" (Chauhan and Agarwal 2026). Fusion helps when BM25 has signal (raw romanised: 0.143 → 0.178).

**11. Tell us about the bug.**
My first run fed zero-score BM25 documents into RRF; sorting zeros lists documents in index order, which RRF rewarded, so the loss looked like 0.788 → 0.187. I found it, filtered zero-score documents, re-ran every hybrid and kept the old numbers labelled "naive". The corrected loss is smaller but still significant.

**12. Your queries are LLM-generated. Why believe the results?**
That is the main limitation and I measured it: 22% of "code-mixed" queries have no Tamil word, so code-mixed results mostly measure English-to-Tamil retrieval. Romanised queries are genuinely Tamil (4.3 Tamil tokens per query), so those findings are stronger. Module 3 replaces them with about 500 human questions.

**13. How do you know the improvements are not luck?**
Every query exists in all four forms, so comparisons are paired: paired bootstrap (2,000 resamples) plus a document-cluster bootstrap because about 4.3 queries come from each document. Intervals widen about 1.6× and every conclusion holds. Non-results are reported (code-mixed dense, p = 0.45).

**14. Where is the bilingual part in Module 2?**
Module 2 has both halves (Tamil documents and their English translations) evaluated separately; romanised Tamil is the weakest form on both (0.684 best on Tamil after rules, 0.557 on English). Because the two halves are parallel, language preference can't be measured yet. Module 3 uses non-parallel Tamil G.O.s and English circulars, tags each question with its gold-document language, and compares a single mixed index with per-language indices.

**15. Why only 500 documents and a small model? Where is chunking?**
To keep every run reproducible on a 2-core CPU; 2,154 paired queries still give ±0.01–0.02 MRR intervals. The news documents are short (median 326 characters), so chunking cannot matter there; Module 3 uses long notices with a Tamil-aware chunker, plus BGE-M3, LaBSE and Morgan-Tanglish-v7.

**16. What is the script-gated router?**
A small decision step that reads the mix of English, romanised and Tamil-script tokens and sends the query to the retriever that works for that form: dense for English-heavy, rules + char BM25 for romanised, fusion only when every list carries signal. The review re-run already supports it: in the "Muthalaq thadai masoda" example, dense fails after normalisation but char 3-gram BM25 ranks the gold document first.

## If asked "what would you do differently?"
Unit-test fusion inputs from day one; gate fusion by script; keep named entities out of the transliterator (it produced "Triple டலக் bill ரஜ்ய Sabha"); collect real Tanglish queries before tuning anything.
