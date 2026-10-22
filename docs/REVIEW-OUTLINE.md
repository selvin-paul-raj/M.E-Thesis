# KEC Model Project review — provisional first-two-module outline

**Purpose:** a low-friction preparation aid for the KEC Model Project review notice. This is not an official KEC template and the college has not supplied module names, a rubric, a review time, or a required presentation format.

The WhatsApp notice says Model Project reviews are on **24 and 26 October 2026**, asks students to complete and bring the first two modules, and warns that nonattendance may bar semester review. A later message says the **model exam** schedule was postponed; it does not explicitly change the Model Project review dates. Confirm with the department before treating the project review as postponed.

## Module 1 — Problem, aim and scope (working label only)

1. **Working title:** AVA Evaluation: An Empirical Study of Conflict Resolution for Assertional State in Multi-Agent AI Systems.
2. **Registration title:** Conflict Resolution for Assertional State in Multi-Agent AI Systems.
3. **Problem:** agents can make competing assertions about one shared state key; replicas may converge mechanically without the resulting value being semantically correct.
4. **Aim:** evaluate when decision mechanisms should Agree, Verify, or Abstain on same-key assertion pairs.
5. **Scope:** four classes—Paraphrase, Compatible, Soft Conflict, Hard Conflict. Evaluation methods include deterministic, embedding, NLI, hybrid, LLM-as-a-Judge, Jev (System-One decision model), and conflict-preserving abstention.
6. **Research questions:** summarize RQ1–RQ7 from the finalized specification; explain that historical reliability is an ablation and semantic methods are not assumed to win.
7. **Boundaries:** no general consensus, open-domain truth verification, Byzantine agents, cross-key intent reasoning, or organizational governance.
8. **Honesty note:** novelty and literature-gap claims remain provisional until Pass 3 full-text verification; the convergence property is a target, not a proven result.

## Module 2 — Related work, method and evaluation plan (working label only)

1. **Research stages:** Pass 3 literature/novelty attack → design and preregistration → labeled dataset → B1–B7 benchmark → calibration/safety/cost → semantics-free deterministic simulator → integration/scaling → analysis → thesis writing after gates.
2. **Dataset:** controlled synthetic cases, human-reviewed generated cases, and real traces only when legally/practically available; three annotators plus adjudication and agreement measurement as specified.
3. **Key metrics:** macro/per-class F1; false-merge and false-conflict rates separately; unnecessary abstention; policy-pathway rates; calibration and cost; distributed convergence and recovery.
4. **SCP-MA:** evaluation environment for concurrent agents and asynchronous network faults, not claimed as the thesis's primary novelty. First prove order-independent deterministic projection without semantic methods.
5. **Safety and limits:** preserve unresolved assertions instead of guessing; deterministic Verify in convergence-proof-bearing tests; model-based Verify is a separately labeled non-convergence-safe condition unless made deterministic.
6. **Resource/ethics needs:** full-text access, annotator availability, pinned model versions, measured compute/API costs, lawful data provenance, and privacy approval for any real traces.
7. **Current gate:** no protocol implementation or thesis/paper drafting until Pass 3 and the novelty matrix are complete and the design is preregistered.

## One-minute spoken summary

“My thesis is AVA Evaluation. It studies how multiple AI agents should handle different assertions about the same shared fact: agree, verify with more evidence, or preserve the conflict and abstain. I’ll compare deterministic and semantic methods, measure both unsafe merges and unnecessary conflicts, and then test deterministic behavior in an asynchronous simulator called SCP-MA. I’m still verifying the literature and challenging the novelty claim, so I’m not presenting the gap or convergence property as proven yet.”

## Bring / confirm

- First two modules in the format the college actually requires; this outline is only a fallback structure.
- Any available supervisor comments, registration form, official template, rubric, and review schedule.
- Notebook / laptop or printed copies only if the department requires them; the notice simply says “bring it for review.”
- Confirm whether the 24 October and 26 October project-review dates still stand; the “model exam postponed” message does not explicitly mention these reviews.
