# ANALYSIS PLAN (2026-11-05). Margins (5-pt TOST, 30-pt fact loss) were agent-proposed; owner confirmation pending. P1 section approved by owner 2026-11-05 17:22 IST.

Base commit: 42cb684 (local). Brief: docs/AGENT_BRIEF.md.

## Fixed rules
- Collapse: new_len <= 0.5 * old_len with old_len >= 300 words (rho=0.5, floor=300). Fixed since A6.
- Fact-loss event: line/fact survival drops >= 30 points in one rewrite (sensitivity 20, 40)..
- Equivalence margin (TOST): 5 accuracy points; 90% cluster-bootstrap CI inside +/-5..
- Bootstrap: 10,000 cluster resamples, seed 0. Permutation: exact 2^n sign flips over clusters.
- Clusters: conversation (LoCoMo), persona (Memora), instance (LongMemEval).
- Confirmatory family (Holm): bounded guard vs stream on held-out LoCoMo (10); bounded guard vs stream pooled (19). Everything else exploratory.
- Judge: openai/gpt-oss-120b, temperature 0, prompt as in code/pilot.py and code/memora_pilot.py (hash to be recorded in judge/).
- Missing data: provider errors retried; units still failing are listed and excluded from all arms equally.

## Honest timing note
- A15 (escalation guard) and A17 (preserve-always, floor-reject, no-cap) were STARTED on 2026-11-05 14:15-14:45 IST, BEFORE this file existed. They are exploratory, not confirmatory.
- The bounded guard was designed after seeing Memora collapses; LoCoMo and LongMemEval are the held-out sets for it.

## Weighting (owner decision A, 2026-11-05 17:22 IST)
- Primary: question-weighted. Each unit has 10 questions; a Memora question scores the mean of its rubric checks; unit accuracy is the mean over its 10 questions. This equals unit-weighted.
- Sensitivity, labelled as such: item-weighted (each LoCoMo question and each Memora check counts once).

## P1 trajectory replicates (owner decision B, 2026-11-05 17:22 IST). Committed before any P1 run.
- Units: all 19 (LoCoMo conv-26..50 as in A7, 10 conversations; Memora 9 personas as in A5, excluding academic_researcher). Same sessions, batching (LoCoMo 1, Memora 10 sessions per rewrite), held-out questions, reader prompt and judge as in A7/A5/A8.
- Models: writer and reader nvidia/nemotron-3.5-lightning-30b-a3b (NVIDIA NIM); judge openai/gpt-oss-120b (Groq) at temperature 0.
- Arms: stream and guard-bounded (A8 rule: on a collapse, new <= 0.5*old with old >= 300, retry once and keep the longer). Writer temperature 0.7, top_p 1.0. The reader stays at temperature 0.
- Seeds: run in rounds. Seed 1 on all 19 units in both arms, then seed 2, then seed 3. The seed is sent as the API `seed` and included in the cache key. If the endpoint ignores `seed`, cached outputs per seed still fix each trajectory.
- Confirmatory analysis uses seeds 1-3 only. Seeds 4 and 5 are an extension, reported separately, and never replace 1-3.
- Confirmatory family (Holm, two tests):
  (C1) guard-bounded − stream over all 19 units: per-unit mean over seeds 1-3 of (guard − stream) question-weighted accuracy; exact sign-flip over 19 units; 10,000-resample cluster bootstrap CI (seed 0).
  (C2) guard-bounded − stream on held-out LoCoMo (10 units), same procedure.
  The T=0 confirmatory results above remain as reported; P1 is a separate, later family.
- Secondary (exploratory): per-unit collapse probability over seeds with Clopper-Pearson CIs. Whether T=0 collapse predicts T=0.7 collapse: compare the mean seed collapse rate of the 6 T=0-collapsed units against the other 13 with an exact permutation test over units, plus Fisher's test on "collapsed in at least 1 of 3 seeds". Leave-one-unit-out for C1 and C2, with conv-42 and marketing_manager named. Item-weighted sensitivity. Guard effect restricted to units with no T=0 collapse.
- Power: with 19 units and per-unit difference SD s, the minimum detectable effect at 80% power, two-sided alpha=.05, is about 0.68*s. Report s once observed.
- Failures: every endpoint error is logged (unit, arm, seed, step, error) to results/p1_errors.log and retried with backoff. A unit-seed still failing at analysis time is excluded from both arms and listed. Runs are resumable from the cache.

## Timing disclosure (added 2026-11-05 18:30 IST)
- This plan (P1 section) was committed as 81a87b2 at about 17:25 IST on 2026-11-05. P1 seed 1 was launched at about 17:27 IST, after the plan commit. The first seed-1 score row appeared at 17:48 IST.
- The run script code/p1_seeds.py and the seed change in code/groq_client.py were written at 17:27 IST and were NOT committed before launch. They implement the committed plan without deviation and will be committed as-is.
- Seed-1 endpoint failures before 18:23 IST are logged in results/p1_errors.log. The runner process was found dead at 18:23 IST (last activity 17:49 IST, most likely a sandbox restart) and was relaunched at 18:30 IST; runs resume from the cache.
