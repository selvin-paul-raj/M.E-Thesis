# AUDIT: every number in paper v7.1, mapped to its script and output (P0, 2026-11-05)

Status values:
- **OK** means the number was recomputed from the saved file in this audit and matches.
- **FIXED** means the number was wrong in v7; CHANGELOG_RESULTS.md records the change.
- **QL** means the number is question-level only; a unit-level version is still owed.

| Paper location | Number(s) | Script | Output file | Status |
|---|---|---|---|---|
| §5 fixed content (pilot) | 1,129→684 words; 79% fact survival at k=1; acc 30.0–36.7 for k=0..8 | pilot.py | results/pilot_scores.csv, pilot_survival.json | OK |
| §5 Memora pilot | 58.3 (k0) → 49.5 (k2, k4, k8); 103 checks | memora_pilot.py | results/memora_scores.csv | OK |
| §5 streaming, Memora | k0 47.5, k2 48.2, stream 50.9 | a5_scale.py | a5_scores_nemotron-3.5-lightning-30b-a3b.csv; a6_guard_stats.txt | OK |
| §5 streaming contrasts | stream−k0 +3.4 [−7.4,+14.6] p=.68; k2−k0 +0.7 [−4.4,+5.8], TOST p=.052 | stats_cluster.py, p0_reconcile.py | contrasts.csv, p0_reconcile.txt | FIXED (TOST) |
| §5 LoCoMo gap | −8 pt total; −6 from 3 collapsed convs, −2 from other 7 | p0_reconcile.py (e) | p0_reconcile.txt | FIXED (wording) |
| §6 rate | 13/351 transitions; 4/89 Memora; 9/262 LoCoMo; 6/19 streams [13,57]% | a9_analysis.py, p0_reconcile.py | a9_analysis.txt, p0_reconcile.txt | OK |
| §6 bimodality | 280 eligible: 256 >0.9, 7 at 0.7–0.9, 4 at 0.5–0.7, 13 ≤0.5 | a9_analysis.py | a9_analysis.txt | OK |
| Table 1 | threshold grid (all 15 cells) | a9_analysis.py | a9_analysis.txt | OK |
| §6 cap bins | per benchmark; eligible 455 (213 LoCoMo, 67 Memora, 175 LME) | p0_reconcile.py (a) | p0_reconcile.txt | FIXED (552 was the count of all transitions) |
| §6 fact survival | 11.6% vs 96.2%; recall 13/19 (survival<.5), 13/23 (<.7), precision 13/13 | a18_fact_survival.py | a18_fact_survival.txt | OK; lexical proxy, replaced in P2 |
| §6 recovery | 5 of 13 | a9_analysis.py | a9_analysis.txt | OK |
| §6 damage | conv 3.3 vs 23.3 (−20.0 [−36.7,−6.7]) | boot.py | a7_locomo_stats.txt | QL |
| §6 550B | 0/281 transitions (293 calls, 12 streams); LoCoMo 39.0 vs 18.0, +21.0 [+6,+34] p=.031 | a13_second_writer.py, a13_unit_stats.py, p0_reconcile.py | a13_ultra_scores.csv, a13_unit_stats.txt | OK |
| §6 LongMemEval | 39/201 transitions (19.4%), 21/23 streams | p0_reconcile.py | p0_reconcile.txt | FIXED (was 39/224 = 17.4%; 224 counts writer calls) |
| Table 2 | all cells | a5/a6/a7/a8 scripts | the CSVs listed above; p0 (b) | OK; "Pooled (190 q)" relabelled to 542 items |
| Table 3 | all rows | stats_cluster.py | contrasts.csv | OK |
| Table 4 | per collapsed unit | stats_cluster.py | stats_cluster.txt | OK |
| §7 triggers | 16 triggers over 105 transitions on 6 diverging streams; 12/16 recovered | a9_analysis.py, p0_reconcile.py | a9_analysis.txt, p0_reconcile.txt | OK |
| §7 LongMemEval guard | 48 triggers / 201 transitions; 4 vs 1 correct; McNemar exact p=.25 | p0_reconcile.py (f) | p0_reconcile.txt | FIXED (was bootstrap p=.077) |
| §8 exploratory | escalate +20.5 [+3.3,+33.3] p=.06; A17 cells | stats_cluster.py, a17_controls.py | stats_cluster.txt, a17_controls_scores.csv | OK (A17 partial) |
| Table 5 hybrid | all cells | a10_hybrid.py | a10_stats.txt | QL |
| Table 6 cost | words | a12_cost.py | a12_cost.txt | OK |
| §10 tokens | 2,302 / 1,645 mean (n=370) | a18_fact_survival.py | a18_fact_survival.txt | OK |

Batching (verified in code):
- LoCoMo: 1 session per rewrite (19–32 rewrites per stream).
- Memora: 10 sessions per rewrite (10–11 per stream).
- LongMemEval: 5 sessions per rewrite (8–11 per stream).

References: every reference is UNCHECKED until Selvin has opened it. The agent opened colaco2026rd (arXiv 2607.08032) on 2026-11-05.
