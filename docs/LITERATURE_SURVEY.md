# Literature Research: Code-Mixed (Tanglish) Retrieval-Augmented Generation

**Thesis:** *Code-Mixed Retrieval-Augmented Generation: An Empirical Study of Chunking, Embedding and Query Normalisation for Tamil–English (Tanglish) Queries*, Selvin PaulRaj K, M.E. CSE, Kings Engineering College.
**Survey date:** 31 October 2026. **Mode:** lit-review (annotated bibliography plus synthesis). **Citation style:** IEEE.
**New verified works:** 54, numbered [24]–[77], continuing the report's [1]–[23]. BibTeX is in `references_new.bib`; the IEEE list is in `references_new_IEEE.md`.

---

## 0. Scope and method

**Research question.** What is known about each component of a RAG retrieval pipeline (normalisation, embedding, lexical and dense retrieval, fusion, chunking, generation-side evaluation) when queries are romanised or code-mixed Tamil–English, and where are the gaps that Modules 3–5 can fill?

**Inclusion.** Peer-reviewed papers, shared-task overviews and working notes, and arXiv preprints from 2013–2026, with 2023–2026 preferred. Also datasets and model cards when they are the only source for a resource the thesis uses (marked *grey*). The topics are mixed-script or code-mixed IR and QA, Indic and Tamil resources, multilingual or romanisation-robust embeddings, hybrid fusion, query rewriting, chunking, and RAG or LLM-judge evaluation.
**Exclusion.** Classification-only code-mixing work (sentiment, hate speech), unless it is a benchmark or resource. Mass-produced Zenodo "studies" with no venue. Anything not opened.

**Sources and tools.**
- `paper-search` CLI with OpenAlex, Crossref and Semantic Scholar: 38 queries. Semantic Scholar returned HTTP 429 on almost every call, so OpenAlex and Crossref carried the CLI work.
- Metadata and abstracts from the ACL Anthology (abstract and BibTeX endpoints), the OpenAlex works API, and the arXiv export API (it rate-limited, so arXiv DOIs were resolved through OpenAlex).
- Ten `web_search` queries for gap validation and venue mining.
- Direct page or PDF checks: Springer chapter pages, Zenodo records, CEUR PDFs, the COLM PDF, the Hugging Face cards for MIRACL, IndicMSMARCO and Sarvam-1, and the arXiv HTML or PDF for Indi-RomCoM and Lost in Transliteration.

**Phrasings, at least 3 per theme.**
- (1) "mixed script information retrieval transliteration", "transliterated search FIRE overview", "transliterated search query back-transliteration", "Hindi-English code-mixed information retrieval", "romanized Tamil transliteration", "romanized Tamil information retrieval dense retriever …"
- (2) "code-mixed question answering retrieval", "code-mixed RAG", "code-mixed retrieval augmented generation", "Hinglish retrieval augmented generation", "code-switched dense retrieval", "code-switching retrieval benchmark", "large language models code-switching evaluation", "Tanglish retrieval-augmented generation romanized Tamil queries"
- (3) "Tamil English code-mixed", "Tanglish", "Tamil large language model", "Tamil retrieval question answering dataset", "IndicIRSuite", "Indic RAG benchmark", "Dakshina romanized South Asian", "IndicTrans2", "multilingual sentence embeddings Indian languages"
- (4) "romanization multilingual language models", "transliteration robustness multilingual embeddings", "romanized Indic language identification"
- (5) "hybrid retrieval fusion functions reciprocal rank", "query rewriting retrieval-augmented large language models", "LLM query rewriting transliteration code-mixed Hinglish", "chunking strategies retrieval augmented generation", "semantic chunking retrieval granularity", "Tamil document chunking strategies RAG"
- (6) "RAG evaluation faithfulness automated", "RAGAS automated evaluation", "LLM evaluators multilingual Indic", "LLM evaluators multilingual evaluation"

**Citation chaining (forward, `get_citing_papers`).**
- Gupta et al. [21]: 99 citers, first 10 read. This surfaced [77].
- Chari et al. [28]: all 5 citers read. None covers Tamil.
- Aksharantar [22]: 26 citers, first 10 read. This surfaced [32].
- Chandu et al. [13]: 38 citers, first 10 read. This surfaced [37].
Backward chaining came from the reference lists of [42], [43] and [30] (Springer and CEUR pages).

**Venue mining.**
- ACL Anthology: ACL, EMNLP, NAACL, EACL, Findings, TACL, LREC, CALCS, W-NUT, KnowLLM.
- DravidianLangTech 2025 and 2026: the volume listings and the 2026 front matter were read. All shared tasks are classification, speech or meme tasks; none is retrieval or QA.
- FIRE: 2013 and 2014 transliterated search, MSIR 2015–16, CMIR 2024–25 (CEUR Vol-4054 and Vol-4173 tables of contents read).
- SIGIR, ECIR and CIKM: SIGIR 2014, 2016, 2021 and 2025 items, the SIGIR 2026 programme page, and the ECIR 2026 proceedings page.
- Interspeech 2021 and 2025 (code-switched ASR, Tamil–English).
- COLM 2026.

**PRISMA-style counts (approximate).** About 600 records came from the CLI and web searches. About 140 titles were screened as plausibly relevant, and about 100 were opened. Of those, 54 are included as new verified works, 34 were verified but left out of the chapter (§8.2), and 12 groups of items are listed as unverified or excluded (§8.3).

**Review-form note.** The ARS skill offers the author a choice of review form when lit-review mode is selected. This survey was commissioned as a lit-review, so it continues in that mode. A systematic review (PRISMA) remains the author's option.

**AI disclosure.** This survey was compiled with AI-assisted search, retrieval and drafting tools. Every bibliographic entry was checked against an opened abstract page, and the author should spot-check the key numbers before submission.

---

## 1. Research landscape

Code-mixed and transliterated retrieval has a long history at FIRE, starting with transliterated search in 2013 [24], [20], [19] and running through Bengali–English CMIR in 2024–25 [9], [10], [29], [30]. Almost all of it is Hindi or Bengali, and it predates RAG. The 2023–2026 literature moves in three directions that this thesis can combine:

- **Script robustness of neural retrievers.** Dense retrievers lose a lot of effectiveness on transliterated queries [28], and code-switched queries degrade every retriever family [11]. Multilingual models place romanised text in representations that align with neither the native script nor English [61].
- **Indic RAG resources.** There are now native-script Tamil retrieval benchmarks [52], [53] and QA benchmarks [54], plus Tamil LLMs [49], [50], [51]. None of them has romanised or code-mixed Tamil queries with relevance judgements.
- **Hinglish code-mixed RAG.** Hinglish RAG studies appear in 2026 [42], [43], [44] and evaluate on small custom sets.

Fusion [63], [64], query rewriting [65], [66], chunking [67], [68] and RAG evaluation [69]–[76] are well studied in English and in native-script multilingual settings. They have not been studied under Tamil romanisation.

---

## 2. Taxonomy paper table (new works [24]–[77], grouped by approach)

"Code?" says whether the abstract or record points to released code or data: **Y** = stated, **Data** = dataset released, **n/s** = not stated on the page opened. "Relevance" is to this thesis: H = high, M = medium, L = low.

### A. Mixed-script and transliterated IR, back-transliteration, romanised LID

| Paper | Year | Venue | Approach | Key result (verified from abstract or page) | Code? | Relevance |
|---|---|---|---|---|---|---|
| Saha Roy et al. [24] | 2013 | FIRE '13 (ACM) | First FIRE transliterated search track: word language labelling plus back-transliteration (Hindi, Bangla, Gujarati); retrieval of Roman-script Bollywood lyrics queries | 25 runs from 5 teams; "considerable scope for improvement" in transliteration accuracy | Data | M |
| Ganguly et al. [25] | 2014 | FIRE '14 (ACM) | Rule-based normalisation of transliterated character sequences at indexing, plus prefix-matched fuzzy query terms | About 56% improvement over a query-likelihood LM baseline (Hindi lyrics) | n/s | **H**: precedent for rule normalisation |
| Chakma and Das [26] | 2016 | Computación y Sistemas | CMIR corpus of Hindi–English tweets (native and Roman) | Formalises code-mixed IR on informal text; reports limits of existing IR | Data | M |
| Riyadh and Kondrak [27] | 2019 | VarDial workshop (ACL) | Joint language ID, back-transliteration and sequence prediction for deromanisation | State of the art on Bengali and Hindi code-mixed deromanisation | n/s | **H**: neural alternative to the Tanglish rules |
| Chari et al. [28] | 2025 | SIGIR '25 | Measures the "script gap" for transliterated queries; transliterate-train fine-tuning | BGE-M3 and other multilingual dense IR "rapidly deteriorate" on Latinised queries; fine-tuning on an even native and Latin mix nearly closes the gap. Languages include Chinese, Russian, Arabic, Greek, Persian; no Indic language | Y (GitHub) | **H**: closest neural-IR precedent |
| Deroy and Maity [29] | 2024 | FIRE 2024 WN (CEUR 4054) | GPT prompting plus mathematical models for Roman Bengali–English CMIR | Participant system for CMIR 2024 [9] | n/s | M |
| Mishra et al. [30] | 2025 | FIRE 2025 WN (CEUR 4173) | BM25 plus SBERT re-ranking for Benglish CMIR | MAP 0.054 (8th place); 83% over its BM25 baseline | n/s | M: hybrid lexical + dense in code-mixed IR |
| Roark et al. (Dakshina) [31] | 2020 | LREC 2020 | Native and Latin-script parallel data, romanisation lexicons, 12 South Asian languages (Tamil included) | Baselines for word and sentence transliteration and LM | Data | **H**: evaluation data for the normaliser |
| Kirov et al. [32] | 2024 | Computational Linguistics 50 | Context-aware sentence-level transliteration, Latin to native | Large gains over prior full-sentence transliteration on all 12 Dakshina languages | n/s | **H** |
| Madhani et al. (IndicLID) [33] | 2023 | ACL 2023 (short) | Native and romanised LID test set and models for 22 Indic languages | First LID for romanised Indic text | Y | **H**: script and language gating for the router |
| Benton et al. [34] | 2025 | EMNLP 2025 | Synthetic training data with natural spelling variation for romanised LID | Bhasha-Abhijnaanam romanised F1 rises from 74.7 to 85.4 (linear) and 88.2 | n/s | **H** |
| Herath and Sumanathilaka (TAMZHI) [35] | 2024 | ICTer 17(1) | Review plus hybrid method for vowel-dropped "shorthand" romanised Tamil to Tamil script | Targets the 12-vs-5 vowel mismatch of Tamil romanisation | n/s | **H**: Tamil-specific, same problem as the Tanglish rules |

### B. Code-mixed QA, RAG and LLM behaviour

| Paper | Year | Venue | Approach | Key result | Code? | Relevance |
|---|---|---|---|---|---|---|
| Gupta, Chinnakotla and Shrivastava [36] | 2018 | CALCS 2018 | Hindi–English code-mixed KBQA; triplet-Siamese re-ranker | Back-transliterated CM questions beat lexically and sentence-translated ones by 5% and 35% accuracy | n/s | **H**: transliterate-vs-translate evidence |
| Khanuja et al. (GLUECoS) [37] | 2020 | ACL 2020 | Code-switched NLU benchmark (Hi–En, Es–En) including QA | Multilingual models fine-tuned on synthetic CS data do best | Data | M |
| Winata et al. [38] | 2023 | Findings ACL 2023 | Systematic survey of code-switching research | Decades-long map of tasks, trends, challenges | n/a | M |
| Zhang et al. [39] | 2023 | EMNLP 2023 | Benchmarks multilingual LLMs on CS sentiment, MT, summarisation, LID | LLMs underperform much smaller fine-tuned models on CS text | n/s | M |
| Winata et al. (CodeMixQA) [40] | 2026 | arXiv | Human-annotated CS QA, 16 language-pair variants, native and transliterated forms | Persistent reasoning and generation failures under CS | Y | M/H |
| Das et al. (Indi-RomCoM) [41] | 2026 | arXiv | Romanised code-mixed instruction benchmark: 7 tasks, Hindi, Bengali, Gujarati, **Tamil**, 3 mixing levels | LLMs degrade as code-mixing density rises | n/s | **H**: Tamil, romanised, but not retrieval |
| Gaikwad and Gaikwad [42] | 2026 | SmartCom 2026, LNNS 1991 | Hallucination-aware RAG: code-mixed query normalisation, multilingual retrieval, abstention layer | Big hallucination reduction, largest for Hindi–English code-mixed queries (custom set) | n/s | **H**: normalisation inside RAG, Hindi |
| Sharma et al. [43] | 2026 | ICAICS 2025, LNNS 2024 | Hinglish queries to English docs; zero-shot vs fine-tuned multilingual embedders | Fine-tuned 96.3% vs best zero-shot 76.7% (strict task) | n/s | **H**: embedder gap on code-mixed RAG |
| Harika et al. (OneVoice) [44] | 2026 | ICTACT J. Soft Computing | Deployed college-support RAG chatbot; Unicode-level code-mix detection; Hinglish, Telugish, **Tamlish** | Production system description (no retrieval ablation) | n/s | M: same college-notice domain as Module 3 |
| Adoptante et al. [45] | 2025 | JAIT 16(2) | Five open LLMs on Tagalog–English code-switched RAG | Mistral and SeaLLM best grounded answers | n/s | M |
| Agarwal [46] | 2026 | W-NUT 2026 | Factorial ablation of normaliser, rules and LLM arbiter in Hinglish banking NLU | Normaliser helps a base encoder but is redundant after noisy-query fine-tuning; on native-reviewed **Tamil** and Telugu probes normalisation is "unstable in sign" | n/s | **H**: cautions against assuming the normaliser always helps |
| Fetahu et al. [77] | 2021 | SIGIR '21 | Gazetteer-infused MoE NER for code-mixed web queries (EMBER, 6 languages) | F1 = 68% on code-mixed query NER | Data | **H**: entity-safe LID |

### C. Tamil and Indic resources and benchmarks

| Paper | Year | Venue | Approach | Key result | Code? | Relevance |
|---|---|---|---|---|---|---|
| Doddapaneni et al. [47] | 2023 | ACL 2023 | IndicCorp v2 (20.9B tokens, 24 languages), IndicXTREME, IndicBERT v2 | First standard Indic zero-shot NLU benchmark | Y | M: source of the nlpctx documents [18] |
| Gala et al. (IndicTrans2) [48] | 2023 | arXiv | Open MT for all 22 scheduled languages; BPCC corpus | First open models covering all 22 | Y | M: used to build [18] |
| Balachandran (Tamil-Llama) [49] | 2023 | arXiv | LLaMA-2 plus 16,000 Tamil tokens, LoRA, Tamil Alpaca and OpenOrca | Big gains in Tamil generation | n/s | M (Module 4 generator) |
| Kumaresan et al. (Agaram 2.5B) [50] | 2026 | arXiv | Tamil-first LM from scratch; Tamil, **Tanglish**, English; tool calling | Tokeniser needs 1.55 tokens per Tamil word vs 9.44 for Qwen2.5; beats Sarvam-1 on 6 FLORES directions | n/s | **H** (Module 4 generator candidate) |
| Sarvam AI (Sarvam-1) [51] *grey* | 2024 | HF model card | 2B LM for 10 Indic languages incl. Tamil | Fertility 1.4–2.1 tokens per word (card claim) | Y (weights) | M |
| Haq et al. (IndicIRSuite) [52] | 2024 | ACL 2024 (short) | INDIC-MARCO (MT of MS MARCO, 11 languages incl. Tamil) plus Indic-ColBERT | +47.47% MRR@10 over INDIC-MARCO baselines | Y | **H**: native-script Tamil IR baseline |
| Prasanjith et al. (IndicRAGSuite) [53] | 2025 | arXiv | IndicMSMarco (1,000 manually translated queries, 13 languages, Tamil included) plus Wikipedia QA training tuples | First Indic RAG retrieval and generation benchmark | Data | **H** |
| Singh et al. (Indic-QA) [54] | 2025 | Findings NAACL 2025 | Context-grounded QA in 11 Indic languages | Translate-Test beats multilingual LLMs in low-resource settings | Data | **H**: Module 4 |
| Zhang et al. (MIRACL) [55] | 2023 | TACL 11 | 18-language monolingual retrieval, 726k judgements | Telugu present, **no Tamil** (README checked) | Data | M (evidence of absence) |
| Raja et al. (MURMUR) [56] | 2026 | COLM 2026 | Cross-lingual multimodal RAG benchmark, **Tamil** and Yoruba | XM-RAG baseline 38.1 answer accuracy, far below English | n/s | M |
| Anthea et al. (TanglishMedBench) [57] *grey* | 2026 | Zenodo dataset | 700 Tanglish medical QA pairs with English equivalents and expert accuracy and safety labels | QA evaluation only; no retrieval corpus or qrels | Data | **H**: closest Tanglish benchmark |

### D. Multilingual embeddings and romanisation

| Paper | Year | Venue | Approach | Key result | Code? | Relevance |
|---|---|---|---|---|---|---|
| Duquenne et al. (SONAR) [58] | 2023 | arXiv | 200-language fixed-size sentence space with text and speech encoders | Beats LASER3 and LaBSE on xsim and xsim++ | Y | M: candidate embedder |
| LCM Team (Large Concept Models) [59] | 2024 | arXiv | Autoregressive modelling in the SONAR concept space | Language-agnostic "concept" LM | Y | L |
| Husain et al. (RomanSetu) [60] | 2024 | ACL 2024 | Continual pre-training and instruction tuning on romanised text | Romanisation cuts token fertility 2–4×; romanised embeddings align more closely with English | Y | **H**: an argument that romanised input is not just noise |
| Verma et al. [61] | 2026 | ACL 2026 | LAPE and SAE analysis of language-associated units | "Romanization induces near-disjoint representations that align with neither native-script inputs nor English" | n/s | **H**: mechanism for the romanised collapse in Ch. 5 |
| Zhu et al. [62] | 2026 | ACL 2026 | Embedding-level interpolation of parallel queries (BGE-M3, mMARCO) | Best mix beats the best monolingual endpoint in 88/105 cases; English queries best for English-containing indices | n/s | **H** |

### E. Hybrid fusion, query rewriting, chunking

| Paper | Year | Venue | Approach | Key result | Code? | Relevance |
|---|---|---|---|---|---|---|
| Bruch et al. [63] | 2023 | ACM TOIS 42 | Analysis of convex combination vs RRF | RRF is sensitive to its parameters; tuned convex combination beats RRF in and out of domain | n/s | **H** |
| Chauhan and Agarwal [64] | 2026 | IEEE Access 14 | Per-query cost of fusion ("fusion tax"), 7 BEIR sets, 5 dense encoders, SPLADE, 3 fusion functions | Best fusion ranks relevant docs below the better component on 13–48% of queries; RRF taxes most when dense is clearly stronger | n/s | **H**: directly matches §5.6 |
| Ma et al. [65] | 2023 | EMNLP 2023 | Rewrite-Retrieve-Read: an LLM or small trained rewriter before retrieval | Query rewriting is a separate, trainable RAG stage | n/s | **H**: LLM rewriter baseline |
| Gao et al. (HyDE) [66] | 2023 | ACL 2023 | LLM-generated hypothetical document, embedded with Contriever | Beats unsupervised dense SOTA zero-shot | Y | M |
| Chen et al. (Dense X) [67] | 2024 | EMNLP 2024 | Retrieval unit choice; propositions as units | Retrieval unit "significantly impacts" retrieval and downstream QA | Y | M/H (chunking) |
| Qu et al. [68] | 2025 | Findings NAACL 2025 | Semantic vs fixed-size chunking on 3 tasks | Semantic chunking's cost "not justified by consistent performance gains" | n/s | **H** (chunking baseline choice) |

### F. RAG and LLM-judge evaluation (multilingual and Indic)

| Paper | Year | Venue | Approach | Key result | Code? | Relevance |
|---|---|---|---|---|---|---|
| Es et al. (RAGAs) [69] | 2024 | EACL 2024 demo | Reference-free RAG metrics (faithfulness, answer and context relevance) | Widely used framework | Y | **H**: Module 4 |
| Saad-Falcon et al. (ARES) [70] | 2024 | NAACL 2024 | Fine-tuned light LM judges plus prediction-powered inference | Accurate with a few hundred human labels; robust to domain shift | Y | **H** |
| Zheng et al. [71] | 2023 | NeurIPS 2023 (D&B) | MT-Bench and Chatbot Arena; LLM-as-judge biases | GPT-4 judge over 80% agreement with humans; position, verbosity and self-enhancement biases | Y | M |
| Hada et al. [72] | 2024 | Findings EACL 2024 | LLM evaluators calibrated on 20K human judgements, 8 languages | Bias towards higher scores; calibration needed esp. for low-resource, non-Latin scripts | n/s | **H** |
| Watts et al. (PARIKSHA) [73] | 2024 | EMNLP 2024 | 30 models, 10 Indic languages, 90K human plus 30K LLM evaluations | Human–LLM evaluator agreement varies; GPT-4o and Llama-3-70B best | Data | **H** |
| Gumma et al. (HEALTH-PARIKSHA) [74] | 2024 | arXiv | 24 LLMs on real Indian patient queries via a uniform RAG pipeline; Indian English plus 4 Indic languages | Factual correctness lower for Indic queries; code-mixed queries challenge evaluators | n/s | **H** |
| Thakur et al. (NoMIRACL) [75] | 2024 | Findings EMNLP 2024 | Relevant and non-relevant passage subsets, 18 languages | LLaMA-2 and Orca-2 hallucinate on over 88% of non-relevant sets | Data | M |
| Chirkova et al. [76] | 2024 | KnowLLM @ ACL 2024 | mRAG pipeline, 13 languages (BERGEN) | Needs prompt engineering for user-language generation; metrics need adjusting for spelling of named entities; code-switching listed as an open limitation | Y | **H** |

---

## 3. Coverage table

The columns are the problem aspects of this thesis. ✓ = covered, ◐ = partly covered, ✗ = not covered.

| Approach / line of work | Representative papers | Tamil | Romanised queries | Code-mixed queries | Modern dense retrieval | RAG (generation) | Controlled component comparison | Gap? |
|---|---|---|---|---|---|---|---|---|
| FIRE transliterated search / MSIR | [19]–[21], [24], [25] | ◐ (LID only, 2014–15) | ✓ | ✓ | ✗ | ✗ | ◐ | **Yes**: no Tamil retrieval |
| FIRE CMIR (Bengali) | [9], [10], [29], [30] | ✗ | ✓ | ✓ | ✓ | ✗ | ◐ (fusion) | **Yes** |
| Script-gap neural IR | [28], [61], [62] | ✗ | ✓ | ◐ | ✓ | ✗ | ◐ | **Yes**: no Indic |
| Code-switching IR benchmarks | [11] | ✗ | ✗ (native scripts) | ✓ | ✓ | ✗ | ✓ | **Yes** |
| Hinglish code-mixed RAG | [42], [43], [44] | ◐ ([44] lists Tamlish, no eval) | ✓ | ✓ | ✓ | ✓ | ◐ ([43] embedders only) | **Yes**: no Tamil, small custom sets |
| Code-mixed LLM benchmarks | [39]–[41], [57] | ✓ ([41], [57]) | ✓ | ✓ | ✗ | ◐ (no retrieval) | ✗ | **Yes** |
| Indic native-script IR / RAG benchmarks | [52]–[55], [14] | ✓ | ✗ | ✗ | ✓ | ◐ ([53], [54]) | ◐ | **Yes**: no romanised queries |
| Transliteration / back-transliteration | [22], [27], [31], [32], [35] | ✓ ([31], [32], [35]) | ✓ | ◐ | ✗ | ✗ | ✗ (accuracy, not retrieval) | **Yes**: not evaluated as retrieval front-end |
| Romanised LID / entity handling | [33], [34], [77] | ✓ ([33], [34]) | ✓ | ✓ ([77]) | ✗ | ✗ | ✗ | Partial |
| Hybrid fusion analysis | [6], [63], [64] | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | **Yes**: no script-mismatch condition |
| Query rewriting for RAG | [65], [66], [42] | ✗ | ✗ | ◐ ([42]) | ✓ | ✓ | ◐ | **Yes** |
| Chunking studies | [15], [16], [67], [68] | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | **Yes**: no Tamil chunker |
| RAG / LLM-judge evaluation | [69]–[76] | ◐ ([73] Indic) | ✗ | ◐ ([74]) | ✓ | ✓ | ◐ | **Yes**: not validated on Tanglish |

---

## 4. Identified gaps

The confidence rule is the labrat one. HIGH means 3+ phrasings were searched, the top venues of the last 2 years were checked, no preprint fills the gap, and the work is feasible and meaningful. MEDIUM means some niche venues (mostly regional Springer and IEEE conferences) were not checked. LOW means the search was limited.

| # | Gap | Confidence | Evidence of absence | Why it matters |
|---|---|---|---|---|
| G1 | **No retrieval benchmark with human-written romanised or code-mixed Tamil queries and relevance judgements.** | **HIGH** | MIRACL has no Tamil [55]. INDIC-MARCO and IndicMSMarco have only native-script, translated Tamil queries [52], [53]. FIRE retrieval tracks are Hindi or Bengali [19], [20], [24], [9], [10]. TanglishMedBench has 700 QA pairs but no corpus or qrels [57]. Indi-RomCoM is instructions, not retrieval [41]. nlpctx is LLM-generated, with 22% of its "code-mixed" queries lacking Tamil (Ch. 5) [18]. DravidianLangTech 2025–26 shared tasks have no retrieval track. Searches across 8+ phrasings, OpenAlex and Crossref, FIRE 2024–25 CEUR, ACL 2026 and SIGIR 2026 programme found only unpublished GitHub demos (LEXIS, a disaster-relief RAG blog). | Without human queries, every finding in Ch. 5 rests on synthetic Tanglish. This is the core Module 3 contribution and a releasable resource for Module 5. |
| G2 | **No controlled comparison of RAG retrieval components (lexical, character n-gram, dense, fusion) for romanised and code-mixed Tamil.** | **HIGH** | The closest neural studies cover other scripts [28] (zh, ru, ar, el, fa) or native-script code-switching [11]. Hinglish RAG compares embedders only [43] or proposes one pipeline [42]. Singh's factorial design is English-only [15]. Forward chaining from [21] and [28] found no Indic follow-up. | Module 2 already gives the first baselines. Modules 3–5 make it a full factorial study on human queries. |
| G3 | **Query normalisation front-ends (Tanglish rules vs neural transliteration such as IndicXlit or Kirov et al. vs LLM rewrite vs translation) have never been compared by their effect on retrieval for Tamil.** | MEDIUM | Transliteration work reports character or word accuracy, not retrieval [22], [27], [31], [32], [35]. Rewrite-Retrieve-Read [65] and HyDE [66] are English. For Hindi KBQA, transliteration beats translation [36]. A normaliser was found redundant after fine-tuning and "unstable in sign" on Tamil probes, but for NLU, not retrieval [46]. Regional Springer and IEEE venues are not exhaustively checked (hence MEDIUM). | It decides Module 3's headline normaliser and whether the rules generalise beyond the 0.3 ms per query result. |
| G4 | **Fusion behaviour when one retriever is near-uninformative because of script mismatch, and script-gated routing as the alternative.** | MEDIUM | Fusion analyses use same-script English BEIR [63], [64]. The FIRE 2025 CMIR overview reports that fusion helps in same-script Roman Bengali [10]. No study has the cross-script setting where BM25 sees no shared tokens. [64] gives the mechanism ("RRF carries the higher tax wherever the dense retriever is clearly stronger") but not the script condition. | It explains and generalises §5.6 (0.788 → 0.710) and motivates the Module 3 script-gated router. |
| G5 | **Generation-side RAG evaluation (faithfulness, answer correctness, LLM-as-judge validity) for Tanglish queries.** | MEDIUM | RAGAs and ARES were validated in English [69], [70]. LLM judges are biased upward in low-resource, non-Latin settings [72]; Indic judge agreement varies [73]; code-mixed queries "pose challenges to evaluators" [74]. TanglishMedBench has expert labels but no RAG [57]. Nothing validates a judge on Tanglish. | Module 4 needs a small human-calibrated judge set before trusting RAGAs-style scores. |
| G6 | **Tamil-aware chunking (sentence and clause boundaries, grapheme-safe splits) for RAG.** | MEDIUM | Chunking studies cover English [15], [67], [68] and Khmer [16]. A Thai government-text segmentation paper (IEEE KST 2026) exists but was not opened. Two Tamil-specific phrasings found nothing. | It is a Module 3 component. The literature also warns that semantic chunking may not pay off [68], so fixed-size baselines must stay. |
| G7 | **Entity-safe, token-level language ID for romanised Tamil queries in a retrieval router.** | LOW | Sentence-level romanised LID exists [33], [34]. Code-mixed NER with gazetteers exists for web queries [77]. FIRE 2014–15 had Tamil word labelling [19], [20]. A dedicated search for Tamil entity-aware LID was not run. | It is a small Module 3 fix for the "Rajya Sabha" errors noted in Ch. 5. |

**Top 5 gaps:** G1 (HIGH), G2 (HIGH), G3 (MEDIUM), G4 (MEDIUM), G5 (MEDIUM).

---

## 5. Top 10 recommended readings

1. **Chari, Ounis and MacAvaney, "Lost in Transliteration" [28], SIGIR 2025.** The closest neural-IR precedent: BGE-M3 collapses on Latinised queries, and transliterate-train fine-tuning closes the gap. It is a ready-made Module 3 baseline (fine-tune mE5 or BGE-M3 on mixed Tamil-script and romanised text).
2. **Zeng et al., CS-MTEB / CSR-L [11]** (now *Findings of ACL 2026*, doi 10.18653/v1/2026.findings-acl.636). The code-switching IR benchmark design to imitate for the Tanglish set.
3. **Chauhan and Agarwal, "The Fusion Tax" [64], IEEE Access 2026.** A per-query fusion diagnostic. Use its "do not fuse" framing and sparse–dense balance rule to support §5.6 and the router.
4. **Bruch, Gai and Ingber [63], TOIS.** Why RRF's defaults are fragile, and convex combination as the fusion baseline to add.
5. **Kirov et al. [32], *Computational Linguistics*, with Dakshina [31].** The strongest sentence-level romanised-to-native transliteration, plus Tamil test data. This is the neural normaliser to compare with the rules (alongside IndicXlit [22]).
6. **Verma et al. [61], ACL 2026.** A mechanistic explanation of why romanised Tamil fails in dense retrieval: near-disjoint representations.
7. **Sharma et al. [43] and Gaikwad and Gaikwad [42], 2026.** The Hinglish code-mixed RAG studies a Tanglish thesis will be compared against.
8. **Prasanjith et al., IndicRAGSuite [53], with Haq et al., IndicIRSuite [52].** Native-script Tamil RAG and IR benchmarks: the "Tamil-script upper bound" condition for Module 3–4.
9. **Hada et al. [72] with Watts et al., PARIKSHA [73].** How far to trust LLM judges in Indic languages. This is required reading before Module 4.
10. **Agarwal [46], W-NUT 2026.** A rigorous ablation showing that normalisers can be redundant or sign-unstable on Tamil. It is the main counter-evidence the thesis must address.

---

## 6. How each gap maps to Modules 3–5

| Gap | Module 3 (human Tanglish set, chunking, router, baselines) | Module 4 (generation-side RAG evaluation) | Module 5 (paper and release) |
|---|---|---|---|
| G1 benchmark | Collect about 500 human Tanglish questions with qrels over long Tamil notices; report the code-mixing index and Tamil-word share per query (fixes the 22% issue in [18]) | Reuse the same questions with reference answers | Release as the first Tanglish retrieval benchmark; compare to FIRE [19], [20], CSR-L [11] and IndicMSMarco [53] |
| G2 components | Full factorial: {raw, rules, IndicXlit, Kirov-style, LLM-rewrite} × {BM25-word, BM25-char3, mE5, BGE-M3, LaBSE, SONAR [58]} × {no fusion, RRF, convex [63], router}, with the Ch. 5 bootstrap tests | Do component wins carry through to answers? | Main results table |
| G3 normalisation | Add IndicXlit [22], the Kirov-style contextual transliterator [32] and an LLM rewriter [65]; add transliterate-train fine-tuning [28] as the "learned" alternative; report latency | Normalisation's effect on faithfulness | Ablation; address [46]'s sign-instability finding head-on |
| G4 fusion | Script-gated router vs RRF vs tuned convex combination; per-query "fusion tax" analysis [64] | — | A short analysis section; link to [10]'s opposite finding |
| G5 evaluation | — | RAGAs [69] and ARES [70] with a Tamil/Tanglish judge calibrated on about 100 human labels, following [72], [73]; abstention on non-relevant context [75], [42] | Report judge–human agreement |
| G6 chunking | Tamil-aware sentence and clause chunker vs fixed, recursive and semantic chunkers [68] and proposition-style units [67] on long documents | Context-length effects on answers | — |
| G7 entity LID | Gazetteer plus IndicLID [33], [34], [77] for entity-safe token tagging | — | — |

---

## 7. Contradictions and devil's-advocate checks

- **Fusion helps vs fusion hurts.** The FIRE 2025 CMIR overview reports that "fusion and hybrid retrieval systems consistently outperform standalone models" [10], and [30] shows BM25 plus SBERT beating BM25 by 83%. Chapter 5 instead finds that equal-weight RRF hurts cross-script retrieval. **Reconciliation:** CMIR queries and documents share the Roman script, so both lists carry signal. In our English→Tamil and romanised→Tamil settings the lexical list is near-empty. [64] predicts the higher tax exactly when "the dense retriever is clearly stronger", and [63] shows RRF is parameter-sensitive. The thesis should state the condition rather than claim that "fusion hurts" in general.
- **Romanisation as a remedy vs romanisation as the problem.** RomanSetu [60] finds romanised text aligns *better* with English in an LLM continually pre-trained on it. [61] finds romanisation yields representations aligned with *neither* script in standard multilingual models. Both can be true: the difference is whether the model was trained on romanised text. This supports the transliterate-train baseline [28] as a Module 3 condition.
- **Normalisation is not always helpful.** [46] reports that a normaliser becomes redundant after noisy-query fine-tuning and is unstable in sign on Tamil probes. Chapter 5 found that normalisation helps lexical retrieval for romanised queries but not dense retrieval for code-mixed ones (p = 0.45). The two results agree. Module 3 should test normalisation together with fine-tuning, not only against a frozen encoder.
- **Translation vs transliteration.** For Hindi KBQA, back-transliteration beats translation [36]. For Indic QA with LLMs, Translate-Test beats direct multilingual LLMs [54]. These are different stages (retrieval front-end vs generation), so Module 3–4 should test both.

---

## 8. Verification record

### 8.1 Verified and included ([24]–[77])
Each entry in `references_new.bib` carries an `x-verified` field naming what was opened. The sources were ACL Anthology abstract plus BibTeX (25 entries), OpenAlex abstracts (23, several also cross-checked on the publisher page), and publisher, CEUR, COLM, Zenodo or Hugging Face pages (6). Every number quoted in §2 appears in the opened abstract or page. Items to re-check against the PDF before submission:
- [32] issue number and year: OpenAlex says 2023 (online); vol. 50 belongs to 2024.
- [63] issue number.
- [48] TMLR version: only arXiv was verifiable.
- [49] author given name: OpenAlex says "Anitha", which is likely wrong; check the arXiv author line.
- [41] full author list.
- [71] NeurIPS volume and track.
- [46] DOI is printed by the Anthology without "v1".

### 8.2 Verified but left out of Chapter 2
These are kept here for possible later use; each abstract was opened:
- WebShodh (Chandu et al., 2017, doi 10.1007/978-3-319-65813-1_9)
- Gupta et al. CoNLL 2018 code-mixed QG/QA (K18-1012)
- LinCE (2020.lrec-1.223)
- COMI-LINGUA (Findings EMNLP 2025)
- SingRAG (ICITR 2024)
- "Neither Here Nor There" (arXiv 2603.19771)
- Code Mixologist (arXiv 2602.11181)
- Nguyen and Tran, Interspeech 2025: Tamil–English code-switched ASR with synthetic data, for a later voice-query extension
- MuRIL (arXiv 2103.10730)
- L3Cube-IndicSBERT (arXiv 2304.11434)
- IndicNLPSuite (Findings EMNLP 2020)
- IndicGenBench (ACL 2024)
- Hindi-BEIR (NAACL 2025)
- BhashaSutra (ACL 2026)
- Mr. TyDi (MRL 2021)
- XOR QA (NAACL 2021)
- DPR (EMNLP 2020)
- MTEB (EACL 2023)
- MMTEB (arXiv 2502.13595)
- Moosa et al. (Findings EACL 2023)
- Purkayastha et al. (Findings EMNLP 2023)
- TransMI (arXiv 2405.09913)
- Liu et al., "How Transliterations Improve Crosslingual Alignment" (arXiv 2409.17326)
- Fadha et al., BM25 vs mE5 vs RRF (JAIC 2026)
- Query2doc (EMNLP 2023)
- Late Chunking (arXiv 2409.04701)
- MEGA (EMNLP 2023)
- CIA/Hercule (arXiv 2410.13394)
- Wu et al., Futurepedia mRAG (arXiv 2410.21970)
- Language drift in mRAG (AAAI 2026)
- Multilingual RAG for KIQA (Findings EACL 2026)
- Ganguly et al., "Retrievability of Code Mixed Microblogs" (SIGIR 2016)
- Prabhakar et al., "Query Expansion for Transliterated Text Retrieval" (TALLIP 2021)
- BanglaTLit (Findings EMNLP 2024)

### 8.3 Unverified or excluded (not cited)
| Item | Why |
|---|---|
| Banerjee et al., "MSIR@FIRE: A comprehensive report 2013–2016", SN Comput. Sci. 2020 (doi 10.1007/s42979-019-0058-0) | Metadata only; abstract not available in OpenAlex and not opened |
| Viswabharathi et al., "Transliteration framework for Tamil-English code-mixed text", SIST 2025 (doi 10.1007/978-981-97-7717-4_33) | Metadata only; abstract not opened. **Worth fetching**: Tamil-specific |
| Chen et al., "Out-of-domain semantics to the rescue! Zero-shot hybrid retrieval", ECIR 2022 | Abstract not returned |
| Alshabrawi et al., "Text chunking strategies for RAG: A survey", IEEE Access 2026 | Abstract not returned |
| Jonjale and Shinde, "The Code-Mixing Penalty in Clinical RAG" (ICCSDI 2026) | Only the Zenodo data artifact was opened; the paper itself was not found |
| Morgan-Tanglish-v7 embeddings and TanglishSTS (HF / Zenodo, 2026) | Seen in search excerpts only; grey, self-reported scores |
| TanglishGuard (IJISRT 2026) | Not opened; venue of concern |
| GitHub demos: LEXIS multilingual RAG, a Tamil disaster-relief RAG, TamilTech-QA | Code repositories without evaluation papers. Cited only as evidence that practitioners are building Tanglish RAG without benchmarks |
| Zenodo 2026 series on "artificially code-switched dense retrieval" (10.5281/zenodo.207…–214…) | Dozens of near-identical deposits with no venue; excluded as likely low-quality or auto-generated |
| "Hybrid Retrieval for Indic Language QA using an Improved RAG Pipeline" (ACSET 2026) and "Exploring Code-Mixed IR … Enhanced Embedding-Based Approach" (CIPHER 2026) | Not opened |
| Thai government-text segmentation for RAG (IEEE KST 2026) | Not opened; relevant to G6 |
| Riyadh and Kondrak Tamil figures (84% Hindi, 78% Tamil) seen in a preview-server PDF | The published abstract and PDF report Bengali and Hindi only, so the Tamil claim is **not** used |

### 8.4 Notes on existing references [1]–[23]
- **[11]** now has a published version: *Findings of the Association for Computational Linguistics: ACL 2026*, doi 10.18653/v1/2026.findings-acl.636 (ACL Anthology abstract opened). Update the entry from arXiv-only.
- **[9]** also appears in the ACM FIRE '24 proceedings as S. Chanda and S. Pal, pp. 29–31, doi 10.1145/3734947.3735670. The CEUR version stays valid; add the DOI if the department prefers DOIs.
- **[10]**'s abstract states that fusion and hybrid systems outperform standalone models in CMIR-2025. Cite this in §5.6 as the same-script contrast (§7 above).

---

## 9. Limitations of this survey
- Semantic Scholar was rate-limited for the whole session, so its coverage and deduplication were lost. OpenAlex and Crossref may miss some workshop papers.
- Google Scholar and IEEE Xplore full-text search were not used, so regional Indian conference proceedings (Springer LNNS, IEEE ICxxx) are under-sampled. This is why G3–G6 are MEDIUM, not HIGH.
- Abstract-level verification only. Table or figure numbers not in an abstract were not checked against PDFs.
- Interspeech was mined lightly: one search, two papers opened. Speech is outside Modules 3–5.
