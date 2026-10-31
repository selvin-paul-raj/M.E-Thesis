# Research Map: who did what, and how
## Tanglish (Tamil–English code-mixed and romanised) retrieval and RAG

Prepared for Selvin PaulRaj K, M.E. CSE (AI), Kings Engineering College. Compiled 31 Oct 2026 (IST).
Builds on `LITERATURE_SURVEY.md`, `references_new_IEEE.md` ([24]–[77]) and `report_src/report_body.md` ([1]–[23]). Bracketed numbers such as [28] refer to that combined list. New items found in this pass are numbered [78]–[84] (§7).

**Method.** This pass followed LabRat literature-research (venue mining across FIRE, DravidianLangTech, ACL Anthology, SIGIR; people and lab pages; citation chaining from the existing seeds) and paper-check (each new citation and number checked against the opened abstract or record). Paper numbers that were already verified come from the earlier survey and are reused here, not re-derived.

**Verification tags**
- **[V]**: the official page, abstract or record was opened in this pass (ACL Anthology, arXiv, OpenAlex, publisher, university or conference site).
- **[V-prior]**: verified in `LITERATURE_SURVEY.md` §8 (abstract opened); reused here.
- **[V-idx]**: the official page blocked direct fetching (HTTP 403), so the content was read from a search-index copy of that same official URL. Treat it as likely but re-check it before citing.
- **[U]**: not verified. Do not cite without checking.

---

## 1. Research groups and labs (22)

Relevance to this thesis: **H** = high, **M** = medium, **L** = low.

### 1.1 Summary table

| # | Group (affiliation) | Key people | What they built | How (one line) | Rel. |
|---|---|---|---|---|---|
| 1 | **AI4Bharat / Nilekani Centre, IIT Madras** (+ Microsoft) | Mitesh M. Khapra, Anoop Kunchukuttan, Raj Dabre, Sumanth Doddapaneni, Jay Gala, Yash Madhani | Aksharantar + IndicXlit [22], IndicLID / Bhasha-Abhijnaanam [33], IndicCMix [23], IndicCorp v2 / IndicBERT v2 [47], IndicTrans2 [48], RomanSetu [60], IndicRAGSuite [53] | Mine and annotate large Indic resources, then release open models for transliteration, LID, MT and RAG | **H** |
| 2 | **Microsoft Research India** | Kalika Bali, Sunayana Sitaram, (formerly) Monojit Choudhury; Rishav Hada, Varun Gumma, Ishaan Watts | MSIR concept [21], early code-mixing analysis [78][79], GLUECoS [37], LLM-evaluator studies [72], PARIKSHA [73], HEALTH-PARIKSHA [74] | Query-log and social-media analysis, then benchmarks and human-vs-LLM evaluation at scale | **H** |
| 3 | **FIRE MSIR organisers (2013–2016)** | Rishiraj Saha Roy, Monojit Choudhury, Prasenjit Majumder, Parth Gupta, Paolo Rosso, Somnath Banerjee, Sudip K. Naskar, Sivaji Bandyopadhyay, Amitava Das, Kunal Chakma | FIRE 2013 transliterated search [24], MSIR 2015 [20], MSIR 2016 [19] | Shared tasks: word-level LID, back-transliteration, and ad-hoc retrieval over Roman-script queries | **H** (historical base) |
| 4 | **IReL, IIT (BHU) Varanasi** (+ Bennett University) | Sukomal Pal, Supriya Chanda (now Bennett), Krishna Tewari | CMIR@FIRE 2024 [9] and 2025 [10] (Bengali–English, Roman then mixed script) | Shared task with qrels; 2025 runs show fusion and hybrids beating standalone models [10] | **H** |
| 5 | **University of Galway + DravidianLangTech consortium** | Bharathi Raja Chakravarthi, John P. McCrae, Ruba Priyadharshini (Gandhigram Rural Inst.), Anand Kumar M (NITK), Sajeetha Thavareesan, Saranya Rajiakodi, Subalalitha C.N. (SRM), Kogilavani S. & Malliga S. (Kongu), Ratnavel Rajalakshmi (VIT) | Tamil–English sentiment corpus [7], FIRE Dravidian-CodeMix [8], DravidianCodeMix [82], offensive-language findings [81], DravidianLangTech workshops 2021–2026 | Crowd-annotated YouTube comment corpora, then recurring shared tasks at ACL/NAACL/EACL/RANLP and FIRE | **H** |
| 6 | **SSN / Shiv Nadar University Chennai NLP** | Durairaj Thenmozhi (now SNU Chennai), B. Bharathi, Sripriya N | Co-organises DravidianCodeMix@FIRE and DravidianLangTech tasks; Tamil–English CLIR [84] | Shared-task organisation plus ontology-based Tamil–English CLIR | **H** (Chennai, local) |
| 7 | **Google Research (South Asian romanisation)** | Brian Roark, Christo Kirov, Cibu Johny, Alexander Gutkin, Adrian Benton, Lawrence Wolf-Sonkin | Dakshina [31], context-aware transliteration [32], better romanised LID [34] | Parallel native/Latin data, then sentence-level transliteration ensembles and synthetic spelling-variation data | **H** |
| 8 | **Terrier Team, University of Glasgow** | Andreas Chari, Iadh Ounis, Sean MacAvaney | "Lost in Transliteration" [28] | Measure the script gap of multilingual dense IR, then "transliterate-train" fine-tuning of BGE-M3 | **H** |
| 9 | **CFILT, IIT Bombay** | Pushpak Bhattacharyya (with Saiful Haq, Omar Khattab and others) | IndicIRSuite: INDIC-MARCO + Indic-ColBERT [52] | Machine-translate MS MARCO into 11 Indic languages, then train late-interaction retrievers | M/H |
| 10 | **JUNLP, Jadavpur University** | Dipankar Das, Sudip K. Naskar, Sivaji Bandyopadhyay | MSIR co-organisation [19][20]; SAIL code-mixed sentiment @ICON-2017 [80] | Shared tasks on Hi–En and Bn–En code-mixed sentiment | M |
| 11 | **LTRC, IIIT Hyderabad** | Manish Shrivastava (with Vishal Gupta, Manoj Chinnakotla) | Code-mixed KBQA: transliteration beats translation [36] | Triplet-Siamese re-ranker over back-transliterated questions | M |
| 12 | **CMU LTI** | Khyathi Chandu, Alan W. Black (with Gupta, Chinnakotla and others) | Code-mixed QA challenge [13] | Crowd-sourced code-mixed QA data with baseline techniques | M |
| 13 | **University of Alberta** | Grzegorz Kondrak, Rashed Rubby Riyadh | Joint deromanisation of code-mixed text [27] | Joint LID + back-transliteration as sequence prediction | M |
| 14 | **CALCS community** | Genta Indra Winata (Capital One), Thamar Solorio (MBZUAI), Sudipta Kar, Marina Zhukova | CALCS workshops 2014–2025; survey [38]; LLM CS studies [39][40] | Workshops, shared tasks and benchmarks for code-switching | M |
| 15 | **Sarvam AI** (Bengaluru) | team (founders not verified here) | Sarvam-1 2B Indic LM incl. Tamil [51] | Indic-optimised tokenizer and pretraining | M |
| 16 | **Krutrim (Ola)** | Aditya Kallappa, Chandra Khatri and others [83] | Krutrim LLM [83] | 2-trillion-token multilingual pretraining aimed at Indian languages and code mixing | M |
| 17 | **Tamil LLM builders** | Abhinand Balachandran (Tamil-Llama, Chennai); Ramchand Kumaresan (Murai Labs), Madhusudhanan G (VIT; independent on Agaram), Kaushik Kezendirane | Tamil-Llama [49]; Agaram 2.5B (Tamil, **Tanglish**, English) [50]; Tanglish safety study [17] | Vocabulary extension + LoRA (Tamil-Llama); Tamil-first pretraining from scratch (Agaram) | **H** (generator candidates) |
| 18 | **Hinglish code-mixed RAG authors (2026)** | S. S. Gaikwad & J. S. Gaikwad [42]; S. Sharma, R. Rathee, N. Mishra, S. Bhatt [43]; T. Harika, Kaniz-E-Fatima, S. Samreen [44] | Hallucination-aware CM RAG, Hinglish embedder study, OneVoice college RAG | Normalise the code-mixed query, retrieve with multilingual embedders, abstain or answer | **H** (closest task; affiliations **[U]**) |
| 19 | **Tanglish data makers** | S. S. Anthea, N. R. Mary, K. Varalakshmi [57]; "nlpctx" [18] | TanglishMedBench (700 QA); tamil-english-retrieval set | Expert-labelled Tanglish medical QA; small retrieval eval set | **H** (affiliations **[U]**) |
| 20 | **Waterloo (Jimmy Lin) / Nandan Thakur** | Xinyu Zhang, Nandan Thakur, Jimmy Lin | MIRACL [55], NoMIRACL [75]; MAST@FIRE 2026 (multilingual agentic search, with an Indic sub-track) [V-idx] | Human-judged multilingual retrieval sets and robustness subsets | M |
| 21 | **NAVER Labs Europe** | Nadezhda Chirkova, Stéphane Clinchant, Vassilina Nikoulina | mRAG study, BERGEN [76] | Benchmark mRAG pipelines across 13 languages | M |
| 22 | **Pune L3Cube** | Raviraj Joshi et al. | L3Cube-IndicSBERT (in survey §8.2) | Multilingual SBERT for Indic languages | L/M (homepage not verified) |

### 1.2 Group details (people, key papers, code, verification)

**1. AI4Bharat / IIT Madras.** Khapra: Professor, DSAI, IIT Madras [V] https://www.cse.iitm.ac.in/~miteshk/. Kunchukuttan: Principal Applied Researcher, Microsoft MT team Hyderabad; founding member and co-lead of AI4Bharat [V] https://anoopkunchukuttan.gitlab.io/. Dabre: Senior Research Scientist, Google Research Australia; Adjunct Faculty IIT Madras (AI4Bharat); Honorary Visiting Asst. Prof. IIT Bombay CFILT [V] https://prajdabre.github.io/.
- Aksharantar (Findings EMNLP 2023) [22]: 26M transliteration pairs, 21 languages, 12 scripts; 103k-pair test set; IndicXlit "improves accuracy by 15% on the Dakshina test set" [V]. Code: https://github.com/AI4Bharat/IndicXlit (MIT) [V].
- Bhasha-Abhijnaanam / IndicLID (ACL 2023 short) [33]: "first LID for romanized text in Indian languages" [V]. Data on HF, CC0-1.0 [V].
- RomanSetu (ACL 2024) [60]: continual pretraining on romanised text "reduces token fertility by 2x-4x" and matches or beats native script; romanised embeddings align more closely with English [V].
- IndicRAGSuite (arXiv 2025, WIP) [53]: IndicMSMarco plus training data (Prasanjith, More, Kunchukuttan, Dabre) [V]. Dataset `ai4bharat/IndicMSMarco`, MIT [V].
- IndicTrans2 (arXiv 2305.16307, "Accepted at TMLR") [48] [V].

**2. Microsoft Research India.** Bali [V] https://www.microsoft.com/en-us/research/people/kalikab/; Sitaram [V] https://www.microsoft.com/en-us/research/people/susitara/. Choudhury moved to MBZUAI as Professor of NLP; MSR India 2009–2022 per the MBZUAI bio [V-idx] https://mbzuai.ac.ae/study/faculty/monojit-choudhury.
- Gupta, Bali, Banchs, Choudhury, Rosso, SIGIR 2014 [21]: defines mixed-script IR; joint cross-script term model gives "12% increase in MRR and 29% increase in MAP" [V].
- Bali et al. 2014 [78] and Vyas et al. EMNLP 2014 [79]: LID and transliteration are "two major challenges" for code-mixed POS [V].
- GLUECoS (ACL 2020) [37]: Hi–En and Es–En benchmark incl. QA [V].

**3. FIRE MSIR organisers.** Saha Roy: now Senior Scientist, Fraunhofer IIS (Scholar shows a Fraunhofer IIS email; the FIRE 2013 coordinator role is on his old IIT KGP page https://cse.iitkgp.ac.in/~rishiraj/) [V-idx]. Rosso: UPV Valencia [V] https://personales.upv.es/prosso/. Papers [24][20][19] are [V-prior]. Banerjee et al. "MSIR@FIRE: A comprehensive report 2013–2016" (SN Comput. Sci. 2020) is still **[U]**.

**4. IReL IIT (BHU).** Sukomal Pal, Associate Professor [V] https://iitbhu.ac.in/dept/cse/people/spalcse. Supriya Chanda, Assistant Professor at Bennett University, PhD IIT (BHU) 2018–2024 [V] https://www.bennett.edu.in/faculties/dr-supriya-chanda/ and https://supriyachanda.github.io/. CMIR site and organisers [V] https://cmir-iitbhu.github.io/cmir/organizers.html. Chanda has also worked on Tamil/Malayalam code-mixed sentiment and sarcasm at FIRE (CEUR Vol-2826 T4-9) [V-idx].

**5. Galway + DravidianLangTech.** Chakravarthi: Lecturer, School of Computer Science, University of Galway; ORCID 0000-0002-4575-7934 [V] https://research.universityofgalway.ie/en/persons/bharathi-raja-asoka-chakravarthi/. McCrae [V] https://john.mccr.ae/. Priyadharshini at Gandhigram Rural Institute; Anand Kumar Madasamy at NITK; full list in the DravidianLangTech 2026 proceedings front matter [V-idx] https://aclanthology.org/2026.dravidianlangtech-1.0.pdf.
- DravidianCodeMix (LRE 56, 2022) [82]: over 60,000 YouTube comments, about 44,000 of them Tamil–English, high Krippendorff's alpha [V]. Data: https://github.com/bharathichezhiyan/DravidianCodeMix-Dataset [V].
- DravidianLangTech-2026 at ACL 2026 (San Diego; held virtually on Underline): 72 papers in the proceedings [V].

**6. SSN / SNU Chennai.** Thenmozhi D: Associate Professor, Dept. of CS, Shiv Nadar University Chennai (Kalavakkam); at SSN from 2000; PhD in NLP from Anna University; Associate Editor of ACM TALLIP; has organised shared tasks at FIRE, ACL, RANLP, NAACL and EACL [V] https://www.snuchennai.edu.in/faculty/dr-thenmozhi-d/. Her page lists "Ontology based Tamil–English Cross Lingual Information Retrieval System" (Sādhanā 2018) [84]. That listing was seen, but the paper itself was not opened, so treat [84] as **[U]** until checked.

**7. Google Research.** Roark [V] https://research.google/people/brianroark/. Kirov's Google page returned 404 **[U]**.
- Dakshina (LREC 2020) [31]: native-script Wikipedia text, romanisation lexicons and parallel sentences for 12 languages incl. Tamil [V]; CC BY-SA 4.0 [V] https://github.com/google-research-datasets/dakshina.
- Kirov et al. (CL 50) [32]: "3.3% absolute (18.6% relative) mean word-error rate reduction" over prior best full-sentence Latin-to-native transliteration on all 12 Dakshina languages [V].
- Benton et al. (EMNLP 2025) [34]: romanised LID F1 74.7 → 85.4 / 88.2 [V-prior].

**8. Glasgow Terrier.** Chari: PhD student working on multilingual and non-English IR [V] https://www.gla.ac.uk/pgrs/andreaschari/. MacAvaney: Reader [V] https://macavaney.us/. Code: https://github.com/andreaschari/transliterations (BGE-M3 fine-tuning scripts) [V]. Note that [28] covers no Indic language, so a Tamil replication is open.

**9. CFILT.** [V] https://www.cfilt.iitb.ac.in/; Bhattacharyya [V] https://www.cse.iitb.ac.in/~pb/. IndicIRSuite [52]: +47.47% MRR@10 [V-prior].

**10. JUNLP.** Dipankar Das: Associate Professor at Jadavpur since 2026; code-mixing listed among his specialisations on the department page [V-idx] https://cse.jadavpuruniversity.in/faculty/dipankar-das (personal site https://dasdipankar.com/ blocked). SAIL_Code-Mixed overview (Hi–En, Bn–En) [80] [V].

**11–13.** Shrivastava [V] https://www.iiit.ac.in/faculty/manish-shrivastava/; LTRC [V] https://ltrc.iiit.ac.in/. [36], [13] and [27] are [V-prior]. Kondrak's old page returned HTTP 410 **[U]**.

**14. CALCS.** Winata: Director of Applied Research, Capital One; interests include code-switching [V] https://gentawinata.com/. CALCS editions run 2014–2025, the 7th at NAACL 2025 [V] https://aclanthology.org/venues/calcs/. No 2026 or 2027 CALCS call was found **[U]**.

**15–16.** Sarvam-1 card lists Tamil [V] https://huggingface.co/sarvamai/sarvam-1; the licence field is empty on the HF API **[U]**. Krutrim [83] [V] https://arxiv.org/abs/2502.09642: "matches or exceeds models like LLAMA-2 on 10 out of 16 tasks, with an average score of 0.57 versus 0.55".

**17. Tamil LLMs.** Abhinand: GitHub location Chennai; tamil-llama repo (GPL-3.0; the instruct-v0.2 weights carry the Llama-2 licence on HF) [V] https://github.com/abhinand5/tamil-llama. Agaram [50]: Kumaresan at Murai Labs, Madhusudhanan G and Kezendirane listed as independent researchers; weights Apache-2.0; 1.55 vs 9.44 tokens per Tamil word; beats Sarvam-1 in all six FLORES directions [V]. On the separate paper [17], Madhusudhanan G is listed at Vellore Institute of Technology [V].

**18–19.** Papers [42]–[44] and [57] are [V-prior]. Author affiliations were not checked in this pass **[U]**.

---

## 2. Timeline 2013 → 2026

| Year | Milestone | Ref | Tag |
|---|---|---|---|
| 2013 | FIRE track on transliterated search (Hindi, Bangla, Gujarati, Roman-script lyrics queries) | [24] | V-prior |
| 2014 | Mixed-script IR defined at SIGIR; cross-script deep term model | [21] | V |
| 2014 | First CALCS workshop; English–Hindi code-mixing on Facebook; code-mixed POS with back-transliteration (EMNLP) | [78][79] | V |
| 2014 | DCU rule-based normalisation + fuzzy queries at FIRE MSIR | [25] | V-prior |
| 2015–16 | FIRE MSIR 2015, 2016; CMIR Hindi–English tweet corpus | [20][19][26] | V-prior |
| 2017 | SAIL code-mixed sentiment shared task at ICON (Hi–En, Bn–En) | [80] | V |
| 2018 | Code-mixed QA challenge; KBQA shows transliteration beats translation | [13][36] | V-prior |
| 2019 | Joint deromanisation of code-mixed text | [27] | V-prior |
| 2020 | Dakshina (12 languages incl. Tamil); GLUECoS; Tamil–English sentiment corpus; FIRE Dravidian-CodeMix | [31][37][7][8] | V / V-prior |
| 2021 | DravidianLangTech-1 at EACL: offensive language in Ta/Ml/Kn code-mixed text | [81] | V |
| 2022 | DravidianCodeMix journal dataset (≈44k Tamil–English) | [82] | V |
| 2023 | Aksharantar/IndicXlit; IndicLID (romanised LID); IndicTrans2; IndicCorp v2; Tamil-Llama; MIRACL (no Tamil); code-switching survey; context-aware transliteration (CL, online 2023) | [22][33][48][47][49][55][38][32] | V / V-prior |
| 2024 | RomanSetu; IndicIRSuite; CMIR@FIRE 2024 (Roman Bengali–English); PARIKSHA; HEALTH-PARIKSHA; Sarvam-1 | [60][52][9][73][74][51] | V / V-prior |
| 2025 | "Lost in Transliteration" (SIGIR); IndicRAGSuite; CMIR 2025 (mixed script; fusion wins); romanised LID with synthetic variation (EMNLP); Krutrim | [28][53][10][34][83] | V / V-prior |
| 2026 | Hinglish code-mixed RAG papers; CS-IR benchmark (Findings ACL); romanisation "aligns with neither" (ACL); query-embedding interpolation (ACL); Indi-RomCoM (incl. Tamil); TanglishMedBench; Agaram 2.5B (Tanglish); DravidianLangTech-6 at ACL; MAST@FIRE 2026 Indic agentic search | [42][43][44][11][61][62][41][57][50] | V / V-prior; MAST V-idx |

**The arc in one line.** Mixed-script IR (2013–16, Hindi/Bengali, lexical) became code-mixed NLP (2014–22, classification-heavy, with Dravidian corpora from 2020), then Indic neural retrieval (2023–25, native script), then code-mixed RAG (2026, Hinglish only). No published work yet covers romanised or code-mixed **Tamil** retrieval with relevance judgements. That is the gap this thesis fills (see survey §4).

---

## 3. Methods playbook: how each line of work did it, and what worked

All numbers come from the opened abstract, either in this pass [V] or in the earlier survey [V-prior]. "n/a" means the abstract gives no number.

| Method family | Representative work | How | Reported result | What it means for Tanglish RAG |
|---|---|---|---|---|
| **Cross-script term modelling** | Gupta et al. 2014 [21] | Native and Roman terms modelled jointly in a low-dimensional space; handles spelling variation | +12% MRR, +29% MAP over baselines [V] | A precedent for a learned cross-script matcher in place of hand rules |
| **Rule normalisation + fuzzy matching** | Ganguly et al. 2014 [25] | Rule-based normalisation at indexing; prefix-matched fuzzy query terms | ≈56% over a QL baseline [V-prior] | Supports the Tanglish rule normaliser for **lexical** retrieval |
| **Word/sentence transliteration models** | IndicXlit [22]; Kirov et al. [32]; TAMZHI [35] | Seq2seq on mined pairs (IndicXlit); ensembles with pretrained LMs on simulated parallel data (Kirov); hybrid rules for vowel-dropped Tamil (TAMZHI) | IndicXlit +15% accuracy on Dakshina [V]; Kirov −3.3 abs / −18.6% rel WER [V]; TAMZHI n/a | Use IndicXlit or Dakshina-trained models as the back-transliteration baseline against the rules |
| **Joint LID + deromanisation** | Riyadh & Kondrak [27] | Joint sequence prediction | SOTA for Bn/Hi (no Tamil in the published paper) [V-prior] | A neural alternative if the rules plateau |
| **Romanised LID / routing** | IndicLID [33]; Benton et al. [34] | Synthetic romanised training data; natural spelling noise | First romanised Indic LID [V]; F1 74.7 → 85.4/88.2 [V-prior] | Script/language gate for the query router |
| **Transliterate vs translate** | Gupta, Chinnakotla, Shrivastava [36]; Singh et al. [54] | Back-transliterate CM questions vs translate them | Back-transliteration +5% and +35% accuracy [V-prior]; Translate-Test beats direct multilingual LLMs [V-prior] | Test both: transliteration at retrieval, translation at generation |
| **Romanised fine-tuning ("transliterate-train")** | Chari et al. [28]; RomanSetu [60] | Fine-tune BGE-M3 on an even native + Latin mix; continual pretraining on romanised text | Script gap "nearly" closed (no number in abstract) [V-prior]; fertility 2–4× lower [V] | The strongest single Module 3 condition to try on Tamil |
| **Fine-tuned vs zero-shot embedders (CM RAG)** | Sharma et al. [43] | Hinglish → English docs | 96.3% vs 76.7% [V-prior] | Expect a large gain from even small Tanglish fine-tuning |
| **Normaliser + fine-tuning interaction** | Agarwal [46] | Factorial ablation | Normaliser redundant after noisy fine-tuning; sign unstable on Tamil probes [V-prior] | Report normaliser × fine-tune as a 2×2 |
| **Hybrid lexical + dense fusion** | Mishra et al. [30]; CMIR-2025 [10]; Bruch et al. [63]; Chauhan & Agarwal [64] | BM25 + SBERT re-rank; RRF vs convex combination | +83% over BM25 (MAP 0.054) [V-prior]; fusion wins in same-script CMIR [V-prior]; RRF parameter-sensitive [V-prior]; fusion hurts on 13–48% of queries [V-prior] | Fusion helps only when both lists carry signal; tune weights for cross-script |
| **Query-embedding interpolation** | Zhu et al. [62] | Mix embeddings of parallel queries | Beats best monolingual endpoint in 88/105 cases [V-prior] | Cheap alternative to fusion: interpolate Tanglish and Tamil-script query vectors |
| **LLM query rewriting** | Ma et al. [65]; Deroy & Maity [29]; HyDE [66] | Rewrite-Retrieve-Read; GPT prompting for CMIR; hypothetical documents | Rewriting is a trainable RAG stage [V-prior]; RetrieveGPT n/a; HyDE beats unsupervised dense SOTA [V-prior] | LLM "Tanglish → Tamil/English" rewriter as a baseline |
| **Native-script Indic dense IR** | IndicIRSuite [52]; IndicRAGSuite [53] | MT of MS MARCO; Indic-ColBERT | +47.47% MRR@10 [V-prior] | Native-script ceiling to compare against |
| **Tokenizer / generator choice** | Agaram [50]; Sarvam-1 [51]; Tamil-Llama [49]; Krutrim [83] | Tamil-first pretraining or vocabulary extension | 1.55 vs 9.44 tokens per Tamil word [V]; Krutrim 0.57 vs 0.55 avg on 16 tasks [V] | Generator shortlist for Module 4 |
| **Corpus building for code-mixed Tamil** | Chakravarthi et al. [7][82] | Crowd annotation of YouTube comments | High Krippendorff's alpha; ≈44k Ta–En [V] | Annotation protocol model for Tanglish qrels |
| **RAG evaluation** | RAGAs [69]; ARES [70]; Hada et al. [72]; PARIKSHA [73]; HEALTH-PARIKSHA [74]; NoMIRACL [75] | Reference-free metrics; light LM judges + PPI; human–LLM agreement | LLM judges inflate scores, worse for low-resource scripts [V-prior]; >88% hallucination on non-relevant sets [V-prior]; code-mixed queries challenge evaluators [V-prior] | Calibrate any LLM judge on a small human-labelled Tanglish set |

---

## 4. Datasets and resources

| Name | Language / script | Size | Task | Licence | Link | Tag |
|---|---|---|---|---|---|---|
| FIRE 2013 transliterated search | Hi/Bn/Gu, Roman + native | n/a | LID, back-transliteration, retrieval | n/s | via FIRE data archive https://fire.irsi.org.in/fire/static/data | V-prior (size **U**) |
| FIRE MSIR 2015/2016 | Hi–En mixed script | n/a | MSIR | n/s | https://ceur-ws.org/Vol-1587/T2-1.pdf ; https://ceur-ws.org/Vol-1737/T3-1.pdf | V-prior |
| CMIR (Chakma & Das) | Hi–En tweets | n/a | Code-mixed IR | n/s | doi 10.13053/cys-20-3-2459 | V-prior |
| CMIR@FIRE 2024/2025 | Bn–En (Roman; then mixed script) | 8 teams / 26 runs (2025) | Code-mixed IR | n/s | https://cmir-iitbhu.github.io/cmir/ | V |
| **Dakshina** | 12 South Asian incl. **Tamil**; native + Latin | lexicons + parallel sentences | Transliteration, LM | CC BY-SA 4.0 | https://github.com/google-research-datasets/dakshina | V |
| **Aksharantar** | 21 Indic, 12 scripts | 26M pairs; 103k test | Transliteration | "cc" on HF (variant not stated) | https://huggingface.co/datasets/ai4bharat/Aksharantar | V |
| IndicXlit models | 21 Indic | n/a | Transliteration | MIT | https://github.com/AI4Bharat/IndicXlit | V |
| Bhasha-Abhijnaanam | 22 Indic, native + romanised | HF size tag n<1K (files) | LID test set | CC0-1.0 | https://huggingface.co/datasets/ai4bharat/Bhasha-Abhijnaanam | V |
| IndicCMix | 11 Indic, code-mixed native + romanised | HF size tag n<1K | CM renderings | MIT | https://huggingface.co/datasets/ai4bharat/IndicCMix | V |
| **DravidianCodeMix** | Ta–En, Kn–En, Ml–En | ≈44k Ta–En; >60k total | Sentiment, offensive | n/s on pages opened | https://github.com/bharathichezhiyan/DravidianCodeMix-Dataset | V (licence **U**) |
| GLUECoS | Hi–En, Es–En | n/a | CS NLU incl. QA | n/s | doi 10.18653/v1/2020.acl-main.329 | V |
| IndicCorp v2 | 24 languages | 20.9B tokens | Pretraining | n/s | [47] | V-prior |
| INDIC-MARCO | 11 Indic incl. Tamil (MT) | MS MARCO scale | Dense IR training | n/s | [52] | V-prior |
| IndicMSMarco (IndicRAGSuite) | 13 languages incl. Tamil | 1,000 manually translated queries | Retrieval eval | MIT | https://huggingface.co/datasets/ai4bharat/IndicMSMarco | V |
| MIRACL | 18 languages (**no Tamil**) | 726k judgements | Retrieval | Apache-2.0 | https://huggingface.co/datasets/miracl/miracl | V |
| Indic-QA | 11 Indic | n/a | Context-grounded QA | n/s | [54] | V-prior |
| MURMUR | Tamil, Yoruba | n/a | Cross-lingual multimodal RAG | n/s | [56] | V-prior |
| **TanglishMedBench** | Tanglish + English | 700 QA pairs | Medical QA eval (no qrels) | n/s (Zenodo blocked) | doi 10.5281/zenodo.22308075 | V-prior (licence **U**) |
| **nlpctx tamil-english-retrieval** | Ta–En code-mixed | HF tag 1K–10K | Retrieval eval | Apache-2.0 | https://huggingface.co/datasets/nlpctx/tamil-english-retrieval | V |
| Indi-RomCoM | Hi, Bn, Gu, **Ta** romanised CM | 7 tasks × 3 mixing levels | LLM instruction eval | n/s | arXiv 2606.30790 | V-prior |
| CodeMixQA | 16 language-pair variants | n/a | CS QA | n/s | arXiv 2601.07153 | V-prior |
| Tamil-Llama weights | Ta + En | 7B/13B | Generation | Llama-2 licence (instruct v0.2) | https://huggingface.co/abhinand/tamil-llama-7b-instruct-v0.2 | V |
| Agaram 2.5B weights | Ta, Tanglish, En | 2.53B | Generation | Apache-2.0 | arXiv 2610.18420 | V |
| Lost-in-Transliteration code | multilingual | n/a | BGE-M3 transliterate-train | n/s | https://github.com/andreaschari/transliterations | V |

---

## 5. Networking plan

### 5.1 Top 15 people to connect with

The ranking reflects how directly each person's work bears on a Tanglish retrieval/RAG study, with a bonus for being local to Chennai.

| # | Person | Affiliation (verified) | Why relevant | Public profile | Tag |
|---|---|---|---|---|---|
| 1 | **Durairaj Thenmozhi** | Assoc. Prof., Shiv Nadar University Chennai (ex-SSN) | Tamil–English CLIR, DravidianCodeMix@FIRE organiser, TALLIP AE; same campus area as Chennai | https://www.snuchennai.edu.in/faculty/dr-thenmozhi-d/ | V |
| 2 | **Bharathi Raja Chakravarthi** | Lecturer, University of Galway | Built the Tamil–English code-mixed corpora; runs DravidianLangTech | https://research.universityofgalway.ie/en/persons/bharathi-raja-asoka-chakravarthi/ | V |
| 3 | **Andreas Chari** | PhD student, University of Glasgow | First author of the closest neural-IR precedent [28]; open code | https://www.gla.ac.uk/pgrs/andreaschari/ | V |
| 4 | **Supriya Chanda** | Asst. Prof., Bennett University | Leads CMIR@FIRE, the only code-mixed IR shared task with qrels | https://www.bennett.edu.in/faculties/dr-supriya-chanda/ | V |
| 5 | **Raj Dabre** | Google Research Australia; Adjunct IIT Madras | IndicRAGSuite and RomanSetu; Chennai link via AI4Bharat | https://prajdabre.github.io/ | V |
| 6 | Anoop Kunchukuttan | Microsoft; co-lead AI4Bharat | IndicXlit, IndicLID, RomanSetu, IndicRAGSuite | https://anoopkunchukuttan.gitlab.io/ | V |
| 7 | Sean MacAvaney | Reader, University of Glasgow | Senior author of [28]; IR methodology | https://macavaney.us/ | V |
| 8 | Sukomal Pal | Assoc. Prof., IIT (BHU) | CMIR senior organiser; FIRE 2025 host | https://iitbhu.ac.in/dept/cse/people/spalcse | V |
| 9 | Mitesh M. Khapra | IIT Madras, AI4Bharat | Indic resources at scale; Chennai | https://www.cse.iitm.ac.in/~miteshk/ | V |
| 10 | Sunayana Sitaram | Microsoft Research India | Multilingual RAG and LLM-judge evaluation [72]–[74] | https://www.microsoft.com/en-us/research/people/susitara/ | V |
| 11 | Monojit Choudhury | Professor, MBZUAI | Co-founded MSIR and code-mixing research [21][24][37] | https://mbzuai.ac.ae/study/faculty/monojit-choudhury | V-idx |
| 12 | Brian Roark | Google Research | Dakshina; context-aware transliteration | https://research.google/people/brianroark/ | V |
| 13 | Genta Indra Winata | Capital One | CALCS organiser; code-switching LLM benchmarks | https://gentawinata.com/ | V |
| 14 | Abhinand Balachandran | Independent / ML engineer, Chennai | Tamil-Llama; MedEmbed (domain embeddings) | https://github.com/abhinand5 | V |
| 15 | Ramchand Kumaresan & Madhusudhanan G | Murai Labs; VIT (independent on Agaram) | Only Tamil LM trained on Tanglish; Tanglish safety eval | https://arxiv.org/abs/2610.18420 (no homepage verified) | V |

Alternates: Kalika Bali (https://www.microsoft.com/en-us/research/people/kalikab/) [V]; Paolo Rosso (https://personales.upv.es/prosso/) [V]; Pushpak Bhattacharyya (https://www.cse.iitb.ac.in/~pb/) [V]; Ruba Priyadharshini (Gandhigram Rural Institute) [V-idx]; Dipankar Das (Jadavpur) [V-idx].

### 5.2 Venues and deadlines (2026–2027)

Checked against official pages on 31 Oct 2026. All ACL, SIGIR and ECIR deadlines are 23:59 AoE (UTC−12), which is 17:29 IST the following day.

| Venue | What / where | Key dates | Fit | Source | Tag |
|---|---|---|---|---|---|
| **ECIR 2027** | Southampton, UK, 21–25 Mar 2027 | **Resource papers 2 Nov 2026**; **DC abstract 2 Nov, DC paper 9 Nov 2026**; demos 2 Nov; notifications 7 Dec 2026. Full papers (5 Oct) have closed | A Tanglish qrels set fits the Resource track | https://www.ecir2027.co.uk/calls ; /call-for-resource-papers ; /call-for-doctoral-consortium-papers | V |
| **FIRE 2026** | ISI Kolkata, 17–20 Dec 2026 | Conference-track deadline passed (7 Sep 2026). Attend; MAST Indic track runs this year | Meet Pal, Chanda, Thenmozhi, Chakravarthi | https://fire.irsi.org.in/fire/2026/home ; /call_for_papers | V |
| **ICON 2026** + BHASHA workshop | Gauhati University, 20–23 Dec 2026 (BHASHA 20 Dec) | Paper deadline passed (4 Sep); notification moved to 10 Nov | Indian NLP community | https://www.icon2026.org/important-dates ; https://bhasha-workshop.github.io/ | V / V-idx |
| CODS 2026 (ex-CODS-COMAD) | 13–16 Dec 2026 | Paper deadline passed (20 Aug 2026) | Attend only | https://ikdd.acm.org/cods-2026/ | V |
| NAACL 2027 / COLING 2027 | San Francisco, 1–5 Jun 2027 / Macau, 9–14 May 2027 | ARR Oct cycle closed 12 Oct; **commitment 23 Dec 2026** (only for already-reviewed papers) | n/a for new work | https://2027.naacl.org/calls/main_conference_papers ; https://2027.eacl.org/calls/workshops/ | V |
| **ACL 2027** (ARR Jan cycle) | Kyoto, 17–22 Aug 2027 (workshops 18–19 Aug) | **ARR submission 4 Jan 2027**; commitment TBA | Main or Findings; ACL workshops (DravidianLangTech has run at ACL 2022 and 2026) | https://2027.aclweb.org/ | V |
| **SIGIR 2027** | San Jose, USA, 18–24 Jul 2027 | **Abstract 14 Jan 2027; full paper 21 Jan 2027** (marked "PROPOSED"); short/resource tracks TBA | Short or resource paper on the Tanglish script gap | https://sigir2027.org/pages/submit-full.html | V |
| **Interspeech 2027** | São Paulo, 29 Aug–2 Sep 2027 | **Paper 9 Feb 2027**; update 16 Feb | Only if a voice-query extension is added | https://interspeech2027.org/calls/call_for_papers/ | V |
| EACL 2027 | Athens, 9–14 Mar 2027 | Main deadlines passed; some workshop CFPs close 15–23 Dec 2026 | Low fit | https://2027.eacl.org/calls/papers/ | V |
| **DravidianLangTech 2027** | Not yet announced. ACL 2027 workshop page empty on 31 Oct 2026 | 2026 pattern: direct submission 5 Mar, ARR commitment 24 Mar, held with ACL | Best-fit workshop | https://sites.google.com/view/dravidianlangtech-2026/home (2026 page) | 2026 V; 2027 **U** |
| **FIRE 2027** | Not yet announced | 2026 pattern: track proposals 15 Apr, runs by 30 Jun, working notes 30 Aug | Propose a "Tanglish CMIR / RAG" track, or join CMIR | FIRE 2026 track timeline (ELRA corpora list) | 2026 V-idx; 2027 **U** |
| CALCS | Last held 2025 (NAACL) | No 2026/2027 call found | Watch | https://aclanthology.org/venues/calcs/ | V / **U** |
| LREC | LREC 2026 held 11–16 May 2026; ELRA is collecting hosting expressions of interest for 2028/2030 | Next main-conference dates not set | Resource-paper venue in 2028 | https://www.elra.info/elra-events/lrec/ | V |

**ARR policy note.** From Oct 2026, ACL Rolling Review caps submissions to reviewer capacity and requires a qualified "service contributor" per submission [V-idx] https://aclrollingreview.org/cfp. A student first author needs a supervisor or co-author who can serve. Check this before the 4 Jan 2027 ACL deadline.

### 5.3 Cold email template (draft only; nothing sent)

> **Subject:** Feedback request: Tanglish (romanised Tamil–English) retrieval for RAG
>
> Dear Dr./Prof. [Surname],
>
> I am Selvin PaulRaj K, an M.E. (CSE, AI) student at Kings Engineering College, Chennai, and an Associate Data Analyst in AI automation at Zinnov. My thesis studies retrieval for RAG when queries are written in Tanglish (romanised, code-mixed Tamil–English) and documents are in Tamil script or English.
>
> Your work on [specific paper, e.g. "transliterate-train for BGE-M3" / "DravidianCodeMix" / "CMIR@FIRE"] shaped my design. My current results show [one-line finding, e.g. "dense retrievers lose most of their accuracy on romanised Tamil queries, and equal-weight RRF fusion hurts cross-script retrieval"].
>
> Would you be willing to look at a 2-page summary (attached) and tell me whether the evaluation setup is sound, or point me to work I have missed? Even a short reply would help a great deal. I am happy to share the code and the small Tanglish test set.
>
> Thank you for your time.
>
> Kind regards,
> Selvin PaulRaj K
> M.E. CSE (AI), Kings Engineering College, Chennai
> jobwithjoe@gmail.com | https://selvinpaulraj.vercel.app

Tips: one specific paper per email; attach the 2-page summary only; send in the recipient's working hours. For Galway and Glasgow, that is about 14:30–22:30 IST while the UK is on GMT (until late March 2027).

---

## 6. Gaps and cautions from this pass

- **No one has built Tamil-romanised retrieval qrels.** None of the groups above has published romanised or code-mixed Tamil retrieval with relevance judgements. CMIR is Bengali; [28] has no Indic language; IndicRAGSuite and INDIC-MARCO are native script. This confirms survey gap G1 (HIGH).
- **Moves since the earlier survey:** Thenmozhi is now at SNU Chennai (FIRE 2025 notes still list SSN); Supriya Chanda is now at Bennett University; Raj Dabre is now at Google Research Australia (still adjunct at IITM); Choudhury is at MBZUAI; Saha Roy appears to be at Fraunhofer IIS [V-idx].
- **Unverified in this pass:** affiliations of the Hinglish-RAG [42]–[44] and TanglishMedBench [57] authors; Sarvam-1 licence; DravidianCodeMix licence; Kirov and Kondrak homepages; DravidianLangTech 2027 and FIRE 2027 dates; the MAST@FIRE 2026 details (search excerpt only).

---

## 7. New references found in this pass (IEEE, continuing from [77])

[78] K. Bali, J. Sharma, M. Choudhury, and Y. Vyas, "'I am borrowing ya mixing?' An analysis of English-Hindi code mixing in Facebook," in *Proc. First Workshop on Computational Approaches to Code Switching*, 2014, pp. 116–126, doi: 10.3115/v1/W14-3914. [V: OpenAlex abstract + ACL BibTeX]

[79] Y. Vyas, S. Gella, J. Sharma, K. Bali, and M. Choudhury, "POS tagging of English-Hindi code-mixed social media content," in *Proc. 2014 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, 2014, pp. 974–979, doi: 10.3115/v1/D14-1105. [V]

[80] B. G. Patra, D. Das, and A. Das, "Sentiment analysis of code-mixed Indian languages: An overview of SAIL_Code-Mixed shared task @ICON-2017," arXiv:1803.06745, 2018. [V: arXiv abstract]

[81] B. R. Chakravarthi, R. Priyadharshini, N. Jose, A. Kumar M, T. Mandl, P. K. Kumaresan, R. Ponnusamy, H. R L, J. P. McCrae, and E. Sherly, "Findings of the shared task on offensive language identification in Tamil, Malayalam, and Kannada," in *Proc. First Workshop on Speech and Language Technologies for Dravidian Languages*, 2021, pp. 133–145 (ACL Anthology 2021.dravidianlangtech-1.17). [V]

[82] B. R. Chakravarthi, R. Priyadharshini, V. Muralidaran, N. Jose, S. Suryawanshi, E. Sherly, and J. P. McCrae, "DravidianCodeMix: Sentiment analysis and offensive language identification dataset for Dravidian languages in code-mixed text," *Language Resources and Evaluation*, vol. 56, pp. 765–806, 2022, doi: 10.1007/s10579-022-09583-7. [V: OpenAlex abstract]

[83] A. Kallappa *et al.*, "Krutrim LLM: Multilingual foundational model for over a billion people," arXiv:2502.09642, 2025. [V: arXiv abstract]

[84] D. Thenmozhi and C. Aravindan, "Ontology based Tamil–English cross lingual information retrieval system," *Sādhanā*, vol. 43, art. 157, 2018, doi: 10.1007/s12046-018-0942-7. **[U]**: listed on the author's official page; abstract not opened. Open it before citing.

Working files for this pass: `litsurvey/raw/map/` (fetch scripts, URL check lists, JSON records under `v/`).
