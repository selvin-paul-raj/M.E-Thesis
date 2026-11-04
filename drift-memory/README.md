# DriftMemory

**Measuring and Mitigating Memory Drift in Long-Term LLM Agents: Render-from-Raw Memory with NLI-Triggered Refresh**

AI agents that work with a user over weeks or months keep a long-term memory by repeatedly rewriting their stored notes, and each rewrite can lose or change small details. This work measures how much an agent forgets as the number of rewrites grows, using standard memory benchmarks. It also proposes a fix: keep the original interaction history unchanged and rebuild the memory from it whenever a check finds the memory wrong or incomplete.

| Path | Contents |
|---|---|
| `proposal/` | Proposal paper (PDF) and LaTeX source |
| `PLAN.md` | Step-by-step plan to ACL Rolling Review (2027-01-04) |
| `STATE.json` | Current step and progress |
| `code/` | DriftBench harness |
| `results/` | Scores and tables (caches and datasets are not committed) |
| `notes/` | Reading notes, pilot verdict, decisions |
| `logs/` | One short log per working day |

Status: proposal v4 done; kill-switch pilot starts 2026-11-04.
