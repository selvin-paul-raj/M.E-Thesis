# S5b: Memora rerun of the kill-switch (2026-11-04)

Setup: Memora weekly (arXiv 2604.20006, Apache-2.0), personas software_engineer + academic_researcher
(the third, startup_founder, was dropped because of Groq free-tier tokens/day caps). 20 questions (remembering + reasoning),
103 rubric checks. Writer/reader qwen/qwen3.8-27b (gpt-oss-20b had hit 200K tokens/day); judge gpt-oss-120b on Memora's
own yes/no checks. Input: Memora's share_memory turns. Fixed-content arm, 1,200-word cap, temperature 0.

| condition | check accuracy % | memory presence % | forgetting absence % |
|---|---|---|---|
| k=0 | 58.3 | 40.8 | 96.9 |
| k=1 | 52.4 | 32.4 | 96.9 |
| k=2 | 49.5 | 31.0 | 90.6 |
| k=4 | 49.5 | 31.0 | 90.6 |
| k=8 | 49.5 | 31.0 | 90.6 |
| raw BM25 top-15 | 56.3 | 46.5 | 78.1 |

Drop k=1 -> k=8: 2.9 pts (< 3) -> **FLAT** by the PLAN.md threshold. With LoCoMo also flat, the kill-switch says: stop and report to owner.

## What both pilots show
1. Rewrite loss is one-shot and converges. Memory reaches a fixed point after 1-2 rounds (word counts identical from k=2 to k=8 in all 5 dialogues); all measurable loss happens before that (Memora k=0 -> k=2: -8.8 pts; presence 40.8 -> 31.0).
2. H1 (log-linear compounding decay on fixed content) is not supported on either benchmark. This agrees with Drift No More (arXiv 2510.07777): bounded equilibria, not runaway decay.
3. Caveat: at temperature 0, rewriting its own output converges by construction. Real agents add new content every round, so compounding could still appear in the streaming arm (H2), which the pilot did not test.
4. Raw BM25 keeps more facts (presence 46.5) but surfaces stale ones (forgetting 78.1 vs 90.6-96.9 for memory): raw is not a free ceiling on Memora.

## Options for the owner
- A. Reframe: "Consolidation loss is front-loaded: one rewrite costs most of it" + Render-from-Raw to avoid that first-pass loss, with a streaming-arm test of whether new content restarts the decay.
- B. Pivot the side paper to the staleness/forgetting trade-off (raw keeps facts but leaks stale ones; memory forgets stale but loses facts).
- C. Drop the drift paper and return to Tanglish RAG / security.
