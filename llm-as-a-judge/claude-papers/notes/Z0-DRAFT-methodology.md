# EmbGen → NeurIPS Pre/Post workshop: proposed evaluation methodology
*(working draft — sections marked [B]/[D]/[E] pending agent returns)*

## Framing for the workshop

The venue is **"Transitioning from Pre-Training to Post-Training"**, non-archival. Its stated themes include
*defining what "success" in post-training means* and *predicting when post-training fails*. That is a gift:
it means a paper whose contribution is **"here is how to measure whether synthetic-SFT knowledge injection
actually worked, when you have no canonical labels"** is squarely on-topic — arguably more on-topic than the
EmbGen pipeline itself. Lead with the measurement contribution, not the pipeline.

Recommended framing: *EmbGen is the testbed; the contribution is a validated, statistically honest protocol
for evaluating synthetic-data post-training without gold labels.*

---

## Tier 0 — free fixes, using data already in hand (do these regardless)

| # | Fix | Cost | Addresses |
|---|---|---|---|
| 0.1 | Report intra-judge agreement across the existing 10 runs (Krippendorff's α ordinal + % unanimous items) | zero — data exists | W3 |
| 0.2 | Wilson 95% CIs on every Binary Accuracy | zero | W4 |
| 0.3 | Paired **McNemar exact** test, EmbGen vs each baseline on the same item ids; Holm correction across the table | zero | W4 |
| 0.4 | Report mean/median answer length per method; refit the win as logistic `correct ~ method + log(len)` | zero | W5 |
| 0.5 | Drop **Clarity** from the headline rubric (9.5% scale utilisation) or justify it as a sanity check; report item-level polychoric correlations between dimensions | zero | W7 |
| 0.6 | Hop-count audit of eval items using the `<REFERENCE> LINE:#` provenance already collected; stratify results by 1-hop vs ≥2-hop | near-zero | **construct validity** |
| 0.7 | Retire relative-uplift framing ("88.9%") on a 3.6% base rate; report absolute differences with CIs | zero | W4 |

Tier 0 alone converts the paper from "reviewer will object" to "reviewer will accept the claims as stated",
because the claims become *smaller and defensible* rather than large and unsupported.

---

## Tier 1 — the human validation (the one thing that most needs new work)

Cannot be avoided: **W1 (no human validation of the judge) is the objection that sinks LLM-as-a-judge papers.**

Design, per Agent A's synthesis of the literature:
- **~150 items**, stratified across the 3 corpora and across systems, and **stratified on the judge's own
  verdict** (essential on Wikitext-10, where a uniform sample yields ~3 judge-positive items).
- **3 annotators**, each labelling all items — the minimum for the alt-test.
- **20-item pilot first**, then revise the rubric (Shankar et al., UIST 2024 — criteria drift).
- Annotate **only Factual Accuracy + Completeness** and the derived Binary Accuracy. Not Clarity: human
  agreement on subjective criteria collapses to 63–66% vs 94% on objective ones (Zeng et al., ICLR 2024).
- Blind to system identity; randomise order.

Report:
1. **Ordinal-weighted Krippendorff's α** (human–human) and **weighted κ / Scott's π** (judge–human), per
   dimension. Never raw percent agreement (Thakur et al., GEM²@ACL 2025).
2. **The human ceiling**, bootstrapped Bavaresco-style (each annotator vs the aggregate of the others), with
   judge agreement expressed *as a fraction of that ceiling*.
3. **The alt-test** (Calderon, Reichart & Dror, ACL 2025): leave-one-annotator-out, BH-FDR, ε = 0.2.
   **ω ≥ 0.5 is the pass mark** and is the single strongest sentence available for the paper.

**Calibrate expectations, and say so in the paper.** Do *not* target α ≥ 0.8. The human–human ceiling for
judging free-form factoid QA correctness is **Fleiss' κ ≈ 0.73** (Kamalloo et al., ACL 2023 — same task);
the best judges in JUDGE-BENCH average **κ ≈ 0.28** (Bavaresco et al., ACL 2025). Judge–human weighted
κ of **0.6–0.75 against the measured ceiling**, plus ω ≥ 0.5, is a strong, honest result.

---

## Tier 2 — statistics that make a small human sample go further

Use **Prediction-Powered Inference** (Angelopoulos et al., *Science* 2023; PPI++; AutoEval Done Right,
Boyeau et al., ICML 2025) to combine the ~150 human labels with the 250-item judge labels into estimates
that are **unbiased even if the judge is biased**, with valid CIs.

Break-even condition I derived and simulated (see `Z2-ppi-budget-simulation.md`):
> PPI beats human-only annotation roughly when **judge–human disagreement `e` < `p(1−p)`**.

| Base rate | Required judge–human agreement |
|---|---|
| 0.07 (Wikitext-10) | **> 93.5%** |
| 0.28 (Pop-QA / SQuAD) | **> 79.8%** |

Simulated effective sample-size gains peak at **~1.7×** at n ≈ 30–50 per cell. This is consistent with
Dorner et al. (ICLR 2025), who prove **no debiasing method beats a factor of 2** — with the important
nuance that their theorem assumes the judge is *no more accurate than the evaluated model*, whereas EmbGen
judges Llama-3-8B with GPT-5 and therefore sits in the favourable regime.

**Set expectations correctly: PPI will not rescue the underpowered comparisons.** The Pop-QA (+4 items) and
SQuAD (+2 items) gaps need ~10⁴ items to resolve. PPI's job is to make the point estimate trustworthy and
the interval honest — not to manufacture significance.

Also report, per the statistics literature: exact/Wilson intervals rather than Wald or CLT-based ones at
these base rates (Brown, Cai & DasGupta, *Statistical Science* 2001; Bowyer et al., ICML 2025).

---

## Tier 3 — breaking the teacher = judge confound  [B — pending]

For Pop-QA-Cities-20 and SQuAD-20, `M_teach` = **GPT-5** and the judge is **also GPT-5**. Even though the
teacher is held fixed across methods, the student trained on GPT-5-derived data produces GPT-5-flavoured
answers, which a GPT-5 judge may systematically prefer.

*(mitigation design pending Agent B)*

---

## Tier 4 — a better-grounded second metric  [D — pending]

*(claim-level factuality protocol pending Agent D)*

---

## Tier 5 — eval-set validity  [E — pending]

See `Z3-eval-set-construct-validity.md` — this may be the highest-priority item in the whole document.
