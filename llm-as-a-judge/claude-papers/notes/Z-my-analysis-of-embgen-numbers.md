# Independent statistical analysis of EmbGen's reported judge numbers
*(computed by me directly from Tables 3 and 4 of the arXiv PDF — no new experiments needed)*

Assumes N = 250 evaluation items per dataset, as stated in §5.1.

---

## Finding 1 — The paper already contains hidden evidence that the judge is NOT deterministic at temperature 0

Binary Accuracy is reported to 3 decimals. If the 10 judge runs agreed on every item, every value would
be expressible as `k/250`. Checking all 37 distinct reported values (Tables 3 and 4):

| Denominator hypothesis | Values representable |
|---|---|
| `k/250` — all 10 runs agree on every item | **24 / 37** |
| `k/2500` — mean over 10 runs of 250 items | **37 / 37** |

13 of 37 values (0.017, 0.042, 0.054, 0.079, 0.178, 0.237, 0.241, 0.245, 0.249, 0.261, 0.266, 0.274, 0.282)
**cannot** be a count out of 250. They are only consistent with the 10 runs disagreeing.

**Implication.** GPT-5 at `temperature = 0` gave different verdicts on the same item across runs. The authors
already have the per-run data to quantify this, and currently discard it by averaging. This is the cheapest
possible reliability result in the paper: report intra-judge agreement across the 10 runs (Krippendorff's α
on the ordinal scores, plus % of items where all 10 runs agree). It costs nothing and directly answers the
"is your judge stable?" reviewer question.

**Caveat to state in the paper:** temperature-0 repetition measures only backend non-determinism, not
prompt/rubric sensitivity. It is a floor on judge variance, not an estimate of it.

---

## Finding 2 — Only ONE of the four headline wins can possibly be statistically significant

95% Wilson intervals on Binary Accuracy at N = 250:

| Comparison | EmbGen | Best baseline | EmbGen 95% CI | Baseline 95% CI | Gap in items |
|---|---|---|---|---|---|
| Wikitext-10 @ 20M | 0.068 (17/250) | 0.036 (9/250) | [0.043, 0.106] | [0.019, 0.067] | **8** |
| Wikitext-10 @ 5M | 0.072 (18/250) | 0.064 (16/250) | [0.046, 0.111] | [0.040, 0.101] | 2 |
| SQuAD-20 @ 20M | 0.288 (72/250) | 0.280 (70/250) | [0.235, 0.347] | [0.228, 0.339] | 2 |
| Pop-QA @ 20M | 0.282 (~71/250) | 0.266 (~67/250) | [0.228, 0.339] | [0.213, 0.322] | 4 |

Every CI overlaps heavily. The "+6.0%", "+2.9%" and "+12.5%" relative gains are **2 to 4 evaluation items**.

McNemar exact test (paired on the same 250 items — the correct test, and much more powerful than comparing
marginals). Discordant counts `b`, `c` are unknown from the paper, so bounds under assumptions:

| Comparison | b=d, c=0 (EmbGen strictly dominates) | c=5 | c=10 | c=20 |
|---|---|---|---|---|
| Wikitext-10 @ 20M (8-item gap) | **p = 0.008** | p = 0.096 | p = 0.185 | p = 0.312 |
| Wikitext-10 @ 5M (2-item gap) | p = 0.500 | p = 0.774 | p = 0.832 | p = 0.878 |
| SQuAD-20 @ 20M (2-item gap) | p = 0.500 | p = 0.774 | p = 0.832 | p = 0.878 |
| Pop-QA @ 20M (4-item gap) | p = 0.125 | p = 0.424 | p = 0.541 | p = 0.652 |

**Minimum detectable effect at N = 250, α = 0.05 (McNemar):**

| items where baseline is right and EmbGen wrong (`c`) | net edge EmbGen needs |
|---|---|
| 0 | ≥ 6 items (2.4 pts) |
| 5 | ≥ 10 items (4.0 pts) |
| 10 | ≥ 13 items (5.2 pts) |
| 20 | ≥ 16 items (6.4 pts) |
| 40 | ≥ 21 items (8.4 pts) |

Unpaired sample size for 80% power (shows why marginal comparison is hopeless):
Wikitext 20M → **738/arm**; Pop-QA 20M → **12,196/arm**; Wikitext 5M → **15,532/arm**; SQuAD 20M → **49,873/arm**.

**Implication.** The paper must (a) run the *paired* McNemar test — the authors have the per-item outcomes,
so this is free; (b) report CIs; and (c) **retire the "88.9% relative uplift" framing**. Relative gains on a
base rate of 3.6% are unstable by construction. State absolute differences with CIs. The Wikitext-10 @ 20M
result is the paper's only defensible win and should be foregrounded as such; the Pop-QA and SQuAD results
should be described as *parity with the strongest baseline*, which is still a perfectly publishable claim.

---

## Finding 3 — The "88.9% uplift" is driven by baseline degradation, not EmbGen improvement

On Wikitext-10, EmbGen's absolute Binary Accuracy **falls** from 0.072 (5M) to 0.068 (20M). The relative
uplift grows from 12.5% to 88.9% purely because the *best baseline* collapses: at 5M the strongest
competitor is EntiGraph at 0.064; at 20M EntiGraph drops to 0.020 and InstructLab holds at 0.036, so the
comparator becomes 0.036. EmbGen did not improve — the field fell away. A reviewer will spot this
immediately. Reframe as: *EmbGen is robust to increased token
budget on heterogeneous corpora while baselines degrade* — which is a more interesting claim anyway, and is
what the data actually shows.

Related: at BA ≈ 0.07, **93% of answers are scored wrong**. That is a floor regime where a binary metric
discards nearly all signal. Report a graded score (partial credit) alongside the binary one, and audit
whether the Wikitext-10 reference answers are actually answerable.

---

## Finding 4 — Two of the four rubric dimensions carry almost no information; Relevance and Clarity are redundant

Computed across the 29 (dataset × budget × method) cells in Table 3, excluding the degenerate
EntiGraph/Wikitext-20M row (Relevance 1.30, Clarity 2.03 — that model looks broken):

**Scale utilisation** (dimension range as % of the 1–3 scale):

| Dimension | min | max | sd | % of scale used |
|---|---|---|---|---|
| Factual Accuracy | 1.05 | 1.75 | 0.207 | 35.0% |
| Completeness | 1.32 | 2.14 | 0.284 | 41.0% |
| Relevance | 2.02 | 2.94 | 0.278 | 46.0% |
| **Clarity** | **2.81** | **3.00** | **0.058** | **9.5%** |

**Clarity is a dead dimension.** It spans 0.19 points on a 2-point scale and never discriminates between
methods. It is rubric padding and should be dropped or explicitly justified as a sanity check.

**Inter-dimension correlations (Pearson):**

| | Factual | Complete | Relevance | Clarity |
|---|---|---|---|---|
| Factual Accuracy | +1.000 | +0.639 | +0.581 | +0.368 |
| Completeness | +0.639 | +1.000 | +0.092 | −0.005 |
| Relevance | +0.581 | +0.092 | +1.000 | **+0.823** |
| Clarity | +0.368 | −0.005 | +0.823 | +1.000 |

Relevance and Clarity correlate at **r = +0.82** — they are measuring one latent "fluency" factor, the
classic LLM-judge halo effect. Completeness is nearly orthogonal to both (+0.09, −0.01), so it *is* carrying
independent signal — which is good for the paper's story (EmbGen wins via Completeness) but means the
verbosity confound lands squarely on the one dimension the headline result depends on.

Correlation of each dimension with Binary Accuracy: Factual r=+0.884, Relevance r=+0.663, Clarity r=+0.424,
Completeness r=+0.417.

**Caveat:** these are correlations over 29 *aggregate* cells, not per-item. The authors have per-item scores
and should recompute at item level (polychoric correlations, given ordinal data), which is the defensible
version of this analysis.

---

## Finding 5 — Answer length is never reported anywhere in the paper

Grepping the full 33-page PDF: no answer-length, response-length, or token-count statistics for model
outputs. The generation config reports `temperature = 0.001` but no `max_new_tokens`.

Since the paper's central mechanism is "EmbGen produces *more complete* answers", and completeness is
mechanically correlated with length, **the paper cannot currently rule out that its headline result is a
verbosity effect**. The fix is free: the authors already have every generated answer.

Minimum: report mean/median answer length per method per condition.
Better: a length-controlled estimate (logistic regression of the per-item binary outcome on method with
answer length as a covariate, or the reweighting used in Length-Controlled AlpacaEval).

---

## Cost context for proposing additions

Main table = 3 datasets × 2 budgets × 5 methods ≈ 27 distinct model-conditions × 250 items ≈ 6,750 answers,
already judged 10× each (~67.5k judge calls). Ablations add 6 configs × 3 datasets × 2 budgets = 36 cells.
Any proposed addition must be cheap relative to this. Human annotation should therefore be a *stratified
subsample*, not a full re-annotation — see the PPI recipe in the statistics notes.
