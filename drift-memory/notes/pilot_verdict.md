# Pilot verdict (S5)

Questions: 30 (LoCoMo conv-26/30/49, evidence >= 5 sessions old, category 5 excluded).
Writer/reader gpt-oss-20b; judge gpt-oss-120b. Memory cap 1,200 words for k>=1.

| condition | accuracy % | memory words | fact survival % |
|---|---|---|---|
| k=0 | 33.3 | 1129 | 100.0 |
| k=1 | 30.0 | 684 | 79.2 |
| k=2 | 36.7 | 672 | 80.8 |
| k=4 | 36.7 | 668 | 80.0 |
| k=8 | 36.7 | 668 | 80.0 |
| raw BM25 top-10 | 33.3 | - | - |

Drop k=1 -> k=8: -6.7 pts; fact survival monotone (k>=1): False.
**Verdict: FLAT -> rerun on 30 Memora questions before deciding**

Caveats: n=30 (one question = 3.3 pts); answer keys not hand-checked yet; single seed; fact survival judged by LLM, not NLI.

## Reading (Hark, 2026-11-04)
- No compounding drift on fixed content: the loss is one-shot. Round 1 cuts memory ~40% (1,129 -> 684 words) and drops ~21% of k=0 facts; rounds 2-8 are a fixed point (words and survival within 1-2%).
- QA accuracy does not follow fact loss (30-37%, within one question per conversation): the lost facts are rarely the ones asked, and k=0 is already lossy (k=0 = raw BM25 = 33%).
- This matches the bounded-equilibrium finding of Drift No More (arXiv 2510.07777) more than H1. Per the kill-switch: rerun on 30 Memora questions; if also flat, reframe to "one-shot consolidation loss + fixed point" or drop.
