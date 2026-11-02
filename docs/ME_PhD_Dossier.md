# How to read this dossier

This dossier puts the whole Tanglish RAG project in one place, from the M.E. thesis (August 2025 to May 2027) through to the PhD it is meant to grow into. Every number in it comes from the Module 2 experiments (`code/results/main_results.csv`, `significance.csv`, `codemix_audit.csv`) or from papers that were opened and checked during the literature survey of 31 October 2026. Planned work is always labelled *planned* and has no results attached. Reference numbers [1]–[77] match the Module 1–2 report, so the two documents can be cited side by side. **Update, 2 November 2026:** the setting has been reframed to *Tanglish questions over a bilingual (Tamil + English) document base*, and papers [84]–[92] were added after being opened and checked (the literature survey §10 has the verification record). Numbers [78]–[83] are research-map entries that are not cited here.

**Status key:** Done = completed with real results; Planned = designed, no results yet.

# 1. Executive summary

**Title.** *Code-Mixed Retrieval-Augmented Generation: An Empirical Study of Chunking, Embedding and Query Normalisation for Tamil–English (Tanglish) Queries.* Selvin PaulRaj K, M.E. CSE (AI), Kings Engineering College, Chennai. The M.E. is the first stage of a PhD line: **trustworthy AI agents for code-mixed Indian languages.**

**The problem, in three lines.**

1. Millions of Tamil speakers type questions in Tanglish (*"scholarship ku last date enna?"*). The documents that hold the answers in Tamil Nadu are **bilingual**: Government Orders and scheme notices often exist only in Tamil, while circulars and FAQs are often only in English.
2. A romanised Tamil query shares the *script* of the English documents but the *language* of the Tamil ones. Keyword search and multilingual embeddings both miss, translating the query into English can't reach an answer that exists only in a Tamil document, and a single mixed index may prefer documents in one language.
3. No published study measures what each RAG retrieval component (dense, lexical, fusion), query normalisation, or a mixed Tamil+English index does when the query is Tanglish.

**USP (what is new).** This is the first controlled, component-level study of RAG retrieval for romanised and code-mixed Tamil–English queries **over a bilingual Tamil + English document base where the answer may exist in only one language**. It is measured on the same information needs in four query forms. It comes with a fast, model-free Tanglish normaliser and the first evidence that the popular "hybrid BM25 + dense" default *hurts* when the query and the documents are in different scripts. Modules 3–5 add the first human-written Tanglish retrieval benchmark over real Tamil Nadu bilingual documents, a test of language-preference bias in a mixed index, a script-gated router and a Tanglish-validated answer-quality evaluation. *What we no longer claim:* language bias for romanised Indic queries in mixed-language indices has been shown for Hindi, Bengali, Marathi and Urdu over machine-translated parallel documents [92], and for Arabic–English bilingual corpora [91]. Our contribution is Tamil, native non-parallel documents, and lexical remedies (Section 3).

**Headline results (Module 2, verified against `main_results.csv` and `significance.csv`).**

| Finding | Number | Evidence |
|---|---|---|
| Tamil-script queries work well | MRR@10 **0.923** (char 3-gram BM25) | Table 5.4 |
| Romanised Tamil queries collapse | dense MRR@10 **0.143** (Recall@10 0.294); best raw configuration 0.178 | Table 5.4 |
| Tanglish rules + char 3-gram BM25 recover most of the loss | MRR@10 **0.058 → 0.684**, Recall@10 0.082 → 0.812; p < 0.001 (query and cluster bootstrap) | Tables 5.5, 5.6 |
| Measured from the dense baseline | **0.143 → 0.684** (dense raw vs rules + char BM25) | Tables 5.4, 5.5 |
| Rules beat the generic ITRANS scheme | 0.684 vs 0.547 (char BM25), +0.137, p < 0.001 | Table 5.6 |
| Cost of the normaliser | **0.34 ms** median per query; whole rules + char BM25 path about 5 ms on 2 CPU cores | Table 5.8 |
| Equal-weight hybrid fusion hurts across scripts | English queries on Tamil docs: dense **0.788 → 0.710** with RRF (−0.079, p < 0.001); 0.305 with a third char-3-gram list | Tables 5.4, 5.6 |
| Normalisation does not help dense retrieval of code-mixed queries | 0.687 → 0.692, p = 0.45 (cluster p = 0.57) | Table 5.6 |
| The public "code-mixed" query set is mostly English | **22.0%** of code-mixed queries have no Tamil word; 13.3% are identical to the English query | Table 5.3 |

**Scale.** 500 Tamil news documents, 2,154 queries in each of 4 forms (8 query sets after normalisation), 5 retrievers, 84 runs, 180,936 ranked lists, all on a 2-core CPU with no GPU.

**Honest note on one number.** An early run reported the fusion loss as 0.788 → 0.187. That was a bug: documents with a BM25 score of zero were fed into the fusion in index order. It was found, fixed and re-run; the corrected loss (0.788 → 0.710) is smaller but still significant, and the report keeps both numbers so the correction is visible.

**Module 2 on the English side.** On the English-translation corpus, code-mixed queries reach MRR@10 0.901 and romanised queries at best 0.557 (both Hybrid-RRF3). Romanised Tamil is hard on both halves of a bilingual base.

**What comes next (M.E.).** Module 3: about 500 human-written Tanglish questions with relevance judgements over a **bilingual collection** of long Tamil and English notices (G.O.s, scheme notices, college circulars). Each question is labelled with the language of its gold document. A **single mixed index vs per-language indices** test measures language-preference bias. A Tamil-aware chunker. Stronger baselines: IndicXlit, an LLM rewriter, translate-query-to-English (the SchemeAI-style existing system [85]), balanced per-language retrieval [91], BGE-M3, LaBSE, SONAR and the Tanglish embedder Morgan-Tanglish-v7 [86]. Module 4: a script-gated router, an LLM generator, a human-calibrated LLM judge, and a demo app. Module 5: paper, public benchmark, thesis. Target: May 2027.

**What comes after (PhD).** Four work packages: script-robust retrieval and the benchmark at scale; voice queries (Tanglish speech to RAG); trust and safety (hallucination, abstention, prompt injection in Tanglish); and on-device, low-cost deployment.

# 2. Problem statement

## 2.1 Who suffers

- **Citizens using e-governance services** in Tamil Nadu, who ask about scholarships, certificates and schemes in the way they type on WhatsApp, which is usually Tanglish.
- **Students** asking college help desks about fees, exam dates and circulars. A deployed college RAG chatbot (OneVoice [44]) already lists Tamlish among the variants it receives.
- **Farmers, patients and bank customers** whose questions reach chatbots in romanised Tamil because the phone keyboard defaults to English letters.
- **Institutions** that deploy RAG chatbots, believe them tested, and never learn that the system fails for most of the people it was built for. A Tamil Nadu college project, SchemeAI [85], already offers a "bilingual" scheme chatbot, but its index is English only and it reports no retrieval evaluation.

## 2.2 Why existing RAG fails on Tanglish

A standard RAG pipeline splits documents into chunks, embeds them, optionally adds a BM25 index, fuses the two lists with Reciprocal Rank Fusion (RRF), and passes the user's query *as typed* to the retrievers (Section 3.1 of the report). Each step has a specific failure:

1. **Lexical retrieval (BM25) sees no shared tokens.** A romanised query (*mothalukku*) and a Tamil-script document (மோதலுக்கு) share no characters. Word BM25 scores almost every document as zero.
2. **Multilingual embeddings do not map romanised Tamil to Tamil.** Models such as multilingual-E5, BGE-M3 and LaBSE are trained mainly on native-script text. Chari et al. [28] showed that multilingual dense retrievers "rapidly deteriorate" on Latinised queries in other languages, and Verma et al. [61] found that romanisation produces representations that align "with neither native-script inputs nor English".
3. **Romanisation is unstandardised.** The same word is typed *kurithu*, *kuritthu* or *kuriththu*, and Tamil's distinctions ல/ள, ன/ண/ந and த/ட are lost in Latin letters.
4. **Fusion is applied blindly.** RRF gives the near-empty lexical list the same weight as the dense list and pushes correct dense results down.
5. **Nothing is measured in Tanglish.** Every Tamil retrieval and RAG benchmark uses native-script queries [52], [53], [55], [14], so the failure stays invisible.
6. **The answer may exist only in a Tamil document.** Tamil Nadu document bases are bilingual and not parallel: a G.O. may be published only in Tamil, a circular only in English. The common fix, translating the query into English and searching English text ([84], [85], tRAG in [89]), cannot reach a Tamil-only answer.
7. **A mixed index has a language preference.** Retrievers prefer high-resource and query-language documents, and generators prefer the query language or Latin script [90]. In bilingual Arabic–English corpora, cross-lingual retrieval falls from 86–92% to 41–56% Hit@20 because the retriever ranks one language above the other [91]. Romanised Indic code-switched queries are pulled towards English evidence [92]. A Tanglish query is in Latin script like the English documents but in the language of the Tamil ones, so it is exposed to this bias.

## 2.3 Evidence from our own experiments

| Query form (same 2,154 information needs) | Best MRR@10 | Best retriever |
|---|---|---|
| Tamil script | 0.923 | char 3-gram BM25 |
| English (on Tamil documents) | 0.788 | dense (mE5-small) |
| Code-mixed (LLM-generated, mostly English) | 0.687 | dense |
| Romanised Tamil | 0.178 | BM25 + dense RRF |
| Romanised + Tanglish rules | 0.684 | char 3-gram BM25 |

*Source: Tables 5.4 and 5.5 of the report.* For 7 in 10 romanised questions, the dense retriever does not place the correct document in its top 10 (Recall@10 = 0.294).

## 2.4 Formal problem statement

> Given a **bilingual document base containing both Tamil and English documents, where the answer to a question may exist in only one language**, and a user query that may be English, Tamil script, romanised Tamil or code-mixed Tanglish, design and evaluate a retrieval front-end, index layout and retriever configuration for RAG that (a) maximises retrieval quality (Recall@k, MRR@10, nDCG@10) for every query form *and for every gold-document language*, without a systematic preference for one language, (b) keeps per-query cost within interactive limits on commodity CPU hardware, and (c) carries its gains through to faithful, correct generated answers. Build the human-written benchmark needed to measure this.

## 2.5 Research questions

- **RQ1.** How much does retrieval quality drop for romanised and code-mixed Tamil versus Tamil script or English? (Module 2)
- **RQ2.** Which retriever type (word BM25, character n-gram BM25, dense, hybrid) is most robust to each query form? (Module 2)
- **RQ3.** How much of the drop does transliteration-based normalisation recover, at what latency, and do Tanglish-specific rules beat a generic scheme? for rules and ITRANS; neural and LLM baselines (Module 3)
- **RQ4.** Does Tamil-aware chunking improve retrieval on long documents for each query form? (Module 3)
- **RQ5.** Do retrieval gains carry through to answer correctness and faithfulness, and can an LLM judge be trusted on Tanglish? (Module 4)
- **RQ6.** Does a script-gated router beat both single retrievers and blind fusion on human Tanglish queries? (Modules 3–4)
- **RQ7.** In a single mixed Tamil + English index, do retrievers show a language preference for Tanglish queries (e.g. towards Latin-script English documents), how much does it cost when the gold document is Tamil-only, and do normalisation, per-language indices, balanced retrieval [91] or query translation remove it? (Module 3)

# 3. USP and novelty versus the closest prior work

**What we do not claim.** Transliteration-based mixed-script retrieval is an established FIRE topic. Rule-based normalisation [25] and transliteration plus character n-gram indexing [20] were used there for Hindi, and we say so in the report. We also do not claim to be first to show **language bias in mixed-language retrieval**: Hira et al. [92] show English anchoring for romanised Hindi, Bengali, Marathi and Urdu code-switched queries (over machine-translated parallel documents), and Amiraz et al. [91] show cross-lingual retrieval loss and a balanced-retrieval fix for bilingual Arabic–English corpora. Nor do we claim the first Tanglish embedder [86] or the first Tamil–English IR system [84].

**What we do claim.** The intersection of three things that no surveyed work combines (report Section 2.11):

- (a) Tamil–English code-mixed and romanised queries, written by people (Module 3);
- (b) retrieval for RAG with modern dense, lexical and fusion components;
- (c) a controlled comparison of those components and of normalisation front-ends on the same information needs;
- (d) a **bilingual, non-parallel Tamil + English document base** where the answer may live in only one language, so language preference in a mixed index becomes a hard miss rather than a matter of taste (Module 3).

| Prior work | What it does | What it lacks for our problem | How ours differs |
|---|---|---|---|
| FIRE MSIR 2013–2016 [24], [20], [19]; Gupta et al. [21] | Mixed-script IR for romanised Hindi (and Bengali); transliteration, char n-grams, query expansion | Retrieval tasks never covered Tamil (Tamil only in word-level labelling); predates dense retrievers and RAG | Tamil; modern dense + lexical + fusion components; RAG framing |
| FIRE CMIR 2024–25 [9], [10] | Bengali–English code-mixed retrieval over social-media comments, with qrels | Bengali; queries and documents share the Roman script; no RAG component study | Cross-script setting (Roman queries, Tamil-script documents), where fusion behaves differently |
| Chari et al., "Lost in Transliteration" [28] | Measures the script gap of multilingual dense IR; fixes it with transliterate-train fine-tuning | No Indic language; dense only; no normaliser or fusion comparison | Tamil; compares rules, ITRANS (and in Module 3, neural and LLM normalisers) across all retriever families |
| Zeng et al., CSR-L / CS-MTEB [11] | Human-annotated code-switching retrieval benchmark; retrievers drop up to 27% | Chinese and Japanese, native script; no romanisation | Romanised Tamil; normalisation as a fix |
| Balasubramaniyam and Madushanka [14] | Query translation vs cross-lingual embeddings for Sinhala and Tamil e-gov IR; BGE-M3 Recall@15 95.6% (Tamil) | Native-script Tamil queries only | Romanised and code-mixed queries, the form citizens actually type |
| Singh [15] | Factorial parser × chunker × embedder study for Indian government RAG | English only | Same factorial rigour, applied to four query forms of Tamil |
| Sharma et al. [43]; Gaikwad and Gaikwad [42]; OneVoice [44] | Hinglish RAG: embedder comparison; normalisation + abstention; deployed college bot | Hindi or no ablation; small custom sets; no Tamil retrieval study | Tamil; paired four-form evaluation with significance and cluster bootstrap |
| Chandu et al. [13]; TanglishMedBench [57]; Indi-RomCoM [41] | Tamlish factoid QA; Tanglish medical QA; romanised Tamil instruction-following | No document collection or relevance judgements, so retrieval cannot be measured | Retrieval collection with relevance judgements (planned human set) |
| nlpctx/tamil-english-retrieval [18] | Four query forms over Tamil news, LLM-generated | No paper, no baselines; 22% of "code-mixed" queries have no Tamil | First published baselines on it; audit of its weakness; human replacement set |
| Bruch et al. [63]; Chauhan and Agarwal [64] | Fusion analysis: RRF fragile; fusion hurts 13–48% of queries | Same-script English BEIR collections only | Shows the cross-script case, where one list is near-empty, and proposes script-gated routing |
| Aksharantar/IndicXlit [22]; Dakshina [31]; Kirov et al. [32]; TAMZHI [35] | Transliteration data and models | Report character or word accuracy, never retrieval effect | Measures transliteration by what it does to retrieval and answers |
| **SchemeAI [85] — the existing system** | Tamil Nadu govt-scheme chatbot: all-MiniLM-L6-v2 + FAISS over an English CSV; language detection; Google Translate renders answers in Tamil | English-only index and English-only embedder; no Tamil documents; no romanised or code-mixed handling; no retrieval metrics | Bilingual index with Tamil-only answers; Tanglish-aware front-end; measured with qrels. Re-implemented as a Module 3 baseline |
| Thenmozhi and Aravindan [84] | Tamil→English CLIR: morphological analyser, dictionary, WSD, ontology reformulation, English web documents | Pre-neural; English target documents only; no code-mixing | Tamil *and* English documents; romanised queries; dense + lexical |
| Ranaldi et al. [89] (tRAG / MultiRAG / CrossRAG) | Translate the query, retrieve across languages, or translate retrieved documents before generation | Wikipedia; no romanised or code-mixed queries; no Tamil; commercial MT | tRAG as a Module 3 baseline, CrossRAG as a Module 4 baseline, on Tanglish over Tamil Nadu documents |
| Park and Lee [90]; Amiraz et al. [91]; Hira et al. [92] | Language preference in multilingual retrieval and RAG; balanced retrieval; English anchoring under code-switched and romanised queries | No Tamil; [92] uses parallel machine-translated documents (every answer exists in every language); [91] native script only; no lexical or normaliser remedies | Tamil; non-parallel documents with gold-language labels; normaliser + char BM25 and script-gated routing compared with balanced retrieval |
| Morgan-Tanglish-v7 [86] / TanglishSTS [87] | Tanglish sentence embedder (MiniLM-L12 fine-tune), STS Spearman 0.869 (self-reported) | Latin-script only; no retrieval test; one annotator | Tested as a Module 3 embedder baseline on cross-script retrieval |

**USP in one sentence for the viva:** *"Tamil Nadu's documents are bilingual and people ask in Tanglish. I am the first to measure what each RAG retrieval component does when Tamil is typed in English letters and the answer may sit only in a Tamil document. I show a 0.3 ms fix that lifts MRR@10 from 0.058 to 0.684 with character BM25, I show that the standard hybrid search setting quietly makes cross-script retrieval worse, and in Module 3 I test whether a mixed Tamil + English index is biased against Tamil documents for Tanglish queries."*

**Three secondary USPs.**

1. **CPU-only and reproducible.** Every experiment runs on a 2-core laptop-class CPU, which matters for colleges and district offices without GPUs.
2. **Statistical care.** Paired bootstrap tests plus a document-cluster bootstrap (queries cluster about 4.3 per document); every conclusion survives the stricter test.
3. **Transparent correction.** The fusion bug and its fix are documented, with both numbers reported.


# 4. Use cases in Tamil Nadu

The example queries below are illustrative, written for this dossier to show the typing style. They are not from the evaluation data. Module 3 will collect real ones.

**The common thread: a bilingual document base.** In every case the searchable collection holds **both Tamil and English documents, and they are not translations of each other**. The answer to a given question may exist only in Tamil (a G.O., a district notice) or only in English (a bank FAQ, a university circular). A system that translates the query into English, or keeps only English documents (as SchemeAI [85] does), silently loses the Tamil-only answers. A single mixed index may also favour one language [91], [92].

| # | Scenario (who asks) | Documents searched | Example Tanglish query | What goes wrong today | What our pipeline does |
|---|---|---|---|---|---|
| 1 | **E-governance helpdesk** (scholarships, community certificates, Government Orders) (Citizens, students) | Tamil-script G.O.s and scheme notices; English circulars | *"post matric scholarship ku last date enna?"* | Dense model misreads romanised words; BM25 finds nothing in Tamil-script G.O.s; translate-to-English pipelines never search the Tamil-only G.O. that holds the date | Language ID keeps *post matric scholarship* (English), transliterates *ku … enna*; char BM25 + dense routed by script |
| 2 | **Agricultural advisory** (Farmers) | Tamil-script crop advisories from agriculture departments | *"nel payirukku entha uram podanum?"* (which fertiliser for paddy?) | Fully romanised Tamil, the worst case (dense MRR@10 0.143 in Module 2) | Rules → Tamil script → char 3-gram BM25, which absorbs suffix and spelling variation |
| 3 | **Healthcare FAQ** (PHC timings, vaccination, scheme eligibility) (Patients, caregivers) | Tamil and English health notices and FAQs | *"sugar patient ku free test enga pannalaam?"* | Mixed English medical terms + Tamil grammar; risk of confident wrong answers | Router + abstention: answer only from retrieved evidence; say "not found" otherwise (Module 4) |
| 4 | **Banking and UPI support** (Bank customers, small traders) | English bank FAQs and Tamil help pages | *"UPI payment fail aachu, amount eppo refund aagum?"* | Mostly English query; blind hybrid fusion can push the right FAQ down | Script-gated router sends English-heavy queries to dense retrieval alone; no blind fusion |
| 5 | **Education / college help desk** (fees, exam schedule, hall tickets) (Students, parents) | College circulars (Tamil and English, non-parallel) — the planned Module 3 collection | *"semester exam hall ticket eppo varum?"* | Circulars are long, so chunking matters; Tamil words split mid-grapheme by naive chunkers | Tamil-aware chunker (sentence/clause, grapheme-safe) + router |
| 6 | **Customer care** (electricity board, telecom, e-commerce) (General public) | Tamil and English service FAQs | *"current bill online la epdi katturadhu?"* | Unstandardised spelling (*epdi / eppadi*); entities typed half-English | Char n-grams tolerate spelling; entity-safe language ID keeps names whole (Module 3) |

**Why these matter for the thesis.** Cases 1 and 5 are the Module 3 bilingual document collection (scholarship notices and G.O.s, mostly Tamil; college circulars, Tamil and English), where each question is tagged with the language of its gold document. Cases 3 and 4 motivate the Module 4 faithfulness and abstention work. Case 2 is the pure-romanised stress test. All six are PhD voice-agent candidates (Section 7).

# 5. The solution, and why each design choice

## 5.1 Pipeline at a glance

**Query path:** user query (any of 4 forms) → token-level script and language ID → Tanglish normaliser (romanised Tamil → Tamil script, English kept) → retrievers (word BM25, char 3-gram BM25, dense) → script-gated routing or fusion → top-k → LLM generator with evidence check (Module 4).
**Corpus path:** documents → chunker (whole document in Module 2; Tamil-aware in Module 3) → word index, char index, dense vectors.
**Evaluation:** Recall@k, MRR@10, nDCG@10, latency, paired and cluster bootstrap; answer-level metrics in Module 4.

## 5.2 Design choices, alternatives and reasons

| Component | Choice | Why | Alternatives considered | Why not (yet) |
|---|---|---|---|---|
| **Language ID** | Per-token: English if wordfreq Zipf ≥ 3.0 and not in a list of ~60 Tanglish particles (*ku, la, enna, pathi, panni, yaar…*) | Tanglish mixes languages *inside* one sentence, so sentence-level LID is too coarse; fast and model-free | IndicLID [33] (sentence-level romanised LID); improved romanised LID [34] | Sentence-level only. Known weakness of ours: Indian named entities (*Talaq, Rajya*) get split across scripts → entity-safe LID with a gazetteer in Module 3 (G7) |
| **Normaliser** | Tanglish rule transliterator (greedy longest match: *zh*→ழ, *th*→த, initial *n*→ந, *nn*→ன்ன, *tr*→ற்ற…) | Encodes how people actually type; 0.34 ms per query; no model; beat ITRANS on every retriever (0.684 vs 0.547 with char BM25, p < 0.001) | ITRANS (tested); IndicXlit [22]; Kirov-style contextual transliteration [32]; LLM rewriter [65]; translation to English | ITRANS is a Sanskrit-style scheme (e.g. maps *e* to long ஏ). Neural and LLM options are the Module 3 baselines; translation is tested against transliteration because [36] found transliteration better for Hindi KBQA |
| **Lexical retriever** | BM25 on character 3-grams with word boundaries (#word#) | Tamil is agglutinative (மோதல், மோதலுக்கு, மோதலில்); with no Tamil stemmer, 3-grams act as an approximate stemmer and tolerate transliteration spelling errors. 0.923 vs 0.811 for word BM25 on Tamil script | Word BM25 (kept as baseline); a Tamil stemmer/lemmatiser; phonetic-skeleton BM25 | No reliable open Tamil stemmer was used; phonetic skeleton (drop vowel signs, merge ல/ள/ழ, ன/ண/ந, த/ட) is a Module 3 extension, following a FIRE 2015 system [20] |
| **Dense retriever** | multilingual-e5-small (118M parameters, 384-d) with "query:"/"passage:" prefixes | Runs on a 2-core CPU (about 32 ms per query encoding); strong multilingual baseline [3] | BGE-M3 [4], LaBSE [5], SONAR [58], fine-tuned mE5 (transliterate-train [28]) | Larger models are slower on CPU; all are scheduled for Module 3 so the factorial covers model size and training |
| **Fusion** | RRF (k = 60) as measured baseline, with zero-score BM25 documents removed | RRF is the industry default, so it must be measured; zero-score filtering fixes the index-order bug | Tuned convex combination [63]; script-gated router; "do not fuse" [64] | Equal-weight RRF hurt cross-script queries (0.788 → 0.710). The router (Module 3–4) chooses retrievers by script and fuses only when every list is informative |
| **Chunking** | Whole document in Module 2 | News documents are short (median 326 characters), so one chunk each; varying chunking would change nothing | Fixed-size, recursive, sentence, semantic (ChunkLab [12]); proposition units [67]; Tamil-aware chunker | Module 3 uses long notices where chunking matters; fixed-size baselines stay because semantic chunking's cost "is not justified by consistent performance gains" [68] |
| **Metrics** | Recall@1/5/10, MRR@10, nDCG@10 (one relevant document per query); per-stage latency | Standard IR metrics; Recall@10 matters because the generator reads the top 10 | MAP, nDCG with graded qrels | Graded, multi-document qrels come with the human set in Module 3 |
| **Statistics** | Paired bootstrap (2,000 resamples) + bootstrap 95% CIs; document-cluster bootstrap | Every query exists in all forms, so comparisons are paired; queries cluster ~4.3 per document, so a cluster bootstrap avoids over-confident intervals | t-tests; mixed-effects models (as in [15]) | Bootstrap needs no normality assumption; mixed-effects models are a Module 5 option |
| **Hardware** | 2 vCPU, 7 GB RAM, no GPU | Reproducible on a student laptop and on the hardware a district office has | GPU cloud | Would hide the latency story and the deployment constraint |
| **Generator** (Module 4) | Candidates: Tamil-first or Indic models (Agaram 2.5B [50], Tamil-Llama [49], Sarvam-1 [51]) plus one API model as reference | Tokeniser efficiency for Tamil (Agaram: 1.55 tokens per Tamil word vs 9.44 for Qwen2.5 [50]); Agaram was trained on Tanglish | English-only LLMs | Must answer in the user's language and form; [76] needed prompt engineering for that |
| **Answer evaluation** (Module 4) | RAGAs [69] / ARES [70]-style LLM judge, calibrated on about 100 human labels | LLM judges inflate scores in low-resource, non-Latin settings [72]; agreement varies across Indic languages [73] | Uncalibrated LLM-as-judge [71]; human-only evaluation | Uncalibrated judges are untrustworthy here; human-only does not scale |

## 5.3 Why the solution works (mechanism)

- **Transliteration moves the query into the documents' script.** After rules, 29.9% of transliterated tokens appear verbatim in the corpus vocabulary, against 15.2% for ITRANS and 0% before (Table 5.2). Exact matches are still rare, so character 3-grams, which match partial words, gain most.
- **Dense models fail on romanised input because they never learned it.** RomanSetu [60] shows romanised text aligns *better* with English in an LLM continually pre-trained on it, while [61] shows near-disjoint representations in standard models. Our result fits the second case, and the transliterate-train baseline [28] tests the first.
- **Fusion hurts when one list is noise.** For English queries on Tamil documents, word BM25 matched nothing for 72% of queries and only incidental tokens (*of, tamil, sri, from, news, a*) for the rest. RRF still weights that list equally. This is the condition under which [64] predicts the largest "fusion tax".

## 5.4 Known limitations of the current solution

Synthetic (LLM-generated) queries; one relevant document per query; a small, easy 500-document corpus; one small dense model; rules written by one author (not tuned on test data); entity splitting in language ID; queries clustered by document (handled by the cluster bootstrap). Each limitation has a Module 3 or 4 fix in Section 6.

# 6. Complete module plan for the M.E. (to May 2027)

## 6.1 Overview

| Module | Title | Status | Period | Main deliverable |
|---|---|---|---|---|
| M1 | Problem, literature and design | Done | Aug–Oct 2026 | Problem statement, 77-reference survey (+[84]–[92], Nov 2026), gaps G1–G7 (+G8), architecture |
| M2 | Data and baseline retrieval | Done | Oct 2026 | 2,154 × 8 query sets × 5 retrievers, significance, latency, audit |
| M3 | Bilingual Tanglish benchmark, mixed-index bias test, chunking and normaliser baselines | Planned | Nov 2026 – Jan 2027 | ~500 human Tanglish questions with qrels and gold-language labels over Tamil + English documents; mixed-index bias analysis; Tamil-aware chunker; full factorial retrieval study |
| M4 | Script-gated router, generation and answer evaluation, demo | Planned | Feb – Mar 2027 | Router; end-to-end RAG; calibrated LLM judge; demo app |
| M5 | Paper, release and thesis | Planned | Apr – May 2027 | Paper submission; public benchmark and code; final thesis |

*Note: the Module 1–2 report placed the router inside Module 3. This plan builds and tests the router on retrieval in Module 3 and moves its end-to-end integration and demo into Module 4, so that Module 3 stays focused on data.*

## 6.2 Module 1 — Problem, literature and design

- **Objective.** Define the problem, survey the field, find a defensible gap, design the system and methodology.
- **Inputs.** Prior ChunkLab project [12]; literature search across OpenAlex, Crossref, ACL Anthology, FIRE CEUR volumes, SIGIR/ECIR.
- **Method.** Literature review (about 600 records screened to 77 verified references, citation chaining from [21], [28], [22], [13]); gap analysis; existing-vs-proposed system comparison.
- **Deliverables.** Chapters 1–4 of the report; `LITERATURE_SURVEY.md` (taxonomy, gaps G1–G7, contradictions); `RESEARCH_MAP.md` (22 groups, 15 people, venues).
- **Metrics.** Coverage of the six themes; every reference opened and checked.
- **Risks met.** Novelty overlap with FIRE MSIR was found and handled by narrowing the claim rather than overstating it.

## 6.3 Module 2 — Data and baseline retrieval

- **Objective.** Answer RQ1–RQ3 on public data.
- **Inputs.** nlpctx/tamil-english-retrieval [18]: 500 documents (seed 42) and all 2,154 queries in four forms; Tamil corpus (main) and English-translation corpus (secondary).
- **Method.** Two normalisers (ITRANS, Tanglish rules) → 8 query sets; 5 retrievers (BM25, BM25-char3, Dense-e5, Hybrid-RRF, Hybrid-RRF3); 60 main runs + 24 naive-fusion comparison runs; bootstrap CIs, paired and cluster bootstrap tests; latency on 200 queries; query-composition audit.
- **Deliverables.** Report (42 pages), slides, code with results CSVs, viva notes.
- **Results.** See the executive summary: 0.923 (Tamil script), 0.143 (romanised dense), 0.684 (rules + char BM25), 0.788 → 0.710 (RRF harm), 22% audit finding.
- **Risks met.** The zero-score fusion bug was found and fixed; all hybrid runs were re-run.

## 6.4 Module 3 — Bilingual Tanglish benchmark, mixed-index bias test, Tamil-aware chunking, normaliser and embedder baselines

- **Objective.** Replace synthetic queries with human ones (G1), make chunking matter (G6), test language-preference bias in a mixed Tamil + English index (G8), and complete the component comparison (G2, G3, G7). Answers RQ3 (fully), RQ4, RQ7 and the retrieval half of RQ6.
- **Inputs.**
  - *Documents:* a **bilingual, non-parallel collection** of long, real documents. Tamil: Tamil Nadu Government Orders and scheme notices. English: college and university circulars, scheme FAQs. All publicly available. Target: at least a third of questions answerable **only** from a Tamil document and at least a third only from an English one, recorded as a *gold-language* label (Tamil-only, English-only, both).
  - *Queries:* about 500 questions written by Tamil-speaking students in the way they normally type, collected with a short form. Each question gets its Tamil-script and English versions (written or checked by a person).
  - *Relevance judgements:* two annotators mark relevant chunks or documents; inter-annotator agreement reported.
- **Method.**
  1. **Data protocol.** Consent form; instructions that ask for natural typing, not "correct" Tamil; report the share of Tamil words and a code-mixing index per query, so the 22% problem in [18] cannot recur.
  2. **Tamil-aware chunker.** Split at Tamil sentence and clause boundaries; never inside a grapheme cluster; compare with ChunkLab's fixed-size, recursive, sentence and semantic chunkers at several sizes, plus proposition-style units [67].
  3. **Normaliser baselines.** {raw, Tanglish rules, ITRANS, IndicXlit [22], Kirov-style contextual transliteration [32] where available, LLM rewriter [65] (Tanglish → Tamil script or English), translation to English}.
     - **3b. Existing-system and translation baselines.** (i) A **SchemeAI-style** pipeline [85]: all-MiniLM-L6-v2 + FAISS, query language-detected and translated to English, English index only. (ii) **tRAG** [89]: translate the query to English, search the whole bilingual index. (iii) **Dual-query**: search with the query and its translation, merge the lists [91]. Evidence translation (CrossRAG [89]) is a Module 4 generation baseline.
     - **3c. Mixed-index bias test (new, G8).** Compare a **single mixed index** with **per-language indices** + {RRF merge, **balanced top-k/2 per language** [91], script-gated choice}. Report Recall@10 and MRR@10 *by gold language*, the share of Tamil vs English documents in the top-10, and the **language gap** (Recall on English-gold minus Recall on Tamil-gold) with a joint-coverage figure for "both" questions, following [92]. Hypothesis from Module 2: dense retrieval of romanised queries leans towards English documents (Latin script); normalisation to Tamil script should reverse it, so the router must choose the mix.
  4. **Embedders.** {mE5-small, BGE-M3 [4], LaBSE [5], SONAR [58] concept-space retriever, **Morgan-Tanglish-v7 [86]** (public Apache-2.0 Tanglish embedder, 384-d, CPU-friendly; first check whether it maps Tanglish onto Tamil-script documents at all, since it was trained only on Latin script)}, plus **transliterate-train** fine-tuning of one model on mixed native and romanised text [28] as the "learned" alternative to normalisation.
  5. **Lexical extensions.** Phonetic-skeleton BM25; entity-safe language ID (gazetteer + capitalisation + IndicLID [33], [34], [77]).
  6. **Fusion.** {none, RRF, tuned convex combination [63], script-gated router}, with a per-query "fusion tax" analysis [64].
  7. **Re-run Module 2 configurations** on the human set to test whether synthetic-data conclusions hold.
- **Deliverables.** Bilingual Tanglish benchmark v1 (queries with gold-language labels, qrels, Tamil and English documents, datasheet); chunker module; full factorial results table including the mixed-index bias analysis; Module 3 report chapter.
- **Metrics.** Recall@5/10, MRR@10, nDCG@10 (graded qrels), all broken down by gold-document language; language gap and top-10 language share; latency per stage; inter-annotator agreement (Cohen's κ); code-mixing index of the query set.
- **Risks and mitigations.**
  - *Too few volunteers* → collect in two batches through classmates and juniors; 300 is still a usable minimum.
  - *Annotation cost* → judge only the pooled top-10 of all systems (standard pooling).
  - *GPU needed for BGE-M3 or fine-tuning* → encode the corpus once on free Colab/Kaggle GPUs and cache vectors; keep querying on CPU.
  - *LLM rewriter cost* → use one small open model, cache outputs.
  - *Rules overfit to one person's spelling* → the human set is the held-out test.
  - *Too few Tamil-only answers* → choose G.O.s that have no English version (check the department's English page) before writing questions.
  - *Morgan-Tanglish-v7 is unreviewed* → treat its numbers as claims; report our own retrieval results only.
- **Timeline.** Nov 2026: protocol, consent form, document collection. Dec 2026: query collection and annotation; chunker. Jan 2027: factorial runs, write-up.
- **Status.** Planned; protocol design starts after the 2 Nov 2026 review.

## 6.5 Module 4 — Script-gated router, generation, answer evaluation and demo

- **Objective.** Turn component findings into a working system and test whether retrieval gains reach the answers (RQ5, RQ6; gaps G4, G5).
- **Inputs.** Module 3 benchmark with reference answers; best normaliser and retrievers from Module 3.
- **Method.**
  1. **Script-gated router.** Detect the query's script mix (share of English, romanised-Tamil and Tamil-script tokens) and route: Tamil script → char BM25 (+ dense); English or English-heavy code-mixed → dense alone; romanised-heavy → rules + char 3-gram BM25 (+ dense when both lists are informative). Never fuse a list with only zero scores. Variant: a small learned router or judge (the "JEV" router in the repo plan) trained on Module 3 per-query outcomes.
  2. **Generation.** One Tamil-first open model (Agaram 2.5B [50] or Tamil-Llama [49]) or Sarvam-1 [51], and one stronger reference model; prompts that answer in the user's form (Tanglish in, Tanglish or Tamil out) [76]. Compare **native-evidence** generation (Tamil and English chunks as retrieved) with **CrossRAG** [89] (retrieved chunks translated into one language before generation). [92] finds the best evidence language is not universal for Indic languages.
  3. **Answer evaluation.** Answer correctness against reference answers; faithfulness and context relevance with RAGAs [69] / ARES [70]-style judges; **judge calibration** on about 100 human-labelled answers before trusting it [72], [73]; **abstention** tests with non-relevant context, following NoMIRACL [75] and the abstention layer of [42].
  4. **Demo app.** A small web app (Streamlit, reusing ChunkLab) for a college help desk: type in any form, see the routed retrievers, retrieved chunks and the answer with sources.
- **Deliverables.** Router module; end-to-end pipeline; judge–human agreement report; demo app and short video.
- **Metrics.** Retrieval metrics per route; answer accuracy; faithfulness; judge–human agreement (κ or correlation); hallucination rate on non-relevant context; end-to-end latency on CPU.
- **Risks and mitigations.** *Generator too slow on CPU* → quantised model or a hosted API for the generation step only. *Judge disagreement with humans* → report it as a finding, and fall back to human-labelled subsets. *Router overfits to the benchmark* → rules-based router first, learned router evaluated with cross-validation.
- **Timeline.** Feb 2027: router + generation. Mar 2027: judge calibration, abstention tests, demo.
- **Status.** Planned.

## 6.6 Module 5 — Paper, public release and thesis

- **Objective.** Publish, release, defend.
- **Inputs.** Modules 1–4.
- **Method and deliverables.**
  1. **Paper.** A resource-plus-analysis paper: *the first human-written Tanglish retrieval benchmark, and what each RAG component does on it.* Target venues (from the research map, dates as checked on 31 Oct 2026): ACL Rolling Review January cycle (submission 4 Jan 2027, which needs Module 3 results early, so it is a stretch); SIGIR 2027 (abstract 14 Jan, full paper 21 Jan 2027, marked "proposed"; short/resource tracks to be announced); **DravidianLangTech 2027** (not announced yet; the 2026 pattern was a direct-submission deadline around 5 March), which is the best fit; FIRE 2027 (2026 pattern: track proposals mid-April), where a Tanglish CMIR/RAG track could be proposed.
  2. **Release.** Benchmark on Hugging Face with a datasheet and licence; code on GitHub with a one-command reproduction script.
  3. **Thesis.** Full thesis (Chapters 1–8), final viva.
- **Metrics.** Submission made; artefacts public and reproducible on CPU.
- **Risks.** *Paper rejection* → workshop fallback (DravidianLangTech, FIRE working notes). *Deadline clash with thesis writing* → write the paper from the thesis chapters, not separately.
- **Timeline.** Apr 2027: paper and release. May 2027: thesis submission and viva.
- **Status.** Planned.

## 6.7 Consolidated timeline

| Month | Work | Milestone |
|---|---|---|
| Nov 2026 | Module 2 review (2 Nov); Module 3 protocol, consent form, documents | Protocol approved by guide |
| Dec 2026 | Collect and annotate ~500 Tanglish questions; Tamil-aware chunker | Benchmark v0 |
| Jan 2027 | Normaliser and embedder factorial; chunking study | Module 3 review; optional ARR/SIGIR attempt |
| Feb 2027 | Script-gated router; generator integration | End-to-end pipeline |
| Mar 2027 | Judge calibration, abstention, demo app | Module 4 review; DravidianLangTech submission (if the call follows the 2026 pattern) |
| Apr 2027 | Paper polishing, public release | Benchmark + code public |
| May 2027 | Thesis submission and viva | M.E. complete |


# 7. PhD extension: trustworthy AI agents for code-mixed Indian languages

## 7.1 The line of research

The M.E. answers one narrow question: *can a RAG system find the right document when the question is Tanglish?* A PhD widens it to: *can an AI agent serve people who speak and type code-mixed Indian languages, correctly, safely and cheaply?* The progression is **Tanglish RAG → voice agents → safety and trust → on-device deployment**, each step reusing the benchmark, the router and the evaluation method built in the M.E.

## 7.2 Work packages

### WP1 — Script-robust retrieval and a multi-language code-mixed benchmark (Year 1)

- **Research questions.** (1) Can one retriever be trained to be robust to native, romanised and code-mixed input without a separate normaliser, and when is normalisation still worth it? (2) Do the Tamil findings transfer to Telugu, Kannada and Malayalam code-mixing?
- **Why it matters.** The M.E. fixes the problem with a front-end; a PhD should ask whether the fix belongs inside the model. Chari et al. [28] closed the script gap for non-Indic languages with transliterate-train fine-tuning; Agarwal [46] found that a normaliser became redundant after noisy-query fine-tuning and was "unstable in sign" on Tamil probes. Nobody has settled this for Dravidian retrieval.
- **Method.** Extend the M.E. benchmark to more domains and to other Dravidian languages (with DravidianLangTech collaborators); compare normaliser, transliterate-train, embedding interpolation [62] and a router; analyse representations following [61].
- **Venues.** SIGIR / ECIR resource and short tracks; ACL / EMNLP Findings; DravidianLangTech; a proposed FIRE Tanglish retrieval track.

### WP2 — Voice queries: code-switched Tamil–English speech to RAG (Year 2)

- **Research questions.** (1) How do ASR errors on code-switched Tamil–English speech propagate into retrieval and answer quality? (2) Is it better to transcribe to Tamil script, to Tanglish, or to retrieve directly from speech embeddings?
- **Why it matters.** Many of the users in Section 4 (farmers, patients, elderly citizens) prefer speaking to typing. A voice agent that mishears a code-switched word fails before retrieval starts. SONAR [58] offers text and speech encoders in one 200-language space, so a speech-to-concept retriever is testable. The survey also noted a verified Interspeech 2025 paper on Tamil–English code-switched ASR with synthetic data (Nguyen and Tran; survey §8.2), as a starting point.
- **Method.** Record spoken versions of the benchmark questions; compare cascaded ASR → normaliser → retriever with SONAR-style speech retrieval; measure error propagation per query form.
- **Venues.** Interspeech (2027 paper deadline 9 Feb 2027 per the research map, too early for this WP; target 2028), ICASSP, ACL/EMNLP.

### WP3 — Trust and safety for code-mixed agents (Year 2–3)

- **Research questions.** (1) Do hallucination, abstention failure and prompt-injection rates rise when the user writes Tanglish? (2) Can an LLM judge be calibrated to evaluate Tanglish answers reliably?
- **Why it matters.** LLM judges are biased upward in low-resource, non-Latin settings [72], human–LLM agreement varies across Indic languages [73], and code-mixed queries "challenge evaluators" in a health RAG study [74]. Many LLMs hallucinate when every retrieved passage is irrelevant [75]. Tanglish already appears in an LLM safety case study of indirect prompt injection [17], but only for one model. TanglishGuard [88] probed four chat models with 90 harmful prompts in English, Tamil and Tanglish and found a small, consistent drop for Tanglish (safety 9.9 vs 10.0), but without significance tests or retrieval. The open question is **retrieval-grounded** risk: injected instructions hidden in retrieved Tamil or English documents, and abstention on irrelevant context.
- **Method.** Build Tanglish abstention and injection test sets on top of the benchmark; calibrate judges against native-speaker labels (extending Module 4); test guardrails that are robust to script switching.
- **Venues.** ACL/EMNLP (safety and evaluation tracks), FAccT, NeurIPS Datasets and Benchmarks.

### WP4 — On-device, low-cost code-mixed agents (Year 3–4)

- **Research questions.** (1) What is the smallest pipeline (normaliser, retriever, generator) that keeps answer quality acceptable for Tanglish on a phone or a district-office CPU? (2) How much does a Tamil-efficient tokeniser save in latency and cost?
- **Why it matters.** The M.E. already shows that the strongest romanised path (rules + char BM25) needs about 5 ms on 2 CPU cores and no neural model. Tamil-first models such as Agaram 2.5B use 1.55 tokens per Tamil word against 9.44 for Qwen2.5 [50], and Sarvam-1 [51] is a 2B Indic model. Small, local agents matter for privacy (health, banking) and for places with poor connectivity.
- **Method.** Quantise and distil the Module 4 pipeline; measure quality–latency–energy trade-offs; field test with one partner (college help desk or an NGO).
- **Venues.** MobiSys / SenSys workshops, EMNLP industry or system demonstrations, COMPASS (ACM computing for development).

## 7.3 Four-year roadmap

| Year | Work packages | Outputs |
|---|---|---|
| Year 1 | WP1 benchmark extension, script-robust retriever; coursework | 1 resource paper (SIGIR/ECIR or DravidianLangTech); public multi-language benchmark |
| Year 2 | WP2 voice; start WP3 | 1 speech paper (Interspeech/ICASSP); spoken Tanglish query set |
| Year 3 | WP3 trust and safety; start WP4 | 1 main-conference paper (ACL/EMNLP); judge-calibration toolkit |
| Year 4 | WP4 on-device; integration, field study, thesis | 1 systems/demo paper; thesis |

## 7.4 Where to do it, and funding fits

These come from the funding and admissions notes made on 31 October 2026. Check each scheme's current rules before applying.

| Option | Fit | Notes |
|---|---|---|
| **PMRF** (Prime Minister's Research Fellowship) | Stated stipend target | Lateral entry route at an IIT or IISc; strongest fit if admitted to IIT Madras |
| **IndiaAI PhD Fellowship** | Strong (AI for Indian languages) | Apply in the first PhD year |
| **NFSC** (National Fellowship for Scheduled Castes) | Eligible | Requires UGC-NET JRF qualification |
| **National Overseas Scholarship** | For a PhD abroad | Income ≤ ₹8 lakh and an offer from a QS top-500 university |
| **IIT Madras PhD (Engg)** | Best local fit (AI4Bharat, Khapra, Kunchukuttan) | July 2027 window expected around late Feb – end Mar 2027; M.E. with a good record, GATE not needed |
| **Anna University PhD** | Local fallback | Supervisor approval; CFR test or GATE/NET exemption + interview |

**People to approach first** (research map): D. Thenmozhi (Shiv Nadar University Chennai), B. R. Chakravarthi (University of Galway, DravidianLangTech), A. Chari (University of Glasgow, author of [28]), S. Chanda (Bennett University, CMIR@FIRE), R. Dabre (Google; adjunct IIT Madras). A public benchmark from Module 5 is the strongest calling card for these emails.

# 8. Past resources: datasets, models, tools, benchmarks, shared tasks

## 8.1 Datasets and benchmarks

| Resource | Link / ID | What it is | How we use it | Limitation |
|---|---|---|---|---|
| nlpctx/tamil-english-retrieval [18] | huggingface.co/datasets/nlpctx/tamil-english-retrieval (Apache-2.0) | 9,299 LLM-generated query rows over 2,183 Tamil news documents; English, Tamil-script, romanised and code-mixed forms | Module 2 evaluation (500 docs, 2,154 queries) | Synthetic queries; 22% of code-mixed queries have no Tamil; no paper or baselines |
| Dakshina [31] | github.com/google-research-datasets/dakshina (CC BY-SA 4.0) | Native and Latin-script parallel sentences and romanisation lexicons, 12 South Asian languages incl. Tamil | Test data for normalisers; spelling-variation statistics | Not retrieval data |
| Aksharantar [22] | huggingface.co/datasets/ai4bharat/Aksharantar | 26M transliteration pairs, 21 Indic languages | Training data behind IndicXlit (Module 3 baseline) | Word-level pairs; accuracy-only evaluation |
| Bhasha-Abhijnaanam [33] | huggingface.co/datasets/ai4bharat/Bhasha-Abhijnaanam (CC0-1.0) | Native and romanised language-ID test set, 22 languages | Evaluate the entity-safe language ID (Module 3) | Sentence-level |
| IndicCMix [23] | huggingface.co/datasets/ai4bharat/IndicCMix (MIT) | ~104,800 Tamil rows: English, native code-mixed, Tamil, casual romanised | Source of realistic Tanglish spelling for augmentation and transliterate-train | No information needs or relevance judgements |
| IndicMSMarco / IndicRAGSuite [53] | huggingface.co/datasets/ai4bharat/IndicMSMarco (MIT) | 1,000 manually translated MS MARCO queries, 13 languages incl. Tamil | Tamil-script upper-bound condition | Native-script queries only |
| INDIC-MARCO / IndicIRSuite [52] | ACL 2024 short paper | MS MARCO machine-translated into 11 Indian languages; Indic-ColBERT | Native-script Tamil training/eval reference | Machine-translated; native script |
| MIRACL [55] | huggingface.co/datasets/miracl/miracl (Apache-2.0) | 18-language retrieval, 726k judgements | Evidence of absence (no Tamil) | No Tamil |
| TanglishSTS [87] | huggingface.co/datasets/vishnu-n/TanglishSTS (CC BY 4.0) | 325 Tanglish sentence pairs scored 0–5 by one native speaker | Sanity check for embedder behaviour on Tanglish | Not retrieval; one annotator; 46% of pairs scored 0 |
| TanglishMedBench [57] | doi 10.5281/zenodo.22308075 | 700 Tanglish medical QA pairs with English equivalents and expert labels | Module 4 generation-side check (health domain) | No document collection or qrels |
| Chandu et al. Tamlish QA [13] | doi 10.18653/v1/W18-3204 | 2,848 crowd-sourced Tamlish factoid questions | Style reference for human query collection | No retrieval collection |
| Indi-RomCoM [41]; CodeMixQA [40] | arXiv 2606.30790; arXiv 2601.07153 | Romanised code-mixed instruction and QA benchmarks (Indi-RomCoM includes Tamil) | Generator robustness context for Module 4 | No retrieval |
| DravidianCodeMix [7], [8] | github.com/bharathichezhiyan/DravidianCodeMix-Dataset | Tamil–English YouTube comments for sentiment/offensive tasks | Real Tanglish spelling statistics | Classification only |
| IndicCorp v2 [47] | ACL 2023 | 20.9B tokens, 24 languages | Source of the nlpctx documents | Pretraining text, not a benchmark |

## 8.2 Models

| Model | ID / source | Role | Limitation |
|---|---|---|---|
| multilingual-e5-small [3] | intfloat/multilingual-e5-small | Module 2 dense retriever (118M, 384-d) | Fails on romanised Tamil (MRR@10 0.143) |
| BGE-M3 [4] | BAAI/bge-m3 | Module 3 dense/sparse/multi-vector baseline | Shown to degrade on Latinised queries [28]; heavier on CPU |
| LaBSE [5] | sentence-transformers/LaBSE | Module 3 sentence-embedding baseline | Native-script training |
| SONAR [58] | Meta, arXiv 2308.11466 | Module 3 concept-space retriever; PhD WP2 speech | Romanised input untested |
| Morgan-Tanglish-v7 [86] | huggingface.co/vishnu-n/Morgan-Tanglish-v7 (Apache-2.0; 470.6 MB fp32 safetensors; downloadable, not gated) | Module 3 Tanglish embedder baseline (MiniLM-L12 fine-tune, 384-d) | Self-reported STS only; Latin-script training; no retrieval evaluation; not yet smoke-tested by us |
| IndicXlit [22] | github.com/AI4Bharat/IndicXlit (MIT) | Module 3 neural normaliser baseline | Word-level; accuracy reported, not retrieval effect |
| IndicTrans2 [48] | AI4Bharat | Translation baseline (and source of nlpctx English text) | Translation may lose Tamil-specific terms |
| Tamil-Llama [49] | abhinand/tamil-llama-7b-instruct-v0.2 | Module 4 generator candidate | 7B; heavy for CPU |
| Agaram 2.5B [50] | arXiv 2610.18420 (Apache-2.0) | Module 4 generator candidate; trained on Tamil, Tanglish, English | New (2026); limited independent evaluation |
| Sarvam-1 [51] | huggingface.co/sarvamai/sarvam-1 | Module 4 generator candidate (2B, 10 Indic languages) | Model-card claims only |

## 8.3 Tools and code

| Tool | Role in the project |
|---|---|
| ChunkLab [12] (github.com/selvin-paul-raj/chunklab) | Author's RAG playground: chunkers, BM25/dense/hybrid RRF retrievers, IR metrics. Retriever and metric design reused in Module 2; chunkers used in Module 3 |
| rank-bm25 0.2.2 | Word and character BM25 |
| sentence-transformers 6.2.0 | Dense encoding |
| indic-transliteration 2.3.82 | ITRANS baseline |
| wordfreq 3.1.1 | English-frequency language ID |
| Lost-in-Transliteration code [28] (github.com/andreaschari/transliterations) | Transliterate-train fine-tuning recipe for Module 3 |
| RAGAs [69], ARES [70] | Module 4 answer evaluation |

## 8.4 Shared tasks and venues with prior data

| Shared task | Years | Languages | Relevance |
|---|---|---|---|
| FIRE Transliterated Search / MSIR [24], [20], [19] | 2013–2016 | Hindi, Bengali, Gujarati retrieval; Tamil only in word labelling (2014–15) | Historical base; transliteration + char n-grams precedent |
| FIRE CMIR [9], [10] | 2024–2025 | Bengali–English | Closest recent code-mixed retrieval task with qrels |
| FIRE Dravidian-CodeMix [8] | 2020–2021 | Tamil, Malayalam, Kannada with English | Tanglish data, classification only |
| DravidianLangTech workshops | 2021–2026 | Dravidian languages | 2025–26 tasks cover abuse, sentiment, memes, speech; none on retrieval — an opening for a Tanglish retrieval task |


# 9. In-depth paper review

The papers below are the ones that most shape the thesis (9.1–9.15 from the 31 October survey; 9.16–9.22 added on 2 November 2026 for the bilingual framing). Facts are taken from the opened abstracts, publisher pages or PDFs recorded in the literature survey; "strengths", "weaknesses" and "relevance" are our own assessment for this project. Where a detail was not in the record we opened, the entry says so instead of guessing.

## 9.1 Chari, Ounis and MacAvaney — "Lost in Transliteration" [28], SIGIR 2025

- **Problem.** Do multilingual dense retrievers still work when the query is typed in Latin letters instead of the language's own script (Greeklish, Arabizi and similar)?
- **Method.** Measure the "script gap" between native and Latinised queries for multilingual dense retrievers including BGE-M3; then fine-tune on an even mix of native and Latinised (transliterated) queries.
- **Data.** Languages include Chinese, Russian, Arabic, Greek and Persian. No Indic language.
- **Key result.** Retrievers "rapidly deteriorate" on Latinised queries; transliterate-train fine-tuning closes most of the gap. Code released on GitHub.
- **Strengths.** Clean experimental question; neural-IR venue; open code; a fix that needs no change at query time.
- **Weaknesses (for us).** No Indic language, so Tamil's specific problems (12 vowels against 5 Roman vowels, lost consonant distinctions, heavy code-mixing with English) are untested. Dense-only: no lexical, fusion or normaliser comparison.
- **Relevance.** The closest neural-IR precedent. Our romanised collapse (0.143) is the same phenomenon, in Tamil.
- **Why it matters / gap it leaves.** It gives Module 3 its "learned" baseline (transliterate-train) to compare against our "front-end" fix. The gap: nobody has asked whether training or normalisation is better for an Indic language, or how either interacts with fusion.

## 9.2 Zeng et al. — Code-switching information retrieval: CSR-L and CS-MTEB [11], Findings of ACL 2026

- **Problem.** How do modern retrievers cope with code-switched queries?
- **Method.** Builds a human-annotated code-switching retrieval benchmark (CSR-L) and an 11-task CS-MTEB suite; tests statistical, dense and late-interaction retrievers; tries vocabulary expansion.
- **Data.** Chinese and Japanese mixed with English.
- **Key result.** Code-switching degrades every retriever family, by up to 27%; vocabulary expansion does not close the gap.
- **Strengths.** Human-annotated queries; broad retriever coverage; now peer-reviewed.
- **Weaknesses (for us).** Native scripts only, so romanisation, the main Tanglish problem, is absent. No normalisation front-end studied.
- **Relevance.** Independent support for our hypothesis that code-mixing hurts retrieval, and a model for how to build the human Tanglish set.
- **Why it matters / gap.** Our benchmark design (Module 3) should imitate its human annotation. The gap it leaves is exactly romanised, code-mixed Indic queries.

## 9.3 Gupta, Bali, Banchs, Choudhury and Rosso — "Query expansion for mixed-script IR" [21], SIGIR 2014

- **Problem.** Queries and documents in one language appear in both native and Roman script (mixed-script IR).
- **Method.** Expand queries with cross-script term equivalents learned by a deep autoencoder.
- **Data.** FIRE 2013 Hindi song-lyrics collection: 62,888 documents, 25 queries. Bing logs used to estimate that 6% of unique queries from India contained romanised Hindi words.
- **Key result.** MRR from 0.686 to 0.874.
- **Strengths.** Defined the problem formally; real query-log evidence; strong gain.
- **Weaknesses (for us).** Hindi only; 25 queries; pre-dense, pre-RAG; song lyrics are a narrow domain.
- **Relevance.** The foundational paper of our sub-field; we cite it to show we are not claiming the idea of mixed-script IR.
- **Why it matters / gap.** It proves cross-script matching was solvable for lexical IR a decade ago. Its gap: Tamil, dense retrievers, fusion and RAG. Forward chaining from it (99 citers, first 10 read) found no Tamil retrieval follow-up.
- **Bilingual-framing note (2 Nov 2026; metadata re-verified, pp. 677–686).** MSIR was defined as *one language in two scripts*, which is our Tamil-script vs romanised axis. It never covered *two languages in one index*, so the bilingual Tamil + English setting and its language-preference question go beyond the MSIR definition.

## 9.4 Sequiera et al. — Overview of FIRE 2015 Mixed Script IR [20] (with FIRE 2013 [24] and MSIR 2016 [19])

- **Problem.** A shared-task series on transliterated search: word-level language labelling, back-transliteration and ad hoc retrieval of mixed-script text.
- **Method.** Shared task with participating systems.
- **Data.** 2015: word labelling for eight languages including Tamil; retrieval only in Hindi (song lyrics, movie reviews, astrology; 25 test queries). 2016: Hindi–English tweet retrieval, best MAP only 0.0377 [19].
- **Key result.** Best NDCG@10 0.716 (2015). One 2015 system transliterated every Roman word to Devanagari and indexed character 2- to 6-grams with vowel signs removed, giving its best nDCG@10.
- **Strengths.** Real shared-task evaluation; many systems; public overviews.
- **Weaknesses (for us).** Tamil only in labelling, never in retrieval; tiny query sets; pre-dense.
- **Relevance.** Direct precedent for our transliteration + character n-gram design, and for the phonetic-skeleton idea (vowel-sign removal) planned in Module 3.
- **Why it matters / gap.** It forces honesty about novelty: our design is not new for Hindi. The gap is Tamil retrieval in this setting, with modern components.
- **MSIR 2016 detail (PDF re-opened 2 Nov 2026).** Subtask 1: code-mixed Bengali–English question classification (330 training and 180 test questions; best accuracy 83.33% against a 79.44% bag-of-words baseline). Subtask 2: Roman-script Hindi–English tweet retrieval with only **12 test queries** over 2,796 tweets; best MAP 0.0377, called "a very challenging task". Every collection was monolingual, so the series says nothing about mixed Tamil + English indices. Our ~500 human queries are a large step up from 12.

## 9.5 Chanda, Tewari and Pal — CMIR at FIRE 2025 [10] (with the 2024 overview [9])

- **Problem.** Retrieve relevant social-media content for code-mixed queries.
- **Method.** Shared task with qrels; 2024 Roman-script Bengali–English, 2025 adds native-script Bengali.
- **Data.** 2024: 50 code-mixed queries over 107,900 comments. 2025: 8 teams, 26 runs (research map).
- **Key result.** 2024 best system (GPT-3.5 Turbo based) MAP 0.70 [9]. 2025: fusion and hybrid systems "consistently outperform standalone models" [10].
- **Strengths.** The only recent code-mixed IR benchmark with relevance judgements in India; active community.
- **Weaknesses (for us).** Bengali; queries and documents mostly share the Roman script; no RAG component study.
- **Relevance.** The apparent contradiction with our result (fusion hurts). Reconciliation: in CMIR both lists carry signal because scripts match; in our cross-script setting the lexical list is nearly empty.
- **Why it matters / gap.** It is the natural home for a Tanglish track. The gap: cross-script Dravidian retrieval, and a statement of *when* fusion helps.

## 9.6 Chauhan and Agarwal — "The fusion tax" [64], IEEE Access 2026 (with Bruch et al. [63], TOIS 2023)

- **Problem.** When does hybrid retrieval hurt?
- **Method.** Per-query diagnostics on seven BEIR collections with five dense encoders, SPLADE and three fusion functions; "do not fuse" treated as a valid outcome. Bruch et al. compare RRF with a tuned convex combination of normalised scores.
- **Key result.** Even the best fusion ranks relevant documents below the better single component on 13–48% of queries; RRF taxes most where the dense retriever is clearly stronger [64]. RRF is parameter-sensitive and a tuned convex combination beats it in and out of domain with few training examples [63].
- **Strengths.** Query-level analysis rather than averages; several encoders; practical guidance.
- **Weaknesses (for us).** English, same-script collections only.
- **Relevance.** Explains our 0.788 → 0.710 result: dense is far stronger than BM25 across scripts, which is the condition [64] predicts.
- **Why it matters / gap.** Supports the script-gated router and convex fusion as Module 3–4 conditions. Gap: the cross-script condition, where one list carries almost no signal.

## 9.7 Verma, Chatterjee, Gupta and Chakraborty — "Multilingual LMs encode script over linguistic structure" [61], ACL 2026

- **Problem.** Are language-associated units in multilingual LMs tied to the language or to its script?
- **Method.** Language-associated neuron analysis (LAPE) and sparse autoencoders.
- **Key result.** "Romanization induces near-disjoint representations that align with neither native-script inputs nor English."
- **Strengths.** Mechanistic evidence; top venue.
- **Weaknesses (for us).** Analysis of LMs, not retrievers; no retrieval metric.
- **Relevance.** The most likely mechanism for our romanised collapse in dense retrieval.
- **Why it matters / gap.** Lets the thesis explain *why* the dense model fails, not just that it fails. Gap: linking representation geometry to retrieval quality for Tamil, a natural PhD WP1 analysis.

## 9.8 Madhani et al. — Aksharantar and IndicXlit [22], Findings of EMNLP 2023 (with Kirov et al. [32] and Dakshina [31])

- **Problem.** Open transliteration data and models for Indic languages.
- **Method.** Mine and collect 26M word pairs across 21 Indic languages; train the IndicXlit transformer. Kirov et al. add sentence-level, context-aware Latin-to-native transliteration on the 12 Dakshina languages (Tamil included).
- **Key result.** Large open resource and model (Aksharantar); "substantial" gains for full-sentence transliteration on all twelve Dakshina languages [32].
- **Strengths.** Open, large, covers Tamil; Dakshina gives attested romanisation lexicons.
- **Weaknesses (for us).** Evaluated by character or word accuracy only; never by its effect on retrieval or answers.
- **Relevance.** The neural normaliser baselines for Module 3.
- **Why it matters / gap.** If IndicXlit beats our 0.34 ms rules on retrieval, we report it; if not, that is a finding about accuracy vs downstream usefulness. Gap G3: no one measures transliteration by retrieval effect.

## 9.9 Agarwal — "Where does noise robustness live?" [46], W-NUT 2026

- **Problem.** In code-mixed NLU, does a normaliser, a rule layer or an LLM arbiter provide robustness?
- **Method.** Factorial ablation with role swaps and cross-lingual transfer in a Hinglish banking NLU pipeline, plus native-reviewed Tamil and Telugu probes.
- **Key result.** A hand-built normaliser helped a base encoder but became redundant after noisy-query fine-tuning; on Tamil and Telugu probes its effect was "unstable in sign".
- **Strengths.** Rigorous factorial design; includes Tamil probes; reports a negative result.
- **Weaknesses (for us).** NLU (intent classification), not retrieval; Tamil only as probes.
- **Relevance.** The main counter-evidence the thesis must answer. It agrees with our finding that normalisation does not help dense retrieval of code-mixed queries (p = 0.45).
- **Why it matters / gap.** Module 3 must test normalisation *together with* fine-tuning, not only against a frozen encoder. Gap: the same question for retrieval.

## 9.10 Balasubramaniyam and Madushanka — Sinhala–Tamil e-government IR [14], arXiv 2026

- **Problem.** For Sinhala and Tamil questions over English e-government content, is query translation or cross-lingual embedding better?
- **Method.** Compare translation with LaBSE, multilingual-E5 and BGE-M3.
- **Data.** 500 human-verified question–answer pairs.
- **Key result.** BGE-M3 reached Recall@15 of 95.6% for Tamil–English.
- **Strengths.** Real e-government domain; human-verified pairs; compares translation with embeddings.
- **Weaknesses (for us).** Tamil queries in native script only; preprint.
- **Relevance.** The closest Tamil retrieval study in our use-case domain (Section 4, case 1).
- **Why it matters / gap.** It shows Tamil-script queries are largely solved by BGE-M3; our results show the romanised form is not. Gap: the form citizens actually type.

## 9.11 Singh — Parser, chunking and embedding interactions in RAG over Indian government regulatory documents [15], arXiv 2026

- **Problem.** How do RAG components interact on real Indian government documents?
- **Method.** Controlled factorial study: 3 parsers × 3 chunking strategies × 5 dense embedders, plus BM25; mixed-effects models and bootstrap intervals.
- **Data.** 800 questions over Indian government regulatory documents.
- **Key result.** Components interact, so they should not be tuned one at a time.
- **Strengths.** Methodological rigour; Indian institutional documents.
- **Weaknesses (for us).** English only.
- **Relevance.** Our methodological model: the Module 3 factorial copies its design and adds query form as a factor.
- **Why it matters / gap.** Shows that factorial RAG studies are publishable. Gap: query language and script as a factor.

## 9.12 Sharma, Rathee, Mishra and Bhatt — Multilingual embedders for explainable Hinglish retrieval in RAG [43], ICAICS 2025 (Springer LNNS 2026)

- **Problem.** Retrieve English documents for informal Hinglish queries in RAG.
- **Method.** Compare zero-shot multilingual embedders with a fine-tuned one.
- **Data.** A custom Hinglish task (size not given in the record we opened).
- **Key result.** Fine-tuned embedder 96.3% accuracy on the strict task against 76.7% for the best zero-shot model.
- **Strengths.** Code-mixed RAG retrieval directly; shows the value of fine-tuning.
- **Weaknesses (for us).** Hindi; small custom task; embedders only (no lexical, normaliser or fusion study).
- **Relevance.** The Hinglish study a Tanglish thesis is compared against. Together with Gaikwad and Gaikwad [42] (normalisation + abstention, fewer hallucinations for Hinglish), it shows code-mixed RAG is an active 2026 topic.
- **Why it matters / gap.** The 20-point zero-shot gap supports the transliterate-train condition. Gap: Tamil, and a component-level comparison.

## 9.13 Prasanjith, More, Kunchukuttan and Dabre — IndicRAGSuite [53], arXiv 2025 (with IndicIRSuite [52], ACL 2024)

- **Problem.** No benchmark for RAG in Indian languages.
- **Method.** IndicMSMarco: 1,000 manually translated MS MARCO queries in 13 languages; Wikipedia-based QA training tuples. IndicIRSuite: MS MARCO machine-translated into 11 languages, with Indic-ColBERT.
- **Key result.** First Indic RAG retrieval-and-generation benchmark [53]; Indic-ColBERT +47.47% MRR@10 over INDIC-MARCO baselines [52].
- **Strengths.** Covers Tamil; from AI4Bharat; open data.
- **Weaknesses (for us).** Native-script queries only; translated rather than naturally written.
- **Relevance.** Provides the Tamil-script upper-bound condition and evidence that every Tamil RAG benchmark is native-script.
- **Why it matters / gap.** The strongest evidence for gap G1: even the leading Indic RAG benchmark has no romanised queries.

## 9.14 Hada et al. — Are LLM-based evaluators the solution to scaling multilingual evaluation? [72], Findings of EACL 2024 (with PARIKSHA [73])

- **Problem.** Can LLMs replace human judges outside English?
- **Method.** LLM evaluators calibrated against 20K human judgements in 8 languages. PARIKSHA: 90,000 human and 30,000 LLM evaluations across 10 Indic languages.
- **Key result.** LLM evaluators are biased towards higher scores, especially in low-resource and non-Latin-script languages, and need calibration [72]; human–LLM agreement varies [73].
- **Strengths.** Large human baselines; Indic coverage.
- **Weaknesses (for us).** No code-mixed or romanised queries.
- **Relevance.** Module 4 cannot trust an uncalibrated judge on Tanglish.
- **Why it matters / gap.** It defines the Module 4 calibration step (about 100 human labels). Gap G5: no judge has been validated on Tanglish.

## 9.15 nlpctx — tamil-english-retrieval dataset [18], Hugging Face 2026 (with TanglishMedBench [57] and Chandu et al. [13])

- **Problem.** No Tamil–English code-mixed retrieval evaluation data.
- **Method.** LLM-generated queries in four forms over Tamil documents from the Mozhi corpus (IndicCorpV2 news), with IndicTrans2 English translations.
- **Data.** 9,299 query rows over 2,183 documents; Apache-2.0.
- **Key result.** No paper or baselines; Module 2 provides the first baselines on it.
- **Strengths.** Parallel four-form queries make paired comparisons possible.
- **Weaknesses.** Synthetic queries; our audit found 22.0% of "code-mixed" queries have no Tamil word and 13.3% equal the English query. TanglishMedBench (700 Tanglish medical QA pairs) and Chandu et al. (2,848 Tamlish questions) are human-written but lack a retrieval collection or qrels.
- **Relevance.** Our Module 2 data, and the clearest evidence for why Module 3 must collect human queries.
- **Why it matters / gap.** Together, these three resources show the exact hole G1 fills: human Tanglish queries *and* a retrieval collection *and* relevance judgements.

## 9.16 Rekha et al. — SchemeAI, a Tamil Nadu bilingual scheme RAG chatbot [85], IJARSCT 2026 (the "existing system")

- **Problem.** Citizens can't easily find the government schemes they qualify for, because portals are scattered and there is a language barrier for Tamil speakers.
- **Method.** A Flask web chatbot. The user picks a state and a category, then types a question. The question is embedded with **all-MiniLM-L6-v2** (Sentence-BERT) and matched against a **FAISS** index built from a structured CSV of central and state schemes (`updated_data.csv`: Agriculture, Education, Housing; Tamil Nadu, Telangana, Puducherry). A language-detection step plus the **GoogleTranslator API** "dynamically translates English scheme details into Tamil" for display. An "Intelligence Explanation" page shows the pipeline (called XAI in the paper).
- **Data.** One English CSV. The paper doesn't give its size, and there is no test set.
- **Results.** Screenshots of one English and one Tamil question, plus an "accuracy comparison" graph and a "response time" graph. The text gives no numbers, metric definitions or evaluation protocol.
- **Strengths.** It addresses exactly our use case 1 (Tamil Nadu scheme help desk), shows that Tamil Nadu colleges are building bilingual RAG, and uses a cheap CPU stack.
- **Weaknesses.** (1) The knowledge base is English only, so there are no Tamil documents. (2) all-MiniLM-L6-v2 is an English-trained embedder, and the paper doesn't say whether Tamil queries are translated before they are embedded. (3) Translation only touches the output. (4) There is no handling of romanised or code-mixed input. A Tanglish query is in Latin letters, so a language detector will probably label it English and pass it straight to an English embedder. This is our inference and isn't tested in the paper. (5) There is no retrieval evaluation. (6) Editorial problems: the in-text literature survey cites authors who don't match the reference list. The venue is a low-selectivity journal.
- **Relevance.** This is the **"existing system"** in our existing-vs-proposed comparison: a translate-around-an-English-index design typical of local deployments.
- **Why it matters.** It shows what a Tamil Nadu bilingual RAG looks like in practice today, and why it can't be judged: nothing is measured. Module 3 re-implements a SchemeAI-style baseline (MiniLM + FAISS, query translated to English) on the bilingual benchmark.
- **Gap it leaves.** No Tamil-language documents, so an answer that exists only in a Tamil G.O. is unreachable. No romanised or code-mixed queries. No retrieval or answer metrics.

## 9.17 Vishnu N — Morgan-Tanglish-v7 embeddings [86] and TanglishSTS [87], Zenodo / Hugging Face 2026

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

## 9.18 Thenmozhi and Aravindan — Ontology-based Tamil–English CLIR [84], Sādhanā 2018

- **Problem.** Tamil users querying English content. Query ambiguity hurts translation-based cross-lingual IR.
- **Method.** A Tamil morphological analyser, a Tamil-English bilingual dictionary and a named-entity database translate the Tamil query into English, with word-sense disambiguation. An automatically built English domain ontology then reformulates the translated query, and a web search engine retrieves English documents.
- **Data / results.** Agriculture domain. The abstract says it "outperforms other approaches in terms of precision"; numbers sit behind the paywall and weren't seen. The appendix tables show example queries in romanised form ("Mutkalappai", "Uzhudhal Upakaranangkal"). Whether users typed them that way or the authors transliterated them for display can't be confirmed without the full text.
- **Strengths.** The closest peer-reviewed Tamil–English IR work. It is from Chennai (a possible local reviewer or collaborator, D. Thenmozhi) and builds real Tamil language resources.
- **Weaknesses.** Pre-neural, with English-only target documents. Submitted in 2014 and published in 2018. No code-mixing.
- **Relevance / why it matters.** It is the classic **translate-the-query-to-English** design, the same family as the SchemeAI baseline. Our bilingual framing explains its blind spot: when the answer exists only in a Tamil document, translating into English searches the wrong half of the collection.
- **Gap it leaves.** No Tamil-language documents in the index, no romanised or code-mixed queries, no dense retrieval or RAG.

## 9.19 Ranaldi, Haddow and Birch — Multilingual RAG: tRAG, MultiRAG and CrossRAG [89], Findings of EACL 2026

- **Problem.** How should RAG work when queries and knowledge are not in English?
- **Method.** Four pipelines compared. **monoRAG** retrieves in the query language only. **tRAG** translates the question into English and then retrieves. **MultiRAG** retrieves directly across many languages. **CrossRAG** retrieves across languages, then **translates the retrieved documents into one language (English)** before generating. Retrieval uses Cohere Embed v3 over a Wikipedia dump; translation uses Google Translate (and GPT-4o as a variant); the generators are GPT-4o, Llama-3-8B and Command-R-35B.
- **Data.** MKQA, MLQA and XOR TyDi QA. The PDF mentions Hindi and Bengali; Tamil isn't mentioned.
- **Results (as stated in the abstract and §4).** tRAG "suffers from limited coverage"; MultiRAG beats monoRAG and tRAG but brings inconsistency across languages; CrossRAG "significantly enhances performance", for both high- and low-resource languages.
- **Strengths.** A clean taxonomy of strategies, a published venue, three generators.
- **Weaknesses.** Wikipedia-based, so models may already know the answers (the critique in [91]). No code-mixed or romanised queries. It depends on a commercial translation API, which raises cost and privacy issues for government documents. The study is mostly about generation. A later paper [92] finds translating into English is "not universal", especially for Indic-script languages. (Note: [92] cites arXiv:2504.03616 with a different author list; [91] and the ACL Anthology give Ranaldi, Haddow and Birch, which we use.)
- **Relevance.** It supplies two baselines. **tRAG** (translate the Tanglish query to English, then retrieve) goes in Module 3. **CrossRAG** (translate retrieved Tamil chunks before generation) goes in Module 4.
- **Why it matters.** For a bilingual Tamil+English base, the key choice is what you translate: the query or the evidence. This paper is the reference point for that choice.
- **Gap it leaves.** No romanised or code-mixed queries, no Tamil, no domain-specific bilingual collection.

## 9.20 Chirkova et al. — Retrieval-augmented generation in multilingual settings [76], KnowLLM 2024

- **Problem.** A strong, reproducible baseline pipeline for multilingual RAG (mRAG).
- **Method / data.** User queries and a datastore in 13 languages, built on the BERGEN toolkit (github.com/naver/bergen). The abstract doesn't list the 13 languages, and we didn't check whether Tamil is one of them.
- **Results.** Off-the-shelf multilingual retrievers and generators are adequate, but **task-specific prompting is needed so the model answers in the user's language**. Metrics need adjusting for **named entities spelled differently**. Remaining failures: code-switching in non-Latin outputs, fluency errors, misreading documents, irrelevant retrieval.
- **Strengths.** Open code and a careful list of failure modes.
- **Weaknesses.** Wikipedia-style data; no romanised or code-mixed queries.
- **Relevance / why it matters.** Two Module 4 design inputs: a prompt that answers in the user's form (Tanglish in, Tanglish or Tamil out), and entity-tolerant answer matching. Tamil names have many Latin spellings.
- **Gap it leaves.** Code-mixed and romanised input, and domain-specific bilingual collections.

## 9.21 Language preference in multilingual retrieval and RAG — Park and Lee [90], Amiraz et al. [91], Hira, Mire and Sap [92]

- **[90] Park and Lee, "Investigating language preference of multilingual RAG systems", Findings of ACL 2025.**
  - *Finding (abstract):* retrievers "prefer high-resource and query languages", but this preference doesn't consistently improve generation. **Generators prefer the query language or Latin scripts.** Fix: DKM-RAG, which fuses translated multilingual passages with the model's own knowledge.
  - *Why it matters for us:* a romanised Tanglish query is in Latin script, so both the retriever and the generator may lean towards English (Latin) evidence over Tamil-script evidence.

- **[91] Amiraz et al., "The cross-lingual cost: Retrieval biases in RAG over Arabic-English corpora", ArabicNLP 2025.** *This is the closest design to our Module 3.*
  - *Setup:* two UAE bilingual corpora (Legal: 390 laws; Travel: Ministry of Foreign Affairs pages). Each document is placed in **exactly one language at random**. Queries are 50/50 Arabic and English, and **each answer exists in one language only**. BGE-M3 or mE5-large, a bge-reranker-v2-m3, and a Qwen2.5-14B generator.
  - *Results:* retrieval is the bottleneck. Cross-lingual pairs drop sharply. Example: BGE-M3 on Legal gets Hit@20 of 56% for English queries on Arabic documents, against 86–92% when query and document share a language; mE5 drops from 88% (same language) to 46% (cross-language). A language-oracle shows the failure comes from **ranking documents of two languages against each other**, not from query–document mismatch. Two fixes, **balanced retrieval** (top-10 from each language) and **query translation with merged lists**, remove most of the cross-lingual loss with no same-language cost. The balanced fix costs nothing extra.
  - *Weaknesses:* synthetic (DataMorgana) questions from parallel source documents, LLM-judged relevance, native script only.
  - *Why it matters:* it gives us the experimental template (non-parallel bilingual index, answer in one language, per-cell analysis), and **balanced per-language retrieval becomes a required Module 3 baseline**. Our new element: a Tanglish query matches English documents by **script** but Tamil documents by **language**, so the bias may pull it the wrong way.

- **[92] Hira, Mire and Sap, "The language of evidence: Robustness and bias in code-switched RAG", EMNLP 2026.** *The paper most threatening to our novelty claim.*
  - *Setup:* CodeMixQA questions (English+X code-switched). The English source pages were **machine-translated into 11 languages** (bn, es, fr, hi, id, it, ja, ko, mr, ur, zh) and all 12 versions pooled into one index, so every answer exists in every language. Retrievers: mE5, LaBSE, mContriever, distiluse, bge-large-en. New metrics: LARS, language gap, joint bilingual coverage. Romanised query variants for Hindi, Bengali, Marathi and Urdu.
  - *Results:* the strongest retrievers show **English anchoring**. **Indic-script queries show the largest English bias.** **Romanisation increases English concentration** in the top-k. Language-targeted contrastive training over-corrects: joint coverage collapses (English recall about 0.003). In RAG, English evidence helps Bengali, Hindi and Urdu, while native evidence helps Japanese, Korean, Marathi and Chinese; transliteration amplifies the English preference (Hindi transliterated: 3.98 with English evidence vs 3.38 with native). The authors recommend bilingual retrieval.
  - *Weaknesses:* parallel, machine-translated corpus (the "answer exists only in one language" case is never tested); no Tamil; dense retrievers only, with no lexical or character n-gram retrieval and no normaliser; an LLM judge (κ = 0.68 against humans on 260 samples).
  - *Why it matters:* it already shows, for other Indic languages, that romanised code-mixed queries over a mixed-language index lean towards English. **We can no longer claim to be first to show language bias for romanised Indic code-mixed queries in mixed-index RAG.** Our claim narrows to: Tamil (absent from [90]–[92]); **native, non-parallel bilingual government documents where the answer exists in only one language**, so English anchoring becomes a hard miss, not just a preference; and **model-free lexical remedies** (Tanglish normaliser + char 3-gram BM25, script-gated routing, balanced retrieval) evaluated on CPU.

- **Seen but not added:** Wang et al., "All languages matter: Understanding and mitigating language bias in multilingual RAG" (ACL 2026, pp. 7441–7455, doi 10.18653/v1/2026.acl-long.338; reranking bias towards English and the query language; Crossref metadata checked, abstract seen only in search). Sharma et al., "Faux Polyglot" (NAACL 2025). Ki et al., "Linguistic nepotism" (2026). Park et al., "Debiased language preference-guided query fusion" (Findings of ACL 2026). Candidates for a later pass.

## 9.22 Vijesh and Gothai — TanglishGuard [88], IJISRT 2026 (PhD WP3)

- **Problem.** LLM safety is tested almost only in English. Is it also robust to Tanglish?
- **Method / data.** 90 harmful prompts (9 categories × 10), each written in English, Tamil and Tanglish. Four chat models (ChatGPT, Gemini, Claude, DeepSeek), 3 runs each. Scored on refusal (binary), cross-language consistency (1–10) and explanation quality (1–5).
- **Results.** Every model refuses more than 95% of prompts. English and Tamil score 10/10 on safety; Tanglish scores 9.9 (DeepSeek 9.8). The authors call this "subtle but consistent".
- **Strengths.** The first Tanglish-specific safety probe, and a clear trilingual design.
- **Weaknesses.** The effect is 0.1–0.2 on a 10-point scale with no significance test. The sample is small and the prompts' release status is unclear. Some references in the paper carry placeholder arXiv IDs ("2603.xxxxx"). The venue is of concern. It does no retrieval: prompts are sent to chat models directly.
- **Relevance.** PhD WP3 (trust and safety): evidence that the question is being asked locally.
- **Why it matters.** It strengthens the WP3 motivation, but it is not strong evidence of a safety gap. WP3 should test **retrieval-grounded** risks (prompt injection hidden in retrieved Tamil or English documents, abstention on irrelevant context), with significance tests.
- **Gap it leaves.** No RAG, no indirect injection, no statistics.

## 9.23 Remaining references, grouped by theme

| Theme | References | What they give the thesis |
|---|---|---|
| RAG and retrieval foundations | [1] Lewis et al. (RAG); [2] Robertson and Zaragoza (BM25); [6] Cormack et al. (RRF, k = 60) | Definitions of the pipeline and the fusion baseline |
| Multilingual embeddings | [3] mE5; [4] BGE-M3; [5] LaBSE; [58] SONAR; [59] Large Concept Models | Dense retrievers tested now and in Module 3 |
| Romanisation and representations | [60] RomanSetu (romanised text aligns better with English after continual pre-training); [62] Zhu et al. (query embedding interpolation beats best single language in 88/105 cases) | Counterpoint to [61]; interpolation as a PhD WP1 idea |
| Mixed-script IR (FIRE era) | [24] FIRE 2013; [19] MSIR 2016; [25] Ganguly et al. (rule normalisation, ~56% over LM baseline); [26] Chakma and Das (CMIR tweet corpus); [27] Riyadh and Kondrak (joint deromanisation) | Prior art for rule-based normalisation |
| Code-mixed IR participants | [29] Deroy and Maity (RetrieveGPT); [30] Mishra et al. (BM25 + SBERT, +83% over BM25) | Same-script fusion evidence |
| Transliteration and LID | [31] Dakshina; [32] Kirov et al.; [33] IndicLID; [34] Benton et al. (romanised F1 74.7 → 88.2); [35] TAMZHI (vowel-dropped Tamil); [77] Fetahu et al. (gazetteer NER, F1 68%) | Normaliser baselines and entity-safe LID |
| Code-mixed QA and LLMs | [13] Chandu et al.; [36] Gupta et al. (transliteration beats translation by 5% / 35%); [37] GLUECoS; [38] Winata et al. survey; [39] Zhang et al. (LLMs are not yet code-switchers); [40] CodeMixQA; [41] Indi-RomCoM | LLM behaviour on code-mixed input; transliterate-vs-translate evidence |
| Code-mixed RAG | [42] Gaikwad and Gaikwad; [44] OneVoice; [45] Adoptante et al. (Tagalog–English RAG) | Comparable 2025–26 systems |
| Tamil and Indic resources | [7], [8] Dravidian code-mix sentiment; [23] IndicCMix; [47] IndicCorp v2; [48] IndicTrans2; [49] Tamil-Llama; [50] Agaram 2.5B; [51] Sarvam-1; [54] Indic-QA (Translate-Test wins in low-resource QA); [55] MIRACL (no Tamil); [56] MURMUR (Tamil multimodal RAG, 38.1 accuracy) | Data, generators and evidence of the native-script bias |
| Query rewriting | [65] Rewrite-Retrieve-Read; [66] HyDE | LLM rewriter baseline design |
| Chunking | [16] Chhoun et al. (Khmer; 300-char recursive best, 18 QA pairs); [67] Dense X (propositions); [68] Qu et al. (semantic chunking not worth its cost) | Module 3 chunking design |
| RAG and LLM evaluation | [69] RAGAs; [70] ARES; [71] LLM-as-a-judge (>80% GPT-4 agreement, with biases); [73] PARIKSHA; [74] HEALTH-PARIKSHA; [75] NoMIRACL; [76] Chirkova et al. (mRAG in 13 languages) | Module 4 evaluation and abstention |
| Safety | [17] Madhusudhanan G. (prompt injection across English, Tamil, Tanglish; one model) | PhD WP3 starting point |
| Author's prior work | [12] ChunkLab | Code base reused |

# 10. Research gaps G1–G8 mapped to modules

| Gap | Description | Strength of evidence | Module 3 | Module 4 | Module 5 | PhD |
|---|---|---|---|---|---|---|
| **G1** | No retrieval benchmark with human-written romanised or code-mixed Tamil queries and relevance judgements | **HIGH** | Collect ~500 human Tanglish questions with qrels over long Tamil notices; report code-mixing index per query | Reuse with reference answers | Release as the first Tanglish retrieval benchmark | WP1: extend to more domains and Dravidian languages |
| **G2** | No controlled comparison of RAG retrieval components for romanised and code-mixed Tamil | **HIGH** (Module 2 gives first baselines) | Full factorial: normalisers × embedders × fusion | Do component wins reach answers? | Main results table | WP1 |
| **G3** | Normalisation front-ends (rules, IndicXlit, contextual transliteration, LLM rewrite, translation) never compared by retrieval effect | MEDIUM | Add all baselines + transliterate-train; report latency | Effect on faithfulness | Ablation; address [46] head-on | WP1 (learned vs front-end) |
| **G4** | Fusion when one retriever is near-uninformative because of script mismatch; script-gated routing | MEDIUM | Router vs RRF vs convex; per-query fusion tax | Router in the end-to-end system | Analysis section; reconcile with [10] | WP4 (cheap routing on device) |
| **G5** | Generation-side evaluation and LLM-judge validity for Tanglish | MEDIUM | — | RAGAs/ARES with judge calibrated on ~100 human labels; abstention tests | Report judge–human agreement | WP3 |
| **G6** | Tamil-aware chunking (sentence/clause, grapheme-safe) for RAG | MEDIUM | Tamil-aware chunker vs fixed, recursive, semantic, proposition units | Context-length effects on answers | — | — |
| **G7** | Entity-safe token-level language ID for romanised Tamil in a retrieval router | LOW | Gazetteer + IndicLID for entity-safe tagging | Used inside the router | — | WP2 (ASR output tagging) |
| **G8** (new, 2 Nov 2026) | Language-preference bias for Tanglish queries in a **mixed, non-parallel Tamil + English index** where the answer exists in only one language; remedies never compared (normaliser + char BM25, script-gated routing, balanced per-language retrieval, query translation, evidence translation) | **MEDIUM**: shown for Arabic–English [91] and romanised Hindi/Bengali/Marathi/Urdu over parallel documents [92]; none for Tamil or non-parallel Indic documents; one search pass only | Single vs per-language indices; per-gold-language Recall; language gap; balanced, tRAG, dual-query and SchemeAI-style baselines | Router picks the language mix; native-evidence vs CrossRAG generation [89] | Bias analysis section of the paper | WP1: other Indic pairs (Hinglish, Manglish, Telugu–English) |

*Gap strengths follow the literature survey: G3–G6 are MEDIUM partly because regional Springer and IEEE proceedings were not searched exhaustively. G8 is MEDIUM because [92] appeared in October 2026 and close preprints may exist; re-check before submission.*


# 11. Likely viva questions with model answers

**1. In one sentence, what is your project?**
I measure what happens to each part of a RAG search pipeline when Tamil questions are typed in English letters, and I build cheap fixes and a human-written benchmark for it.

**2. What exactly is new?**
No prior study evaluates RAG retrieval components (dense, lexical, fusion) and query normalisation for romanised and code-mixed Tamil–English queries. Mixed-script IR existed at FIRE, but for Hindi and Bengali, before dense retrievers and RAG; I say that openly. My additions are the first component-level baselines for Tamil, the cross-script fusion finding, the dataset audit, and (Module 3) the first human Tanglish retrieval benchmark.

**3. Why does romanised Tamil fail so badly?**
BM25 has no shared characters with Tamil-script documents, and the embedding model was trained mostly on native-script text, so it splits romanised words into English-like pieces with no link to Tamil. Verma et al. [61] found that romanisation gives representations aligned with neither the native script nor English. Dense MRR@10 is 0.143; Recall@10 is 0.294.

**4. Why write your own rules instead of using a tool?**
I did use a tool, ITRANS, as a baseline. It is a Sanskrit-style scheme and gets Tanglish habits wrong. My rules encode how people type (*zh*→ழ, *nn*→ன்ன, *tr*→ற்ற). They beat ITRANS on every retriever (0.684 vs 0.547 with char BM25, p < 0.001) at 0.34 ms per query. IndicXlit and an LLM rewriter are the Module 3 baselines.

**5. Did you tune the rules on the test set?**
No. They were written from Tamil spelling knowledge before the evaluation was run. They reflect one author's view, so the human-written Module 3 set is the real held-out test.

**6. Why does character 3-gram BM25 beat word BM25 even on Tamil script (0.923 vs 0.811)?**
Tamil is agglutinative: மோதல், மோதலுக்கு, மோதலில் are one stem with different suffixes. Without a stemmer, word BM25 treats them as different words. Character 3-grams share the stem's pieces, so they work like a rough stemmer, and they also tolerate transliteration spelling errors.

**7. Everyone recommends hybrid search. Why does it hurt here?**
RRF gives every list equal weight. For English queries on Tamil documents, word BM25 matched nothing for 72% of queries and only stray words like "of" or "news" for the rest, yet RRF still trusted it and pushed the correct dense result down: 0.788 → 0.710 (p < 0.001, also under the cluster bootstrap). This matches the "fusion tax" result [64]: fusion costs most when one retriever is clearly stronger. Fusion does help when BM25 has real signal (raw romanised: 0.143 → 0.178).

**8. Tell us about the bug.**
My first run fed documents with a BM25 score of zero into RRF. Sorting zero scores just lists documents in index order, which RRF rewarded, so the loss looked like 0.788 → 0.187. I found it, filtered zero-score documents, re-ran every hybrid configuration and kept the old numbers labelled "naive". The corrected loss is smaller but still significant. Lesson: unit-test fusion inputs.

**9. Your queries are LLM-generated. Why should we believe the results?**
That is the main limitation, and I measured it: 22% of the "code-mixed" queries have no Tamil word and 13.3% equal the English query. So my code-mixed results mostly measure English-to-Tamil retrieval. The romanised queries are genuinely Tamil (4.3 Tamil tokens per query), so the romanised findings are more trustworthy. Module 3 replaces the synthetic queries with about 500 human ones.

**10. How do you know the improvements are not luck?**
Every query exists in all four forms, so comparisons are paired. I used a paired bootstrap (2,000 resamples) and 95% bootstrap intervals. Because about 4.3 queries come from each document, I also used a cluster bootstrap over documents: intervals widen about 1.6 times and every conclusion holds. Non-results are reported as such (code-mixed dense, p = 0.45).

**11. Why only 500 documents and a small model?**
To keep every experiment reproducible on a 2-core CPU. 2,154 paired queries give tight intervals (about ±0.01 to ±0.02 MRR). Larger models (BGE-M3, LaBSE, SONAR) and longer documents are in Module 3.

**12. Where is chunking, which is in your title?**
The news documents are short (median 326 characters), so each is one chunk and chunking cannot matter there. Module 3 uses long notices and circulars, and compares a Tamil-aware chunker (sentence and clause boundaries, never splitting a grapheme cluster) with ChunkLab's chunkers.

**13. Why not just translate the query into English?**
Translation is a Module 3 baseline (tRAG [89] and a SchemeAI-style pipeline [85]). In a bilingual base it has a structural blind spot: if the answer exists only in a Tamil G.O., searching English text cannot find it. For Hindi knowledge-base QA, back-transliteration beat translation by 5% and 35% in accuracy [36]; for Indic QA with LLMs, Translate-Test helped in low-resource settings [54]. They act at different stages, so I test both rather than assume.

**14. Why not fine-tune the embedding model instead of normalising?**
That is a fair alternative. Chari et al. [28] closed the script gap with transliterate-train fine-tuning, and Agarwal [46] found a normaliser redundant after fine-tuning. Module 3 includes a transliterate-train condition. The rules have practical advantages: no GPU, no retraining, 0.34 ms, and they work with any retriever.

**15. What is the script-gated router?**
A small decision step that looks at the mix of English, romanised-Tamil and Tamil-script tokens in the query and sends it to the retriever that works for that form: dense for English-heavy queries, rules plus char BM25 for romanised ones, and fusion only when every list carries signal. It turns my Module 2 findings into a system.

**16. How will you evaluate answers, not just retrieval?**
With answer correctness against reference answers and faithfulness and context relevance using RAGAs- or ARES-style judges. LLM judges inflate scores in low-resource, non-Latin settings [72], so I first calibrate the judge on about 100 human-labelled answers and report judge–human agreement. I also test abstention when the retrieved context is irrelevant, following NoMIRACL [75].

**17. Who would use this?**
E-governance and college help desks, agricultural advisory, health FAQs, bank and UPI support, and customer care in Tamil Nadu, wherever people type the way they text. The fix is cheap enough to add to an existing RAG system on CPU.

**18. What are your threats to validity?**
Synthetic queries; one relevant document per query (scores are a lower bound); an easy 500-document corpus; one small dense model; rules by one author; language ID that splits Indian named entities across scripts (*Triple டலக் bill ரஜ்ய Sabha*); clustered queries (handled by the cluster bootstrap).

**19. Where will you publish?**
Best fit is DravidianLangTech (held with ACL) or a FIRE track; SIGIR or ECIR resource tracks for the benchmark. A public benchmark plus code is the main release.

**20. How does this lead to a PhD?**
The benchmark, router and evaluation method become the base for a PhD on trustworthy agents for code-mixed Indian languages: script-robust retrieval across Dravidian languages, voice queries, trust and safety (hallucination, abstention, prompt injection in Tanglish), and on-device deployment.

**21. Why not just use ChatGPT or another LLM?**
An LLM can read Tanglish well in a chat. But a help desk has to answer from thousands of G.O.s, notices and circulars, more than fit in a prompt, so the LLM depends on a retrieval step to pick a few documents. That retrieval step collapses on romanised Tamil: dense MRR@10 0.143 in Module 2. The LLM never sees the right document, and then it either guesses or abstains. The answer may also exist only in a Tamil G.O., which an English-only or translate-the-query pipeline never searches. Sending every citizen query and document to a paid API also raises cost and privacy issues for government and health data. I don't ignore LLMs: an LLM query rewriter (Tanglish → Tamil script or English) is a Module 3 baseline, and an LLM is the Module 4 generator. My question is what gets the right evidence in front of it.

**22. Isn't Tanglish too niche?**
Tamil has more than 80 million speakers, and most of them type in Latin letters on phones. But Tanglish is the M.E. entry point, not the end point. The same problem (an Indian language typed in Roman script, mixed with English, over native-script and English documents) applies to Hinglish, Manglish, Telugu–English and others. Hira et al. [92] already show the bias for romanised Hindi, Bengali, Marathi and Urdu. The PhD (WP1) broadens the benchmark and methods to romanised and code-mixed Indic languages, which fits national programmes for Indian-language AI such as the IndiaAI Mission and Bhashini.

**23. Hira et al. [92] and Amiraz et al. [91] already studied language bias in mixed indices. What is left for you?**
They are close, and I cite them as the closest work. [92] pools *machine-translated parallel* documents, so every answer exists in every language; it has no Tamil and only dense retrievers. [91] is Arabic–English in native script only. My setting has *native, non-parallel* Tamil and English government documents, where the answer exists in one language only, so a language preference becomes a hard miss. My queries are human-written Tanglish, which matches English documents by script but Tamil documents by language. I also test model-free fixes (normaliser + char BM25, script-gated routing) against their balanced-retrieval fix, on CPU.

**24. There is already a Tanglish embedding model (Morgan-Tanglish-v7). Why build a normaliser?**
It is a useful baseline and I will test it in Module 3. Its only evidence is a self-reported score on a 325-pair similarity set from one annotator, with no retrieval test. It was trained only on Latin-script Tanglish, so it may not map a Tanglish query onto Tamil-script documents at all, and that mapping is our problem. The normaliser needs no model or GPU, runs in 0.34 ms and works with any retriever. If the embedder wins on English documents and the normaliser wins on Tamil ones, that supports the router.

**If asked "what would you do differently?"** Unit-test the fusion input from day one; gate fusion by script; keep named entities out of the transliterator; collect real Tanglish queries before tuning anything.

# 12. References (IEEE)

<div class="refs">

[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, 2020, pp. 9459–9474.

[2] S. Robertson and H. Zaragoza, "The probabilistic relevance framework: BM25 and beyond," *Foundations and Trends in Information Retrieval*, vol. 3, no. 4, pp. 333–389, 2009.

[3] L. Wang, N. Yang, X. Huang, L. Yang, R. Majumder, and F. Wei, "Multilingual E5 text embeddings: A technical report," arXiv:2402.05672, 2024.

[4] J. Chen, S. Xiao, P. Zhang, K. Luo, D. Lian, and Z. Liu, "BGE M3-Embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation," arXiv:2402.03216, 2024.

[5] F. Feng, Y. Yang, D. Cer, N. Arivazhagan, and W. Wang, "Language-agnostic BERT sentence embedding," in *Proc. 60th Annual Meeting of the Association for Computational Linguistics (ACL)*, 2022, pp. 878–891.

[6] G. V. Cormack, C. L. A. Clarke, and S. Büttcher, "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods," in *Proc. 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval*, 2009, pp. 758–759.

[7] B. R. Chakravarthi, V. Muralidaran, R. Priyadharshini, and J. P. McCrae, "Corpus creation for sentiment analysis in code-mixed Tamil-English text," in *Proc. 1st Joint Workshop on Spoken Language Technologies for Under-resourced Languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)*, 2020, pp. 202–210.

[8] B. R. Chakravarthi, R. Priyadharshini, V. Muralidaran, S. Suryawanshi, N. Jose, E. Sherly, and J. P. McCrae, "Overview of the track on sentiment analysis for Dravidian languages in code-mixed text," in *Proc. 12th Annual Meeting of the Forum for Information Retrieval Evaluation (FIRE '20)*, 2020, pp. 21–24, doi: 10.1145/3441501.3441515.

[9] S. Chanda and S. Pal, "Overview of the shared task on code-mixed information retrieval from social media data," in *FIRE 2024 Working Notes*, CEUR Workshop Proceedings, vol. 4054, 2024, pp. 124–128. [Online]. Available: https://ceur-ws.org/Vol-4054/T2-1.pdf

[10] S. Chanda, K. Tewari, and S. Pal, "Overview of the CMIR track at FIRE 2025: Code-mixed information retrieval from social media data," in *Proc. 17th Annual Meeting of the Forum for Information Retrieval Evaluation (FIRE '25)*, ACM, 2025, pp. 13–16, doi: 10.1145/3777867.3778255. (Author order as in ACM's corrected Version of Record of 27 January 2026; DBLP still lists the original order, Tewari, Chanda and Pal.)

[11] Q. Zeng, Y. Lu, Z. Zhou, H. Qi, P. Yu, F. Zhao, H. Yanaka, W. Xuan, and N. Yokoya, "Code-switching information retrieval: Benchmarks, analysis, and the limits of current retrievers," in *Findings of the Association for Computational Linguistics: ACL 2026*, 2026, doi: 10.18653/v1/2026.findings-acl.636.

[12] S. PaulRaj K, "ChunkLab: The interactive RAG engineering playground," GitHub repository, 2026. [Online]. Available: https://github.com/selvin-paul-raj/chunklab

[13] K. Chandu, E. Loginova, V. Gupta, J. van Genabith, G. Neumann, M. Chinnakotla, E. Nyberg, and A. W. Black, "Code-mixed question answering challenge: Crowd-sourcing data and techniques," in *Proc. Third Workshop on Computational Approaches to Linguistic Code-Switching*, Melbourne, Australia, 2018, pp. 29–38, doi: 10.18653/v1/W18-3204.

[14] D. Balasubramaniyam and T. Madushanka, "Query translation vs. cross-lingual embeddings for Sinhala-Tamil e-government information retrieval," arXiv:2608.12820, 2026.

[15] S. K. Singh, "Parser, chunking, and embedding interactions in retrieval-augmented generation over Indian government regulatory documents," arXiv:2609.31660, 2026.

[16] S. Chhoun, P. Po, S. Ros, W.-S. Cho, and S. Khoeurn, "Evaluation of chunking strategies for effective text embedding in low-resource language on agricultural documents," arXiv:2605.22203, 2026.

[17] Madhusudhanan G., "Visible reasoning and indirect prompt-injection monitorability across English, Tamil, and Tanglish," arXiv:2608.15392, 2026.

[18] nlpctx, "Tamil-English code-mixed retrieval evaluation dataset (tamil-english-retrieval)," Hugging Face Datasets, 2026, Apache-2.0. [Online]. Available: https://huggingface.co/datasets/nlpctx/tamil-english-retrieval

[19] S. Banerjee, K. Chakma, S. K. Naskar, A. Das, P. Rosso, S. Bandyopadhyay, and M. Choudhury, "Overview of the mixed script information retrieval (MSIR) at FIRE-2016," in *Working Notes of FIRE 2016*, CEUR Workshop Proceedings, vol. 1737, 2016. [Online]. Available: https://ceur-ws.org/Vol-1737/T3-1.pdf

[20] R. Sequiera, M. Choudhury, P. Gupta, P. Rosso, S. Kumar, S. Banerjee, S. K. Naskar, S. Bandyopadhyay, G. Chittaranjan, A. Das, and K. Chakma, "Overview of FIRE-2015 shared task on mixed script information retrieval," in *Post Proceedings of the FIRE 2015 Workshops*, CEUR Workshop Proceedings, vol. 1587, 2015, pp. 19–25. [Online]. Available: https://ceur-ws.org/Vol-1587/T2-1.pdf

[21] P. Gupta, K. Bali, R. E. Banchs, M. Choudhury, and P. Rosso, "Query expansion for mixed-script information retrieval," in *Proc. 37th International ACM SIGIR Conference on Research and Development in Information Retrieval*, 2014, pp. 677–686, doi: 10.1145/2600428.2609622.

[22] Y. Madhani, S. Parthan, P. Bedekar, G. NC, R. Khapra, A. Kunchukuttan, P. Kumar, and M. Khapra, "Aksharantar: Open Indic-language transliteration datasets and models for the next billion users," in *Findings of the Association for Computational Linguistics: EMNLP 2023*, Singapore, 2023, pp. 40–57, doi: 10.18653/v1/2023.findings-emnlp.4.

[23] AI4Bharat, "IndicCMix (code-mixed, native-script and romanised renderings for 11 Indic languages)," Hugging Face Datasets, MIT licence. [Online]. Available: https://huggingface.co/datasets/ai4bharat/IndicCMix

[24] R. Saha Roy, M. Choudhury, P. Majumder, and K. Agarwal, "Overview of the FIRE 2013 track on transliterated search," in *Proc. 5th Forum for Information Retrieval Evaluation (FIRE '13)*, ACM, 2013, pp. 1–7, doi: 10.1145/2701336.2701636.

[25] D. Ganguly, S. Pal, and G. J. F. Jones, "DCU@FIRE-2014: Fuzzy queries with rule-based normalization for mixed script information retrieval," in *Proc. 6th Forum for Information Retrieval Evaluation (FIRE '14)*, ACM, 2014, pp. 80–85, doi: 10.1145/2824864.2824888.

[26] K. Chakma and A. Das, "CMIR: A corpus for evaluation of code mixed information retrieval of Hindi-English tweets," *Computación y Sistemas*, vol. 20, no. 3, 2016, doi: 10.13053/cys-20-3-2459.

[27] R. R. Riyadh and G. Kondrak, "Joint approach to deromanization of code-mixed texts," in *Proc. 6th Workshop on NLP for Similar Languages, Varieties and Dialects (VarDial)*, Ann Arbor, MI, USA, 2019, doi: 10.18653/v1/W19-1403.

[28] A. Chari, I. Ounis, and S. MacAvaney, "Lost in transliteration: Bridging the script gap in neural IR," in *Proc. 48th Int. ACM SIGIR Conf. Research and Development in Information Retrieval (SIGIR '25)*, Padua, Italy, 2025, pp. 2900–2905, doi: 10.1145/3726302.3730226.

[29] A. Deroy and S. Maity, "RetrieveGPT: Merging prompts and mathematical models for enhanced code-mixed information retrieval," in *FIRE 2024 Working Notes*, CEUR Workshop Proceedings, vol. 4054, 2024, [Online]. Available: https://ceur-ws.org/Vol-4054/T2-2.pdf (arXiv:2411.04752).

[30] H. Mishra, R. Sharma, and N. Yadav, "Decoding Benglish: Scalable information retrieval for transliterated code-mixed conversations," in *FIRE 2025 Working Notes*, CEUR Workshop Proceedings, vol. 4173, 2025, [Online]. Available: https://ceur-ws.org/Vol-4173/T3-9.pdf.

[31] B. Roark, L. Wolf-Sonkin, C. Kirov, S. J. Mielke, C. Johny, I. Demirsahin, and K. Hall, "Processing South Asian languages written in the Latin script: The Dakshina dataset," in *Proc. 12th Language Resources and Evaluation Conf. (LREC)*, Marseille, France, 2020, pp. 2413–2423.

[32] C. Kirov, C. Johny, A. Katanova, A. Gutkin, and B. Roark, "Context-aware transliteration of romanized South Asian languages," *Computational Linguistics*, vol. 50, 2024, pp. 475–534, doi: 10.1162/coli_a_00510.

[33] Y. Madhani, M. M. Khapra, and A. Kunchukuttan, "Bhasha-Abhijnaanam: Native-script and romanized language identification for 22 Indic languages," in *Proc. 61st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, Toronto, Canada, 2023, doi: 10.18653/v1/2023.acl-short.71.

[34] A. Benton, A. Gutkin, C. Kirov, and B. Roark, "Improving informally romanized language identification," in *Proc. 2025 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Suzhou, China, 2025, pp. 2318–2336, doi: 10.18653/v1/2025.emnlp-main.117.

[35] H. M. A. D. Herath and T. G. D. K. Sumanathilaka, "TAMZHI: Shorthand romanized Tamil to Tamil reverse transliteration using novel hybrid approach," *Int. J. Advances in ICT for Emerging Regions (ICTer)*, vol. 17, no. 1, 2024, pp. 1–7, doi: 10.4038/icter.v17i1.7271.

[36] V. Gupta, M. Chinnakotla, and M. Shrivastava, "Transliteration better than translation? Answering code-mixed questions over a knowledge base," in *Proc. Third Workshop on Computational Approaches to Linguistic Code-Switching*, Melbourne, Australia, 2018, doi: 10.18653/v1/W18-3205.

[37] S. Khanuja, S. Dandapat, A. Srinivasan, S. Sitaram, and M. Choudhury, "GLUECoS: An evaluation benchmark for code-switched NLP," in *Proc. 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, 2020, doi: 10.18653/v1/2020.acl-main.329.

[38] G. Winata, A. F. Aji, Z. X. Yong, and T. Solorio, "The decades progress on code-switching research in NLP: A systematic survey on trends and challenges," in *Findings of the Association for Computational Linguistics: ACL 2023*, Toronto, Canada, 2023, doi: 10.18653/v1/2023.findings-acl.185.

[39] R. Zhang, S. Cahyawijaya, J. C. B. Cruz, G. Winata, and A. F. Aji, "Multilingual large language models are not (yet) code-switchers," in *Proc. 2023 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Singapore, 2023, doi: 10.18653/v1/2023.emnlp-main.774.

[40] G. I. Winata *et al.*, "Can large language models understand, reason about, and generate code-switched text?," arXiv:2601.07153, 2026.

[41] A. Das, M. Parmar, M. Ramnath, and P. Verma, "Indi-RomCoM: Code-mixed benchmark for evaluating LLMs on romanized Indic-English instructions," arXiv:2606.30790, 2026.

[42] S. S. Gaikwad and J. S. Gaikwad, "Reducing hallucinations in retrieval-augmented LLM question answering for Indian code-mixed queries," in *Smart Trends in Computing and Communications (SmartCom 2026)*, Lecture Notes in Networks and Systems, vol. 1991, Cham: Springer, 2026, pp. 402–415, doi: 10.1007/978-3-032-27754-1_37.

[43] S. Sharma, R. Rathee, N. Mishra, and S. Bhatt, "Multilingual embedders for explainable Hinglish retrieval in RAG," in *Proc. Int. Conf. Artificial Intelligence and Cyber Security (ICAICS 2025)*, Lecture Notes in Networks and Systems, vol. 2024, Cham: Springer, 2026, pp. 157–172, doi: 10.1007/978-3-032-28379-5_13.

[44] T. Harika, Kaniz-E-Fatima, and S. Samreen, "OneVoice: A code-mixed RAG framework for multilingual student support," *ICTACT J. Soft Computing*, vol. 17, 2026, pp. 4297–4305, doi: 10.21917/ijsc.2026.0591.

[45] A. J. M. Adoptante, J. A. D. V. Castro, M. L. B. Medrana, A. P. B. Ocampo, E. C. Peramo, and M. R. M. Miranda, "Benchmarking open-source large language models on code-switched Tagalog-English retrieval augmented generation," *J. Advances in Information Technology*, vol. 16, no. 2, 2025, pp. 233–242, doi: 10.12720/jait.16.2.233-242.

[46] P. Agarwal, "Where does noise robustness live? Evidence from ablation, role swaps, and cross-lingual transfer in code-mixed banking NLU," in *Proc. 11th Workshop on Noisy and User-generated Text (W-NUT)*, 2026, pp. 356–367, doi: 10.18653/2026.wnut-1.26.

[47] S. Doddapaneni, R. Aralikatte, G. Ramesh, S. Goyal, M. M. Khapra, A. Kunchukuttan, and P. Kumar, "Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages," in *Proc. 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Toronto, Canada, 2023, doi: 10.18653/v1/2023.acl-long.693.

[48] J. P. Gala *et al.*, "IndicTrans2: Towards high-quality and accessible machine translation models for all 22 scheduled Indian languages," arXiv:2305.16307, 2023.

[49] A. Balachandran, "Tamil-Llama: A new Tamil language model based on Llama 2," arXiv:2311.05845, 2023.

[50] R. Kumaresan, Madhusudhanan G., and K. Kezendirane, "Agaram 2.5B: The first Tamil-first language model trained from scratch with tool calling. A playbook for under-represented languages," arXiv:2610.18420, 2026.

[51] Sarvam AI, "Sarvam-1," Hugging Face model card, 2024, [Online]. Available: https://huggingface.co/sarvamai/sarvam-1.

[52] S. Haq, A. Sharma, O. Khattab, N. Chhaya, and P. Bhattacharyya, "IndicIRSuite: Multilingual dataset and neural information models for Indian languages," in *Proc. 62nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, Bangkok, Thailand, 2024, doi: 10.18653/v1/2024.acl-short.46.

[53] P. Prasanjith, P. More, A. Kunchukuttan, and R. Dabre, "IndicRAGSuite: Large-scale datasets and a benchmark for Indian language RAG systems," arXiv:2506.01615, 2025.

[54] A. K. Singh, V. Kumar, R. Murthy, J. Sen, A. Mittal, and G. Ramakrishnan, "INDIC QA BENCHMARK: A multilingual benchmark to evaluate question answering capability of LLMs for Indic languages," in *Findings of the Association for Computational Linguistics: NAACL 2025*, Albuquerque, NM, USA, 2025, pp. 2607–2626, doi: 10.18653/v1/2025.findings-naacl.141.

[55] X. Zhang, N. Thakur, O. Ogundepo, E. Kamalloo, D. Alfonso-Hermelo, X. Li, Q. Liu, M. Rezagholizadeh, and J. Lin, "MIRACL: A multilingual retrieval dataset covering 18 diverse languages," *Trans. Association for Computational Linguistics*, vol. 11, 2023, doi: 10.1162/tacl_a_00595.

[56] K. Raja, M. Abejide, A. Ram, U. Sharma, and K. Zhu, "MURMUR: Cross-lingual and multimodal retrieval augmented reasoning for open question answering in Tamil and Yoruba," in *Proc. Conf. Language Modeling (COLM)*, 2026, [Online]. Available: https://proceedings.colm.cc/paper_files/paper/2026/file/2098f348d1d071e3ce652a5edadae3b1-Paper-Conference.pdf.

[57] S. S. Anthea, N. R. Mary, and K. Varalakshmi, "TanglishMedBench: A benchmark for evaluating LLMs on Tamil-English code-mixed medical queries," Zenodo dataset, v1.0.0, 2026, doi: 10.5281/zenodo.22308075.

[58] P.-A. Duquenne, H. Schwenk, and B. Sagot, "SONAR: Sentence-level multimodal and language-agnostic representations," arXiv:2308.11466, 2023.

[59] LCM Team, L. Barrault, P.-A. Duquenne, M. Elbayad *et al.*, "Large concept models: Language modeling in a sentence representation space," arXiv:2412.08821, 2024.

[60] J. A. Husain, R. Dabre, A. Kumar, J. Gala, T. Jayakumar, R. Puduppully, and A. Kunchukuttan, "RomanSetu: Efficiently unlocking multilingual capabilities of large language models via romanization," in *Proc. 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Bangkok, Thailand, 2024, doi: 10.18653/v1/2024.acl-long.833.

[61] A. A. K. Verma, A. Chatterjee, M. Gupta, and T. Chakraborty, "Multilingual language models encode script over linguistic structure," in *Proc. 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, San Diego, CA, USA, 2026, pp. 33685–33719, doi: 10.18653/v1/2026.acl-long.1554.

[62] T. Zhu, H. C. Ming, and M.-Y. Kan, "When does mixing help? Analyzing query embedding interpolation in multilingual dense retrieval," in *Proc. 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, San Diego, CA, USA, 2026, pp. 31544–31562, doi: 10.18653/v1/2026.acl-long.1455.

[63] S. Bruch, S. Gai, and A. Ingber, "An analysis of fusion functions for hybrid retrieval," *ACM Trans. Information Systems*, vol. 42, 2023, pp. 1–35, doi: 10.1145/3596512.

[64] A. Chauhan and A. Agarwal, "The fusion tax: A diagnostic analysis of when hybrid retrieval hurts," *IEEE Access*, vol. 14, 2026, pp. 159620–159637, doi: 10.1109/ACCESS.2026.3743502.

[65] X. Ma, Y. Gong, P. He, H. Zhao, and N. Duan, "Query rewriting in retrieval-augmented large language models," in *Proc. 2023 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Singapore, 2023, doi: 10.18653/v1/2023.emnlp-main.322.

[66] L. Gao, X. Ma, J. Lin, and J. Callan, "Precise zero-shot dense retrieval without relevance labels," in *Proc. 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Toronto, Canada, 2023, doi: 10.18653/v1/2023.acl-long.99.

[67] T. Chen, H. Wang, S. Chen, W. Yu, K. Ma, X. Zhao, H. Zhang, and D. Yu, "Dense X retrieval: What retrieval granularity should we use?," in *Proc. 2024 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Miami, FL, USA, 2024, doi: 10.18653/v1/2024.emnlp-main.845.

[68] R. Qu, R. Tu, and F. S. Bao, "Is semantic chunking worth the computational cost?," in *Findings of the Association for Computational Linguistics: NAACL 2025*, Albuquerque, NM, USA, 2025, pp. 2155–2177, doi: 10.18653/v1/2025.findings-naacl.114.

[69] S. Es, J. James, L. Espinosa Anke, and S. Schockaert, "RAGAs: Automated evaluation of retrieval augmented generation," in *Proc. 18th Conf. European Chapter of the Association for Computational Linguistics: System Demonstrations*, St. Julians, Malta, 2024, doi: 10.18653/v1/2024.eacl-demo.16.

[70] J. Saad-Falcon, O. Khattab, C. Potts, and M. Zaharia, "ARES: An automated evaluation framework for retrieval-augmented generation systems," in *Proc. 2024 Conf. North American Chapter of the Association for Computational Linguistics (NAACL), Volume 1: Long Papers*, Mexico City, Mexico, 2024, doi: 10.18653/v1/2024.naacl-long.20.

[71] L. Zheng *et al.*, "Judging LLM-as-a-judge with MT-Bench and Chatbot Arena," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 36, Datasets and Benchmarks Track, 2023, pp. 46595–46623.

[72] R. Hada, V. Gumma, A. de Wynter, H. Diddee, M. Ahmed, M. Choudhury, K. Bali, and S. Sitaram, "Are large language model-based evaluators the solution to scaling up multilingual evaluation?," in *Findings of the Association for Computational Linguistics: EACL 2024*, St. Julian's, Malta, 2024, doi: 10.18653/v1/2024.findings-eacl.71.

[73] I. Watts, V. Gumma, A. Yadavalli, V. Seshadri, M. Swaminathan, and S. Sitaram, "PARIKSHA: A large-scale investigation of human-LLM evaluator agreement on multilingual and multi-cultural data," in *Proc. 2024 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Miami, FL, USA, 2024, pp. 7900–7932.

[74] V. Gumma, A. Raghunath, M. Jain, and S. Sitaram, "HEALTH-PARIKSHA: Assessing RAG models for health chatbots in real-world multilingual settings," arXiv:2410.13671, 2024.

[75] N. Thakur, L. Bonifacio, C. Zhang, O. Ogundepo, E. Kamalloo, D. Alfonso-Hermelo, X. Li, Q. Liu, B. Chen, M. Rezagholizadeh, and J. Lin, ""Knowing when you don't know": A multilingual relevance assessment dataset for robust retrieval-augmented generation," in *Findings of the Association for Computational Linguistics: EMNLP 2024*, Miami, FL, USA, 2024, doi: 10.18653/v1/2024.findings-emnlp.730.

[76] N. Chirkova, D. Rau, H. Déjean, T. Formal, S. Clinchant, and V. Nikoulina, "Retrieval-augmented generation in multilingual settings," in *Proc. 1st Workshop on Towards Knowledgeable Language Models (KnowLLM 2024)*, Bangkok, Thailand, 2024, doi: 10.18653/v1/2024.knowllm-1.15.

[77] B. Fetahu, A. Fang, O. Rokhlenko, and S. Malmasi, "Gazetteer enhanced named entity recognition for code-mixed web queries," in *Proc. 44th Int. ACM SIGIR Conf. Research and Development in Information Retrieval (SIGIR '21)*, 2021, pp. 1677–1681, doi: 10.1145/3404835.3463102.

[84] D. Thenmozhi and C. Aravindan, "Ontology-based Tamil–English cross-lingual information retrieval system," *Sādhanā*, vol. 43, art. no. 157, 2018, doi: 10.1007/s12046-018-0942-7.

[85] M. Rekha, P. Pragadeeshwaran, S. Surendhar, and B. Udhayachandran, "Government schemes recommendation system API with bilanguage chatbot using RAG vector search," *Int. J. Advanced Research in Science, Communication and Technology (IJARSCT)*, vol. 6, no. 9, Apr. 2026, doi: 10.48175/IJARSCT-33228.

[86] Vishnu N, "Morgan-Tanglish-v7: Sentence embeddings for romanised Tamil-English code-mixed text," Zenodo preprint, Jun. 2026, doi: 10.5281/zenodo.20792177. Model: huggingface.co/vishnu-n/Morgan-Tanglish-v7 (Apache-2.0).

[87] Vishnu N, "TanglishSTS: A human-annotated semantic textual similarity benchmark for romanised Tamil-English," Hugging Face Datasets, 2026, CC BY 4.0. [Online]. Available: https://huggingface.co/datasets/vishnu-n/TanglishSTS

[88] V. Vijesh and E. Gothai, "TanglishGuard: Benchmarking AI safety guardrails on Tamil-English code-mixed prompts," *Int. J. Innovative Science and Research Technology (IJISRT)*, vol. 11, no. 7, Jul. 2026, doi: 10.38124/ijisrt/26jul962.

[89] L. Ranaldi, B. Haddow, and A. Birch, "Multilingual retrieval-augmented generation for knowledge-intensive question answering task," in *Findings of the Association for Computational Linguistics: EACL 2026*, Rabat, Morocco, 2026, pp. 697–716, doi: 10.18653/v1/2026.findings-eacl.35. (Preprint: arXiv:2504.03616.)

[90] J. Park and H. Lee, "Investigating language preference of multilingual RAG systems," in *Findings of the Association for Computational Linguistics: ACL 2025*, Vienna, Austria, 2025, pp. 5647–5675, doi: 10.18653/v1/2025.findings-acl.295.

[91] C. Amiraz, Y. Fyodorov, E. Haramaty, Z. Karnin, and L. Lewin-Eytan, "The cross-lingual cost: Retrieval biases in RAG over Arabic-English corpora," in *Proc. Third Arabic Natural Language Processing Conf. (ArabicNLP 2025)*, 2025, pp. 69–83, doi: 10.18653/v1/2025.arabicnlp-main.6.

[92] M. Hira, J. Mire, and M. Sap, "The language of evidence: Robustness and bias in code-switched RAG," in *Proc. 2026 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, 2026, pp. 41664–41685. [Online]. Available: https://aclanthology.org/2026.emnlp-main.1830


</div>


