# `claude-papers/` — literature collection for EmbGen's LLM-as-a-judge evaluation

Assembled to support the NeurIPS 2026 Pre-to-Post workshop submission (deadline 29 Aug 2026 AoE).
Read **`../METHODOLOGY-RECOMMENDATION.md`** first — it is the actual proposal. This folder is its evidence base.

## Layout

| Path | What |
|---|---|
| `00-CONTEXT-BRIEF.md` | The brief the search agents worked from: EmbGen's current protocol and its weaknesses W1–W7 |
| `notes/A-meta-evaluation.md` | Validating a judge against humans — agreement statistics, the alt-test, human ceilings |
| `notes/B-judge-bias.md` | Judge biases: self-preference, preference leakage, verbosity, position; mitigations |
| `notes/C-statistical-rigor.md` | Confidence intervals, paired tests, power, PPI/PPI++ |
| `notes/D-claim-level-factuality.md` | Atomic-claim decomposition and corpus-grounded verification |
| `notes/E-eval-set-validity.md` | LLM-generated benchmark validity, multi-hop controls, **the workshop CFP**, and how EntiGraph/InstructLab/Knowledge-Instruct/Ovadia actually evaluate |
| `notes/Z-my-analysis-of-embgen-numbers.md` | Statistics computed directly from EmbGen's Tables 3–4 |
| `notes/Z2-ppi-budget-simulation.md` | How many human annotations you need, simulated |
| `notes/Z3-eval-set-construct-validity.md` | ⚠ The eval sets may not test cross-document reasoning |
| `notes/Z4-seven-day-plan.md` | Day-by-day schedule to the deadline |
| `notes/Z5-teacher-judge-confound.md` | Teacher = judge, and its entanglement with the heterogeneity variable |
| `code/judge_stats.py` | Runnable: Wilson CIs, McNemar exact, Krippendorff's α, length control, PPI++, Rogan–Gladen |

PDFs are prefixed by the search front that found them (`A_`…`E_`) and named
`<Prefix>_<FirstAuthor><Year>_<ShortTitle>_<Venue>.pdf`.

## Provenance and caveats

- Every PDF was checked for a valid `%PDF` header and >50KB size. No duplicates across fronts.
- Venues were verified against ACL Anthology / OpenReview / DBLP rather than assumed. Several initial
  guesses were wrong and corrected: *Molecular Facts* and *VeriScore* are **Findings** of EMNLP 2024;
  Thakur et al. *Judging the Judges* is a **GEM² workshop** paper at ACL 2025, not a main-conference paper;
  Boyeau et al. *AutoEval Done Right* is **ICML 2025**, not arXiv-only.
- arXiv-only items are flagged as such in the notes. Two low-quality 2026 preprints were deliberately dropped.
- Known imperfections: the Dietterich (1998) PDF is the author's preprint (MIT Press is paywalled); the
  Brown/Cai/DasGupta (2001) PDF has no extractable text layer, though metadata confirms the article.
- Prometheus-1 and FLASK PDFs came from arXiv because OpenReview blocks scripted download; both are
  ICLR 2024 (venue verified via DBLP).

## The eight papers already in `../papers/` are not duplicated here

MT-Bench (Zheng et al.), the two versions of the Gu et al. survey, Li et al. (EMNLP 2025) survey,
Yamauchi et al. empirical study, Themis, *When the Judge Changes*, and *Explicit Reasoning Makes Better Judges*.
