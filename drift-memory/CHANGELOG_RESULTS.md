# CHANGELOG_RESULTS

## 2026-11-05: cluster-level re-analysis (code/stats_cluster.py, results/contrasts.csv)
| Claim in v6 | v6 value (question-level bootstrap) | Cluster-level value | Cause |
|---|---|---|---|
| Bounded guard vs stream, LoCoMo held-out | +6.0 [+2.0,+11.0], p=0.002 | +6.0 [0.0,+13.0], perm p=0.25, Holm 0.25; wins 3/3, ties 7 | questions clustered in conversations; 3 collapsed convs carry the effect |
| Bounded guard vs stream, pooled | +4.6 [+0.6,+9.3], p=0.020 | +4.6 [0.0,+10.9], perm p=0.0625, Holm 0.125; wins 5/6 collapsed units | same |
| Guard-append vs stream, pooled | (not headline) | +6.3 [+1.6,+12.6], perm p=0.031, wins 6/6 | exploratory; length confound |
| "No compounding" (Memora k2 vs k0) | n.s. | +0.7 [-4.4,+5.8]; TOST 5pt equivalence holds | margin pending confirmation |
| Stream vs k0 pooled | n.s. | +1.3 [-8.1,+10.3], perm p=0.43; NOT equivalent at 5pt | underpowered |
| LongMemEval collapse rate 17.4% (39/224 rewrites) | 17.4% of all rewrites | 39/201 rewrites from >=300 words (19.4%); 21/23 streams [72,99]% | denominator: A9 rule counts only old>=300 |

## 2026-11-05 17:30 IST — paper v7
- Inference unit changed from question to conversation/persona (code/stats_cluster.py, a16_review_stats.py): LoCoMo bounded guard − stream +6.0 [0.0,+13.0] perm p=0.25 (was p=0.002 question-level); pooled +4.6 [0.0,+11.0] p=0.062; Holm (2 confirmatory) 0.25 / 0.125 → not significant.
- Memora stream−k0 now [−7.4,+14.6] p=0.68 (was [−2.8,+9.9] p=0.31). Pooled g-bnd−k0 p=0.63 (was 0.086).
- 550B vs 30B LoCoMo stream at unit level: +21.0 [+6.0,+34.0] perm p=0.031 (code/a13_unit_stats.py).
- Added: collapse rates per stream (Clopper-Pearson), cap length bins, A18 fact survival (11.6% vs 96.2%), A15 escalation (exploratory), A17 controls (partial, exploratory), 30B token costs.
- Removed claims: "pre-registered" kill-switch, "fades with writer scale", "statistically indistinguishable".

## 2026-11-05 P0 (v7 → v7.1), saved-output reanalysis only (code/p0_reconcile.py → results/p0_reconcile.txt)
| Item | Old (v7) | New | Cause |
|---|---|---|---|
| Rewrites ≥300 words (30B, all benchmarks) | 552 | 455 (LoCoMo 213, Memora 67, LongMemEval 175) | 552 counted all transitions, not eligible ones |
| LongMemEval collapse rate | 39/224 = 17.4%, "one in six" | 39/201 = 19.4%, "one in five" | 224 counted writer calls, including the first from empty; others use transitions |
| LongMemEval guard trigger rate | 48/224 = 21.4% | 48/201 = 23.9% | same denominator fix |
| LongMemEval stream vs guard test | bootstrap p=.077 | exact McNemar p=.25 (3 discordant, all favour stream) | correct test for paired binary outcomes |
| Memora k2−k0 TOST | "equivalent within 5 pt" (90% CI [−2.8,+4.1]) | not established: TOST p=.052, 90% CI [−3.7,+5.0] | bug: stats_cluster.py used the 10th–90th percentile (an 80% CI); fixed to 5th–95th |
| Pooled label | "Pooled (190 q)" | "Pooled (542 items)" plus question-weighted values (k0 29.7, stream 25.3, append 31.2, bounded 29.5) | the pooled value weighted 442 Memora checks against 100 LoCoMo questions |
| Pooled stream−k0 | +1.3 only | +1.3 item-weighted; −4.4 [−10.9,+2.0] question-weighted | the sign depends on the weighting |
| LoCoMo gap wording | "whole gap from three conversations" | 6 of 8 pt from the 3 collapsed conversations, 2 from the other 7 | exact decomposition |
| Cap bins | pooled across benchmarks | per benchmark; LoCoMo+Memora 0/116 above 1,500 words, LongMemEval 35–36% above 900 | pooling hid a benchmark difference |
| Batching | "batches of 10" | LoCoMo 1, Memora 10, LongMemEval 5 sessions per rewrite | v7 text was wrong for LoCoMo |
| Fact-loss detector | "13 of 13 flagged are collapses" | precision 13/13, recall 13/19 (13/23 at 0.7), with the event defined | brief P0(d) |

## 2026-11-05 v7.1 → v7.2 (owner review 17:22 IST)
| Item | Old | New | Cause |
|---|---|---|---|
| Table 5 (hybrid) | question-level, item-weighted: Memora raw 54.3 vs hybrid 50.9 (−3.4, p=.355); LoCoMo p=.108; Collapsed 53.5/51.4 | unit-level, question-weighted, exploratory: LoCoMo +8.0 [+1.0,+17.0] p=.16; Memora 36.4/36.7 +0.3 p=.94; Pooled +4.3 [−0.6,+9.9] p=.14; Collapsed +1.3 p=.81 (code/p0b_hybrid_unit.py) | conversations and personas are the unit; question weighting is primary |
| Damage paragraph | −20.0 [−36.7,−6.7], p=.001 | descriptive only; with 3 units the minimum exact p is .25 | the question-level test contradicts the unit rule |
| Collapse denominators | all rewrites after the first only | both: 13/351 (3.7%) and 13/280 eligible (4.6%); LME 39/201 (19.4%) and 39/175 (22.3%) | consistency |
| Abstract | "Across LoCoMo, Memora and LongMemEval … fixed content"; "guard hurt" | "In two pilots"; 11.6% labelled a lexical proxy; "did not help" | overclaim |
