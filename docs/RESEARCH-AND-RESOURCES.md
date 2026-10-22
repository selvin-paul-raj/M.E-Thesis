# AVA Evaluation — literature and resources register

**Last updated:** 22 October 2026
**Status:** Pass 3 is open. The specification explicitly says that no source has yet met its level-P verification standard. Earlier AEON notes sometimes say “read in full” or “verified”; those labels need source-by-source reconciliation, not automatic promotion.

## A. Mandatory Pass 3 sources

| Work | Current lead | What to verify in the full text | Status |
|---|---|---|---|
| Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents | Ding et al., [arXiv:2606.30306](https://arxiv.org/abs/2606.30306) | Exact scope/taxonomy; whether it covers assertion-level conflict, semantic resolution, abstention, and evaluation gaps; check cited primary studies. AEON notes say body §§1–12 and Appendix A were read, references skimmed; apply the project's P standard and log page-level evidence. | Pass 3 reconciliation pending |
| StateFuse | [arXiv:2607.05844](https://arxiv.org/abs/2607.05844) | Event-log/projection model, conflict preservation, resolution semantics, safety claims, limits and relationship to AVA's Agree/Verify/Abstain policy. | Required full-text read pending |
| TOKI | [arXiv:2606.06240](https://arxiv.org/abs/2606.06240) | Concurrency-control model, temporal operators, write-path decisions, evaluation setup and whether its treatment subsumes AVA's decision layer. | Required full-text read pending |
| S-Bus | [arXiv:2605.17076](https://arxiv.org/abs/2605.17076) | Read-set reconstruction/isolation guarantees, topology/workload conditions, and how semantic conflict handling differs from AVA. | Required full-text read pending |
| Semantic Consensus Framework (SCF) | Acharya et al., [arXiv:2604.16339](https://arxiv.org/abs/2604.16339) | Exact task, conflict labels, methods, abstention/verification path, data and metrics. AEON marks the source VERIFIED and a full-text note exists; reconcile against level P and record exact passages. | Pass 3 reconciliation pending |
| CodeCRDT | [arXiv:2510.18893](https://arxiv.org/abs/2510.18893) | Separate mechanical convergence from semantic correctness; validate conflict-rate, speed and setup claims and assess how closely the task matches assertional state. | Required full-text read pending |

## B. Mandatory search / novelty attack

- Review NLI and contradiction-detection literature relevant to same-key structured assertions, including dataset construction, pairwise labels, calibration, and known failure modes. Record the exact primary papers and benchmarks found rather than treating this line as one source.
- Explicitly attack WH-1 and the other working hypotheses in the novelty-analysis file. Search for systems that already combine same-key conflict classes, semantic matching, evidence-aware verification, abstention, and distributed evaluation.
- Complete a novelty matrix at level P. For each candidate, compare task/key model, labels, decision actions, evidence path, concurrency/event model, metrics, dataset, and result. State which parts are exact overlap, partial overlap, or genuinely different; retain citations and limitations.
- Do not use abstracts, secondary citations, a title match, or an empty search result to establish that a contribution is novel or absent.

## C. High-priority counterexamples and adjacent work

These are leads from the existing AEON search and must be checked as primary sources when relevant; their mention does not establish findings.

| Work | Lead | Why it matters to the novelty attack |
|---|---|---|
| MELD | [arXiv:2608.16357](https://arxiv.org/abs/2608.16357) | AEON's prior search describes a merge/relate/conflict pair taxonomy and false-merge rate. It is a direct counterexample candidate for pair labels and FMR. |
| Selective QA over Conflicting Multi-Source Personal Memory | [arXiv:2605.30087](https://arxiv.org/abs/2605.30087) | Possible resolver-by-input factorial design and abstention; compare task and evaluation carefully. |
| Judge, Retrieve, or Abstain | [arXiv:2608.17994](https://arxiv.org/abs/2608.17994) | Possible overlap in selective decision policies, evidence retrieval and abstention. |
| MemoryAgentBench | See exact record and links in `AEON/departments/research/papers.md` | Candidate external-validity set; determine whether its task can test multi-agent assertional conflicts or is only a single-agent memory benchmark. |
| Other sources from RES-005 | `AEON/departments/research/lit-search-2026-10-13-res005.md` | Reuse the recorded search and queries. Recheck fast-moving sources and avoid duplicating discovery; follow exact primary links from the record. |

## D. Reconciliation ledger rules

For each source, record: canonical title/authors/venue or repository; DOI/arXiv/version; full-text location and access date; exact sections/pages read; claimed result and quoted evidence; sample/task/method; limitations; AVA dimension compared; verification level and reviewer. Correct a previous record only with an evidence trail. If a paper cannot be obtained, record the attempted route and keep the dependent novelty claim unresolved.

Existing AEON records conflict in scope: `projects/me-project.md` says seven papers were read in full; `papers.md` and `RES-002` say several sources were verified; the supplied 22 October AVA specification says no paper is level P. These statements may reflect different standards or different source sets. Reconcile, do not erase either history or assume equivalence.

## E. Resource checklist

- **Sources:** lawful full-text access; citations and page-level notes; no full copyrighted papers committed here.
- **Annotation:** written codebook, at least three independent annotators as planned, adjudication, and a justified agreement statistic. Availability, compensation and ethics approval remain unknown.
- **Data:** provenance/licensing for synthetic, generated and real-trace levels; leakage-safe splits; public release only for material that may be shared. Private or personal traces require consent, minimization and a restricted approved store.
- **Models:** pinned embedding/NLI versions; fixed judge model/prompt/temperature where supported; repeated trials; Jev access and API terms to be established. Do not put provider credentials in GitHub.
- **Compute:** measure local hardware, runtime, memory, API calls and costs during a pilot. No GPU or paid-API requirement is assumed; no spending until an explicit budget is approved.
- **Reproducibility:** environment lockfile, deterministic seeds, event traces, versioned dataset manifests, tests, analysis scripts, and provenance for every result.
- **Institutional:** supervisor, official template/module names, rubric, review timing, submission requirements and deadline. All remain unknown until sourced.
