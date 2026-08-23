# ⏰ Seven days to deadline — what actually fits

**Deadline: Fri 29 Aug 2026, AoE. Today: 22 Aug 2026.**
Short papers **4–5 pages**, NeurIPS style, references and appendices excluded. Non-archival.
OpenReview: `NeurIPS.cc/2026/Workshop/Pre-to-Post`. Notification 29 Sep; workshop 11 Dec, Sydney.
Each submission must **nominate a reciprocal reviewer** — sort this out early, it is easy to forget.
(Anonymity policy NOT stated on the CFP page — check OpenReview when the portal renders the form.)

Since it is **non-archival** and the arXiv preprint already exists, the workshop paper does not have to be
the whole EmbGen paper. **Submit a focused 4–5 page evaluation-methodology paper** built on the EmbGen
testbed. That plays directly to CFP topic #9 ("Evaluation and open science… standardized protocols") and
topic #6 (synthetic data), and it fits the page limit in a way a condensed EmbGen cannot.

---

## The positioning that makes this publishable in seven days

Agent E's survey of EmbGen's own subfield found the norm:

| | EntiGraph | InstructLab/LAB | Knowledge-Instruct | Ovadia 2024 |
|---|---|---|---|---|
| Uses an LLM judge | summarisation only | yes | yes | no |
| **Judge validated against humans** | **No** | **No** | **No** | n/a |
| **CIs / significance tests** | **None** | **None** | **None** | **None** |
| Judge-free scoring slice | yes (MCQ) | — | yes (oracle filter) | yes (log-prob MCQ) |
| Contamination / oracle control | yes | no | yes | yes |

**Nobody in this subfield validates their judge or reports error bars.** That is the paper. EmbGen can be
the first, and a workshop on defining "success" in post-training is exactly the room for it.

Working title direction: *"What counts as success? Validating LLM-as-a-judge for synthetic-data
post-training when no gold labels exist."*

---

## Day-by-day

**Days 1–2 (Sat–Sun) — Tier 0, zero new compute. Do all of it.**
- Intra-judge agreement across the existing 10 runs (α + % unanimous). The data is already on disk.
- Wilson CIs + paired McNemar + Holm on every comparison. `code/judge_stats.py` runs this as-is.
- Answer-length table + length-controlled logistic refit.
- Inter-dimension correlation matrix at item level (discriminant validity → kills W7 in one table).
- **Hop-count audit** from the `<REFERENCE> LINE:#` provenance already collected (see `Z3-…`).
- Reframe the headline: drop "88.9%", report absolute differences with intervals.

**Days 2–4 (Sun–Tue) — the human validation. This is the load-bearing new work.**
- 20-item pilot → revise rubric → then **150 items × 3 annotators**, Factual Accuracy + Completeness only.
  Three co-authors can do 150 items each in roughly half a day. You have four authors.
- Report weighted κ / Krippendorff's α, the bootstrapped human ceiling, and the **alt-test** (ω ≥ 0.5).
- Feed the same labels into **PPI** for the headline cells.

**Days 3–5 (Mon–Wed) — two cheap controls, inference only, no training.**
- **Oracle-answerability filter** (Knowledge-Instruct's trick): does a third model answer the question
  correctly *given the source chunks*? Report the pass rate over all 250. Judge-free.
- **Single-chunk vs full-context ablation** → evidence the questions genuinely need multiple hops.

**Days 5–6 (Wed–Thu) — write.** 4–5 pages is tight; the tables above are the paper.

**Day 7 (Fri) — submit early in the AoE window.** Nominate the reciprocal reviewer.

---

## Explicitly cut (good ideas, wrong week)

- Full claim-level / FActScore-style re-evaluation of all 6,750 answers — too expensive; mention as future
  work, or run it on **one** cell (Wikitext-10 @ 20M) as a proof of concept if days 5–6 go well.
- Swapping in a second judge family across every condition — instead run the **judge-swap on the headline
  cell only** to break the teacher = judge confound (see Tier 3).
- Adding MuSiQue/LongBench-v2 as an external control — high value, but it needs a new training/eval cycle.
  Flag it as the obvious next step.
- Regenerating the eval sets. If the hop-count audit shows they are mostly 1-hop, **say so honestly in the
  limitations** rather than hiding it; an honest negative finding about your own benchmark is publishable at
  a workshop like this one and is far safer than a claim a reviewer can falsify from your appendix.
