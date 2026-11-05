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
