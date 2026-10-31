# AVA Evaluation

## Agree, Verify, or Abstain: Conflict Resolution for Assertional State in Multi-Agent AI Systems

**Research Area:** Distributed Systems & Multi-Agent AI **Degree:** M.E. Computer Science and Engineering **Research Type:** Empirical Evaluation + System Prototype **Framework Name:** AVA Evaluation **Experimental Environment:** SCP-MA **Status:** Structure locked (naming, decision model, metrics). Underlying novelty and literature-gap claims remain **provisional pending Pass 3** full-text literature verification, per the project's own novelty-analysis and literature-review documents. Not yet authorized for implementation or paper drafting.

---

## 1. Abstract

Multi-agent AI systems increasingly allow multiple autonomous agents to work concurrently on a shared task. When agents independently produce information about shared state, they may generate assertions that are identical, compatible, outdated, or mutually contradictory. Traditional distributed-system mechanisms such as CRDTs can provide mechanical convergence, but convergence of replicas does not necessarily imply semantic correctness.

This research proposes **AVA Evaluation — Agree, Verify, or Abstain**, an empirical framework for studying how multi-agent AI systems should handle conflicting assertions over **assertional state**: single-valued facts associated with a state key where competing values may represent a logical conflict.

The study compares deterministic rules, embedding-based methods, Natural Language Inference (NLI), hybrid semantic methods, LLM-as-a-Judge, a System-One structured decision model (**Jev**), and conflict-preserving abstention. Methods are evaluated on false-merge rate, false-conflict rate, classification performance, confidence calibration, latency, computational cost, and distributed convergence behavior.

A decentralized environment based on the **SCP-MA** design is used as the evaluation vehicle — a reproducible environment with concurrent agents, asynchronous communication, event reordering, duplication, delay, and eventual reconciliation.

The research does not assume semantic AI methods will outperform deterministic ones. A negative result (deterministic beats semantic) is considered a scientifically valid and reportable outcome, consistent with the project's falsifiability commitment.

---

## 2. Naming Reference (Locked)

| Term | Meaning |
| --- | --- |
| **AVA Evaluation** | The research/evaluation framework — the scientific question of *when a multi-agent system should agree, verify, or abstain* |
| **SCP-MA** | The decentralized multi-agent experimental environment used to test AVA under asynchronous, faulty network conditions. Not claimed as a novel protocol. |
| **Jev** | The specific System-One structured decision model evaluated as arm B6. "System-One" is the category/concept; Jev is the particular instance. Always written as **Jev (System-One decision model)** on first use to avoid confusion with the unrelated tic-tac-toe project of the same name. |

**Thesis title:** AVA Evaluation: An Empirical Study of Conflict Resolution for Assertional State in Multi-Agent AI Systems **College registration title:** Conflict Resolution for Assertional State in Multi-Agent AI Systems

**Internal definition:** *Conflict Resolution = Classification + Decision + Verification + Abstention.* The title is kept simple for registration purposes; the research is broader than picking a winner.

---

## 3. Background

Multi-agent AI systems are moving from centralized orchestration toward architectures where multiple agents independently perform tasks, exchange information, and maintain shared state without a designated leader.

The core problem: two agents produce different assertions about the same fact (e.g., `database = PostgreSQL` vs. `database = DynamoDB`). A distributed system may successfully replicate both events to every replica — but **replica convergence does not automatically imply semantic correctness.**

Literature reviewed so far (verification level A — abstracts/partial text only, not yet level P) indicates this distinction is real: CodeCRDT reports mechanical convergence with a persistent 5–10% semantic conflict rate; other work reports low precision in semantic conflict detection (SCF: 65.2% detection at 27.9% precision) and, in at least one comparison, deterministic resolution outperforming LLM-judgment pipelines by +10.8 to +21 percentage points. These are **working hypotheses**, not established findings, until Pass 3 full-text verification is complete.

AVA focuses on the decision that occurs **after disagreement is detected**.

---

## 4. Problem Statement

A group of independent AI agents maintains shared operational state. Each agent may observe information, generate or update an assertion, receive another agent's assertion, encounter stale information, operate temporarily without communication, or reconnect later.

When two assertions concern the same state key, the system must determine their relationship — one of four classes (§6). The research is scoped to **same-key assertional conflicts**, not general open-domain contradiction detection, and not cross-key intent conflicts (§13).

State is split into two classes:

$$S_i = (A_i, Q_i)$$

- **(A_i) — Additive state:** mergeable facts (logs, observations, discovered entities). Standard CRDT structures (G-Set, OR-Set). **Not claimed as novel.**
- **(Q_i) — Assertional state:** single-valued facts per key where competing values can genuinely conflict. This is the primary research object.

An assertion: (q = (k, v, a, c, t)) — key, value, originating agent, causal metadata (vector clock), logical timestamp.

---

## 5. Research Objective

**Primary objective:** To empirically evaluate how different decision mechanisms classify and resolve conflicting assertions produced by independent AI agents, and determine when a system should agree, verify, or abstain.

**Secondary objectives:**

- Construct a labeled assertional-conflict dataset
- Establish deterministic and semantic baselines
- Evaluate NLI, embedding-based, and hybrid approaches
- Evaluate LLM-as-a-Judge and Jev (System-One)
- Measure confidence calibration
- Measure false-merge and false-conflict rates separately
- Build a reproducible decentralized evaluation environment (SCP-MA)
- Evaluate behavior under asynchronous distributed conditions

---

## 6. Research Questions

**Primary:** When two agents produce different assertions about the same state key, can decision mechanisms reliably determine whether those assertions actually conflict, and when should the system agree, verify, or abstain?

| # | Question |
| --- | --- |
| RQ1 | How accurately can different decision mechanisms classify assertion pairs as paraphrase, compatible, soft conflict, or hard conflict? |
| RQ2 | Do semantic methods outperform deterministic alternatives for assertional conflict classification? |
| RQ3 | Can confidence-aware decision policies reduce unsafe automatic merges while maintaining a practical resolution rate? |
| RQ4 | How do semantic models, LLM-as-a-Judge, and Jev (System-One) compare in accuracy, calibration, latency, and cost? |
| RQ5 | How do these mechanisms behave in a decentralized environment with concurrent updates, delay, duplication, reordering, and reconnection? |
| RQ6 | How do conflict-resolution strategies behave as agent count, event count, and conflict rate increase? |
| RQ7 (ablation) | Does historical agent reliability (trust-weighting) improve resolution quality under heterogeneous agent reliability? |

---

## 7. Four Conflict Classes

| Class | Description | Example A | Example B |
| --- | --- | --- | --- |
| **Paraphrase** | Same fact, different wording | "PostgreSQL is the selected database" | "The project uses PostgreSQL" |
| **Compatible** | Different facts, no real conflict | "PostgreSQL stores transactions" | "DynamoDB stores session metadata" |
| **Soft Conflict** | Genuinely different, resolvable by policy | "Service uses API v1" | "Service is migrating to API v2" |
| **Hard Conflict** | Mutually exclusive, unsafe to auto-merge | `database = PostgreSQL` | `database = DynamoDB` |

---

## 8. AVA Decision Model (Locked)

**AVA defines three policy actions: Agree, Verify, and Abstain. Verify is an intermediate action — it is not a fourth terminal outcome.** Successful verification terminates in Agree; unsuccessful verification terminates in Abstain. Results are therefore reported at two levels: policy-action rates and final resolution outcomes.

- **Policy actions:** (A = {\\text{Agree}, \\text{Verify}, \\text{Abstain}})
- **Terminal outcomes:** (O = {\\text{Agree}, \\text{Abstain}}), with (\\text{Verify} \\rightarrow {\\text{Verified_Agree}, \\text{Abstain}})

```text
                    ASSERTION PAIR
                          │
                          ▼
                    AVA DECISION
                 ┌────────┼────────┐
                 ▼        ▼        ▼
              AGREE     VERIFY   ABSTAIN
                 │        │        │
                 │        ▼        │
                 │  Deterministic  │
                 │  evidence check │
                 │     │      │    │
                 │    YES    NO    │
                 │     │      │    │
                 └─────┘      └────┘
                    │             │
                    ▼             ▼
                  AGREE        ABSTAIN
```

### Definitions

- **Agree:** Sufficient evidence exists to automatically reconcile the assertions. Recorded as `direct_agree`.
- **Verify:** The system does not immediately merge or select an assertion. It performs a second-stage check using available evidence — provenance, timestamps, causal metadata, or an independent deterministic policy. If evidence supports a confident resolution, the system resolves to `verified_agree`; otherwise it abstains.
- **Abstain:** Safe resolution is not justified. The competing assertions are preserved (`UNRESOLVED`), not deleted or guessed. *Principle: when evidence is insufficient, do not fabricate a merged state.* (This principle is not itself claimed as novel — it is already present in StateFuse and TOKI.)

**Important:** Verify is *not* the deterministic timestamp/agent-ID tiebreak — that rule is arm **B1**. Verify asks "can we obtain enough additional evidence to safely decide?"; B1 asks "which assertion wins by a predefined rule?" Keeping these separate is what gives AVA its own identity distinct from the underlying classifier arms.

### Determinism constraint (convergence-critical experiments)

For **convergence-proof-bearing experiments only**, the Verify stage must use exclusively deterministic evidence sources (provenance, timestamps, causal metadata, deterministic rules) — **no live non-deterministic model call inside the convergence-critical decision path.** Two replicas receiving identical inputs must reach identical Verify outcomes, or the deterministic-convergence proof obligations do not hold for that arm.

Model-based Verify (NLI/LLM/Jev inside the Verify stage) is a **separate, explicitly non-convergence-safe experimental condition**, valid for the classification benchmark (Phase 3) but excluded from the convergence simulator (Phase 1/5) unless made deterministic via decision caching/replay.

---

## 9. Experimental Arms

AVA compares seven experimental arms for the underlying classification/resolution decision:

| Arm | Method | Notes |
| --- | --- | --- |
| B1 | Deterministic | `argmax(timestamp, agent_id)`. Strong baseline, not a strawman. |
| B2 | Embedding | Cosine similarity of assertion embeddings. High similarity ≠ logical compatibility — must be measured, not assumed. |
| B3 | NLI | Entailment / contradiction / neutrality estimate. |
| B4 | Hybrid (SCS) | (\\alpha(1-\\text{CosSim}) + \\beta D). Formulation itself is under test, not assumed optimal. |
| B5 | LLM-as-a-Judge | Requires fixed model/version, fixed prompt, controlled temperature, repeated trials, and variance reporting due to non-determinism risk. |
| B6 | **Jev (System-One Decision Model)** | Structured decision questions (e.g., "are these paraphrases?", "can both be true?", "is auto-merge safe?") rather than free-form generation. Research question: does it provide a useful accuracy/calibration/cost trade-off vs. B3–B5? |
| B7 | Conflict-Preserving / Abstention | StateFuse-style: flags non-identical values as `UNRESOLVED` rather than picking a winner. Safety baseline. |

---

## 10. Metrics

### Classification

Accuracy, Precision, Recall, Macro F1, Per-class F1.

### Safety (reported separately — never folded into one composite score)

| Metric | Definition |
| --- | --- |
| **False-Merge Rate (FMR)** | Incorrect Agree outcomes (via direct-Agree *or* verified-Agree) on genuinely conflicting cases, over all actual conflicting cases |
| **False-Conflict Rate (FCR)** | Failure to safely resolve genuinely Paraphrase/Compatible cases — includes unnecessary abstention — over all actual Paraphrase + Compatible cases |
| **Unnecessary-Abstention Rate** | Subset of FCR: cases where the system abstained after Verify on a case whose ground truth was Paraphrase or Compatible |

$$FMR = \\frac{\\text{incorrect Agree decisions on actual conflicts}}{\\text{actual conflicting cases}} \\qquad FCR = \\frac{\\text{incorrect conflict handling on actual resolvable cases}}{\\text{actual Paraphrase + Compatible cases}}$$

**Note on double-counting:** Unnecessary-abstention cases are deliberately counted in *two* metrics at once — their own rate, and as a contributing case to FCR. These metric categories are not mutually exclusive and do not sum to 100%; this is intentional (it isolates the failure mechanism while still reflecting it in the overall conflict-resolution error), not an artifact to be reconciled.

### Pathway breakdown

| Metric | Captures |
| --- | --- |
| Direct-Agree rate | Cases resolved without verification |
| Verify rate | Cases routed through verification |
| Verified-Agree rate | Verify cases successfully resolved |
| Verify→Abstain rate | Verify cases with insufficient evidence |
| Overall Abstain rate | All final Abstain outcomes |

### Calibration (for probabilistic methods, esp. Jev and probabilistic NLI)

Expected Calibration Error, Brier Score, reliability diagrams, risk-coverage curves, selective accuracy, abstention rate.

### Cost

Latency, inference time, token usage, API calls, computational cost, throughput.

### Distributed (within SCP-MA)

Convergence rate, convergence latency, state divergence, message count, bytes transferred, recovery time, duplicate-processing handling, partition recovery.

---

## 11. SCP-MA Evaluation Environment

SCP-MA is the decentralized experimental scaffold — **not claimed as the primary novel contribution.**

**Fault model — included:** cooperative agents, stale information, slow/delayed/duplicated/reordered messages, temporary disconnection and reconnection, concurrent updates. **Fault model — excluded (future PhD work):** Byzantine/adversarial agents, permanent network partitions, cross-key intent reasoning.

**Design commitment (resolves DC-1, rollback vs. monotonic progress):** No destructive rollback is used for semantic conflict. State is projection-time resolved from an immutable event log: `Immutable Event History → Projection → Resolved Value OR UNRESOLVED`. This avoids the tension between rollback and CodeCRDT's monotonic-progress requirement.

**Convergence requirement (target, not yet proven — see §14):** If all replicas eventually receive the same valid event set (E), and `Resolve` is a deterministic pure function of the canonicalized event set, then (State_i = Resolve(Canonicalize(E)) = State_j) for all replicas, regardless of arrival order, duplication, delay, or reconnection timing. Deterministic convergence must be validated on a semantics-free simulator *before* the semantic/AVA layer is added.

---

## 12. Dataset

Each record: `id, state_key, assertion_a, assertion_b, agent_a, agent_b, context, temporal_context, evidence, gold_label, difficulty` (+ optional domain, lexical_overlap, semantic_similarity, temporal_relation, source_quality, ambiguity).

**Construction levels** (results reported separately per level):

1. Controlled synthetic examples
2. LLM-generated realistic examples
3. Real agent traces (where legally/practically available)

**Ground truth:** multi-annotator process (3 annotators → agreement measurement via Cohen's kappa / Fleiss' kappa / Krippendorff's alpha, as appropriate → adjudication → gold label). Ground truth is **not** generated by another LLM alone.

---

## 13. Scope Boundaries

The M.E. thesis will **not** attempt to solve:

- General distributed consensus
- Open-domain NLI
- Universal truth verification
- Byzantine/adversarial multi-agent AI
- Cross-key intent conflicts (e.g., SCF's refund-issued vs. account-held example — a different resource/key pair producing a jointly invalid state; structurally undetectable by a same-key model)
- Autonomous organizational governance

These are explicit scope boundaries, not solved problems, and are reserved for potential PhD extension.

---

## 14. Current Status of Novelty & Literature Claims

**This section exists specifically to prevent overclaiming.** Per the project's own documents:

- No paper in the literature review has yet been read at verification level **P** (full text) — all analysis is level A (abstract/partial) or S (secondary mention, not citable).
- The research gap (§ Working Hypotheses WH-1/WH-2/WH-3 in the novelty analysis) is a **working hypothesis to be actively attacked**, not an established finding. The project must not claim "nobody has done this" until Pass 3 verification is complete.
- The convergence property (§11) is a **target theorem**, not a completed proof. Formal-model obligation 3 (determinism of `classify()`/Verify across replicas) is an **open risk**, mitigated in design (decision caching, or restricting convergence claims to deterministic arms) but not yet resolved in implementation.
- **Explicitly not yet authorized:** protocol implementation, thesis writing, paper drafting (per novelty-analysis Go/No-Go, §7). Mandatory preconditions before implementation: full-text reads of Always-On Agents survey, StateFuse, TOKI, S-Bus, SCF, CodeCRDT; NLI/contradiction-detection literature review; an active attempt to disprove WH-1; a completed novelty matrix with level-P verification.

---

## 15. Falsifiability

AVA does not assume semantic methods are superior. All of the following are valid, reportable outcomes: Deterministic > Semantic; Semantic > Deterministic; Jev > LLM-Judge; NLI > Jev; no single method dominates. A negative result (deterministic wins) is a complete, reportable finding — not a failure requiring reframing after the fact.

---

## 16. Experimental Phases

1. **Literature** — complete Pass 3 full-text reads (see §14); attempt to disprove the research gap
2. **Dataset** — construct and validate the labeled assertion-pair dataset
3. **Classification benchmark** — implement and compare B1–B7
4. **Calibration** — confidence, ECE, Brier, risk-coverage, abstention analysis
5. **Distributed simulator** — build SCP-MA (agents, event model, vector clocks, additive/assertional state, async network faults)
6. **Integration** — connect all seven decision methods to SCP-MA
7. **Scalability** — (N \\in {2,4,8,16,32}); vary event count, conflict rate, delay, duplication, state size
8. **Analysis** — determine, as open research questions (not predetermined rankings): most accurate, safest, best-calibrated, cheapest, fastest, most stable method; when AVA should abstain

---

## 17. Expected Artifacts

1. **AVA Dataset** — labeled assertional-conflict dataset
2. **AVA Evaluation Framework** — reproducible benchmark comparing decision mechanisms
3. **SCP-MA Simulator** — decentralized test environment
4. **Experimental Results** — correctness, safety, calibration, cost, latency, distributed-behavior measurements

Potential thesis contributions (finalize only after experimentation — do not pre-promise all five): a benchmark for assertional-conflict classification; a controlled comparison across deterministic/semantic/generative/structured approaches; an empirical FMR-vs-FCR analysis; an evaluation of confidence-aware Agree/Verify/Abstain policies; a reproducible decentralized evaluation environment.

---

## 18. Core Scientific Principle

> **Do not assume the intelligent method is better. Measure it.**