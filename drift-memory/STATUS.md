# STATUS (2026-11-05 15:00 IST)
Done: B (stats_cluster.py, contrasts.csv); C partial (a18 lexical line survival on 19 plain streams; LLM entailment + fixed-content k up to 16 NOT done); D partial (cap bins in stats_cluster.txt; no-cap run going; cap-2400 not run; logistic regression not run).
Running: A15 escalation (exploratory), A17 preserve/floor/nocap (exploratory, started before PREREGISTRATION).
Not started: A audit (AUDIT.md), judge protocol (second judge, deterministic check, 150-item human audit), seeds at T=0.7, second family (no non-Nemotron 30-70B model reachable on NVIDIA so far), 7 LME reruns, 7 Ultra personas, single-question-read check.
Needs Selvin: confirm TOST margin 5 and fact-loss 30; label audit_for_human.csv (150 items) himself; confirm which cited papers he has opened (brief rule 7); target venue/date.

## 2026-11-05 16:05 IST A17 controls (partial, exploratory)
- floor-reject (keep old memory on collapse), LoCoMo collapsed 3: conv-26 0.0, conv-42 10.0, conv-47 10.0 (stream 0/10/0; bounded retry 10/40/20). Floor << retry.
- preserve-always: conv-26 STILL collapsed (2276->173 words) 10.0; conv-30 50.0 (stream 40); conv-41 0.0 (stream 0); business_executive 60.0 (stream 35.6, retry 31.1). 4 of 19 units done.
- no-cap: marketing_manager still collapsed (524->157) at 38.2 (stream 40.0). Cap is not the sole cause. 1 of 19 units done.
- run17.sh restarted (resumable); NVIDIA 30B endpoint failing intermittently.

## 2026-11-05 17:45 IST
- Paper v7: paper/DriftMemory_Collapse_v7.pdf (unit-level inference; guard not significant after Holm).
- Running (runall.sh): A15 last LME instance, A17 controls, A19 Qwen writer, A20 Mistral second judge.
- Preregistration margins locked (5-pt TOST, 30-pt fact loss); still to commit before confirmatory runs.
- Human audit sheet: to be built from results/a20_preds.jsonl once A20 is done; the owner labels it himself.

## 2026-11-05 ~18:00 IST — brief v2 (docs/AGENT_BRIEF_v2.md)
- DONE P0: code/p0_reconcile.py → results/p0_reconcile.txt; AUDIT.md; CHANGELOG (TOST bug fixed in stats_cluster.py); paper v7.1 PDF.
- RUNNING: A17 controls, A19 Qwen writer (P6), A20 Mistral judge (P5), A15 last LME instance.
- BLOCKED / NEEDS SELVIN: P1 design and primary weighting must be fixed in PREREGISTRATION.md and committed before any P1 run.
- 17:40 Owner decisions: A = question-weighted primary; B = seeds 1→2→3 in rounds, 4–5 as extension. Text fixes 1–5 applied (v7.2). Plan committed via the GitHub web UI; P1 launches after that.
