# Strengthening EmbGen's LLM-as-a-Judge evaluation
### A methodology proposal for the NeurIPS 2026 Pre-to-Post workshop submission

**Deadline: 29 Aug 2026 AoE (7 days). Short papers 4–5 pages, NeurIPS style, non-archival.**
OpenReview: `NeurIPS.cc/2026/Workshop/Pre-to-Post`. Notification 29 Sep; workshop 11 Dec, Sydney.
Submissions must nominate a reciprocal reviewer.

Supporting literature: 110 papers in `claude-papers/`, annotated in `claude-papers/notes/`.
Runnable statistics: `claude-papers/code/judge_stats.py`.

---

## 1. The headline recommendation

**Do not submit a compressed EmbGen. Submit a focused evaluation-methodology paper that uses EmbGen as its
testbed.**

Three reasons:

1. **It fits the venue.** The CFP asks about *defining what "success" in post-training means* and
   *predicting when post-training fails* (topics #6 and #9). A protocol for measuring whether synthetic-SFT
   knowledge injection worked, when no gold labels exist, is squarely on-topic.
2. **It fits 4–5 pages.** The full EmbGen pipeline does not.
3. **It is a real gap.** Surveying EmbGen's own subfield:

| | EntiGraph | InstructLab/LAB | Knowledge-Instruct | Ovadia 2024 |
|---|---|---|---|---|
| Uses an LLM judge | summarisation only | yes (GPT-4) | yes (GPT-4o) | no |
| **Judge validated against humans** | **No** | **No** | **No** | n/a |
| **CIs / significance tests** | **None** | **None** | **None** | **None** |
| Judge-free scoring slice | yes (MCQ) | — | yes (oracle filter) | yes (log-prob MCQ) |
| Oracle-context / contamination control | yes | no | yes | yes |

**Nobody in this subfield validates their judge or reports error bars.** Being first is a contribution.

Since the venue is non-archival and the arXiv preprint exists, this costs you nothing.

---

## 2. Eight problems, ordered by how likely they are to sink the paper

| | Problem | Severity | Cost to fix |
|---|---|---|---|
| **P0** | **Eval sets may not test cross-document reasoning at all** (§5.1 claim vs Appendix D.6 prompts) | **critical** | low |
| **P1** | Judge never validated against humans | critical | medium |
| **P2** | Teacher = judge (GPT-5/GPT-5), confounded with the heterogeneity variable | high | low |
| **P3** | No CIs, no significance tests; 3 of 4 "wins" are 2–4 items | high | **zero** |
| **P4** | Verbosity confound on Completeness, the dimension carrying the result | medium | **zero** |
| **P5** | temp-0 × 10 runs does not measure judge variance | medium | **zero** |
| **P6** | Clarity is a dead dimension; Relevance/Clarity redundant (r = +0.82) | low | **zero** |
| **P7** | Lexical metrics chosen (BLEU/ROUGE/METEOR) all penalise the longer answers that are EmbGen's mechanism | medium | **zero** |
| **P8** | No known-vs-new-knowledge stratification; hallucination-from-new-knowledge is an unaddressed alternative explanation | medium | **zero** |

**Six of eight cost nothing** — the data is already on disk. Tier 0 alone converts the paper from
"reviewer will object" to "reviewer will accept the claims as stated", because the claims become *smaller
and defensible* rather than large and unsupported.

---

## 3. P0 — the construct-validity problem (read this first)

§5.1 says the eval questions *"frequently require reasoning over information distributed across multiple
chunks, pages, or documents."* Your own appendix prompts say otherwise:

- **Pop-QA** (D.6.1) mandates **50% surface-level** questions (`"What is [entity]'s [attribute]?"`). The
  multi-reference rule applies only to non-surface questions and asks for two paragraphs *of the same context*.
- **Wikitext-10** (D.6.2) is a **paraphrase** prompt operating on one document at a time — and this is where
  your headline result lives.
- **SQuAD-20** uses native SQuAD: single-paragraph extractive QA by design.

If the evaluation does not require cross-document integration, EmbGen's central hypothesis is untested, and
no judge improvement can fix that.

**Verify against your actual generation code first** — the appendix may not document a filtering step.

**Then, the cheap decisive fix — a hop-count audit.** Your Pop-QA prompt already collects
`<REFERENCE> LINE:#` provenance. Use it to record, per item, how many distinct source chunks/documents the
reference answer needs. Report the distribution, then **stratify every result table by 1-hop vs ≥2-hop**.
If EmbGen's advantage concentrates in ≥2-hop items, that is a far stronger and more mechanistic result than
the current aggregate — it evidences the thesis directly.

Add a **single-chunk vs full-context oracle ablation** (inference only): questions answerable from one
chunk are not multi-hop. MuSiQue (TACL 2022) shows a single-hop model dropping 30 F1 — that gap is the
diagnostic to replicate.

If the audit shows the sets are mostly 1-hop, **say so in Limitations**. An honest negative finding about
your own benchmark is publishable at this venue and far safer than a claim a reviewer can falsify from
your appendix.

---

## 4. Tier 0 — zero-cost fixes, using data already on disk

Run `claude-papers/code/judge_stats.py` on your per-item judge outputs.

**4.1 Judge stability (P5).** Your paper already contains the evidence. Binary Accuracy is reported to 3
decimals; if the 10 runs agreed on every item, every value would be a multiple of 1/250. Of the 37 distinct
values in Tables 3–4, **13 cannot be `k/250`** — but **all 37 are expressible as `k/2500`**. So GPT-5 at
`temperature=0` gave different verdicts across runs, and averaging discards that.

Report **Krippendorff's α (ordinal) across the 10 runs** and **% of items where all 10 runs agree**. Caveat
honestly: temp-0 repetition measures backend non-determinism only — a *floor* on judge variance, not an
estimate. The proper version (Yamauchi et al. show non-deterministic sampling aligns *better* with humans)
is **T = 1 with ≥5 samples**, plus rubric paraphrases, reported as a variance decomposition. Report
**Repetition Stability** (Shi et al.; ≥0.87 is the healthy band) or **CALM's Consistency Rate** (Ye et al.,
ICLR 2025).

Also emit **G-Eval probability-weighted scores** (Liu et al., EMNLP 2023): weight each label by its token
probability to get a continuous score, instead of your current categorical → ordinal → averaged → *rounded
back to categorical* round-trip, which throws away precisely the information that distinguishes methods
separated by 2–4 items.

**4.2 Confidence intervals (P3).** **Wilson intervals, not Wald and not bootstrap.** Bowyer et al.
(ICML 2025, Position track) show that at N≈100 with few successes, nominal-95% CLT intervals achieve only
92.5% coverage and **the bootstrap is equally badly calibrated**; only Wilson and Bayesian Beta hold. Your
N=250 with 9–17 successes on Wikitext-10 is squarely in that failure regime.

| Comparison | EmbGen | Baseline | EmbGen 95% Wilson | Baseline 95% Wilson |
|---|---|---|---|---|
| Wikitext-10 @ 20M | 0.068 (17/250) | 0.036 (9/250) | [0.043, 0.106] | [0.019, 0.067] |
| Wikitext-10 @ 5M | 0.072 (18/250) | 0.064 (16/250) | [0.046, 0.111] | [0.040, 0.101] |
| SQuAD-20 @ 20M | 0.288 (72/250) | 0.280 (70/250) | [0.235, 0.347] | [0.228, 0.339] |
| Pop-QA @ 20M | 0.282 (~71/250) | 0.266 (~67/250) | [0.228, 0.339] | [0.213, 0.322] |

**4.3 Paired significance tests (P3).** Dietterich (*Neural Computation* 1998) states the two-proportion
difference test **"should never be used"** — pre-empt the reader who applies it to 0.068 vs 0.036. Use
**McNemar's exact test** on the same item ids (discordant counts here are ~10–25, so exact not chi-square):

| Comparison | Gap | *p* if EmbGen strictly dominates | *p* if c=5 | *p* if c=10 |
|---|---|---|---|---|
| Wikitext-10 @ 20M | 8 items | **0.008** | 0.096 | 0.185 |
| Pop-QA @ 20M | 4 items | 0.125 | 0.424 | 0.541 |
| SQuAD-20 @ 20M | 2 items | 0.500 | 0.774 | 0.832 |
| Wikitext-10 @ 5M | 2 items | 0.500 | 0.774 | 0.832 |

Minimum detectable effect at N=250: **≥6 items (2.4 pts) even in the best case**, rising to ~16 items if 20
items are baseline-only-correct. Add **cluster-robust SEs by source document** (eval items are corpus-clustered)
and **Benjamini–Hochberg at q=0.05** across the ~24 comparisons.

**4.4 Reframe the headline (P3).** Retire *"88.9% relative uplift"*. On a 3.6% base rate, relative gains are
unstable by construction — and the increase from 12.5% to 88.9% happens because the **best baseline collapsed**
(EntiGraph 0.064 → 0.020; InstructLab steady at 0.036) while **EmbGen itself declined** (0.072 → 0.068).

Two better framings, both defensible:
- **Robustness:** *"EmbGen maintains Binary Accuracy under a 4× token-budget increase on the most
  heterogeneous corpus, where every baseline degrades."* This is what the data actually shows.
- **Replicability count** (Dror et al., TACL 2017): *"EmbGen beats baseline X on u of 6 (dataset, budget)
  settings at FDR 0.05."* Multiplicity-corrected and small-N robust.

State Pop-QA and SQuAD as **parity with the strongest baseline**. That is still publishable.

**4.5 Verbosity control (P4).** The paper reports no answer-length statistics anywhere. Since the mechanism
is *"EmbGen produces more complete answers"* and completeness correlates mechanically with length, the
result cannot currently be distinguished from a verbosity effect. You have every generated answer.

Do all three, cheapest first:

1. **Length-stratified accuracy** (Singhal et al., COLM 2024): bucket answers in 20-token bins and report
   the share of the gap that survives within-bucket. One line of pandas — and the number to beat is
   sobering: in two of their three settings only **2.0%** and **27.2%** of the apparent gain survived
   length stratification. That is the figure to report against your 88.9%.
2. **The Dubois GLM** (Length-Controlled AlpacaEval, COLM 2024):
   `logit P(BinAcc = 1) = θ_system + φ·tanh((len − len_ref)/σ) + ψ_item`, then zero the length term.
   Bonus: the `ψ_item` term is itself a paired-design variance reduction, so this also helps P3.
   `length_controlled()` in the toolkit implements the simpler `correct ~ method + log(len)` form.
3. **Content-preserving expansion probe** (CALM, Ye et al., ICLR 2025): lengthen answers *without adding
   information* and measure how often the judge's verdict flips.

**4.6 Rubric validity (P6).** Computed across the 29 cells of Table 3, excluding the degenerate
EntiGraph/Wikitext-20M row:

| Dimension | min | max | sd | % of 1–3 scale used |
|---|---|---|---|---|
| Factual Accuracy | 1.05 | 1.75 | 0.207 | 35.0% |
| Completeness | 1.32 | 2.14 | 0.284 | 41.0% |
| Relevance | 2.02 | 2.94 | 0.278 | 46.0% |
| **Clarity** | **2.81** | **3.00** | **0.058** | **9.5%** |

**Clarity is dead** — 0.19 points of a 2-point scale, never discriminating between methods. Drop it from the
headline rubric or justify it as a sanity check.

Inter-dimension correlations: **Relevance × Clarity = +0.82** (one latent "fluency" factor — the classic halo
effect). Completeness is near-orthogonal to both (+0.09, −0.01), so it *is* carrying independent signal —
good for your story, but it means the verbosity confound lands on exactly the dimension the result depends on.

Recompute at **item level with polychoric correlations** (these are ordinal) and publish the matrix as a
**discriminant-validity check**. That answers P6 in one table.

**Two further points on the scale itself.** Stureborg et al. find that (i) **finer score granularity
improves judge reliability**, so your 3-level Strong/Adequate/Weak scale is a *liability, not a safeguard*;
and (ii) **GPT-4's inter-sample agreement (α = 0.587) is below human inter-annotator agreement
(α = 0.659)** — useful calibration for §5, and a good sentence to quote when setting reviewer expectations.
Amidei et al. (COLING 2018) add the complementary warning: collapsing categories *mechanically inflates* κ
(0.463 → 0.862 in their example), so acknowledge that your 3-level scale flatters your agreement numbers.

**4.7 Fix the lexical-metric table too (P4, zero cost).** Adlakha et al. (**TACL 2024**) human-annotated
1,800 QA responses and ranked automatic metrics by correlation with humans (Spearman ρ×100):

| Metric | Spearman ρ×100 | Kendall τ×100 |
|---|---|---|
| Exact Match | 27.3 | 27.3 |
| BERTScore-F1 | 31.9 | 26.1 |
| Precision | 43.9 | 37.6 |
| ROUGE-L | 45.9 | 38.8 |
| F1 | 47.3 | 40.2 |
| METEOR | 48.2 | 39.8 |
| BEM | 53.7 | 43.9 |
| **Token-level Recall** | **60.0** | **55.6** |
| GPT-3.5-Eval | 61.4 | 61.4 |
| GPT-4-Eval | 67.5 | 67.5 |

(Their Table 3, verified against the PDF. The paper's own explanation: recall correlates best among lexical
metrics *"likely because it does not penalize the additional verbosity in model responses."*)

**Token-level recall beats every other lexical metric precisely because it does not penalise verbosity.**
Your Table 2 currently reports BLEU/ROUGE/METEOR, all of which penalise the longer, more complete answers
that are your mechanism — which is why the lexical table disagrees with the judge table. Adding recall
would likely *resolve* that disagreement in your favour, and it is a one-line computation on data you have.

Also compute **K-Precision** — the fraction of answer tokens appearing in the source corpus. It is a
corpus-grounded faithfulness proxy requiring no model at all, and it previews the Tier 4 metric for free.

**4.8 Stratify by known vs newly-injected knowledge (a threat you should get ahead of).**
Gekhman et al. (**EMNLP 2024**), *Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?*, show
that SFT examples carrying genuinely new knowledge are learned much more slowly and, once fitted,
**linearly increase hallucination on previously-known questions**. EmbGen is doing precisely
knowledge-injection SFT, so this is a direct alternative explanation for degradation — and possibly for why
Wikitext-10 accuracy *falls* from 5M to 20M.

Use their Known/Unknown categorisation to split your 250 eval items by whether the base Llama-3-8B-Instruct
already answers correctly (you have that number — it is your no-augmentation baseline). Then report the
EmbGen effect separately on each stratum. If EmbGen injects new facts *without* degrading pre-existing
knowledge, that is a strong positive result and one no baseline in your comparison has demonstrated. If it
does degrade, you have found the mechanism behind your own token-budget decline — also publishable, and far
better discovered by you than by a reviewer.

---

**4.9 Validate the judge with ZERO annotation (partial P1 fix — do this first).**
Before spending any human budget, run your exact judge prompt on two benchmarks that already have
**objective, human-verified labels**:

- **LLMBar** (Zeng et al., ICLR 2024) — objective instruction-following preference labels; expert human
  agreement is 94% here, vs 63–66% on subjective preference sets.
- **EvalBiasBench** (Park et al., Findings EMNLP 2024) — six bias types; GPT-4o scores 86.9.

This costs API calls only and gives you a *citable, externally-benchmarked* number for your judge before
any annotator is recruited. It does not replace the human study in §5 — those benchmarks are not your task
— but it is the cheapest possible evidence that your judge is not broken, and it de-risks the human study.

Add a **40-item flawed-answer probe** built from your own questions (Wu & Aji, COLING 2025): correct vs
minor-error vs major-error, crossed with long vs short. Their headline failure is the one to test for —
GPT-4 rated *"several minor factual errors at 100 words"* (Elo 1206) **above** *"correct at 50 words"*
(Elo 1096). If your judge does that, you need to know before a reviewer does. Zero annotation required —
you construct the errors, so you know the labels.

---

---

## 5. Tier 1 — human validation of the judge (the load-bearing new work)

This is the objection that sinks LLM-as-a-judge papers, and it cannot be avoided.

**Design.** ~**150 items**, stratified across the three corpora *and* **on the judge's own verdict** (on
Wikitext-10 a uniform sample of 50 yields ~3 judge-positive items — useless). **3 annotators**, each
labelling all items — the minimum for the alt-test, and the norm in JUDGE-BENCH. Run a **20-item pilot
first and revise the rubric**: Shankar et al. (UIST 2024) show criteria drift makes an unrevised a-priori
rubric unreliable. Blind to system identity; randomise order.

**Annotate only Factual Accuracy + Completeness**, plus derived Binary Accuracy. Not Clarity — human
agreement on subjective criteria collapses to 63–66% vs 94% on objective ones (LLMBar, ICLR 2024), so a low
κ there would tell you nothing.

Three co-authors × 150 items ≈ half a day each. You have four authors.

**Report:**
1. **Ordinal-weighted Krippendorff's α** (human–human) and **weighted κ / Scott's π** (judge–human), per
   dimension. Never raw percent agreement — judges with matching percent agreement differ by 10–20 score
   points (Thakur et al., GEM²@ACL 2025).
2. **The bootstrapped human ceiling** (each annotator vs the aggregate of the others), with judge agreement
   expressed **as a fraction of that ceiling**.
3. **The alt-test** (Calderon, Reichart & Dror, **ACL 2025**): leave-one-annotator-out, BH-FDR, ε = 0.2 for
   experts. **ω ≥ 0.5 is the pass mark**, and it is the single strongest sentence available to the paper.

**Calibrate expectations in the text.** Do *not* target α ≥ 0.8. The human–human ceiling for judging
free-form factoid QA correctness is **Fleiss' κ ≈ 0.728** (Kamalloo et al., ACL 2023 — the same task); the
best judges in JUDGE-BENCH average **κ ≈ 0.28** (Bavaresco et al., ACL 2025). **Weighted κ of 0.6–0.75
against the measured ceiling, plus ω ≥ 0.5, is a strong and honest result.** Frame residual disagreement as
label variation (Plank, EMNLP 2022; Aroyo & Welty 2015), and note that a 3-level scale mechanically
inflates κ relative to a finer one (Amidei et al., COLING 2018).

**Free add-on, no human labels:** a **misinformation-oversight probe** — inject known factual errors into
~50 correct answers and measure how often the judge downgrades Factual Accuracy. Evaluator LLMs miss >50%
of such drops (Doddapaneni et al., EMNLP 2024), so a good number is a real result.

---

## 6. Tier 2 — making 150 human labels go further (PPI++)

Combine the human subsample with the 250-item judge labels using **PPI++** (Angelopoulos et al., *Science*
2023; Boyeau et al., **ICML 2025**, `ppi_py`). The estimate is **unbiased even if the judge is biased** —
the judge only needs to be *correlated* with humans.

**Use the tuned-λ form, not plain PPI.** Plain PPI can be *worse* than just using the human labels at
n ≲ 50–100 (Eyre & Madras, ICML 2025) — exactly your budget. With λ̂ tuned, λ̂→0 recovers the human-only
estimator, so PPI++ is never worse. Verified by simulation (worst case: p=0.07, mediocre judge):

| n human | human-only ± | plain PPI ± | **PPI++ ±** | λ̂ | gain |
|---|---|---|---|---|---|
| 30 | 0.083 | 0.112 ✗ | **0.069** | 0.35 | **1.43×** |
| 60 | ~0.063 | ~0.089 ✗ | **~0.055** | 0.29 | ~1.27× |
| 100 | 0.049 | 0.079 ✗ | **0.045** | 0.22 | 1.18× |

**Budget: 60–80 items per cell**, not 50 (Eyre & Madras floor). Label **all ~17 judge-positive items** on
Wikitext-10 plus a 15–30% sample of judge-negatives, **recording sampling probabilities**.

**Break-even condition** I derived and simulated — PPI helps when judge–human disagreement `e < p(1−p)`:

| Base rate | Required judge–human agreement |
|---|---|
| 0.07 (Wikitext-10) | **> 93.5%** |
| 0.28 (Pop-QA / SQuAD) | **> 79.8%** |

This converges with Chaganty et al. (ACL 2018), who found only 7–13% cost reduction because variance
reduction goes as `1−ρ²` and you need **ρ ≈ 0.93 just to halve cost**. So **measure and report judge–human ρ**
rather than assuming PPI is free.

**Set expectations honestly: PPI will not rescue the underpowered comparisons.** Dorner et al. (ICLR 2025)
prove no debiasing method beats a factor of 2 in label savings. The Pop-QA (+4 items) and SQuAD (+2 items)
gaps need ~10⁴ items. PPI's job is to make the point estimate trustworthy and the interval honest — not to
manufacture significance.

*(Useful nuance: Dorner's theorem assumes the judge is no more accurate than the evaluated model. You judge
Llama-3-8B with GPT-5, so you sit in the favourable regime. Cite it as "we operate where debiasing is
provably useful", not as a limitation of your setup.)*

Cross-check every PPI estimate with **Rogan–Gladen**: `p̂_corr = (p̂_judge + Sp − 1)/(Se + Sp − 1)`.

---

## 7. Tier 3 — breaking the teacher = judge confound

| Dataset | Heterogeneity | Teacher | Judge | Relatedness (Li et al., ICLR 2026) |
|---|---|---|---|---|
| Pop-QA-Cities-20 | lowest | **GPT-5** | GPT-5 | **same model** |
| SQuAD-20 | intermediate | **GPT-5** | GPT-5 | **same model** |
| Wikitext-10 | **highest** | **gpt-4o-mini** | GPT-5 | same family |

*Preference Leakage: A Contamination Problem in LLM-as-a-Judge* (Li et al., **ICLR 2026**) defines exactly
these relatedness levels and confirms judges favour students trained on data from related generators, noting
it is *"harder to detect than previously identified biases."*

**Partial defence you already have:** the teacher is fixed across methods within a dataset, so between-method
comparisons are partly protected. Say this — it is real and costs nothing.

**The serious part:** teacher identity is **confounded with your central independent variable**. Wikitext-10
is both the most heterogeneous corpus *and* the only one with a different teacher. A reviewer can offer:
*"the Wikitext-10 result differs because the teacher was weaker and leakage was lower, not because
heterogeneity was higher."* With 3 datasets and 2 teachers this cannot be separated from existing runs.

**Minimum (hours, inference only):** re-judge the **Wikitext-10 @ 20M** cell with a **non-OpenAI judge**
(Claude, Gemini, or open-weight Prometheus-2). If the ranking survives a different judge family, the
objection is answered for the claim that matters — and it simultaneously addresses the single-judge problem.

**Strongly recommended:** also re-judge **Pop-QA @ 20M** with that judge. The **difference-in-differences**
between a GPT-5-teacher cell and the gpt-4o-mini-teacher cell is a direct estimate of preference leakage in
your own setup — a genuinely novel measurement, and exactly what CFP topic #9 asks for.

**Non-negotiable:** add the teacher column to the dataset table and state the confound in Limitations. A
reviewer who finds it unaided in Appendix A.8 reads it as concealment.

**7.1 A scope correction to state explicitly.** EmbGen grades **one answer at a time against a reference**.
Classic **position/order bias does not apply** — it is a property of pairwise or list-wise comparison. Say
this in the paper, because a reviewer who sees no position-bias analysis will otherwise assume you ignored
it. What *does* apply to pointwise grading is: (a) **anchoring across the four dimensions scored in a single
prompt**, (b) **verbosity/salience bias**, (c) **self-preference / preference leakage**, and
(d) **ordinal-scale compression**.

**7.2 Score each dimension in a separate call.** You currently score all four dimensions in one prompt.
Stureborg et al. measure anchoring across exactly this design: Kendall τ falls **0.400 → 0.368** from the
first attribute scored to the fourth. **Clarity is your fourth dimension** — so its degeneracy (§4.6) may be
partly an artefact of prompt position rather than a property of the answers. Splitting the calls is cheap
and tests that directly.

**7.3 Quantify the leakage.** Li et al.'s **Preference Leakage Score requires no human labels** — it is
computed from two generator models × two judges — and they measure PLS up to **37.1%**, near-zero for
unrelated pairs, *growing with the proportion of synthetic data* and *worst for small students*.

A caveat on applying it here: the clean 2×2 needs both teachers crossed with both judges on the *same*
corpus, whereas your teachers vary *with* the dataset. So the exact PLS is not directly computable from
existing runs — the difference-in-differences in §7 is the closest available substitute, and generating one
small Wikitext-10 dataset with GPT-5 as teacher would make the true 2×2 possible.

For the second judge, **Prometheus-2-8x7B** (EMNLP 2024) is free, open-weight, and **reference-based, so it
matches EmbGen's prompt format exactly**.

> ⚠ **Use it as a disagreement detector, not a gold standard.** Prometheus-2-7B scores only **34.4 on
> EvalBiasBench (17.6 on the Length category)**. It is a *de-confounding* judge — valuable because its
> lineage is disjoint from GPT-5's, not because it judges better. Do not present its agreement as
> validation; present *disagreement* as evidence of leakage.

A small Claude/Gemini panel is the better instrument if budget allows. Aggregate by **PoLL max-voting**
(Verga et al.: σ = 2.2 vs 6.1 for a single judge, κ = 0.76–0.91, 7–8× cheaper than one large judge).
Report the headline under both judges.

CALM's own recommendation is quotable and blunt: *"Avoid using the same model to generate and judge answers."*

Note the risk profile honestly: **an 8B student trained on ~100% synthetic GPT-5 data, judged by GPT-5, is
the maximum-risk configuration in Li et al.'s taxonomy.**

---

## 8. Tier 4 — a corpus-grounded second metric (if time allows)

Your reference answers are themselves LLM-written, so Binary Accuracy measures agreement with another LLM,
not with truth. The accepted alternative decomposes answers into atomic claims and verifies each **against
the source corpus you already own**.

**CorpusFActScore.** (1) Decompose each answer into verifiable atomic claims (FActScore, EMNLP 2023;
VeriScore's fine-tuned Mistral-7B extractor is a drop-in), decontextualised to molecular granularity
(Gunjal & Durrett, EMNLP 2024). (2) Retrieve top-5 chunks from the corpus using the embedding index EmbGen
already built. (3) Verify with **MiniCheck-FT5 (770M)** — 74.7 vs GPT-4's 75.3 balanced accuracy on
LLM-AggreFact at **~400× lower cost** (EMNLP 2024). (4) Report claim **precision**, and **F1@K** with
recall capped à la SAFE (NeurIPS 2024).

**Why it is strictly better grounded:** it measures agreement with the corpus rather than with a Claude-written
reference; precision penalises unsupported additions while K caps the reward for length (defusing P4); and it
is computed by non-GPT models, breaking the teacher/judge overlap (P2).

**Cost: under $1 of compute for ~20k claims, minutes on one GPU.** Genuinely feasible.

*One caveat to handle:* moving from 250 answers to ~250×10–30 claims does raise effective N, but claims
within an answer are **not independent** — use cluster-robust SEs by item, or the gain is illusory.

Given the deadline, run this on **one cell (Wikitext-10 @ 20M)** as a proof of concept, and present it as the
protocol's natural extension.

---

## 9. What to cut

- Full claim-level re-evaluation of all ~6,750 answers → one cell only.
- Swapping judges across every condition → headline cell + one control cell.
- Adding MuSiQue / LongBench-v2 as an external human-authored control → high value, needs a new eval cycle.
  Name it as the obvious next step.
- Regenerating eval sets → only if the hop-count audit forces it; otherwise report honestly.

---

## 10. Seven-day schedule

| Days | Work |
|---|---|
| **1** (Sat) | §4.9 zero-annotation judge validation (LLMBar + EvalBiasBench + flawed-answer probe) — do this **first**, it de-risks everything after. Start the P0 hop-count audit. |
| **1–2** (Sat–Sun) | The rest of Tier 0 (§4) — no new compute. |
| **2–4** (Sun–Tue) | Human validation: 20-item pilot → rubric revision → 150 items × 3 annotators. Feed into PPI++. |
| **3–5** (Mon–Wed) | Judge-swap on 2 cells (§7). Oracle-answerability filter + single-chunk ablation (inference only). |
| **5–6** (Wed–Thu) | Write. 4–5 pages — the tables *are* the paper. |
| **7** (Fri) | Submit early in the AoE window. Nominate the reciprocal reviewer. |

---

## 11. On the DeepEval blog you linked

It is a vendor doc and **cites zero academic sources**, so do not cite it. But its three named patterns all
have peer-reviewed ancestors — cite those instead:

| DeepEval term | Cite instead |
|---|---|
| **G-Eval** | Liu et al., *G-Eval*, EMNLP 2023 |
| **QAG** (question-answer generation) | FActScore (EMNLP 2023); QAFactEval (NAACL 2022) |
| **DAG** (decision-tree scoring) | Checklist-based judging: TICK; CheckEval; FLASK (ICLR 2024) |
| "validate against human annotations" | The whole of §5 above |

Its advice to use `strict_mode` binary pass/fail is, in effect, what your Binary Accuracy already does.
