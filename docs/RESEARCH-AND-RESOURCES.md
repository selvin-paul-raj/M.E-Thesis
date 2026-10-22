# AVA Evaluation — literature and resources register

**Last updated:** 22 October 2026
**Status:** Pass 3 is incomplete. Selected passages from primary full-text versions have been checked and an evidence matrix is available at [Pass 3 evidence matrix](PASS-3-EVIDENCE-MATRIX-2026-10-22.md). This is useful partial progress, not a completed level-P review. No novelty finding is admitted.

## A. Mandatory Pass 3 sources

| Work | Primary lead | Verification needed | Checkpoint status |
|---|---|---|---|
| Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents | Ding et al., [arXiv:2606.30306](https://arxiv.org/html/2606.30306v1) | Reconcile survey scope and AOEP against all sections, full search protocol, appendices and references; follow cited primary studies where they threaten the exact AVA claim. | Full HTML retrieved; selected taxonomy, validation, evaluation-protocol and limitation sections inspected. Not read end-to-end; not P-complete. |
| StateFuse: Deterministic Conflict-Preserving Memory for Multi-Agent Systems | Volkov, Li and Luo, [arXiv:2607.05844](https://arxiv.org/html/2607.05844v1) | Compare all resolver semantics and appendices directly to AVA Verify/Abstain and the proposed simulator. | Main paper reviewed broadly; §§3–6 and selected formal appendix excerpts checked. Appendices/supplements remain; not P-complete. |
| TOKI: A Bitemporal Operator Algebra for Contradiction Resolution in LLM-Agent Persistent Memory | Wang, [arXiv:2606.06240](https://arxiv.org/html/2606.06240v1) | Complete operator, temporal, concurrency and evaluation comparison; specifically assess await-confirmation and evidence-weighted operators against Verify. | Full text retrieved; abstract, §2.1, §3 and selected §4/§6/appendix passages inspected. Not complete; not P-complete. |
| S-Bus: Automatic Read-Set Reconstruction for Multi-Agent LLM State Coordination | Khan, [arXiv:2605.17076](https://arxiv.org/html/2605.17076v2) | Complete formal guarantees, workload conditions, evaluation and limitation comparison; keep its structural race scope separate from semantic conflict. | Full text retrieved; selected abstract, §§1–3, experiment, limitations and Table 9 inspected. Not complete; not P-complete. |
| Semantic Consensus: Process-Aware Conflict Detection and Resolution for Enterprise Multi-Agent LLM Systems (SCF) | Acharya, [arXiv:2604.16339](https://arxiv.org/html/2604.16339v1) | Verify all labels, detector/resolver path, data generation, controls, metric denominators, result tables and threats. | Full text retrieved; selected §§4–8 and Table 2/limitations checked. The 65.2% figure is recall; 27.9% is precision; F1 39.0. Not complete; not P-complete. |
| CodeCRDT: Observation-Driven Coordination for Multi-Agent LLM Code Generation | Pugachev, [arXiv:2510.18893](https://arxiv.org/html/2510.18893v1) | Complete convergence method and manual semantic-conflict sampling; retain the authors' uncertainty. | Full text retrieved; selected §§4.3, 5, 6.4, 7.2 and conclusion checked. The ~5–10% is a preliminary manual estimate from 60/600 runs, not a validated persistent rate. Not complete; not P-complete. |

## B. High-priority prior-art and NLI checks

| Work | Primary lead | Why it matters / checkpoint status |
|---|---|---|
| MELD: A Protocol for Merging Knowledge Across Distributed Agentic Memories | Lovén et al., [arXiv:2608.16357](https://arxiv.org/html/2608.16357v1) | Closest pair-classification overlap: merge/relate/conflict/no-relation and reported FMR. Selected §§4, 6.5, 7.2, 7.4, 9.1 and experiment-inventory excerpts checked; full source not complete. |
| LatticeMind: A Conflict-Aware Memory Primitive for Multi-Agent Systems | Zhou et al., [arXiv:2608.08236](https://arxiv.org/html/2608.08236v1) | Keyed state claims, evidence/time/status, contested alternatives and reconciliation overlap AVA's setting. Selected main/appendix sections checked; not a same-key pair-classification benchmark; not complete. |
| KC-Bench: A Dynamic Interactive Benchmark for Evaluating Knowledge Conflicts in LLM Agents | Lyu et al., [arXiv:2609.03588](https://arxiv.org/html/2609.03588v1) | 238 multi-turn conflict tasks with tools and trajectory-level safety evaluation. Adjacent to, but not identical with, pair classification or replica convergence. Selected abstract, taxonomy and evaluation-scope excerpts read. |
| SubtleMemory: A Benchmark for Fine-Grained Relational Memory Discrimination in Long-Horizon AI Agents | [arXiv:2606.05761](https://arxiv.org/html/2606.05761v3) | Relation-controlled long-horizon memory benchmark, including complementary, nuanced and contradictory relations; not an isolated assertion-pair classifier. Selected construction/scoring excerpts read. |
| ECon: On the Detection and Resolution of Evidence Conflicts | [arXiv:2410.04068](https://arxiv.org/html/2410.04068v1) | Prior evidence-pair detection/resolution work and NLI/LLM comparison. Selected abstract, §§2–3, Table 2 and results excerpts read; complete comparison remains. |
| Don't Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution | Reddy and Challaram, [arXiv:2606.01435](https://arxiv.org/html/2606.01435v1) | Matched FactConsolidation comparison reports +10.8 pp at fact-level and +21 pp at 262K, but changes resolver, prompt, format and temperature together; not a causal estimate of resolver effect. Selected primary abstract and §5 excerpts read. |
| On Reference (In-)Determinacy in Natural Language Inference (REFNLI) | Chen et al., Findings of NAACL 2025, [ACL Anthology PDF](https://aclanthology.org/2025.findings-naacl.450.pdf) | 1,143 claim/evidence pairs including 135 reference-ambiguous cases; important for distinguishing true contradiction from context mismatch. PDF excerpts on labels, counts and agreement read; not end-to-end. |
| Adversarial NLI (ANLI): A New Benchmark for Natural Language Understanding | Nie et al., [arXiv:1910.14599](https://arxiv.org/abs/1910.14599) | NLI robustness benchmark. Only bibliographic/abstract evidence checked in this pass; full text still required before detailed claims. |
| Temporal Natural Language Inference: Evidence-based Evaluation of Temporal Text Validity | Hosokawa, Jatowt and Sugiyama, ECIR 2023, [paper PDF](https://ds-informatik.uibk.ac.at/lib/exe/fetch.php?media=wiki:ecir-tnli.pdf) | 10,659 temporal-validity sentence pairs and SUPPORTED/INVALIDATED/UNKNOWN labels; adjacent temporal/unknown precedent, not multi-agent state. Task/data excerpts read; not end-to-end. |

See the [evidence matrix](PASS-3-EVIDENCE-MATRIX-2026-10-22.md) for exact task scopes, overlap, selected sections, claim corrections and limitations. No row is described as a complete level-P review in this checkpoint.

## C. Active novelty attack

- Test WH-1, WH-2 and WH-3 separately. Their exact current wording is recorded in `AEON/departments/research/research-gaps.md`; do not replace those definitions with a vague claim that the area is “new.”
- Treat MELD as the closest direct prior-art threat to four-way claim-pair classification and FMR. Test whether the remaining distinction is substantive rather than relabeling.
- Compare Verify directly against StateFuse's deterministic projection-time resolver and TOKI's await-confirmation/evidence-weighted operators. These may narrow or defeat a general “verification/abstention is novel” claim.
- Use the NLI and temporal datasets to improve a scoped codebook, not to claim AVA's operational labels already have validated agreement.
- Decide whether AVA remains defensible only after all mandatory full-text checks, a source-by-source novelty matrix, and an active search designed to disprove each hypothesis. Outcome may be retain, narrow, reframe or abandon; no result is predetermined.

## D. Design issues to settle before dataset work

1. The specification's “compatible” example assigns PostgreSQL and DynamoDB to different roles. That is not a same-key pair unless role/scope is encoded in the key. Make the key schema explicit and use genuinely same-key examples.
2. Define “soft” and “hard” conflict as annotatable relationship labels, separately from the later Agree/Verify/Abstain policy. Record edge cases for scope, time, version, role and insufficient evidence.
3. Define whether pair classification can see context and provenance, and what additional evidence Verify may consult. Keep experimental inputs fixed across arms where possible.
4. Predefine FMR/FCR denominators, Verify pathway counts, adjudication rules and treatment of ambiguous ground truth; do not combine the safety rates into a score.
5. Establish sample-size/power and annotation-capacity rationale before constructing the main dataset; a pilot is not a powered final result.

## E. Resources and limits

- Full text: use lawful public or institutionally available copies; preserve exact version and page/section notes; do not commit copyrighted PDFs.
- Annotation: three independent annotators and adjudication are planned; availability, compensation and ethics approval are unknown.
- Data: synthetic and generated cases first; real traces only with appropriate authorization, minimization, and approved restricted storage. Public release requires licenses/consent.
- Models: pin embedding/NLI versions and fixed LLM-judge configuration; Jev access, provider terms and budget remain unknown. No paid use without an explicit budget decision.
- Compute: begin with a reproducible CPU-capable pilot after gates; estimate actual runtime/memory/API cost before requesting resources.
- KEC: official college template, module titles, rubric, supervisor instructions, review time/venue and final submission deadline remain unknown. The working outline is not an official format.

## F. Current gate

Pass 3 remains OPEN. The literature identifies substantial direct and partial overlap. The candidate residual policy question is still unverified, and no implementation or thesis/paper drafting is authorized until the project gates are satisfied.
