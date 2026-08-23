# embgen-lit-rev

Literature review and evaluation-methodology work supporting the **EmbGen** submission to the
NeurIPS 2026 workshop *Transitioning from Pre-Training to Post-Training*.

EmbGen (arXiv:[2605.19394](https://arxiv.org/abs/2605.19394)) is a synthetic SFT data-generation
pipeline: it decomposes a corpus into entity–description pairs, reassembles them via embedding
clustering and proximity graphs, and synthesises QA pairs for fine-tuning. Because the training data is
generated rather than curated, there are no canonical labels — so the evaluation leans on an
LLM-as-a-judge rubric. This repo collects the literature needed to put that judge on a defensible
footing, and works out what to change.

## Start here

| File | What |
|---|---|
| **[`llm-as-a-judge/METHODOLOGY-RECOMMENDATION.md`](llm-as-a-judge/METHODOLOGY-RECOMMENDATION.md)** | **The proposal.** Eight ranked problems, a tiered fix list, and a seven-day schedule. |
| [`llm-as-a-judge/PAPERS.md`](llm-as-a-judge/PAPERS.md) | Every paper, with a link to its source |
| [`llm-as-a-judge/claude-papers/README.md`](llm-as-a-judge/claude-papers/README.md) | Guide to the paper collection and its provenance |
| [`llm-as-a-judge/claude-papers/code/judge_stats.py`](llm-as-a-judge/claude-papers/code/judge_stats.py) | Runnable statistics toolkit |

## Branches

| Branch | Contents | Clone size |
|---|---|---|
| `main` | Everything, including all 119 PDFs | ~278 MB |
| **`no-pdfs`** | **Notes, methodology and code only — no PDFs** | **~1 MB** |

For a restricted or bandwidth-limited environment, clone the lightweight branch. It shares no history
with `main`, so none of the PDF blobs are transferred:

```bash
git clone --single-branch --branch no-pdfs https://github.com/AndreaR82/embgen-lit-rev.git
```

Then re-download the papers from a machine with open web access:

```bash
bash llm-as-a-judge/claude-papers/fetch_papers.sh   # run it twice; some requests get rate-limited
```

Every paper's canonical link is also listed in [`llm-as-a-judge/PAPERS.md`](llm-as-a-judge/PAPERS.md),
so the collection can be rebuilt by hand if scripted downloads are blocked.

## Layout

```
llm-as-a-judge/
├── METHODOLOGY-RECOMMENDATION.md   the proposal
├── papers/                         papers gathered manually (9, incl. the EmbGen preprint)
└── claude-papers/                  papers gathered by literature search (110)
    ├── 00-CONTEXT-BRIEF.md         the brief the search worked from
    ├── notes/
    │   ├── A-meta-evaluation.md        validating a judge against humans
    │   ├── B-judge-bias.md             self-preference, leakage, verbosity, position
    │   ├── C-statistical-rigor.md      CIs, paired tests, power, PPI/PPI++
    │   ├── D-claim-level-factuality.md atomic-claim decomposition and verification
    │   ├── E-eval-set-validity.md      LLM-generated benchmark validity + the workshop CFP
    │   └── Z*.md                       analysis derived from EmbGen's own tables
    └── code/judge_stats.py
```

## The statistics toolkit

`judge_stats.py` operates on per-item, per-run judge outputs and implements what the current
evaluation is missing:

- **Wilson** confidence intervals for Binary Accuracy (not Wald, not bootstrap — both are
  miscalibrated at N≈250 with few successes)
- **McNemar exact** paired tests with Holm correction
- **Krippendorff's α** across repeated judge runs, to measure judge stability
- **Length-controlled** logistic refit, to separate a completeness effect from a verbosity effect
- **PPI++** with tuned λ, to combine a small human-annotated sample with the full judge-labelled set
- **Rogan–Gladen** sensitivity/specificity correction as a cross-check

```bash
pip install numpy pandas scipy statsmodels krippendorff scikit-learn
python -c "import judge_stats; help(judge_stats)"
```

## Papers

119 PDFs, named `<Front>_<FirstAuthor><Year>_<ShortTitle>_<Venue>.pdf`. Venues were verified against
ACL Anthology, OpenReview and DBLP rather than assumed; arXiv-only items are flagged as such in the
notes. Every PDF was checked for a valid header and non-trivial size, and the collection is
deduplicated.

Papers are included here for personal research reference; copyright remains with their respective
authors and publishers. Full citations, DOIs and arXiv IDs are in the `notes/` bibliographies, so the
collection can be rebuilt from canonical sources.
