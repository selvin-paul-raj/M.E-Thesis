# PREREGISTRATION (2026-11-05; margins accepted by owner 2026-11-05 16:51 IST "do anything you want"; commit pending)

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
