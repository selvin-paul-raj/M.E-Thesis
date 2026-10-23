# AVA Evaluation — end-to-end thesis plan

**Owner:** Selvin PaulRaj K
**Programme:** M.E. Computer Science and Engineering, Kings Engineering College (August 2025–May 2027)
**Thesis title:** AVA Evaluation: An Empirical Study of Conflict Resolution for Assertional State in Multi-Agent AI Systems
**College registration title:** Conflict Resolution for Assertional State in Multi-Agent AI Systems
**Plan status:** Planning and evidence reconciliation only. The literature gap is provisional; implementation and thesis/paper drafting are gated.

## 1. Outcome

Deliver a defensible, reproducible M.E. thesis that evaluates how decision mechanisms handle same-key assertional conflicts and when they should Agree, Verify, or Abstain. Preserve the possibility that a deterministic baseline wins. Do not promise the expected contributions before the literature audit and experiments.

## 2. Non-negotiable gates

### Gate A — Pass 3 literature and novelty audit (must precede implementation or thesis/paper drafting)

1. Read the full texts named in the finalized specification: Always-On Agents survey, StateFuse, TOKI, S-Bus, SCF, and CodeCRDT. Also complete source-wide checks of the closest added threats: MELD, Governed Shared Memory, STALE, MemGraphRAG, AMA, TANGLE, Selective QA over Conflicting Multi-Source Personal Memory, LatticeMind, Memanto, and relevant NLI/selective-prediction work. For arXiv:2606.01435, use the latest v2 title and test the targeted executor-only ablation, not just the v1 headline whole-pipeline gain. Record exact versions, sections/pages actually read, methods/results, limitations, and whether each meets the project's level-P verification standard.
2. Complete an NLI/contradiction-detection and selective-prediction review, including ANLI, REFNLI, temporal NLI, TANGLE and selective QA; compare benchmark labels, calibration, abstention and coverage to the four AVA classes without assuming they are equivalent.
3. Actively search for counterexamples to the concrete AVA task and claims stated in the specification. The spec names WH-1/2/3 without defining them; do not invent wording or claim exact falsification until authoritative definitions are available. Treat MELD and other near-overlaps as counterexamples to investigate, not as proof of novelty or proof that no gap remains.
4. Apply the owner specification's explicit verification mapping source by source: A means abstract/partial text; P means full text; S means secondary mention. The 22 October statement that none had reached P is a starting status, superseded only for sources whose exact full-text coverage is now documented in the matrix. Record version, sections/pages, available appendices, and artifact limits; P does not mean independent reproduction. No finer operational checklist was found in the tracked project records.
5. Produce a novelty matrix with level-P evidence, scope comparisons, and an explicit outcome: retain, narrow, reframe, or abandon each gap claim. No “first,” “novel,” “unaddressed,” or “nobody has done this” claim before this gate is complete.

**Exit evidence:** dated source ledger, full-text verification notes, active counterexample search, completed novelty matrix, and a recorded go/no-go decision. If the gap does not survive, revise the research question before building.

### Gate B — Lock research design before collecting the main dataset

Resolve the documented design-review issues without silently changing the supplied specification: assertion-key/cardinality model; how compatible values fit a same-key task; whether “soft conflict” is a relation or a policy/context label; equality and edge-case handling; separation of classification from action-policy effects; evidence available to Verify; typed timestamps/causal metadata; B5/B6 model and prompt versioning; confidence outputs; FMR/FCR denominator and case scoring; sample-size/power rationale; annotation codebook and adjudication; late-event projection stability; and privacy/licensing for real traces.

Write a preregistration/protocol after Gate A: hypotheses, operational definitions, splits, methods, thresholds, seeds, planned comparisons, exclusions, sample size, analysis code, and treatment of missing or inconclusive outcomes. Pilot and revise the codebook before freezing it.

## 3. Ordered work plan

### Phase 0 — Prepare for the KEC Model Project reviews (now; dates in source notice)

The WhatsApp notice lists reviews on **24 and 26 October 2026**, asks for the first two modules to be completed and brought, and warns that nonattendance may bar semester review. No exact review time, module titles, official format, or submission channel is stated. A later message says the model-exam schedule was postponed; it does not explicitly postpone the Model Project reviews. Use the provisional outline in `REVIEW-OUTLINE.md`, compare it with any official KEC template, and keep the dated notice available. Do not represent the outline as the college's required format.

**User-only details to obtain when available:** official module/template names, review times and venue, supervisor's instructions, and the current status of the first two modules. The review notice is evidence of a near-term academic obligation; it does not prove attendance or module completion.

### Phase 1 — Literature and gap verification (Gate A)

Complete source-by-source Pass 3; map prior work against AVA's exact task, four classes, three policy actions, deterministic Verify constraint, safety metrics, and decentralized evaluation. Include direct competitors and adjacent selective prediction, NLI, memory conflict, and distributed-systems work, especially the newly identified TANGLE and Selective QA abstention results. Separate conceptual overlap from exact task overlap. Update the research questions only after the evidence is reconciled.
Use `RESEARCH-AND-RESOURCES.md` and the dated Pass 3 evidence matrix to track exact versions, passages read, quantitative-claim corrections and remaining checks. The matrix is a partial checkpoint, not a Gate A pass; no row marked partial should be promoted to level P without source-wide review. New close threats materially change the plan: Governed Shared Memory is a direct asynchronous same-key supersession study; STALE, MemGraphRAG and AMA add memory-update, evidence-repair and explicit Pass/Retry/Refresh precedents. They must be compared against the exact AVA task, not dismissed as adjacent by label alone.

### Phase 2 — Design audit and preregistration (Gate B)

Resolve the blocking definitions. Keep classification labels and terminal outcomes separate. Define the ground-truth and policy-action tables so Verify is an intermediate action, then report both path rates and final outcomes. Specify denominator and scoring examples for every safety metric. Have an independent reviewer challenge the protocol before the main dataset.

### Phase 3 — Dataset construction and validation

1. Freeze a written annotation guide with same-key rules, temporal scope, evidence/provenance, ambiguity, and class-boundary examples.
2. Build controlled synthetic cases first; then realistic generated cases with human review; add real traces only if lawfully available and ethically appropriate.
3. Use at least three independent annotators as planned; measure suitable agreement (Cohen's kappa for two annotators, Fleiss' kappa or Krippendorff's alpha for three or more, as justified), adjudicate disagreements, and document uncertainty.
4. Keep train/dev/test splits isolated by template/source and avoid leakage between paraphrase variants. Track provenance, licensing, generation prompts/model versions, exclusions, and adjudication.
5. Treat the approximately 100-pair pilot in the earlier AEON design review as a proposed pilot size, not a powered final sample. Determine the main sample size from the preregistered precision/power goal and annotation capacity.

### Phase 4 — Classification and resolution benchmark

Implement only after Gate A and Gate B. Compare the specified B1–B7 arms: deterministic timestamp/agent-ID rule; embeddings; NLI; hybrid SCS; fixed/versioned LLM judge with repeated trials; Jev (System-One decision model); and conflict-preserving abstention. Keep a common dataset and clearly distinguish each arm's classifier, confidence estimate, resolution policy, and Verify evidence. Report per-class metrics and every failure mode, not only aggregate accuracy. Freeze model/API versions and prompts where possible; record drift or unavailable services.

### Phase 5 — Calibration, safety, and cost

For probabilistic arms, report ECE, Brier score, reliability diagrams, risk-coverage and selective accuracy. Report false-merge rate, false-conflict rate, unnecessary-abstention rate, direct-Agree, Verify, verified-Agree, Verify-to-Abstain, and total abstention separately using predeclared denominators. Measure latency, tokens, API calls, compute, and throughput. Do not combine safety metrics into a single score.

### Phase 6 — Semantics-free deterministic SCP-MA simulator

Before connecting a semantic classifier, validate a semantics-free event-log simulator. Use immutable events and projection-time resolution; include concurrency, delay, duplication, reordering, disconnect/reconnect, and eventual reconciliation. Test the convergence property on deterministic canonicalization and resolution over identical event sets. Do not add destructive semantic rollback. Record seeds, event traces, convergence latency, divergence, message count, bytes, and recovery behavior.

### Phase 7 — Integrate and scale

Connect only methods whose behavior is compatible with each experiment's stated convergence claim. Deterministic Verify is required in convergence-proof-bearing experiments. Model-based Verify can be tested in the classification benchmark, and in a separately labeled non-convergence-safe condition; use decision caching/replay only if formally specified and tested. Run the preregistered agent counts N∈{2,4,8,16,32} and vary event count, conflict rate, network delay, duplication, and state size. Report exact environment and repeatability.

### Phase 8 — Analysis and thesis writing (only after gates and actual results)

Run the preregistered analysis, uncertainty estimates and robustness checks. Compare methods without changing hypotheses after seeing results; label exploratory follow-ups. Discuss negative and null results, failure cases, external validity, limitations, and scope boundaries. Only then draft the thesis and any paper, using the college's actual format and supervisor feedback. Final contribution claims must match what the experiments and literature audit establish.

### Phase 9 — Submission and archiving

Obtain the supervisor's sign-off and official deadlines/format; validate citations, permissions, data handling, reproducibility, code/data availability, and required forms. Archive exact source versions, environment lockfiles, seeds, analysis outputs, and final submitted artifact. The programme end month May 2027 is not a substitute for a confirmed submission deadline.

## 4. Resource plan (no unapproved spending)

| Resource | Needed for | Decision/status |
|---|---|---|
| Full-text papers and stable version records | Pass 3 and novelty matrix | Public/arXiv or institutionally accessible copies; cite/record metadata and notes, do not commit copyrighted full texts to this public repo |
| Annotation guide and 3 annotators | Gold labels and agreement | Annotator availability, expertise, compensation and ethics approval are UNKNOWN; do not claim collected labels |
| Dataset storage | Synthetic/generated/approved traces | Public repo may contain synthetic, licensed and anonymized material only; private/raw traces need an approved restricted location |
| Embedding and NLI implementations | B2–B4 | Select and pin model/library versions after source review; record hardware and configuration |
| LLM judge and Jev access | B5/B6 | Provider/model/version, API access, terms, privacy, rate limits and cost UNKNOWN; no paid use until a budget is approved |
| Compute environment | Benchmarks and simulator | Start with reproducible local CPU-capable baselines; decide GPU/API needs only after pilot and measure actual resource use |
| Version control and reproducibility | Code, data manifests, tests, experiment records | `selvin-paul-raj/M.E-Thesis` is the public thesis-plan repo; AEON remains the working research brain. Never commit credentials or private traces |
| KEC documentation | Review and final submission | Official template, module names, rubric, review times, supervisor, submission dates UNKNOWN; obtain from Selvin/college before final formatting |

## 5. Project controls

- Maintain one source register and one results ledger. For every literature statement, preserve provenance and verification level.
- Public commits may contain the plan, specification, synthetic examples, code, and safe metadata; never include API keys, passwords, private messages, personal identifiers, raw agent traces, or unlicensed papers.
- Keep existing AEON MAMC-Bench v0 seed results separate from AVA results. They are exploratory scaffold evidence, not a formal experiment or thesis finding.
- Preserve the current locked naming and metrics until a documented design review explicitly revises them. Flag contradictions instead of silently normalizing them.
- No implementation or thesis/paper drafting before Gates A and B. Planning, literature review, review preparation, source notes, and research design audit may proceed.

## 6. Open items that cannot be inferred

Supervisor and expectations; official KEC module/template/rubric; review times/venue; confirmed review status after the “model exam postponed” note; thesis submission date; annotator availability; budget and API access; approved location/permissions for any real traces. These stay UNKNOWN until a source or Selvin supplies them.
