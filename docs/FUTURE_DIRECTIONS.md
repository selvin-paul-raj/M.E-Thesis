# Future Directions (Modules 3–5 and PhD)

## Module 3 — Real data and normalisation
- Human-written Tanglish question set (~200–500, collected with a Google Form from students)
- Longer real documents: TN scholarship notices, Government Orders (G.O.s), so chunking matters
- Baselines: IndicXlit (Aksharantar) neural transliteration and an LLM query rewriter, against the rule normaliser
- Entity-safe language ID (keeps names like *Talaq* or *Rajya* in English), and phonetic-skeleton BM25 (ல/ள/ழ, ன/ண/ந, ர/ற)
- **Concept-space retrieval:** add Meta's SONAR sentence space (from Large Concept Models, arXiv 2412.08821; Mimir, arXiv 2605.25263) as a retriever arm

## Module 4 — Script-gated RAG system (headline)
Tanglish query → script detector → normaliser → router (BM25-char3 / e5 / SONAR) → reranker → LLM answer → faithfulness check
- JEV (TypeSafe) as a low-cost relevance judge, router gate and answer-faithfulness gate
- Contextual chunk headers (contextual retrieval) and multilingual rerankers

## Module 5 — Paper
Target: FIRE / DravidianLangTech / a code-switching workshop.

## Beyond the M.E. (PhD seeds)
- Next-Concept Modeling (Stanford, arXiv 2610.14162): fast coarse-to-fine generation for low-cost Tanglish bots
- Tanglish voice agents, code-mixed prompt-injection safety, on-device small models
