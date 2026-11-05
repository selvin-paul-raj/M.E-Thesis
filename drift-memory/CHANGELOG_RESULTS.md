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
