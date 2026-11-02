### A1. Rekha, Pragadeeshwaran, Surendhar and Udhayachandran — SchemeAI: Government schemes recommendation with a bilingual RAG chatbot [85], IJARSCT 2026

- **Problem.** Citizens can't easily find the government schemes they qualify for, because portals are scattered and there is a language barrier for Tamil speakers.
- **Method.** A Flask web chatbot. The user picks a state and a category, then types a question. The question is embedded with **all-MiniLM-L6-v2** (Sentence-BERT) and matched against a **FAISS** index built from a structured CSV of central and state schemes (`updated_data.csv`: Agriculture, Education, Housing; Tamil Nadu, Telangana, Puducherry). A language-detection step plus the **GoogleTranslator API** "dynamically translates English scheme details into Tamil" for display. An "Intelligence Explanation" page shows the pipeline (called XAI in the paper).
- **Data.** One English CSV. The paper doesn't give its size, and there is no test set.
- **Results.** Screenshots of one English and one Tamil question, plus an "accuracy comparison" graph and a "response time" graph. The text gives no numbers, metric definitions or evaluation protocol.
- **Strengths.** It addresses exactly our use case 1 (Tamil Nadu scheme help desk), shows that Tamil Nadu colleges are building bilingual RAG, and uses a cheap CPU stack.
- **Weaknesses.** (1) The knowledge base is English only, so there are no Tamil documents. (2) all-MiniLM-L6-v2 is an English-trained embedder, and the paper doesn't say whether Tamil queries are translated before they are embedded. (3) Translation only touches the output. (4) There is no handling of romanised or code-mixed input. A Tanglish query is in Latin letters, so a language detector will probably label it English and pass it straight to an English embedder. This is our inference and isn't tested in the paper. (5) There is no retrieval evaluation. (6) Editorial problems: the in-text literature survey cites authors who don't match the reference list. The venue is a low-selectivity journal.
- **Relevance.** This is the **"existing system"** in our existing-vs-proposed comparison: a translate-around-an-English-index design typical of local deployments.
- **Why it matters.** It shows what a Tamil Nadu bilingual RAG looks like in practice today, and why it can't be judged: nothing is measured. Module 3 re-implements a SchemeAI-style baseline (MiniLM + FAISS, query translated to English) on the bilingual benchmark.
- **Gap it leaves.** No Tamil-language documents, so an answer that exists only in a Tamil G.O. is unreachable. No romanised or code-mixed queries. No retrieval or answer metrics.

### A2. Vishnu N — Morgan-Tanglish-v7 sentence embeddings [86] and TanglishSTS [87], Zenodo / Hugging Face 2026

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

### A3. Gupta, Bali, Banchs, Choudhury and Rosso — Query expansion for mixed-script IR [21], SIGIR 2014 (already in the list; re-verified)

- **Verification.** Crossref metadata re-checked: pp. 677–686, doi 10.1145/2600428.2609622. The full review is in Dossier §9.3.
- **What it adds to the new framing.** Mixed-script IR was defined as **one language written in two scripts** (native and Roman) for both queries and documents. That is our Tamil-script vs romanised Tamil axis. It does **not** cover two *languages* in one index, so the bilingual Tamil+English setting goes beyond the MSIR definition. The 2014 setting is lexical and pre-neural, with no RAG.
- **Gap it leaves (bilingual view).** No language-preference question, because every document was in one language.

### A4. Banerjee et al. — Overview of MSIR at FIRE-2016 [19] (already in the list; PDF re-opened)

- **Problem.** The fourth year of the FIRE mixed-script track.
- **Method / data.** Subtask 1: classifying code-mixed Bengali-English questions in Roman script (330 training and 180 test questions, 9 classes). Subtask 2: retrieving Roman-script Hindi-English code-mixed tweets (training: 6,133 tweets, 23 queries; test: 2,796 tweets, **12** queries; queries average 3.25 words and are mostly named entities).
- **Results.** Subtask 1: best accuracy 83.33% against a bag-of-words baseline of 79.44%. Subtask 2: best **MAP 0.0377**. The organisers call code-mixed tweet retrieval "a very challenging task".
- **Strengths.** Public tasks with qrels, and a long organiser lineage (MSR India, Jadavpur).
- **Weaknesses.** Tiny query sets (12 test queries) and social-media text only. Tamil appeared only in the 2014 word-labelling subtask, never in retrieval.
- **Relevance / why it matters.** It anchors the history of the problem and shows how small earlier evaluation sets were. Our planned ~500 human queries are a large step up. Every document was monolingual, so it doesn't speak to the bilingual-index question.
- **Gap it leaves.** No Tamil retrieval, no native-script documents mixed with English documents, no dense retrievers.

### A5. Vijesh and Gothai — TanglishGuard [88], IJISRT 2026

- **Problem.** LLM safety is tested almost only in English. Is it also robust to Tanglish?
- **Method / data.** 90 harmful prompts (9 categories × 10), each written in English, Tamil and Tanglish. Four chat models (ChatGPT, Gemini, Claude, DeepSeek), 3 runs each. Scored on refusal (binary), cross-language consistency (1–10) and explanation quality (1–5).
- **Results.** Every model refuses more than 95% of prompts. English and Tamil score 10/10 on safety; Tanglish scores 9.9 (DeepSeek 9.8). The authors call this "subtle but consistent".
- **Strengths.** The first Tanglish-specific safety probe, and a clear trilingual design.
- **Weaknesses.** The effect is 0.1–0.2 on a 10-point scale with no significance test. The sample is small and the prompts' release status is unclear. Some references in the paper carry placeholder arXiv IDs ("2603.xxxxx"). The venue is of concern. It does no retrieval: prompts are sent to chat models directly.
- **Relevance.** PhD WP3 (trust and safety): evidence that the question is being asked locally.
- **Why it matters.** It strengthens the WP3 motivation, but it is not strong evidence of a safety gap. WP3 should test **retrieval-grounded** risks (prompt injection hidden in retrieved Tamil or English documents, abstention on irrelevant context), with significance tests.
- **Gap it leaves.** No RAG, no indirect injection, no statistics.

### A6. Thenmozhi and Aravindan — Ontology-based Tamil–English CLIR [84], Sādhanā 2018 (SSN, Chennai)

- **Problem.** Tamil users querying English content. Query ambiguity hurts translation-based cross-lingual IR.
- **Method.** A Tamil morphological analyser, a Tamil-English bilingual dictionary and a named-entity database translate the Tamil query into English, with word-sense disambiguation. An automatically built English domain ontology then reformulates the translated query, and a web search engine retrieves English documents.
- **Data / results.** Agriculture domain. The abstract says it "outperforms other approaches in terms of precision"; numbers sit behind the paywall and weren't seen. The appendix tables show example queries in romanised form ("Mutkalappai", "Uzhudhal Upakaranangkal"). Whether users typed them that way or the authors transliterated them for display can't be confirmed without the full text.
- **Strengths.** The closest peer-reviewed Tamil–English IR work. It is from Chennai (a possible local reviewer or collaborator, D. Thenmozhi) and builds real Tamil language resources.
- **Weaknesses.** Pre-neural, with English-only target documents. Submitted in 2014 and published in 2018. No code-mixing.
- **Relevance / why it matters.** It is the classic **translate-the-query-to-English** design, the same family as the SchemeAI baseline. Our bilingual framing explains its blind spot: when the answer exists only in a Tamil document, translating into English searches the wrong half of the collection.
- **Gap it leaves.** No Tamil-language documents in the index, no romanised or code-mixed queries, no dense retrieval or RAG.

### A7. Ranaldi, Haddow and Birch — Multilingual RAG for knowledge-intensive QA (CrossRAG) [89], Findings of EACL 2026

- **Problem.** How should RAG work when queries and knowledge are not in English?
- **Method.** Four pipelines compared. **monoRAG** retrieves in the query language only. **tRAG** translates the question into English and then retrieves. **MultiRAG** retrieves directly across many languages. **CrossRAG** retrieves across languages, then **translates the retrieved documents into one language (English)** before generating. Retrieval uses Cohere Embed v3 over a Wikipedia dump; translation uses Google Translate (and GPT-4o as a variant); the generators are GPT-4o, Llama-3-8B and Command-R-35B.
- **Data.** MKQA, MLQA and XOR TyDi QA. The PDF mentions Hindi and Bengali; Tamil isn't mentioned.
- **Results (as stated in the abstract and §4).** tRAG "suffers from limited coverage"; MultiRAG beats monoRAG and tRAG but brings inconsistency across languages; CrossRAG "significantly enhances performance", for both high- and low-resource languages.
- **Strengths.** A clean taxonomy of strategies, a published venue, three generators.
- **Weaknesses.** Wikipedia-based, so models may already know the answers (the critique in [91]). No code-mixed or romanised queries. It depends on a commercial translation API, which raises cost and privacy issues for government documents. The study is mostly about generation. A later paper [92] finds translating into English is "not universal", especially for Indic-script languages. (Note: [92] cites arXiv:2504.03616 with a different author list; [91] and the ACL Anthology give Ranaldi, Haddow and Birch, which we use.)
- **Relevance.** It supplies two baselines. **tRAG** (translate the Tanglish query to English, then retrieve) goes in Module 3. **CrossRAG** (translate retrieved Tamil chunks before generation) goes in Module 4.
- **Why it matters.** For a bilingual Tamil+English base, the key choice is what you translate: the query or the evidence. This paper is the reference point for that choice.
- **Gap it leaves.** No romanised or code-mixed queries, no Tamil, no domain-specific bilingual collection.

### A8. Chirkova et al. — Retrieval-augmented generation in multilingual settings [76], KnowLLM @ ACL 2024 (already in the list; re-verified)

- **Problem.** A strong, reproducible baseline pipeline for multilingual RAG (mRAG).
- **Method / data.** User queries and a datastore in 13 languages, built on the BERGEN toolkit (github.com/naver/bergen). The abstract doesn't list the 13 languages, and we didn't check whether Tamil is one of them.
- **Results.** Off-the-shelf multilingual retrievers and generators are adequate, but **task-specific prompting is needed so the model answers in the user's language**. Metrics need adjusting for **named entities spelled differently**. Remaining failures: code-switching in non-Latin outputs, fluency errors, misreading documents, irrelevant retrieval.
- **Strengths.** Open code and a careful list of failure modes.
- **Weaknesses.** Wikipedia-style data; no romanised or code-mixed queries.
- **Relevance / why it matters.** Two Module 4 design inputs: a prompt that answers in the user's form (Tanglish in, Tanglish or Tamil out), and entity-tolerant answer matching. Tamil names have many Latin spellings.
- **Gap it leaves.** Code-mixed and romanised input, and domain-specific bilingual collections.

### A9. Language preference / language bias in multilingual retrieval and RAG (search pass, 2 Nov 2026)

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
