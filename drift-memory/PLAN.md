# DriftMemory: Research Plan (autonomous daily runs)

**Title:** Measuring and Mitigating Memory Drift in Long-Term LLM Agents: Render-from-Raw Memory with NLI-Triggered Refresh
**Target:** ACL Rolling Review, deadline 2027-01-04 AoE. Backup: ICLR 2027 workshops (2027-02-01).
**Owner:** Selvin PaulRaj K. Daily work by Hark (one step per day, ~1 run/day, pushed here).

## Fixed decisions (2026-11-04)
- Groq free tier no longer serves Llama 3.1 8B / 3.3 70B. Available: `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`.
  - Memory writer + reader: `openai/gpt-oss-20b`. Judge: `openai/gpt-oss-120b` + exact match. Second writer (H3 subset): `qwen/qwen3.8-27b`.
  - Limits per model: 8,000 tokens/min, 1,000 requests/day. All code must throttle and resume from a cache.
- NLI model: `cross-encoder/nli-deberta-v3-small` on CPU (fallback: `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`).
- Retrieval: `bm25s`. Datasets are downloaded at run time and never committed (LoCoMo CC BY-NC; Memora and LongMemEval per their licences).
- Every LLM call is cached in `results/cache/*.jsonl` (gitignored) keyed by sha256(model, prompt), so reruns cost nothing.

## Hypotheses (from proposal v4)
- H1: fixed-content accuracy on old-evidence questions falls >= 5 pts from k=1 to k=8 (log-linear). H1' (competing): plateau.
- H2: eta-hat from fixed arm predicts streaming accuracy within 3 pts at every k.
- H3: detector-triggered Render-from-Raw matches scheduled refresh within 2 pts with >= 30% fewer refresh tokens; detector recall >= 0.8.
- H4, H5: extensions (router, Tanglish), only if time allows.

## Steps (status in STATE.json; one or two steps per daily run)
| # | Target date | Step | Done when |
|---|---|---|---|
| S1 | Nov 4 | Repo scaffold, PLAN, STATE, harness skeleton, Groq client with throttle + cache | code/groq_client.py runs a cached call |
| S2 | Nov 5 | LoCoMo loader; select 30 pilot questions with evidence >= 5 sessions old; evidence-age tags | results/pilot_questions.jsonl |
| S3 | Nov 5-6 | Rewrite-in-place consolidator (Mem0-style, frozen prompt, 2,000-token cap); fixed arm k=0,1,2,4,8 | results/pilot_memories/ |
| S4 | Nov 6 | Reader + judge; raw BM25S baseline; fact-survival via NLI | results/pilot_scores.csv |
| S5 | Nov 7 | Pilot verdict (falling / plateau / flat) with thresholds; plot; 5-line verdict in notes/ | notes/pilot_verdict.md |
| S6 | Nov 8-9 | Read REALM 2609.16053, All-Mem 2603.19595, Memora 2604.20006 in full; revise gap | notes/reading_*.md |
| S7 | Nov 10-16 | Memora + LongMemEval loaders; harness generalised; evidence-age bands | code/data_*.py |
| S8 | Nov 17-23 | Main fixed-arm runs (H1 vs H1'), power check, fit eta-hat | results/fixed_arm.csv |
| S9 | Nov 24-30 | Streaming arm (H2) | results/streaming_arm.csv |
| S10 | Dec 1-7 | Staleness detector (contradiction + coverage), oracle labels, P/R | results/detector_pr.csv |
| S11 | Dec 8-14 | Triggered vs scheduled refresh (H3); 2nd writer subset | results/h3_frontier.csv |
| S12 | Dec 15-28 | Paper writing (ACL format), figures, related work refresh | paper/ |
| S13 | Dec 29-Jan 4 | Guide review; arXiv preprint decision; ARR submission (owner only) | submitted |

## Kill-switch thresholds (S5)
- Falling: acc(k=8) <= acc(k=1) - 10 and fact survival monotone down -> continue.
- Plateau: drop 3-10 pts, levelling by k=4 -> continue with equilibrium framing.
- Flat: < 3 pts -> rerun 30 Memora questions; if still flat, stop and report to owner.

## Rules for the autonomous runs
- Never submit, email, post, pay, or contact anyone. Owner submits.
- Never commit datasets, caches, keys or tokens. Secret-grep before every push.
- Stop and report if a step fails twice, a limit blocks progress, or a result changes the plan.

## Revision 2026-11-04 (after kill-switch): Option A chosen by owner
Both pilots were flat: rewrite loss is one-shot (k <= 2), then a fixed point. New framing:
"Consolidation loss is front-loaded, not compounding" + does streaming new content restart it? + Render-from-Raw avoids the first-pass loss.
| # | Step | Done when |
|---|---|---|
| A1 | Streaming rewrite-in-place arm on the 30 LoCoMo pilot questions (code/stream_pilot.py) vs append-only (k=0), fixed k=8, BM25; accuracy by evidence age | results/stream_summary.md |
| A2 | Same streaming arm on Memora (2-3 personas, qwen3.8-27b writer if 20b capped) incl. presence vs forgetting | results/memora_stream.csv |
| A3 | Render-from-Raw: keep raw sessions, rebuild memory from raw at query time / on trigger; compare to rewrite at equal tokens | results/rfr.csv |
| A4 | Staleness detector (NLI + coverage) deciding when to rebuild; P/R vs oracle | results/detector_pr.csv |
| A5 | Scale-up (more convs/personas, 2 seeds, temperature 0.7 to test the fixed-point caveat), then S12 writing | results/main_*.csv |
Groq free tier: 200K tokens/day per model; split work across days and models.
