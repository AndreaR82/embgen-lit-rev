# Agent C — Statistical validity, uncertainty quantification, and combining few human labels with many LLM-judge labels

Target: EmbGen (arXiv:2605.19394), NeurIPS 2026 workshop *pretrain2posttrain*.
Primary weaknesses addressed: **W4** (no UQ / no significance tests), **W3** (temp=0 x 10 runs does not measure judge variance), **W1** (no human validation of the judge), **W2** (self-preference), **W6** (synthetic references).

All PDFs live in `/Users/andreanicastro/Documents/repos/embgen-lit-rev/llm-as-a-judge/claude-papers/`.
All 25 files verified: `>50KB` and magic bytes `%PDF`.

Notation used throughout: EmbGen's Binary Accuracy is a **proportion** `p̂ = S/N` with `N = 250` per (dataset, budget) cell. Headline claim is `0.068 vs 0.036` ≈ **17 vs 9 successes out of 250**.

---

## Part 1 — Prediction-Powered Inference (PPI) and LLM autoevaluation

### 1. Angelopoulos, Bates, Fannjiang, Jordan & Zrnic (2023). "Prediction-Powered Inference."
**Venue (verified): *Science* 382(6671):669–674, 2023.** DOI 10.1126/science.adi6000. Preprint arXiv:2301.09633.
File: `C_Angelopoulos2023_PredictionPoweredInference_Science.pdf`

The founding paper of the PPI family. Given a small labelled set of size `n` (gold `Y`, prediction `f(X)`) and a large unlabelled set of size `N ≫ n` with only predictions, PPI forms a **rectifier**: the point estimate is the machine-learning estimate on the big set *minus* the estimated bias measured on the small labelled set. The resulting CI is **provably valid regardless of how bad the predictor is** — no assumption of accuracy, calibration, or even that `f` is related to `Y`. Formally for a mean: `θ̂^PPI = (1/N)Σ_{i∈unlab} f(X_i) − (1/n)Σ_{i∈lab}(f(X_i) − Y_i)`, with variance `σ²_f/N + σ²_Δ/n` where `Δ = f(X) − Y`. Because `Var(Δ) ≪ Var(Y)` whenever the judge is decent, the CI is much narrower than the human-only CI computed from the same `n` labels.
**EmbGen should apply**: treat the GPT-5 judge's Binary Accuracy label as `f(X)`, and a small human-labelled subset as `Y`; report a PPI 95% CI on Binary Accuracy per (method, dataset, budget) cell.
**USE FOR: W4 (primary), W1, W6.** — PPI is the single mechanism that converts "we have no gold set" into "we have a valid CI from ~50 gold labels."
**Numbers**: PPI's CI half-width scales as `√(σ²_f/N + σ²_Δ/n)`; with a judge whose disagreement rate with humans is `e`, the human-label requirement to match a human-only CI shrinks roughly by the factor `Var(Δ)/Var(Y) ≈ e(1−e)/(p(1−p))`. For `p ≈ 0.07` and judge–human disagreement `e ≈ 0.10`, this is ≈ 1.4 — i.e. modest; for a well-agreeing judge (`e ≈ 0.05`) it is ≈ 0.73. **Do not overclaim PPI gains at low `p`** (see #4).

### 2. Angelopoulos, Duchi & Zrnic (2023). "PPI++: Efficient Prediction-Powered Inference."
**Venue (verified): arXiv:2311.01453 — arXiv-only preprint, but canonical (it is the version implemented in `ppi_py` and the one every downstream paper uses). FLAGGED as non-peer-reviewed.**
File: `C_Angelopoulos2023_PPIplusplus_arXiv.pdf`

Fixes the one real defect of vanilla PPI: when the predictor is weak or `n` is small, the rectifier term adds variance and PPI can be *wider* than the classical human-only CI. PPI++ introduces a scalar **power-tuning parameter λ**: `θ̂^λ = (λ/N)Σ_unlab f(X_i) − (λ/n)Σ_lab f(X_i) + (1/n)Σ_lab Y_i`. λ is estimated to minimise asymptotic variance; `λ = 0` exactly recovers the classical human-only estimator and `λ = 1` recovers vanilla PPI. Consequently PPI++ is **asymptotically never worse than classical inference**, which is exactly the safety property a reviewer will demand.
**EmbGen should apply**: use PPI++ (not vanilla PPI) as the default estimator, and **report the fitted λ̂** — λ̂ near 0 is itself an honest admission that the judge is uninformative; λ̂ near 1 is evidence the judge tracks humans.
**USE FOR: W4, W1.**
**Numbers**: variance is reduced by a factor `1 − ρ²` relative to classical, where `ρ` is the correlation between judge label and human label on the labelled subset; λ̂* = `Cov(f, Y)/Var(f)` scaled by `n/(n+N)`.

### 3. Boyeau, Angelopoulos, Li, Yosef, Malik & Jordan (2025). "AutoEval Done Right: Using Synthetic Data for Model Evaluation."
**Venue (verified): ICML 2025, PMLR 267:5276–5290.** Preprint arXiv:2403.07008.
File: `C_Boyeau2025_AutoEvalDoneRight_ICML2025.pdf`

**This is the single most directly transferable paper for EmbGen.** It instantiates PPI/PPI++ specifically for *model evaluation with AI-generated labels* — i.e. exactly EmbGen's setting (GPT-5 judge labels on 250 items, few or no human labels). It shows how to autoevaluate accuracy, pairwise win-rates, and *rankings* of models with calibrated CIs, extends PPI to the case where the annotator emits a **distribution** over labels rather than a point label (relevant to EmbGen's 10-run averaged ordinal scores), and ships the tooling as `ppi_py` (`github.com/aangelopoulos/ppi_py`; experiment code `github.com/PierreBoyeau/autoeval`).
**EmbGen should apply**: the paper's Algorithm for *accuracy* — identical to Binary Accuracy — and its **effective sample size (ESS)** diagnostic, which reports "how many human labels the classical estimator would have needed to be this precise."
**USE FOR: W4, W1, W6.**
**Numbers (from the paper)**: PPI++ ESS was systematically **~50% higher** than the classical human-only approach; rank recovery improved **five-fold at n = 1000**; PPI and PPI++ produced **calibrated CIs at all labelled-set sizes** while being strictly tighter than the classical baseline; and critically, **vanilla PPI performed *worse* than classical in one experiment — a known failure that PPI++ mitigates**. With a *very poor* annotator model, PPI++ degrades gracefully to λ = 0 and matches classical.

### 4. Eyre & Madras (2025). "Regression for the Mean: Auto-Evaluation and Inference with Few Labels through Post-hoc Regression."
**Venue (verified): ICML 2025, PMLR 267 (eyre25a).** Earlier version: *"Auto-Evaluation with Few Labels through Post-hoc Regression"*, **NeurIPS 2024 Workshop on Statistical Foundations of LLMs and Foundation Models**. Preprint arXiv:2411.12665.
File: `C_Eyre2025_RegressionForTheMean_ICML2025.pdf`

**Read this before committing to a human-label budget.** The key finding is a warning: **in the low-label regime PPI++ can perform *worse* than classical inference**, because λ̂ itself is estimated noisily from `n` points. The authors propose post-hoc regression / shrinkage variants (a tuned "PPI-with-regression" estimator and a shrinkage estimator on λ) that dominate both PPI++ and classical when `n` is small (tens, not hundreds) — precisely EmbGen's budget.
**EmbGen should apply**: if the human-label budget is `n < 100`, use the shrinkage/post-hoc-regression estimator from this paper rather than plain PPI++, and state which you used.
**USE FOR: W4, W1.**
**Numbers**: the failure regime is roughly `n ≲ 50–100`; the fix removes the λ̂-estimation penalty and gives lower-variance estimates than PPI++ throughout the low-label regime.

### 5. Chaganty, Mussmann & Liang (2018). "The Price of Debiasing Automatic Metrics in Natural Language Evaluation."
**Venue (verified): ACL 2018, pp. 643–653.** ACL Anthology `P18-1060`.
File: `C_Chaganty2018_PriceOfDebiasingAutomaticMetrics_ACL2018.pdf`

The classical NLP precursor to PPI, using **control variates** — mathematically the same construction (an unbiased human estimate corrected by a cheap automatic metric, weighted by their correlation). It is also the **honest, sobering counterweight** the paper should cite: the authors prove their estimator is statistically optimal and then measure only a **7–13% cost reduction** on summarization and open-response QA, because BLEU/ROUGE-class metrics correlate too weakly with human judgement. The variance reduction is exactly `1 − ρ²`, so a metric needs `ρ ≈ 0.93` merely to *halve* annotation cost.
**EmbGen should apply**: cite this as the reason the *judge–human correlation must be measured and reported*, not assumed; it converts the PPI story from hand-waving into a quantified budget argument. It also justifies using an LLM judge rather than BLEU/ROUGE as the control variate — an LLM judge plausibly has `ρ` far above BLEU's.
**USE FOR: W4, W1, and the framing of why lexical metrics (BLEU/ROUGE/METEOR) should be demoted in the results table.**
**Numbers**: **7–13%** cost reduction achieved; variance reduction factor `1 − ρ²`; `ρ > 0.93` needed for 2× savings.

### 6. Zrnic & Candès (2024). "Active Statistical Inference."
**Venue (verified): ICML 2024 (Oral), PMLR 235:62993–63010.** Preprint arXiv:2403.03208.
File: `C_Zrnic2024_ActiveStatisticalInference_ICML2024.pdf`

Answers the question "*which* of the 250 items should we pay a human to label?". Under a fixed labelling budget, it uses the model's own uncertainty to **sample items for labelling with non-uniform probabilities** and then reweights (Horvitz–Thompson style) so the estimator stays unbiased and the CI stays valid. Gains are largest when the predictor is confidently right on most items and uncertain on a few — exactly the regime of an LLM judge on easy vs. borderline QA pairs.
**EmbGen should apply**: draw the human-label subset with probability proportional to *judge uncertainty* — operationalised as the **entropy / disagreement across the 10 judge runs** — and use the paper's reweighted estimator. This turns EmbGen's existing 10-run protocol into a useful sampling signal instead of a near-degenerate one.
**USE FOR: W4, W3 (repurposes the 10 runs), W1.**
**Numbers**: active labelling reaches the same CI width with **~half to ~1/3 the labels** of uniform sampling in the paper's experiments; validity holds for *any* sampling rule as long as the probabilities are known and bounded away from 0 (set a floor, e.g. `π_i ≥ 0.05`).

### 7. Zrnic & Candès (2024). "Cross-Prediction-Powered Inference."
**Venue (verified): *PNAS* 121(15):e2322083121, 2024.** Preprint arXiv:2309.16598.
File: `C_Zrnic2024_CrossPredictionPoweredInference_PNAS2024.pdf`

Handles the case where you have **no pre-trained predictor** and must train the "judge"/imputation model on your own labelled data. Cross-prediction uses K-fold cross-fitting: train on `K−1` folds, predict the held-out fold, and rectify — preserving validity while extracting more signal than PPI with a fixed off-the-shelf predictor. Shows cross-prediction typically achieves the precision of a classical approach with **far more** labels than the labelled set actually contains.
**EmbGen should apply**: relevant if EmbGen fits a *calibration model* mapping the 4 judge dimensions (+ answer length!) onto human Binary Accuracy — that model must be cross-fitted or the CI is invalid. This is also the clean way to **regress out the verbosity confound (W5)** inside a valid-inference framework.
**USE FOR: W4, W5, W7.**
**Numbers**: reported ESS gains equivalent to a **2–5× larger** labelled set depending on predictor quality.

### 8. Chen, Lu, Li, Guo & Li (2026). "Efficient Inference for Noisy LLM-as-a-Judge Evaluation."
**Venue (verified): arXiv:2601.05420, 12 Jan 2026 — arXiv-only preprint, NOT peer-reviewed. FLAGGED. Cite as supporting, not load-bearing.**
File: `C_Chen2026_EfficientInferenceNoisyLLMJudge_arXiv.pdf`

The most on-topic recent work: it formally compares the **two** debiasing families for LLM judges — (i) **direct measurement-error correction** via **Rogan–Gladen**-style estimators (correct `p̂_judge` using the judge's estimated sensitivity/specificity against humans), and (ii) **surrogate-outcome / PPI** approaches. Using semiparametric efficiency theory it derives efficient-influence-function estimators for both and characterises exactly when PPI attains strictly smaller asymptotic variance. Code: `github.com/yiqunchen/debias-llm-as-a-judge`.
**EmbGen should apply**: the **Rogan–Gladen correction** is an excellent *second*, cheap estimator to report alongside PPI, because it maps directly onto EmbGen's binary setting: `p̂_corrected = (p̂_judge + Spec − 1)/(Sens + Spec − 1)`, with sensitivity/specificity estimated on the human-labelled subset. Agreement between PPI and Rogan–Gladen is a strong robustness signal.
**USE FOR: W4, W1, W2** (a judge with self-preference has *asymmetric* sensitivity/specificity, which this framework makes visible and correctable).

---

## Part 2 — Error bars and significance testing for LLM evaluations

### 9. Miller (2024). "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations."
**Venue (verified): arXiv:2411.00640 (Anthropic technical report) — arXiv-only. FLAGGED, but canonical and directly cited by ICML/NeurIPS work (e.g. #10 below).**
File: `C_Miller2024_AddingErrorBarsToEvals_arXiv.pdf`

The de facto standard checklist for LLM-eval statistics. Its five recommendations, verbatim: (1) compute standard errors of the mean via the CLT; (2) **when questions are drawn in related groups, compute clustered standard errors**; (3) **reduce variance by resampling answers and by analysing next-token probabilities**; (4) **when two models are compared, do inference on the question-level *paired differences*, not on the population-level summary statistics**; (5) **use power analysis** to decide whether an eval (or a random subsample) can even test the hypothesis of interest.
**EmbGen should apply**: recommendation (4) is the fix for the headline claim — compute `D_i = 1{EmbGen correct on item i} − 1{baseline correct on item i}` and test `mean(D) = 0`; the paired SE is `√(Var(D)/N)`, which is much smaller than the unpaired SE when the two systems succeed on overlapping items. Recommendation (2) matters because EmbGen's eval sets are **generated from clustered corpora** — items derived from the same entity/cluster are not independent.
**USE FOR: W4 (paired analysis + clustering), W3 (resampling answers).**
**Numbers**: for a paired binary comparison at `p₁ ≈ 0.068, p₂ ≈ 0.036`, `N = 250` gives roughly 20–30% power at α = 0.05 unless the outcomes are strongly positively correlated — i.e. **EmbGen's headline result is, as reported, almost certainly underpowered.** This must be stated.

### 10. Bowyer, Aitchison et al. (2025). "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints."
**Venue (verified): ICML 2025 (Position Paper track).** Preprint arXiv:2503.01747. Code: `github.com/sambowyer/bayes_evals`.
File: `C_Bowyer2025_DontUseCLTinLLMEvals_ICML2025.pdf`

**The most surgically applicable paper for the "which CI?" question.** Large simulation study measuring *empirical coverage* of CI methods on LLM evals. Findings: CLT-based (Wald) intervals and **bootstrap** intervals both under-cover badly at small `N`, sometimes producing intervals extending beyond `[0,1]` or collapsing to zero width; **only Wilson score intervals and Bayesian (Beta) credible intervals achieve nominal coverage** in the IID single-model setting. Clopper–Pearson is valid but **over-conservative / too wide** (they cite Agresti & Coull 1998; Newcombe & Nurminen 2011). For **clustered** questions, neither naive CLT nor clustered-CLT achieves correct coverage at small `N`; Bayesian methods extend cleanly. For **paired model comparison**, they explicitly recommend **Bayesian intervals for the difference or the odds ratio**, plus Fisher's exact odds ratio.
**EmbGen should apply**: report **Wilson 95% CIs** on Binary Accuracy (one line of SciPy: `binomtest(k=S, n=N).proportion_ci("wilson", 0.95)`), and a **Bayesian Beta(1+S, 1+N−S) credible interval for the paired difference/odds ratio** when comparing EmbGen to each baseline. **Do not use the naive bootstrap** — Bowyer et al. show it is poorly calibrated here, which is a trap since bootstrap is the reflexive choice.
**USE FOR: W4 (this is the direct answer).**
**Numbers**: at **N = 100, nominal-95% CLT intervals achieved only 92.5% empirical coverage**; coverage error for CLT/bootstrap grows sharply below `N ≈ 300` ("a few hundred datapoints"); Wilson and Bayesian intervals hold nominal coverage down to `N = 3–30`. **EmbGen's N = 250 with p̂ ≈ 0.05 sits squarely in the failure regime**, because the *effective* count is `S ≈ 9–17`, not 250.

### 11. Dror, Baumer, Shlomov & Reichart (2018). "The Hitchhiker's Guide to Testing Statistical Significance in NLP."
**Venue (verified): ACL 2018, pp. 1383–1392.** ACL Anthology `P18-1128`.
File: `C_Dror2018_HitchhikersGuideStatSig_ACL2018.pdf`

The community's standard decision procedure for *which* significance test to use in NLP, organised by the measure's distributional properties (parametric vs. non-parametric, paired vs. unpaired, bounded vs. unbounded). Provides a decision tree plus a replicable protocol and code.
**EmbGen should apply**: follow the decision tree for a **paired, binary, bounded** measure — it lands on **McNemar's exact test** or a **paired permutation (approximate randomisation) test**. Cite this to preempt "why this test?" from a reviewer.
**USE FOR: W4.**

### 12. Card, Henderson, Khandelwal, Jia, Mahowald & Jurafsky (2020). "With Little Power Comes Great Responsibility."
**Venue (verified): EMNLP 2020, pp. 9263–9274.** ACL Anthology `2020.emnlp-main.745`.
File: `C_Card2020_LittlePowerGreatResponsibility_EMNLP2020.pdf`

The power-analysis paper for NLP. Surveys published NLP results and finds most are **underpowered** to detect the effect sizes actually claimed. Gives explicit power curves for both automatic-metric comparisons and **human/LLM-rating designs**, and recommends reporting **minimum detectable effect size (MDE)** rather than only a p-value. It also cites Lachenbruch (1992) on sample size for **McNemar's test** — directly usable for EmbGen's design.
**EmbGen should apply**: report an MDE for `N = 250` and add a power statement. The paper's guidance on retiring/expanding underpowered test sets applies if the MDE exceeds the claimed uplift.
**USE FOR: W4 (power), and a defensible answer to "is 250 items enough?").**
**Numbers (from the paper)**: the most common EMNLP-2019 human-eval design (**3 raters × 100 items**) is underpowered unless the effect size is **≥ 0.2 on a [0,1] scale**; even in the low-variance regime, detecting a **0.05** effect needs **10+ ratings per item at 100 items**. EmbGen's claimed absolute effect is **0.032 on a [0,1] scale** — smaller than either threshold.

### 13. Berg-Kirkpatrick, Burkett & Klein (2012). "An Empirical Investigation of Statistical Significance in NLP."
**Venue (verified): EMNLP-CoNLL 2012, pp. 995–1005.** ACL Anthology `D12-1091`.
File: `C_BergKirkpatrick2012_EmpiricalInvestigationStatSig_EMNLP2012.pdf`

Empirically characterises the relationship between observed metric gains, test-set size, and p-values across NLP tasks, using **bootstrap and paired permutation tests**. Shows that the *paired* structure matters enormously and gives rules of thumb for the size of gain that is significant at a given `N`.
**EmbGen should apply**: use its **paired bootstrap / paired permutation** protocol as the non-parametric companion to McNemar's; it is the test NLP reviewers recognise on sight.
**USE FOR: W4.**

### 14. Koehn (2004). "Statistical Significance Tests for Machine Translation Evaluation."
**Venue (verified): EMNLP 2004, pp. 388–395.** ACL Anthology `W04-3250`.
File: `C_Koehn2004_StatSigTestsMTEvaluation_EMNLP2004.pdf`

The origin of **bootstrap resampling for NLP metric comparison** — the canonical citation for "we bootstrap the test set." Establishes that CIs from bootstrap resampling of the test set closely match true sampling variability for BLEU at realistic sizes, and gives the paired-bootstrap procedure for system comparison.
**EmbGen should apply**: use paired bootstrap for the **BLEU/ROUGE/METEOR** table (where the metric is a non-linear corpus statistic and Wilson does not apply). Note the tension with #10: bootstrap is fine for corpus-level continuous metrics at `N = 250`, but **not** for the low-count binary proportion.
**USE FOR: W4** (specifically the lexical-metric table).

### 15. Deutsch, Dror & Roth (2021). "A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods."
**Venue (verified): *TACL* 9:1132–1146, 2021.** ACL Anthology `2021.tacl-1.67`.
File: `C_Deutsch2021_StatisticalAnalysisSummarizationMetricsResampling_TACL2021.pdf`

Provides bootstrap and permutation methods for putting **confidence intervals and hypothesis tests on the *correlation* between an automatic metric and human judgement** — i.e. on the judge-validation statistic itself, not just on the metric. Evaluates which resampling scheme (resample systems / resample inputs / resample both) is appropriate, then shows on real data that **the CIs on metric–human correlations are surprisingly wide**, so claims that metric A correlates better than metric B are frequently unsupported.
**EmbGen should apply**: when EmbGen reports judge–human agreement (Cohen's κ or correlation) on the human-labelled subset, it must attach a **bootstrap CI over inputs** using this paper's "resample inputs" scheme, and must not claim its judge beats another judge without the paired permutation test.
**USE FOR: W1, W4, W7.**

### 16. Deutsch, Dror & Roth (2022). "Re-Examining System-Level Correlations of Automatic Summarization Evaluation Metrics."
**Venue (verified): NAACL-HLT 2022, pp. 6038–6052.** ACL Anthology `2022.naacl-main.442`.
File: `C_Deutsch2022_ReExaminingSystemLevelCorrelations_NAACL2022.pdf`

Shows that the standard system-level correlation used to validate automatic metrics **does not match how the metric is actually used** (to compare a small number of specific systems), and proposes a corrected definition plus a **pairwise-accuracy** evaluation that reflects the real decision. Also demonstrates that measured correlations depend heavily on which systems are in the pool.
**EmbGen should apply**: validate the GPT-5 judge by **pairwise decision accuracy** — "how often does the judge rank system A above system B the way humans do" — over the 5 methods × 3 datasets, rather than by a single global correlation. This is far more honest for a 5-system table.
**USE FOR: W1, W7, W4.**

### 17. Dietterich (1998). "Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms."
**Venue (verified): *Neural Computation* 10(7):1895–1923, 1998.** DOI 10.1162/089976698300017197. (File is the author's preprint version, obtained via CiteSeerX; MIT Press direct PDF is paywalled/blocked.)
File: `C_Dietterich1998_ApproxStatTestsComparingClassifiers_NeuralComp1998.pdf`

**The canonical justification for McNemar's test.** Compares five tests by measured Type-I error rate. Two widely-used tests are shown to have unacceptably high Type-I error and *"should never be used"*: (a) **the test for the difference of two proportions** (i.e. the naive two-sample z-test — which is exactly what a reader would default to for EmbGen's 0.068 vs 0.036!) and (b) a paired-differences t-test over random train/test splits. **McNemar's test is shown to have low Type-I error**; the 5×2cv test is introduced and also has acceptable error.
**EmbGen should apply**: **McNemar's exact test** on the 2×2 discordant table `(b, c)` = (items EmbGen got right and baseline wrong, vice-versa). At EmbGen's counts the discordant cells will be tiny (order 10–20), so use the **exact binomial** version, `p = 2·P(Bin(b+c, 0.5) ≥ max(b,c))`, not the χ² approximation.
**USE FOR: W4** — and it lets you say, with a 1998 *Neural Computation* citation, exactly *why* the obvious two-proportion test is wrong.

---

## Part 3 — Multiple-comparison correction across a benchmark table

### 18. Demšar (2006). "Statistical Comparisons of Classifiers over Multiple Data Sets."
**Venue (verified): *JMLR* 7:1–30, 2006.**
File: `C_Demsar2006_StatisticalComparisonsClassifiers_JMLR2006.pdf`

The standard reference for comparing **multiple methods across multiple datasets**. Recommends the **Friedman test** (non-parametric, rank-based, across datasets) as an omnibus test, followed by post-hoc **Nemenyi** (all-pairs) or **Bonferroni–Dunn** (all-vs-control) tests, and popularised the **critical-difference (CD) diagram**. Argues explicitly against averaging metrics across datasets and against per-dataset t-tests without correction.
**EmbGen should apply**: EmbGen's table is 5 methods × 3 datasets × 2 budgets = **30 cells and 4×3×2 = 24 pairwise EmbGen-vs-baseline comparisons**. Run Friedman across the 6 (dataset, budget) blocks over the 5 methods, then **Bonferroni–Dunn all-vs-control with EmbGen as control**. Caveat honestly: with only 6 blocks the Friedman test is itself low-powered — Demšar recommends `k` datasets substantially larger than the number of methods.
**USE FOR: W4 (multiple comparisons).**
**Numbers**: Demšar's power analysis suggests Friedman + Nemenyi needs roughly **`N_datasets ≥ 10`** to be useful with 5 algorithms; with 6 blocks EmbGen should report this as a limitation and lean on per-cell corrected p-values instead.

### 19. Dror, Baumer, Bogomolov & Reichart (2017). "Replicability Analysis for Natural Language Processing: Testing Significance with Multiple Datasets."
**Venue (verified): *TACL* 5:471–486, 2017.** ACL Anthology `Q17-1033`.
File: `C_Dror2017_ReplicabilityAnalysisNLP_TACL2017.pdf`

The NLP-native answer to the multiple-dataset problem, and a better fit than Demšar for a 3-dataset paper. Instead of asking "is the mean difference significant?", it asks **"on how many of the `N` datasets is method A genuinely better?"** — a *partial conjunction* hypothesis — and gives valid procedures under both independence (Fisher / Bonferroni-type) and arbitrary dependence (Benjamini–Heller–Yekutieli), controlling FDR via **Benjamini–Hochberg**.
**EmbGen should apply**: this is the **right headline claim**. Rather than "88.9% relative uplift", claim *"EmbGen is significantly better than each baseline on `u` out of 6 (dataset, budget) settings at FDR 0.05"*, with `u` the replicability count. It is defensible, corrected for multiplicity, and it survives the small-`N` problem better than a single pooled test.
**USE FOR: W4 (multiple comparisons + the reframing of the headline claim).**

---

## Part 4 — Judge score variance and reliability

### 20. Stureborg, Alikaniotis & Suhara (2024). "Large Language Models are Inconsistent and Biased Evaluators."
**Venue (verified): arXiv:2405.01724, May 2024 — arXiv-only. FLAGGED, but well-cited in the LLM-judge literature.**
File: `C_Stureborg2024_LLMsInconsistentBiasedEvaluators_arXiv.pdf`

Measures LLM judges' **self-inconsistency across repeated runs and across prompt/scale perturbations**, and documents a strong **familiarity/anchoring bias** toward certain score values (heavy clustering at particular points on a Likert scale — a direct analogue of EmbGen's 3-level Strong/Adequate/Weak compression). Shows scores drift substantially under paraphrase of the rubric and under reordering.
**EmbGen should apply**: cite as evidence that **temperature-0 repeats do not bound judge variance** — the relevant variance is over *rubric phrasings, item orderings, and judge models*, not over decoding seeds. Also supports W7: score clustering on a 3-level ordinal scale destroys resolution.
**USE FOR: W3 (primary), W7, W2.**

### 21. Song, Lee & Jiao (2025). "Exploring LLM Autoscoring Reliability in Large-Scale Writing Assessments Using Generalizability Theory."
**Venue (verified): arXiv:2507.19980, 26 Jul 2025 — arXiv-only, low citation count. FLAGGED; include only as the existence proof that G-theory has been applied to LLM scoring.**
File: `C_Song2025_LLMAutoscoringGeneralizabilityTheory_arXiv.pdf`

Applies **generalizability theory** (a `person × task × rater` crossed design) to AP Chinese writing assessments, decomposing observed score variance into person, task, rater, and residual components, and running a **D-study** to determine how many raters/tasks are needed for a target reliability. Finds human raters more reliable overall, but that **composite scoring combining human and LLM raters improves reliability** — a G-theory-flavoured argument for the same hybrid design PPI gives statistically.
**EmbGen should apply**: run a small **G-study with facets `item × judge-model × prompt-variant`**, report the variance components (σ²_item, σ²_judge, σ²_prompt, σ²_residual) and a **generalizability coefficient (Eρ²)**, then a D-study answering "how many judge models / prompt variants do we need?". This is a far more credible answer to W3 than "10 runs at temperature 0", and it also directly tests W7 (are the 4 dimensions carrying independent variance?).
**USE FOR: W3 (primary), W7, W2.**

---

## Part 5 — Reliability of small benchmarks

### 22. Polo, Weber, Choshen, Sun, Xu & Yurochkin (2024). "tinyBenchmarks: evaluating LLMs with fewer examples."
**Venue (verified): ICML 2024, PMLR 235.** Preprint arXiv:2402.14992.
File: `C_Polo2024_tinyBenchmarks_ICML2024.pdf`

Shows that LLM benchmark performance can be estimated from very few examples using **Item Response Theory (IRT)** — modelling per-item difficulty and discrimination — plus stratified/clustered example selection, and quantifies the resulting estimation error.
**EmbGen should apply**: two uses. (i) It is the **defence of `N = 250`**: a curated 250-item set can be adequate *for the average*, which supports EmbGen's design. (ii) It is simultaneously the **attack**: adequacy is defined at ~2% error on the *mean*, which is the same order as EmbGen's entire claimed 3.2-point effect. Also, IRT-style difficulty modelling gives a principled way to say whether the eval items actually discriminate among the 5 methods (many may be too hard for all — consistent with accuracies of 0.036–0.068).
**USE FOR: W4, and framing the eval-set-size discussion.**
**Numbers**: **100 curated examples per scenario suffice to estimate LLM performance to within ~2% error on average** across Open LLM Leaderboard, MMLU, HELM, and AlpacaEval 2.0.

### 23. Perlitz, Gera, Arviv, Yehudai, Bandel, Shnarch, Shmueli-Scheuer & Choshen (2024). "Benchmark Agreement Testing Done Right: A Guide for LLM Benchmark Evaluation."
**Venue (verified): NeurIPS 2025 Workshop on Evaluating the Evolving LLM Lifecycle. Preprint arXiv:2407.13696. FLAGGED as workshop/preprint.**
File: `C_Perlitz2024_BenchmarkAgreementTestingDoneRight_NeurIPS2025ws.pdf`

Formalises **Benchmark Agreement Testing** — validating a new/cheap benchmark by measuring its agreement with a trusted reference — and shows the practice is riddled with methodological errors: agreement estimates are **highly sensitive to the set of models compared, to the number of models, and to the choice of correlation metric**, and small model pools produce wildly unstable agreement scores. Provides best practices and the `benchbench` tooling.
**EmbGen should apply**: EmbGen validates its judge/eval implicitly by agreement with lexical metrics and with a reference LLM. This paper says: **report agreement with CIs, over ≥ some minimum number of systems, and state the metric.** With only 5 systems, agreement statistics are essentially uninformative — say so rather than reporting a bare correlation.
**USE FOR: W1, W6, W4.**
**Numbers**: recommends a **minimum of ~10 models** in the comparison pool before agreement estimates stabilise; below that, reported agreement varies by large margins purely from pool composition.

### 24. Chiang, Zheng, Sheng, Angelopoulos, Li, Li, Zhu, Zhang, Jordan, Gonzalez & Stoica (2024). "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference."
**Venue (verified): ICML 2024, PMLR 235.** Preprint arXiv:2403.04132.
File: `C_Chiang2024_ChatbotArena_ICML2024.pdf`

The reference implementation of **statistically principled ranking with confidence intervals** in LLM evaluation: Bradley–Terry (not naive Elo) maximum-likelihood estimation, **bootstrap CIs on the BT coefficients**, a rank derived from CI overlap rather than point estimates, and **active sampling of which model pairs to query** to shrink CIs fastest. Shares an author (Angelopoulos) with the PPI line, and the paper explicitly discusses detecting anomalous users and measuring agreement with LLM judges.
**EmbGen should apply**: if EmbGen ever moves from pointwise grading to pairwise judging (which mitigates W5/verbosity and W2/self-preference better), this is the estimator and CI construction to adopt; and the **"rank by CI overlap, not by point estimate"** convention is exactly what EmbGen's results table needs.
**USE FOR: W4, W2, W5.**

### 25. Brown, Cai & DasGupta (2001). "Interval Estimation for a Binomial Proportion."
**Venue (verified): *Statistical Science* 16(2):101–133, 2001** (with discussion). DOI 10.1214/ss/1009213286.
File: `C_Brown2001_IntervalEstimationBinomialProportion_StatSci2001.pdf`
*(PDF obtained from T. Cai's Wharton page; text layer is unextractable but the file is the Statistical Science article — internal metadata `JSCI-2SSCI259`, 737 KB.)*

**The authoritative statistics citation for "which binomial CI".** Demonstrates that the standard **Wald (normal-approximation) interval is "persistently chaotic"** and has erratic coverage that does *not* improve monotonically with `n` — and is catastrophically bad when `p` is near 0 or 1, which is exactly EmbGen's regime (`p̂ ≈ 0.036–0.068`). Recommends the **Wilson score** interval and the **Agresti–Coull** interval for small `n`, and the **Jeffreys (Beta(½,½)) interval** as the Bayesian option; notes Clopper–Pearson is conservative.
**EmbGen should apply**: cite this alongside Bowyer et al. (#10) as the statistics-literature justification for reporting **Wilson** rather than `p̂ ± 1.96·√(p̂(1−p̂)/N)`.
**USE FOR: W4 (the exact CI choice).**
**Numbers**: for `p ≈ 0.05` the nominal-95% Wald interval can have true coverage well below 90% even at `n = 250`; the rule "`np ≥ 5`" is shown to be inadequate. **EmbGen has `np̂ ≈ 9–17`** — right in the danger zone.

---

## Recommended statistical protocol for EmbGen

**1. The metric is a proportion with a tiny numerator.** Binary Accuracy is `S/250` with `S ≈ 9–17`. The Wald interval `p̂ ± 1.96√(p̂(1−p̂)/N)` is invalid here: Brown, Cai & DasGupta (2001) show its coverage is chaotic and severely below nominal near `p = 0`, and Bowyer et al. (ICML 2025) measure only **92.5% empirical coverage for a nominal 95% CLT interval at N = 100**, with the failure regime extending to "a few hundred" points. **Report Wilson score 95% CIs** — `scipy.stats.binomtest(S, N).proportion_ci("wilson", 0.95)` — as the primary interval. Clopper–Pearson is valid but conservatively wide; report it only if you want a guaranteed-coverage sensitivity check. **Do not use the naive bootstrap**: Bowyer et al. show it is as badly calibrated as the CLT at these counts. Optionally add the Bayesian `Beta(1+S, 1+N−S)` credible interval, which has the best small-`N` coverage and extends to clustered and paired settings.

**2. Comparisons must be paired and item-level.** EmbGen and every baseline are graded on the *same* 250 items, so per-item outcomes are positively correlated and the unpaired two-proportion test is both wrong and wasteful. Dietterich (1998, *Neural Computation*) shows the two-proportion difference test has unacceptably high Type-I error and *"should never be used"*, and identifies **McNemar's test** as the one with reliably low Type-I error. **Primary test: McNemar's exact test** on the discordant counts `(b, c)`; with `b + c` on the order of 10–25 use the exact binomial form `p = 2·P(Bin(b+c, ½) ≥ max(b,c))`, never the χ² approximation. **Secondary test: paired approximate-randomisation (permutation) test** over item-level differences (Berg-Kirkpatrick et al. 2012; Dror et al. 2018 select exactly this branch for a paired bounded binary measure). Report the **paired difference with a Bayesian credible interval on the difference or odds ratio**, as Bowyer et al. recommend for the small-`N` paired setting. Miller (2024) recommendation #4 is the same point stated for LLM evals. For the lexical-metric table (BLEU/ROUGE/METEOR), use the **paired bootstrap** (Koehn 2004) — those are corpus-level continuous statistics where bootstrap is appropriate.

**3. The eval items are not IID.** EmbGen's eval sets are generated from clustered corpora, so items sharing an entity or source document are dependent. Follow Miller (2024) recommendation #2 and compute **cluster-robust standard errors** (cluster by source document / entity cluster), or use a cluster bootstrap resampling *clusters*, not items. Bowyer et al. show even clustered-CLT under-covers at small `N`, so prefer the Bayesian hierarchical version or state the caveat.

**4. Multiplicity.** 5 methods × 3 datasets × 2 budgets means ~24 EmbGen-vs-baseline tests. Apply **Benjamini–Hochberg FDR at q = 0.05** across the full family and report BH-adjusted p-values in the table. Better still, reframe the headline using Dror et al. (TACL 2017) **replicability analysis**: report *"EmbGen beats baseline X on `u` of 6 (dataset, budget) settings at FDR 0.05"* rather than a pooled relative uplift. If you also want an omnibus statement, run **Friedman + Bonferroni–Dunn with EmbGen as control** (Demšar, JMLR 2006), acknowledging that 6 blocks is below the ~10 Demšar recommends.

**5. Report power, and retire the relative-uplift framing.** "88.9% relative uplift" on 17 vs 9 items is indefensible; report absolute numbers, counts, and the CI. Add a **minimum detectable effect** statement for `N = 250` at 80% power (Card et al., EMNLP 2020). Card et al. find that even low-variance rating designs are underpowered for effects of 0.05 on a [0,1] scale; EmbGen's absolute effect is **0.032**. Say plainly that the study is powered to detect direction-consistent trends, not to certify per-cell significance — and use the replicability count as the load-bearing claim instead.

**6. Report judge variance honestly.** Temperature-0 × 10 runs measures decoding noise, which is near zero, not judge variance (Stureborg et al. 2024). Replace or supplement it with: (a) **temperature ≥ 0.7 resampling** to get a real run-to-run distribution; (b) **≥ 2 rubric paraphrases**; (c) **≥ 2 judge models** including at least one non-OpenAI judge, which simultaneously addresses W2 (teacher/judge overlap); (d) a small **G-study** (`item × judge × prompt-variant`) reporting variance components and a generalizability coefficient (Song et al. 2025), plus a D-study saying how many judges/variants are needed for Eρ² ≥ 0.8. Report the **judge-flip rate** — the fraction of items whose Binary Accuracy label changes across conditions — as a headline reliability number.

---

## PPI recipe

**Goal.** Produce a *valid* 95% CI on Binary Accuracy that is not merely "agreement with GPT-5", using a small human-label budget. This is the single change that most improves the paper's defensibility (W1 + W4 + W6 simultaneously).

**Budget.** Human-label **n = 60–80 of the 250 items per dataset** (180–240 total across the three corpora). Below `n ≈ 50` Eyre & Madras (ICML 2025) show PPI++ can be *worse* than the classical human-only estimator, so 60 is the floor; above ~80 the marginal CI narrowing is small at these `p` values. One annotator per item plus a 20-item doubly-annotated overlap to report human–human κ.

**Sampling.** Stratify, then optionally weight by judge uncertainty (Zrnic & Candès, ICML 2024). Concretely: stratify by the judge's predicted Binary Accuracy label (all judge-positive items are precious — there are only ~17 of them, so **label all judge-positives**) and sample the judge-negative stratum with probability `π ∈ [0.15, 0.30]`. Record the sampling probabilities `π_i` (floor at 0.05) and use Horvitz–Thompson weights `1/π_i` so the estimator stays unbiased. If you prefer the simplest defensible option, use **simple random sampling without replacement** — PPI's validity does not require clever sampling.

**Estimator (PPI++ for a mean/proportion).** Let `L` be the labelled set (size `n`, gold human binary `Y_i`, judge binary `f_i`) and `U` the unlabelled remainder (size `N − n`, judge label `f_i` only). Then

```
θ̂(λ) = (λ / |U|) Σ_{i∈U} f_i  +  (1/n) Σ_{i∈L} [ Y_i − λ f_i ]

Var̂(θ̂(λ)) = λ² σ̂²_f / |U|  +  σ̂²_{Y−λf} / n

λ̂* = Cov̂(f, Y) / Var̂(f)  ×  |U| / (|U| + n)          (power tuning; clip to [0,1])

95% CI:  θ̂(λ̂*)  ±  1.96 · sqrt( Var̂(θ̂(λ̂*)) )
```

`λ̂* = 0` recovers the classical human-only estimator exactly, so **PPI++ is asymptotically never worse than ignoring the judge**. With `n < 60`, substitute Eyre & Madras's shrunk λ̂ instead of the plug-in λ̂*. Because `p̂` is near 0, also compute a **Wilson-style / logit-transformed** PPI interval, or at minimum clip the interval to `[0,1]` and note the normal approximation is being pushed.

**Cross-check estimator.** Report the **Rogan–Gladen** measurement-error correction alongside (Chen et al. 2026): estimate judge sensitivity `Se` and specificity `Sp` on `L`, then `p̂_corr = (p̂_judge + Sp − 1)/(Se + Sp − 1)`, with a bootstrap CI over `L`. Agreement between PPI++ and Rogan–Gladen is strong evidence the correction is real rather than an artefact of one estimator.

**Software.** **`ppi_py`** — `pip install ppi-py`, `github.com/aangelopoulos/ppi_py` (Angelopoulos et al.; used by Boyeau et al. ICML 2025). Use `ppi_mean_ci(Y_labeled, Yhat_labeled, Yhat_unlabeled, alpha=0.05, lhat=None)` for automatic power tuning. Comparison utilities for the measurement-error family: `github.com/yiqunchen/debias-llm-as-a-judge`. Bayesian/Wilson eval intervals: `github.com/sambowyer/bayes_evals`.

**What to report.** For each (method, dataset, budget) cell: `n` human labels; the classical human-only estimate + Wilson CI; the PPI++ estimate + CI; the fitted **λ̂**; the **effective sample size (ESS)** = the number of human labels the classical estimator would need for the same CI width (Boyeau et al. report **~+50% ESS** for PPI++ over classical); judge–human **Cohen's κ** and sensitivity/specificity with bootstrap CIs. Then run McNemar's exact test on the **human labels of the shared labelled subset** for the primary EmbGen-vs-best-baseline comparison, and use PPI++ CIs for the full-set estimates. Be honest about the ceiling: Chaganty et al. (ACL 2018) obtained only **7–13%** cost reduction from the equivalent control-variate machinery because their automatic metric was weak; the variance-reduction factor is `1 − ρ²`, so **report ρ** and let the reader judge.
