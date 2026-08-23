# How many human annotations does EmbGen actually need? — a simulation

Run with `claude-papers/code/judge_stats.py`. Simulates N = 250 evaluation items per
(dataset × budget × method) cell, comparing three ways to estimate Binary Accuracy:

1. **judge-only** — narrow interval, but centred on the wrong value if the judge is biased
2. **human-only** — unbiased, but wide at small annotation budgets
3. **PPI** (Prediction-Powered Inference) — unbiased *and* narrower, when the judge is good enough

## The break-even condition (analytic)

PPI variance ≈ `var(ŷ)/(n+N) + var(ŷ − y)/n`; human-only ≈ `p(1−p)/n`.
So **PPI beats human-only roughly when the judge–human disagreement rate `e` < `p(1−p)`**:

| Binary Accuracy base rate `p` | `p(1−p)` | required judge–human agreement |
|---|---|---|
| 0.07 (Wikitext-10) | 0.065 | **> 93.5%** |
| 0.15 | 0.128 | > 87.2% |
| 0.28 (Pop-QA / SQuAD) | 0.202 | **> 79.8%** |
| 0.50 | 0.250 | > 75.0% |

**This is the key planning number.** EmbGen's low-base-rate corpus (Wikitext-10, BA ≈ 0.07) is the
*hardest* place to buy precision with a judge: you need a near-perfect judge before PPI pays for itself.
The mid-base-rate corpora are where PPI is clearly worth doing.

## Simulation with a realistic judge (sensitivity / specificity)

| Scenario | agreement | n=30 | n=50 | n=75 | n=100 | n=150 |
|---|---|---|---|---|---|---|
| Pop-QA/SQuAD, good judge (sens .85 / spec .92) | 90.0% | **1.70×** | **1.45×** | 1.26× | 1.11× | 0.90× |
| Pop-QA/SQuAD, mediocre judge (.75 / .85) | 82.2% | 1.01× | 0.92× | 0.84× | 0.77× | 0.66× |
| Wikitext-10, good judge (.80 / .97) | 95.8% | 1.26× | 1.15× | 1.00× | 0.89× | 0.74× |
| Wikitext-10, mediocre judge (.70 / .92) | 90.5% | 0.54× | 0.54× | 0.51× | 0.47× | 0.41× |

(“eff. gain” = effective sample-size multiplier from PPI vs annotating the same n items and using
humans only. Values < 1 mean PPI is *worse* than just using the human labels directly.)

Judge-only bias in these scenarios ranges **+0.014 to +0.054** in absolute Binary Accuracy — i.e. of the
same order as, or larger than, every EmbGen-vs-baseline gap except Wikitext-10 @ 20M. That is the
strongest single argument for doing the human validation at all: **an unmeasured judge bias of +0.02 is
enough to manufacture three of the paper's four claimed wins.**

## Convergence with the literature

My simulated PPI gains top out at **~1.7×**. Independently, Dorner, Nastl & Hardt (ICLR 2025, *Limits to
scalable evaluation at the frontier: LLM as judge won't beat twice the data*) prove that **no debiasing
method can reduce the required number of ground-truth labels by more than half** — and they add that
"the sample size savings achievable in practice are even more modest than what our theoretical limit
suggests." My simulation reproduces that bound from the other direction, which is reassuring for both.

**Important nuance — this bound is favourable to EmbGen, and should be cited carefully.** Dorner et al.'s
theorem is conditioned on *the judge being no more accurate than the evaluated model*. EmbGen judges
Llama-3-8B-Instruct outputs with GPT-5, so the judge is almost certainly the stronger model and EmbGen sits
in the *favourable* regime, not the frontier regime the theorem targets. Cite it as "we operate inside the
regime where debiasing is provably useful, unlike frontier-model evaluation" — do **not** cite it as a
limitation of EmbGen's own setup, which would be a misreading.

**Practical consequence:** do not expect PPI to rescue the underpowered comparisons. It buys at most ~2×
effective sample size. The Pop-QA (+4 items) and SQuAD (+2 items) gaps need ~10,000+ items to resolve —
PPI cannot close that. PPI's real job here is to make the *point estimate* trustworthy and put an honest
interval on it, not to manufacture significance.

## CORRECTION — use PPI++ with a tuned λ, not plain PPI

The tables above use **plain PPI (λ = 1)**, which is why several cells show gains *below* 1× — PPI actively
losing to just using the human labels. Eyre & Madras (ICML 2025) identify exactly this failure at
n ≲ 50–100, and **PPI++** fixes it: tuning λ (λ̂ = Cov(f,y)/Var(f) · N/(N+n)) means λ̂ → 0 recovers the
human-only estimator, so PPI++ is **never worse than classical inference**.

Re-run of the worst case above (Wikitext-10-like, p = 0.07, *mediocre* judge, 90.5% agreement):

| n human | human-only ± | plain PPI ± | **PPI++ ±** | λ̂ | PPI++ gain |
|---|---|---|---|---|---|
| 30 | 0.083 | 0.112 ✗ | **0.069** | 0.35 | **1.43×** |
| 50 | 0.068 | 0.095 ✗ | **0.059** | 0.30 | **1.30×** |
| 75 | 0.057 | 0.083 ✗ | **0.051** | 0.27 | 1.24× |
| 100 | 0.049 | 0.079 ✗ | **0.045** | 0.22 | 1.18× |
| 150 | 0.041 | 0.081 ✗ | **0.038** | 0.15 | 1.11× |

The break-even table earlier in this note still describes *when the judge adds information*; PPI++ simply
means that when it doesn't, you lose nothing instead of losing precision. `judge_stats.ppi_binary(...,
tune_lambda=True)` implements this and is the default. Package alternative: `ppi_py` (`ppi_mean_ci`).

Cross-check every PPI estimate against **Rogan–Gladen**: `p̂_corr = (p̂_judge + Sp − 1)/(Se + Sp − 1)`,
using the sensitivity/specificity measured on the human subsample. If the two disagree materially,
something is wrong with the sampling weights.

## Recommended budget

- **60–80 items per cell**, not 50. Eyre & Madras (ICML 2025) put the floor where plain PPI turns harmful
  at n ≈ 50–100; 60 is the safe lower bound, and it also satisfies the alt-test requirement
  (Calderon et al., ACL 2025: 3 annotators × 50–100 instances).
- Label **all ~17 judge-positive items** on Wikitext-10 plus a 15–30% sample of judge-negatives, and
  **record the sampling probabilities** — the rectifier cannot be estimated from a sample with no positives.
- Stratify the sample on the judge's own verdict (`stratified_annotation_sample()` in the toolkit) —
  on Wikitext-10 a uniform sample of 50 yields ~3 judge-positive items, far too few to estimate the
  rectifier.
- Prioritise: Wikitext-10 @ 20M (the headline claim) > Pop-QA @ 20M > SQuAD @ 20M. Two systems per
  cell (EmbGen + strongest baseline) is enough; you do not need all five.
