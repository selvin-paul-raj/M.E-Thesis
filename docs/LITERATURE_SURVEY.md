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
| Morgan-Tanglish-v7 embeddings and TanglishSTS (HF / Zenodo, 2026) | *Superseded 2 Nov 2026:* opened and added as [86], [87] (§10) |
| TanglishGuard (IJISRT 2026) | *Superseded 2 Nov 2026:* opened and added as [88] (§10); venue still of concern |
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


---

## 10. Additions Nov 2, 2026: bilingual document base framing

### 10.1 Framing change (agreed 2 Nov 2026)
The thesis setting is now **Tanglish questions (romanised and code-mixed Tamil–English) over a bilingual document base** holding both Tamil and English documents: Tamil Nadu Government Orders, scheme notices, college circulars. Two consequences follow. (1) The answer may exist **only in a Tamil document**, so a translate-the-query-to-English pipeline cannot reach it. (2) In a single mixed index, retrievers may show **language-preference bias**. Module 2 stays as the groundwork. On the Tamil corpus, romanised queries go from MRR@10 0.143 (raw, dense) to 0.684 (Tanglish normaliser + char 3-gram BM25), against 0.923 for Tamil-script queries. On the English side, code-mixed queries reach 0.901 and romanised queries at best 0.557. The mixed single-index test is new Module 3 work.

### 10.2 New references and duplicate check
Numbering continues from [84], the highest number in RESEARCH_MAP.md §7. New: [85]–[92]. [84] was previously unverified and is now verified. Already present and **not** re-added: Gupta et al. SIGIR 2014 = [21]; MSIR FIRE-2016 = [19]; Chirkova et al. 2024 = [76]. Full entries are in `references_new_IEEE.md` and `references_new.bib` (which now also carry [78]–[83] copied from RESEARCH_MAP.md).

### 10.3 Paper table (additions)
| Paper | Year | Venue | Approach | Key result | Code / model? | Relevance |
|---|---|---|---|---|---|---|
| SchemeAI [85] | 2026 | IJARSCT | MiniLM + FAISS over English CSV; translate output to Tamil | No numbers reported | No | "Existing system" baseline |
| Morgan-Tanglish-v7 [86] / TanglishSTS [87] | 2026 | Zenodo preprint / HF | Fine-tuned MiniLM-L12 for Tanglish | STS Spearman 0.869 (self-reported) | Yes, Apache-2.0 | Module 3 embedder baseline |
| TanglishGuard [88] | 2026 | IJISRT | 90 prompts × 3 languages × 4 LLMs | Tanglish 9.9 vs 10.0 safety | No | PhD WP3 motivation (weak) |
| Thenmozhi and Aravindan [84] | 2018 | Sādhanā | Tamil→English query translation + ontology | Better precision (no numbers seen) | No | Translate-query family |
| Ranaldi et al. [89] | 2026 | Findings EACL | tRAG / MultiRAG / CrossRAG | CrossRAG best; tRAG limited coverage | n/s | Module 3 tRAG, Module 4 CrossRAG baselines |
| Park and Lee [90] | 2025 | Findings ACL | Language-preference analysis; DKM-RAG | Retrievers prefer high-resource and query language; generators prefer query language or Latin script | Yes | Bias evidence |
| Amiraz et al. [91] | 2025 | ArabicNLP | Non-parallel Ar–En corpus; oracle; balanced and translation retrieval | Cross-lingual Hit@20 down to 41–56%; balanced fix | Yes (data) | Template for the Module 3 mixed index |
| Hira et al. [92] | 2026 | EMNLP | Code-switched queries over a 12-language parallel pool | English anchoring, worst for Indic; romanisation amplifies it | Yes | Main novelty threat; bilingual-retrieval baseline |

### 10.4 Coverage update and new gap
| Approach | Papers | Tamil | Romanised / code-mixed query | Bilingual non-parallel index | Answer in one language only | Lexical / normaliser remedy | Gap? |
|---|---|---|---|---|---|---|---|
| Translate query to English | [84], [85], tRAG in [89] | ✓ | ✗ | ✗ (English only) | ✗ | ✗ | Yes |
| Translate evidence (CrossRAG) | [89] | ✗ | ✗ | ✗ (Wikipedia) | ✗ | ✗ | Yes |
| Language-bias analysis | [90], [92] | ✗ | ◐ ([92]: Hi/Bn/Mr/Ur romanised) | ✗ (parallel) | ✗ | ✗ | Yes |
| Bilingual domain index | [91] | ✗ | ✗ | ✓ | ✓ | ◐ (balanced, translation) | Yes for Tamil / romanised |
| Tanglish embedder | [86] | ✓ | ✓ | ✗ | ✗ | ✗ | Yes (no retrieval test) |

**G8 (new).** *No study measures language-preference bias for romanised and code-mixed Tamil (Tanglish) queries over a mixed, non-parallel Tamil+English index where the answer exists in only one language, or compares remedies (normaliser + char BM25, script-gated routing, balanced per-language retrieval, query translation, evidence translation).*
**Confidence: MEDIUM.** [91] covers the design for Arabic and [92] covers romanised Indic bias with parallel documents. Neither covers Tamil, non-parallel Indic documents or lexical remedies. Only one search pass was made (ACL Anthology, Google-style web search). [92] appeared in October 2026, so preprints from the last six months may exist and should be re-checked before submission.
**Maps to:** Module 3 (mixed index vs per-language indices; bias metrics; balanced retrieval and translation baselines), Module 4 (router chooses a language mix; CrossRAG vs native-evidence generation), PhD WP1 (other Indic pairs).

### 10.5 What weakens the novelty claim (candid)
1. **[92] Hira et al. (EMNLP 2026)** already shows English anchoring for romanised Indic code-switched queries in a mixed-language index. Drop any "first to show language bias" wording.
2. **[91] Amiraz et al. (2025)** already uses a bilingual index with each answer in one language and shows balanced retrieval as a fix. Our Module 3 is partly a Tamil/Tanglish replication with a script twist.
3. **[86] Morgan-Tanglish-v7** means "no Tanglish embedder exists" can't be claimed, even though its evidence is weak.
4. **[85] SchemeAI** means "first bilingual Tamil Nadu scheme RAG" can't be claimed; ours is the first *evaluated* one.
5. What still stands: Tamil (absent from [89]–[92]); native non-parallel Tamil+English government documents; human Tanglish queries with qrels (G1); a cross-script fusion finding and model-free lexical remedies on CPU; per-gold-language analysis where English anchoring causes hard misses.

### 10.6 Verification record (Nov 2, 2026)
| Ref | Status | What was opened |
|---|---|---|
| [84] Thenmozhi and Aravindan, Sādhanā 2018 | **Verified** (abstract) | Springer article page: abstract, metadata, appendix table titles; full text paywalled |
| [85] SchemeAI, IJARSCT 2026 (RG 403743494) | **Verified** (full text) | doi.org/10.48175/ijarsct-33228 PDF, 8 pages |
| [86] Morgan-Tanglish-v7 (RG 407468354) | **Verified** (record + model); scores self-reported | Zenodo record 10.5281/zenodo.20792177; HF model card README; HF API (public, Apache-2.0, 470.6 MB safetensors); config.json. Not smoke-loaded (no torch) |
| [87] TanglishSTS | **Verified** (dataset card, HF API: public, CC BY 4.0) | huggingface.co/datasets/vishnu-n/TanglishSTS |
| [88] TanglishGuard, IJISRT 2026 (RG 410941564) | **Verified** (abstract + PDF) | ijisrt.com abstract page via DOI; IJISRT26JUL962.pdf |
| [89] Ranaldi, Haddow and Birch, Findings EACL 2026 | **Verified** (abstract + PDF) | aclanthology.org/2026.findings-eacl.35 and its PDF |
| [90] Park and Lee, Findings ACL 2025 | **Verified** (abstract) | aclanthology.org/2025.findings-acl.295 |
| [91] Amiraz et al., ArabicNLP 2025 | **Verified** (full PDF + Crossref) | aclanthology.org/2025.arabicnlp-main.6.pdf |
| [92] Hira, Mire and Sap, EMNLP 2026 | **Verified** (full PDF); DOI not yet in Crossref | aclanthology.org/2026.emnlp-main.1830.pdf |
| [21] Gupta et al., SIGIR 2014 (existing) | Re-verified | Crossref metadata |
| [19] MSIR FIRE-2016 (existing) | Re-verified | ceur-ws.org/Vol-1737/T3-1.pdf |
| [76] Chirkova et al. 2024 (existing) | Re-verified | aclanthology.org/2024.knowllm-1.15 |
| Wang et al. ACL 2026; Faux Polyglot; Linguistic nepotism; DeLP | **Not added** | Crossref / search excerpts only |

ResearchGate pages were not used. Each RG item was matched by title through its DOI, publisher, Zenodo or Hugging Face page.

### 10.7 In-depth reviews

#### A1. Rekha, Pragadeeshwaran, Surendhar and Udhayachandran — SchemeAI: Government schemes recommendation with a bilingual RAG chatbot [85], IJARSCT 2026

- **Problem.** Citizens can't easily find the government schemes they qualify for, because portals are scattered and there is a language barrier for Tamil speakers.
- **Method.** A Flask web chatbot. The user picks a state and a category, then types a question. The question is embedded with **all-MiniLM-L6-v2** (Sentence-BERT) and matched against a **FAISS** index built from a structured CSV of central and state schemes (`updated_data.csv`: Agriculture, Education, Housing; Tamil Nadu, Telangana, Puducherry). A language-detection step plus the **GoogleTranslator API** "dynamically translates English scheme details into Tamil" for display. An "Intelligence Explanation" page shows the pipeline (called XAI in the paper).
- **Data.** One English CSV. The paper doesn't give its size, and there is no test set.
- **Results.** Screenshots of one English and one Tamil question, plus an "accuracy comparison" graph and a "response time" graph. The text gives no numbers, metric definitions or evaluation protocol.
- **Strengths.** It addresses exactly our use case 1 (Tamil Nadu scheme help desk), shows that Tamil Nadu colleges are building bilingual RAG, and uses a cheap CPU stack.
- **Weaknesses.** (1) The knowledge base is English only, so there are no Tamil documents. (2) all-MiniLM-L6-v2 is an English-trained embedder, and the paper doesn't say whether Tamil queries are translated before they are embedded. (3) Translation only touches the output. (4) There is no handling of romanised or code-mixed input. A Tanglish query is in Latin letters, so a language detector will probably label it English and pass it straight to an English embedder. This is our inference and isn't tested in the paper. (5) There is no retrieval evaluation. (6) Editorial problems: the in-text literature survey cites authors who don't match the reference list. The venue is a low-selectivity journal.
- **Relevance.** This is the **"existing system"** in our existing-vs-proposed comparison: a translate-around-an-English-index design typical of local deployments.
- **Why it matters.** It shows what a Tamil Nadu bilingual RAG looks like in practice today, and why it can't be judged: nothing is measured. Module 3 re-implements a SchemeAI-style baseline (MiniLM + FAISS, query translated to English) on the bilingual benchmark.
- **Gap it leaves.** No Tamil-language documents, so an answer that exists only in a Tamil G.O. is unreachable. No romanised or code-mixed queries. No retrieval or answer metrics.

#### A2. Vishnu N — Morgan-Tanglish-v7 sentence embeddings [86] and TanglishSTS [87], Zenodo / Hugging Face 2026

- **Problem.** General multilingual sentence embedders handle Tanglish (romanised Tamil-English chat text) poorly.
- **Method.** A fine-tune of `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. This is the `base_model` on the Hugging Face card, and the config (12-layer BERT, 384-d, 250,037-token vocabulary, about 118M parameters) matches it. The paper's own name for its augmentation is "Concept Cluster Training": C(n,2) positive pairs from n paraphrases of one concept. The config's `_name_or_path` is `models/tanglish-mnrl-v6`, which suggests MNRL contrastive training. The card's mention of CoSENT loss on 1,375 human-scored pairs was seen only in a search excerpt.
- **Data.** Tanglish-Corpus-185k: 185,973 Latin-script sentences scraped from YouTube and Reddit in June 2026, filtered with a 1,018-token Tamil lexicon and 27 pattern rules. TanglishSTS: 325 pairs scored 0–5 by one native speaker, covering college, work, cricket, food, tech and social-media topics.
- **Results (self-reported, from the card and the Zenodo abstract).** TanglishSTS Spearman: **0.8689**, against 0.7642 for L3Cube-IndicSBERT, 0.7583 for BGE-M3, 0.7510 for all-MiniLM-L6-v2 and 0.7279 for the base model. It wins 8 of 9 domains and loses on social media (0.385 vs 0.485 for BGE-M3).
- **Strengths.** It is the only public embedder built for Tanglish. It is Apache-2.0, small (384-d, the same size as our mE5-small, so it runs on CPU), and released with data. The author is a Chennai-based undergraduate (Sri Sairam Institute of Technology).
- **Weaknesses.** (1) Single-author preprint: the Zenodo PDF is 15.8 kB and there is no peer review. (2) The benchmark has one annotator and 325 pairs. 149 of them (46%) are scored 0 ("completely unrelated"), so Spearman mostly rewards telling unrelated pairs from related ones, which is easy. (3) No retrieval evaluation at all. (4) Everything is Latin script: it was trained and tested Tanglish to Tanglish. **Whether it maps a Tanglish query onto Tamil-script or English government documents is unknown**, and that mapping is what we need. (5) The card is inconsistent: the benchmark is introduced under the model's name, the domain table says "Morgan-tanglish-st-1", and there are two namespaces (`vishnu-n`, `vishnuexe`). (6) Possible overlap between training and test data wasn't checked.
- **Downloadable?** **Yes.** The Hugging Face API shows `vishnu-n/Morgan-Tanglish-v7` as public, not gated, licence apache-2.0, with `model.safetensors` of 470,637,416 bytes (fp32) in sentence-transformers format (checked 2 Nov 2026). It was **not smoke-loaded**: the sandbox has no PyTorch, and installing it plus the 470 MB weights wasn't cheap. Its config and file list are consistent with `SentenceTransformer("vishnu-n/Morgan-Tanglish-v7")`.
- **Relevance.** A Module 3 embedder baseline: the learned "Tanglish embedder" alternative to our model-free normaliser.
- **Why it matters.** If a Tanglish-tuned embedder alone recovered romanised retrieval over Tamil and English documents, our normaliser contribution would shrink. So it must be tested, not ignored. Our prediction is that it helps on English documents and code-mixed queries but not on Tamil-script documents, because it never saw Tamil script in training.
- **Gap it leaves.** No retrieval benchmark, no cross-script test, no RAG.

#### A3. Gupta, Bali, Banchs, Choudhury and Rosso — Query expansion for mixed-script IR [21], SIGIR 2014 (already in the list; re-verified)

- **Verification.** Crossref metadata re-checked: pp. 677–686, doi 10.1145/2600428.2609622. The full review is in Dossier §9.3.
- **What it adds to the new framing.** Mixed-script IR was defined as **one language written in two scripts** (native and Roman) for both queries and documents. That is our Tamil-script vs romanised Tamil axis. It does **not** cover two *languages* in one index, so the bilingual Tamil+English setting goes beyond the MSIR definition. The 2014 setting is lexical and pre-neural, with no RAG.
- **Gap it leaves (bilingual view).** No language-preference question, because every document was in one language.

#### A4. Banerjee et al. — Overview of MSIR at FIRE-2016 [19] (already in the list; PDF re-opened)

- **Problem.** The fourth year of the FIRE mixed-script track.
- **Method / data.** Subtask 1: classifying code-mixed Bengali-English questions in Roman script (330 training and 180 test questions, 9 classes). Subtask 2: retrieving Roman-script Hindi-English code-mixed tweets (training: 6,133 tweets, 23 queries; test: 2,796 tweets, **12** queries; queries average 3.25 words and are mostly named entities).
- **Results.** Subtask 1: best accuracy 83.33% against a bag-of-words baseline of 79.44%. Subtask 2: best **MAP 0.0377**. The organisers call code-mixed tweet retrieval "a very challenging task".
- **Strengths.** Public tasks with qrels, and a long organiser lineage (MSR India, Jadavpur).
- **Weaknesses.** Tiny query sets (12 test queries) and social-media text only. Tamil appeared only in the 2014 word-labelling subtask, never in retrieval.
- **Relevance / why it matters.** It anchors the history of the problem and shows how small earlier evaluation sets were. Our planned ~500 human queries are a large step up. Every document was monolingual, so it doesn't speak to the bilingual-index question.
- **Gap it leaves.** No Tamil retrieval, no native-script documents mixed with English documents, no dense retrievers.

#### A5. Vijesh and Gothai — TanglishGuard [88], IJISRT 2026

- **Problem.** LLM safety is tested almost only in English. Is it also robust to Tanglish?
- **Method / data.** 90 harmful prompts (9 categories × 10), each written in English, Tamil and Tanglish. Four chat models (ChatGPT, Gemini, Claude, DeepSeek), 3 runs each. Scored on refusal (binary), cross-language consistency (1–10) and explanation quality (1–5).
- **Results.** Every model refuses more than 95% of prompts. English and Tamil score 10/10 on safety; Tanglish scores 9.9 (DeepSeek 9.8). The authors call this "subtle but consistent".
- **Strengths.** The first Tanglish-specific safety probe, and a clear trilingual design.
- **Weaknesses.** The effect is 0.1–0.2 on a 10-point scale with no significance test. The sample is small and the prompts' release status is unclear. Some references in the paper carry placeholder arXiv IDs ("2603.xxxxx"). The venue is of concern. It does no retrieval: prompts are sent to chat models directly.
- **Relevance.** PhD WP3 (trust and safety): evidence that the question is being asked locally.
- **Why it matters.** It strengthens the WP3 motivation, but it is not strong evidence of a safety gap. WP3 should test **retrieval-grounded** risks (prompt injection hidden in retrieved Tamil or English documents, abstention on irrelevant context), with significance tests.
- **Gap it leaves.** No RAG, no indirect injection, no statistics.

#### A6. Thenmozhi and Aravindan — Ontology-based Tamil–English CLIR [84], Sādhanā 2018 (SSN, Chennai)

- **Problem.** Tamil users querying English content. Query ambiguity hurts translation-based cross-lingual IR.
- **Method.** A Tamil morphological analyser, a Tamil-English bilingual dictionary and a named-entity database translate the Tamil query into English, with word-sense disambiguation. An automatically built English domain ontology then reformulates the translated query, and a web search engine retrieves English documents.
- **Data / results.** Agriculture domain. The abstract says it "outperforms other approaches in terms of precision"; numbers sit behind the paywall and weren't seen. The appendix tables show example queries in romanised form ("Mutkalappai", "Uzhudhal Upakaranangkal"). Whether users typed them that way or the authors transliterated them for display can't be confirmed without the full text.
- **Strengths.** The closest peer-reviewed Tamil–English IR work. It is from Chennai (a possible local reviewer or collaborator, D. Thenmozhi) and builds real Tamil language resources.
- **Weaknesses.** Pre-neural, with English-only target documents. Submitted in 2014 and published in 2018. No code-mixing.
- **Relevance / why it matters.** It is the classic **translate-the-query-to-English** design, the same family as the SchemeAI baseline. Our bilingual framing explains its blind spot: when the answer exists only in a Tamil document, translating into English searches the wrong half of the collection.
- **Gap it leaves.** No Tamil-language documents in the index, no romanised or code-mixed queries, no dense retrieval or RAG.

#### A7. Ranaldi, Haddow and Birch — Multilingual RAG for knowledge-intensive QA (CrossRAG) [89], Findings of EACL 2026

- **Problem.** How should RAG work when queries and knowledge are not in English?
- **Method.** Four pipelines compared. **monoRAG** retrieves in the query language only. **tRAG** translates the question into English and then retrieves. **MultiRAG** retrieves directly across many languages. **CrossRAG** retrieves across languages, then **translates the retrieved documents into one language (English)** before generating. Retrieval uses Cohere Embed v3 over a Wikipedia dump; translation uses Google Translate (and GPT-4o as a variant); the generators are GPT-4o, Llama-3-8B and Command-R-35B.
- **Data.** MKQA, MLQA and XOR TyDi QA. The PDF mentions Hindi and Bengali; Tamil isn't mentioned.
- **Results (as stated in the abstract and §4).** tRAG "suffers from limited coverage"; MultiRAG beats monoRAG and tRAG but brings inconsistency across languages; CrossRAG "significantly enhances performance", for both high- and low-resource languages.
- **Strengths.** A clean taxonomy of strategies, a published venue, three generators.
- **Weaknesses.** Wikipedia-based, so models may already know the answers (the critique in [91]). No code-mixed or romanised queries. It depends on a commercial translation API, which raises cost and privacy issues for government documents. The study is mostly about generation. A later paper [92] finds translating into English is "not universal", especially for Indic-script languages. (Note: [92] cites arXiv:2504.03616 with a different author list; [91] and the ACL Anthology give Ranaldi, Haddow and Birch, which we use.)
- **Relevance.** It supplies two baselines. **tRAG** (translate the Tanglish query to English, then retrieve) goes in Module 3. **CrossRAG** (translate retrieved Tamil chunks before generation) goes in Module 4.
- **Why it matters.** For a bilingual Tamil+English base, the key choice is what you translate: the query or the evidence. This paper is the reference point for that choice.
- **Gap it leaves.** No romanised or code-mixed queries, no Tamil, no domain-specific bilingual collection.

#### A8. Chirkova et al. — Retrieval-augmented generation in multilingual settings [76], KnowLLM @ ACL 2024 (already in the list; re-verified)

- **Problem.** A strong, reproducible baseline pipeline for multilingual RAG (mRAG).
- **Method / data.** User queries and a datastore in 13 languages, built on the BERGEN toolkit (github.com/naver/bergen). The abstract doesn't list the 13 languages, and we didn't check whether Tamil is one of them.
- **Results.** Off-the-shelf multilingual retrievers and generators are adequate, but **task-specific prompting is needed so the model answers in the user's language**. Metrics need adjusting for **named entities spelled differently**. Remaining failures: code-switching in non-Latin outputs, fluency errors, misreading documents, irrelevant retrieval.
- **Strengths.** Open code and a careful list of failure modes.
- **Weaknesses.** Wikipedia-style data; no romanised or code-mixed queries.
- **Relevance / why it matters.** Two Module 4 design inputs: a prompt that answers in the user's form (Tanglish in, Tanglish or Tamil out), and entity-tolerant answer matching. Tamil names have many Latin spellings.
- **Gap it leaves.** Code-mixed and romanised input, and domain-specific bilingual collections.

#### A9. Language preference / language bias in multilingual retrieval and RAG (search pass, 2 Nov 2026)

**[90] Park and Lee, "Investigating language preference of multilingual RAG systems", Findings of ACL 2025.**
- *Finding (abstract):* retrievers "prefer high-resource and query languages", but this preference doesn't consistently improve generation. **Generators prefer the query language or Latin scripts.** Fix: DKM-RAG, which fuses translated multilingual passages with the model's own knowledge.
- *Why it matters for us:* a romanised Tanglish query is in Latin script, so both the retriever and the generator may lean towards English (Latin) evidence over Tamil-script evidence.

**[91] Amiraz et al., "The cross-lingual cost: Retrieval biases in RAG over Arabic-English corpora", ArabicNLP 2025.** *This is the closest design to our Module 3.*
- *Setup:* two UAE bilingual corpora (Legal: 390 laws; Travel: Ministry of Foreign Affairs pages). Each document is placed in **exactly one language at random**. Queries are 50/50 Arabic and English, and **each answer exists in one language only**. BGE-M3 or mE5-large, a bge-reranker-v2-m3, and a Qwen2.5-14B generator.
- *Results:* retrieval is the bottleneck. Cross-lingual pairs drop sharply. Example: BGE-M3 on Legal gets Hit@20 of 56% for English queries on Arabic documents, against 86–92% when query and document share a language; mE5 drops from 88% (same language) to 46% (cross-language). A language-oracle shows the failure comes from **ranking documents of two languages against each other**, not from query–document mismatch. Two fixes, **balanced retrieval** (top-10 from each language) and **query translation with merged lists**, remove most of the cross-lingual loss with no same-language cost. The balanced fix costs nothing extra.
- *Weaknesses:* synthetic (DataMorgana) questions from parallel source documents, LLM-judged relevance, native script only.
- *Why it matters:* it gives us the experimental template (non-parallel bilingual index, answer in one language, per-cell analysis), and **balanced per-language retrieval becomes a required Module 3 baseline**. Our new element: a Tanglish query matches English documents by **script** but Tamil documents by **language**, so the bias may pull it the wrong way.

**[92] Hira, Mire and Sap, "The language of evidence: Robustness and bias in code-switched RAG", EMNLP 2026.** *The paper most threatening to our novelty claim.*
- *Setup:* CodeMixQA questions (English+X code-switched). The English source pages were **machine-translated into 11 languages** (bn, es, fr, hi, id, it, ja, ko, mr, ur, zh) and all 12 versions pooled into one index, so every answer exists in every language. Retrievers: mE5, LaBSE, mContriever, distiluse, bge-large-en. New metrics: LARS, language gap, joint bilingual coverage. Romanised query variants for Hindi, Bengali, Marathi and Urdu.
- *Results:* the strongest retrievers show **English anchoring**. **Indic-script queries show the largest English bias.** **Romanisation increases English concentration** in the top-k. Language-targeted contrastive training over-corrects: joint coverage collapses (English recall about 0.003). In RAG, English evidence helps Bengali, Hindi and Urdu, while native evidence helps Japanese, Korean, Marathi and Chinese; transliteration amplifies the English preference (Hindi transliterated: 3.98 with English evidence vs 3.38 with native). The authors recommend bilingual retrieval.
- *Weaknesses:* parallel, machine-translated corpus (the "answer exists only in one language" case is never tested); no Tamil; dense retrievers only, with no lexical or character n-gram retrieval and no normaliser; an LLM judge (κ = 0.68 against humans on 260 samples).
- *Why it matters:* it already shows, for other Indic languages, that romanised code-mixed queries over a mixed-language index lean towards English. **We can no longer claim to be first to show language bias for romanised Indic code-mixed queries in mixed-index RAG.** Our claim narrows to: Tamil (absent from [90]–[92]); **native, non-parallel bilingual government documents where the answer exists in only one language**, so English anchoring becomes a hard miss, not just a preference; and **model-free lexical remedies** (Tanglish normaliser + char 3-gram BM25, script-gated routing, balanced retrieval) evaluated on CPU.

**Seen but not added:** Wang et al., "All languages matter: Understanding and mitigating language bias in multilingual RAG" (ACL 2026, pp. 7441–7455, doi 10.18653/v1/2026.acl-long.338; reranking bias towards English and the query language; Crossref metadata checked, abstract seen only in search). Sharma et al., "Faux Polyglot" (NAACL 2025). Ki et al., "Linguistic nepotism" (2026). Park et al., "Debiased language preference-guided query fusion" (Findings of ACL 2026). Candidates for a later pass.
