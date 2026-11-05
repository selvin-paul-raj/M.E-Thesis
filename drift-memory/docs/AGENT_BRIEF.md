# Agent brief: "Memory Rewrites Do Not Drift, They Collapse"

Paste this whole document to the agent as its working brief. Selvin remains the author and is responsible for every claim; the agent does the engineering and analysis and reports back honestly.

## 0. Rules for the agent (read first)

1. **Never invent or estimate a number.** Every number that goes into the paper must come from a script in the repo and a saved CSV or log. If you cannot reproduce a number, say so and mark it UNVERIFIED.
2. **Never change an existing result silently.** If a new analysis disagrees with a number in the draft (v6), list both values and the cause in `CHANGELOG_RESULTS.md`.
3. **Do not tune on the held-out data.** Anything fixed in advance (thresholds, rules, margins) is written in `PREREGISTRATION.md` with a date and git commit before the run.
4. **Log everything**: prompts, model names, versions, decoding settings, seeds, cache keys, timestamps, provider errors. Failed runs are reported, not dropped.
5. **Report negative and null results.** Do not make the story prettier than the data.
6. **Flag uncertainty.** If a step needs a decision from Selvin (a threshold, a model choice, a claim to drop), stop and ask with options and a recommendation.
7. **Do not invent or add citations.** Only cite papers whose text Selvin has opened and checked.
8. **Scope freeze.** Work only on this paper. Do not start Render-from-Raw, Tanglish, LAG-Mem or other projects until this paper is submitted.

## 1. Direction and scope

**One-sentence claim (to be earned, not assumed):** In streaming LLM-rewritten memory, loss is mostly front-loaded, and the harmful failures are rare single-step collapses that a length signal detects; a retry-with-fallback guard helps when collapses are rare and does not help when they are frequent.

**What is solid:** the bimodal length-ratio distribution, the model-free detector, and honest negative results.

**What is currently weak (the work below fixes these):**

- p-values treat questions as independent although they are clustered in conversations.
- "Collapse" is defined by length, not by lost facts.
- Collapses may be caused by the 1,200-word cap in the writer prompt.
- The guard lacks control arms.
- "No compounding" rests on pilots and few rewrites per stream.
- LongMemEval is incomplete (23 of 30) and inconclusive.
- Scale claim rests on two models of one family.
- The only judge is gpt-oss-120b with no human validation.

**Target deliverable:** a revised paper whose every claim is supported at the right unit of analysis, plus a reproducible repo.

## 2. Work packages, in priority order

Each package ends with **Done when** criteria. Do them in this order. Packages A to D use mostly cached data and need few or no new model calls.

### A. Reproducibility audit (do first)

- Rebuild every table in v6 (Tables 1 to 6) from the cached outputs and CSVs using the scripts in the repo (`stream_pilot.py`, `a7_locomo.py`, `a8_retry_only.py`, `a9_analysis.py`, `a10_hybrid.py`, `a11_longmemeval.py`, `a13_second_writer.py`, `boot.py`).
- Produce `AUDIT.md` with a row per table cell: paper value, recomputed value, script, match yes/no.
- Specifically resolve these known issues:
  1. The "Pooled (190 q)" row: state exactly how questions and Memora rubric checks are weighted, and fix the label.
  2. LongMemEval: 39 collapses but 48 guard triggers; LoCoMo/Memora: 13 collapses but 16 guard triggers. Explain (guarded trajectories diverge from plain ones) and show it with a table of triggers per stream.
  3. 17.4% appears as both the LongMemEval collapse rate and stream accuracy; verify both.
  4. "The whole gap came from three conversations": compute the exact share of the gap from collapsed vs other conversations.
- **Done when:** every cell is matched or has a documented discrepancy, and `make tables` regenerates all tables from raw outputs.

### B. Statistics at the correct unit of analysis

The independent unit is the **conversation / persona / instance (cluster)**, not the question.

- For every contrast in Tables 2 and 3, compute per-cluster mean accuracy for each arm, then the paired per-cluster difference.
- Report: mean paired difference, **cluster bootstrap 95% CI (10,000 resamples of clusters)**, and an **exact paired sign-flip permutation test** over clusters (2^n sign flips for n clusters; use all of them for n up to about 20).
- Report n clusters next to every result (LoCoMo 10, Memora 9, LongMemEval 23 instances).
- Mark which contrasts are **confirmatory** (declared in advance: g-bnd vs stream on held-out LoCoMo; g-bnd vs stream pooled) and which are **exploratory**. Apply **Holm correction** within the confirmatory family and say so.
- For "no compounding" and "stream is not worse than k0", run an **equivalence test (TOST)** with a margin declared in advance (default: 5 accuracy points; Selvin confirms). If the CI is too wide to establish equivalence, say "no evidence of difference; underpowered", not "indistinguishable".
- Collapse rates: report **per-stream** rates, and a cluster bootstrap CI over streams. State clearly that the 351 rewrites are not independent (13 events in 6 of 19 streams).
- Keep question-level bootstrap only as a sensitivity analysis, labelled as such.
- **Done when:** a new `stats_cluster.py` outputs a single CSV of all contrasts with cluster CIs, permutation p-values, Holm-adjusted p-values and n clusters, and a short note says which headline claims survive.

### C. Fact-level validation of "collapse"

Goal: show whether a length drop really means lost facts, and whether the detector misses fact loss that does not show up as length drop.

- Build a **reference fact set** per stream: for LoCoMo, facts from the gold evidence turns of the evaluation questions; for all benchmarks, also the k0 notes (one fact per line). Keep this fixed and independent of the arm being tested.
- For each memory state M\_t (every rewrite), compute **fact survival** = fraction of reference facts (those introduced up to session t) still entailed by M\_t. Use an LLM entailment check with a fixed prompt (see section 3 for the judge protocol) and, as a cross-check, a lexical-overlap or NLI check on a random 20% subset.
- Define a **fact-loss event**: survival drops by at least 30 points in one rewrite (declare the number in advance; also report 20 and 40 as sensitivity).
- Report the 2x2 table: length-collapse (yes/no) vs fact-loss event (yes/no), with **precision and recall of the length detector**. Include the non-collapse rewrites that still lost many facts.
- Report median survival for collapsed vs non-collapsed rewrites.
- Run the fixed-content (kn) experiment on the main Nemotron writer for k = 0, 1, 2, 4, 8, 16 using the same fact-survival metric, so "loses facts once, then fixed point" is shown with the main model and more rounds, not only the pilot.
- **Done when:** one figure (survival vs rewrite step for collapsed and normal streams), one 2x2 table, and one fixed-content curve with at least 16 rounds are produced from scripts.

### D. Cap-confound analysis and experiment

Hypothesis to test: collapses are triggered by the prompt's "keep under {cap} words" instruction when memory is at or above the cap.

- For every rewrite, log `old_len`, `new_len`, `cap`, `old_len/cap`, `new_len/old_len`.
- Plot collapse probability against `old_len/cap` (binned) and fit a simple logistic regression of collapse on `old_len/cap` with stream as a cluster.
- Run a **new subset** (the 6 collapsed LoCoMo/Memora streams plus 4 random uncollapsed ones, 30B writer, temperature 0) under three prompt variants: cap 1,200 (original), cap 2,400, and no word cap. Same sessions, same reader and judge.
- Report collapse counts for each variant per stream.
- **Done when:** the answer to "is collapse mainly a cap artifact?" is stated with the evidence, and the paper text matches it either way.

### E. Guard controls (isolate what actually helps)

Run on held-out LoCoMo (all 10 conversations) and Memora (9 personas), same writer, reader, judge:

1. `stream` (existing)
2. `guard-bounded` (existing)
3. `preserve-always`: use the "keep every existing fact unless contradicted" prefix on **every** rewrite, no detection
4. `floor-reject`: if a rewrite collapses, discard it and keep the old memory (skip the session's update), no retry
5. `length-matched`: stream with the cap raised so mean memory length matches guard-bounded

Report accuracy, mean and max memory length, number of extra writer calls, all at cluster level (section 2B). The question answered: does detection plus retry beat simply preserving more or simply refusing bad rewrites?

- **Done when:** a table of the five arms with cluster CIs exists, and the conclusion about the guard is rewritten to match.

### F. Completeness and generality

- **LongMemEval:** rerun the 7 lost instances (retry on provider errors, log them). Then try to extend to at least 60 instances if budget allows. If provider errors persist, say so and keep it labelled as an inconclusive probe. Do not draw a mechanism conclusion ("crowds out knowledge updates") unless supported by a per-question analysis, for example separate accuracy for knowledge-update and temporal questions.
- **Second writer family:** run `stream` and `guard-bounded` with one more open model family of similar size (for example Llama or Qwen, 30B to 70B class) on LoCoMo and Memora. Same reader. Report collapse rate per family.
- **Scale claim:** run the 550B writer on the 7 Memora personas that were lost. Do not write "fades with scale" unless there are at least three writer sizes; otherwise phrase it as "the 550B writer did not collapse in our runs".
- **Reader and batching:** rerun one benchmark with single-question reads for all arms to check the effect of batching 10 questions per call.
- **Done when:** the limitations section can honestly say which of these were done.

### G. Hybrid section (lowest priority)

- If time permits, add the missing comparison **guarded memory alone vs hybrid** with single-question reads, so the section's question is actually answered. Otherwise move the section to an appendix and retitle it "raw retrieval vs hybrid".

## 3. LLM-as-judge protocol

The current judge (gpt-oss-120b) is the single point of failure for every accuracy number. Treat it as a measurement instrument that must be validated.

### 3.1 Judge design

- **Fixed judge prompt**, temperature 0, JSON output with fields `verdict` (0/1) and `reason` (one sentence). Store the prompt text with a hash. Do not change it after the main runs start.
- **Inputs to the judge:** question, gold answer, predicted answer. Nothing else. The judge never sees the memory text, the arm name, the model name, or other arms' answers.
- **Blinding and order:** shuffle the evaluation order across arms so no arm is judged in a block. Judge each answer independently (no pairwise comparison across arms unless a separate pairwise study is declared).
- **Rubric (Memora):** judge each rubric check separately; aggregate per question; keep per-check results.
- **Treat "unknown" explicitly:** record the reader's "unknown" rate per arm separately from wrong answers. Collapsed memories may produce more "unknown", which interacts with the judge.
- **Date and format tolerance:** the prompt already allows different date formats; add 10 worked examples (5 equivalent, 5 not equivalent) in the prompt and keep them fixed.

### 3.2 Validation of the judge

1. **Human audit sample.** The agent draws a stratified random sample of **150 judged items** (balanced across arms, benchmarks and correct/incorrect verdicts), strips arm labels, and writes `audit_for_human.csv` with columns: id, question, gold, predicted. **Selvin labels them himself** (0/1) without seeing the judge verdict. The agent must not label them.
2. **Agreement metrics:** percent agreement, Cohen's kappa, and the confusion matrix of judge vs human. Report false-positive and false-negative rates **per arm**, not only overall, to check the judge does not favour one arm (for example longer or more verbose answers).
3. **Second judge from a different family.** Re-judge **all** answers with one other strong model of a different family. Report inter-judge kappa. The main contrasts must be recomputed with each judge.
4. **Deterministic cross-check.** For short-answer questions, compute normalised exact match and token-level F1 against the gold answer. Report how often they agree with the LLM judge, and recompute the main contrasts using them as a sensitivity analysis.
5. **Judge sensitivity table:** rows = main contrasts (stream vs k0, g-bnd vs stream, g-bnd vs k0, guard on LongMemEval); columns = judge A, judge B, deterministic metric, human-labelled subset. The paper only claims results whose **sign and rough size hold under all of them**.
6. **Self-preference check:** the judge, reader and writer should not be the same model. If any pair shares a family (the Nemotron reader and Nemotron writer already do), say so and, where possible, repeat the main result with a reader from another family.

### 3.3 Acceptance thresholds (declare now, report honestly)

- Judge-human kappa of 0.7 or more is acceptable. Below 0.6, fix the judge prompt (before the confirmatory reruns) or report the limitation prominently.
- Any arm with a false-positive or false-negative rate more than 10 points away from another arm is flagged as a judge bias.

## 4. Test methodology rules (apply to every experiment)

- **Units of analysis:** cluster = conversation (LoCoMo), persona (Memora), instance (LongMemEval). All inference is at this level.
- **Fixed in advance (write in `PREREGISTRATION.md`, commit before running):** collapse rule (rho = 0.5, floor = 300 words), fact-loss threshold (30 points), equivalence margin (5 points), confirmatory contrasts, judge prompt hash, model versions, seeds, number of bootstrap resamples (10,000).
- **Held-out discipline:** the guard was designed after seeing Memora collapses. Treat LoCoMo (10 conversations) and LongMemEval as held-out. For any **new** guard variant, design it on Memora only and test once on untouched data.
- **Controls and ablations:** every claimed benefit needs the nearest control that would produce it without the claimed mechanism (section 2E).
- **Seeds and repeats:** temperature 0 gives one trajectory per stream. Run **3 seeds at temperature 0.7** on the 6 collapsed units plus 4 uncollapsed to show whether collapse is a stable property of the unit or a random event. Report per-seed collapse counts.
- **Multiplicity:** Holm correction for the confirmatory family; label everything else exploratory.
- **Missing data:** provider errors are logged and retried up to 3 times; units that still fail are listed in a table and excluded from all arms equally (not per arm).
- **Reproducibility:** all model calls cached by prompt hash; `make all` rebuilds the tables; release scripts, prompts and per-question CSVs.

## 5. Paper changes the agent may draft (Selvin reviews and edits)

- Soften: "no compounding" to "no evidence of compounding within N rewrites"; "statistically indistinguishable" unless TOST supports it; "fades with writer scale" unless three sizes are tested; "rule fixed in advance" to match the Limitations section.
- Rewrite the abstract to about 150 words, leading with the finding, and with cluster-level results only.
- Fix the "17.4%" duplication, the "190 q" label, and "the whole gap" wording.
- Add: per-stream collapse rates, fact-survival results, cap analysis, guard control table, judge validation table, equivalence test results.
- Precisely position against Zhang et al. (2026), Zerhoudi et al. (2026, "compaction cliff") and Dongre et al. (2025): say what is new (streaming conversational memory, bimodal length distribution, model-free detector, guard) and what is not.
- Add an AI-assistance disclosure sentence (Selvin edits wording; check the target venue's policy).

The agent **drafts**; Selvin rewrites the introduction, discussion and limitations in his own words and verifies each claim.

## 6. Deliverables and checklist

Create these files in the repo and keep them updated:

- `PREREGISTRATION.md` (dated, committed before confirmatory runs)
- `AUDIT.md` (table-by-table reproduction, package A)
- `CHANGELOG_RESULTS.md` (every number that changed and why)
- `stats_cluster.py` and `results/contrasts.csv` (package B)
- `fact_survival.py` and figures (package C)
- `cap_analysis.py` and the three-prompt experiment outputs (package D)
- `guard_controls/` outputs (package E)
- `judge/` folder: judge prompt and hash, `audit_for_human.csv`, agreement report, judge sensitivity table (section 3)
- `STATUS.md`: what is done, running, blocked, and what needs Selvin's decision

**Reporting format after each work package (keep it short):**

1. What was run (script, commit, models, seeds).
2. Main numbers with cluster CIs.
3. Anything that disagreed with the draft.
4. Decisions needed from Selvin.

## 7. Definition of done for the paper

The paper is ready to share when: all tables are reproducible from a clean checkout; every headline result is at the cluster level with Holm-adjusted p-values where confirmatory; the judge is validated by human audit and a second judge; fact loss and cap analyses are in; the guard controls are reported; weak claims are softened or supported; and Selvin can explain the pipeline, the collapse rule, the guard and the judge without notes.

## 8. Suggested order and rough effort

1. A (audit) then B (cluster statistics): mostly cached data, days not weeks.
2. C (fact survival) and the judge protocol in section 3 (needs Selvin's 150 human labels).
3. D (cap) and E (controls): new model calls, moderate cost.
4. F (completeness and second family): largest cost; do what the budget allows and report the rest as limitations.
5. Rewrite the claims and abstract last, after the results are in.
