# B — LLM-judge biases: measurement and mitigation

Agent B annotated bibliography. Scope: naming/quantifying judge bias (self-preference, familial/teacher-judge
contamination, position, verbosity/length, rubric-scale artefacts), accepted mitigations, and — most importantly —
**probes EmbGen can actually run** given it uses *reference-based pointwise (single-answer) grading*.

All venues verified via DBLP / ACL Anthology DOI / arXiv header. `arXiv-only` is flagged explicitly.
Files live in `/Users/andreanicastro/Documents/repos/embgen-lit-rev/llm-as-a-judge/claude-papers/`.

**Note on shared directory.** Seven papers I would otherwise have downloaded were already present under other
agents' prefixes (`A_`, `C_`, `D_`). I deleted my duplicate copies and annotate them below under their **existing**
filenames. Nothing was re-downloaded that the brief told me to skip.

---

## 1. Self-preference, self-recognition, and the teacher==judge confound (W2, W6)

### 1.1 Panickssery, Bowman & Feng (2024) — LLM Evaluators Recognize and Favor Their Own Generations
**Venue: NeurIPS 2024 (main track).** arXiv:2404.13076. DBLP: `papers.nips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e0e5c`.
File: `B_Panickssery2024_SelfPreference_NeurIPS.pdf`

The canonical causal study of self-preference. It separates *self-preference* (rating own output higher than others'
when humans call them equal) from *self-recognition* (ability to identify own output), and shows via fine-tuning
interventions that the two are **linearly correlated**, with confounders (length, perplexity, style) controlled out.
The key transferable artefact is the **self-recognition probe**: present the judge with a pair (own generation,
other generation) and ask "which did you write?" — measurable without any human labels. EmbGen can run exactly this
on GPT-5 vs. its student outputs to establish whether the self-preference precondition even holds on its corpora.

**Reusable numbers:** GPT-4 self-recognition accuracy **73.5%** out of the box (3-way: itself vs. two other LLMs vs.
human); all three tested LLMs > 50% zero-shot; fine-tuning on **500 examples** pushes self-recognition >90%, and
self-preference rises linearly with it.

**USE FOR: W2** (primary), **W6** (secondary — self-recognition of the LLM-written reference answers).

---

### 1.2 Li, Sun, Huang, Zhong, Jiang, Han, Zhang, Wang & Liu (2026) — Preference Leakage: A Contamination Problem in LLM-as-a-Judge
**Venue: ICLR 2026 (accepted; camera-ready header confirms "Published as a conference paper at ICLR 2026").** arXiv:2502.01534.
File: `B_Li2026_PreferenceLeakage_ICLR.pdf`

**This is the single most on-point paper for EmbGen's W2.** It studies precisely EmbGen's setting: an LLM generates
the *synthetic SFT training data*, a student is fine-tuned on it, and a *related* LLM judges the student. They define
three relatedness levels (same model / inheritance / same family) and a **Preference Leakage Score (PLS)**,
PLS(i,j) = (WR(i,i)−AVG(i,j))/AVG(i,j) + (WR(j,j)−AVG(j,i))/AVG(j,i), where WR(i,j) is judge j's win rate for
student i. PLS is computable with **no human labels** — it only needs two teachers and two judges — so EmbGen can run
it directly by additionally generating a corpus with a non-GPT teacher and judging with a non-GPT judge.
They also show mitigation: **contextual calibration** on a held-out set beats prompting/CoT/paraphrase.

**Reusable numbers:** PLS up to **37.1%** (Arena-Hard, GPT-4o & Gemini-1.5 judges, Qwen-2.5-14B student), **27.9%**
average; near-zero (−0.1% to 1.7%) for unrelated pairs. Leakage **grows with the synthetic-data proportion** and is
**worse for smaller students** (LLaMA-3-1B, Qwen-3-1.7B highest) — directly relevant to Llama-3-**8B** + LoRA.
Stripping style cues drops PLS **17.5% → 9.0%**; stripping format **→ 9.8%**. Mitigation: contextual calibration cuts
their Error Bias metric **17.8 → 7.3**; plain prompting (18.3) and paraphrase (18.7) *make it worse*.
Also: **preference leakage is harder to detect than previously identified biases** — a sentence worth quoting verbatim
against a reviewer who says "GPT-5 is strong enough to be neutral".

**USE FOR: W2** (primary, decisive), **W5** (style/format are the leakage conduits), **W6**.

---

### 1.3 Wataoka, Takahashi & Ri (2024) — Self-Preference Bias in LLM-as-a-Judge
**Venue: NeurIPS 2024 Safe Generative AI Workshop** (non-archival workshop — flag as such). arXiv:2410.21819.
File: `B_Wataoka2024_SelfPreferenceBias_NeurIPSworkshop.pdf`

Proposes a self-preference metric defined **relative to human evaluation** (unlike Panickssery, who compares model to
model), which is the correct definition when the question is "is the judge wrong, or is the output actually better?"
Its mechanistic result is the useful one: LLM judges assign systematically higher scores than humans to **low-perplexity
(more familiar) text**, *whether or not the text was self-generated*. This reframes EmbGen's confound: the risk is not
that GPT-5 recognises its own tokens, but that EmbGen's GPT-5-distilled student produces text that is *low-perplexity
under GPT-5*, which is enough to inflate scores. EmbGen can compute judge-side perplexity of each student answer as a
cheap covariate and regress Binary Accuracy on it.

**Reusable numbers:** GPT-4 shows the strongest self-preference of the models tested; the LLM-vs-human score gap is
significant and monotone in output perplexity.

**USE FOR: W2, W6.**

---

### 1.4 Xu, Zhu, Zhao, Pan, Li & Wang (2024) — Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement
**Venue: ACL 2024 (Long).** `2024.acl-long.826`, DOI 10.18653/v1/2024.acl-long.826. arXiv:2402.11436.
File: `B_Xu2024_PridePrejudiceSelfBias_ACL.pdf`

Formally defines self-bias with **two statistics** that are directly copyable into EmbGen's analysis: (i) **bias** =
mean difference between LLM score and human score on the same items, and (ii) **distance skewness (D_skew)** of the
LLM−human score-difference distribution, where an unbiased evaluator has D_skew = 0. This is exactly the estimator
EmbGen needs once it has even a small human-annotated slice (see Agent A's PPI/budget notes): it converts a handful of
human labels into a *signed, testable* bias number rather than a raw agreement percentage. Studied across six LLMs and
three task families; self-refinement *amplifies* the bias while improving surface fluency — a caution for any
"judge-in-the-loop" data filtering in EmbGen's pipeline. Larger models and *external* feedback reduce it.

**USE FOR: W1** (this is the statistic to report once humans are collected), **W2.**

---

### 1.5 Verga, Hofstätter, Althammer, Su, Piktus, Arkhangorodsky, Xu, White & Lewis (2024) — Replacing Judges with Juries (PoLL)
**Venue: arXiv-only (CoRR 2024, Cohere); highly cited / canonical for judge panels — flag as non-peer-reviewed.**
arXiv:2404.18796. File: `B_Verga2024_PanelOfLLMEvaluators_arXiv.pdf`

The standard reference for the cheapest real fix to a single-judge design: replace one big judge with a **Panel of LLM
evaluators (PoLL)** drawn from **disjoint model families**, aggregated by max-voting (binary correctness) or average
pooling (graded scores). Their QA setting is close to EmbGen's (KILT-NQ, HotpotQA, Bamboogle — multi-hop, short-answer,
reference-based, binary correctness), so the recipe transfers almost verbatim. Crucially they report the *signature* of
intra-model bias EmbGen must rule out.

**Reusable numbers:** "the highest positive delta for each individual model being scored occurs **when it is judged by
itself**". PoLL deviation from human accuracy: **σ = 2.2** vs. GPT-3.5 **σ = 6.1**. Cohen's κ vs. humans: PoLL 0.763 /
0.906 / 0.867 across three KILT sets, beating GPT-4 on 2 of 3. Ranking correlation with Chatbot Arena: PoLL Kendall τ
**0.778** vs. GPT-4 **0.667**. Cost: **7–8× cheaper** than a single GPT-4-Turbo judge. GPT-4 ranked another GPT-4
variant at position 2 when its true position was 4.

**USE FOR: W2** (primary mitigation), **W3** (panel disagreement is a real variance signal), **W1.**

---

## 2. Position / order bias — and why it does *not* apply to EmbGen as-is (W3)

### 2.1 Wang, Li, Chen, Cai, Zhu, Lin, Cao, Kong, Liu, Liu & Sui (2024) — Large Language Models are not Fair Evaluators
**Venue: ACL 2024 (Long).** `2024.acl-long.511`, DOI 10.18653/v1/2024.acl-long.511. arXiv:2305.17926.
File: `B_Wang2024_NotFairEvaluators_ACL.pdf`

The canonical position-bias paper and the source of the **swap-and-average** protocol. Three calibrations: **Multiple
Evidence Calibration (MEC** — force evidence *before* the score, then ensemble), **Balanced Position Calibration (BPC** —
score in both orders and average), and **Human-In-The-Loop Calibration (HITLC** — use a Balanced Position Diversity
Entropy score to route only the *uncertain* items to humans). **MEC generalises to EmbGen's pointwise setting** (its
prompt already asks for reasoning); BPC does not. HITLC is the piece EmbGen should steal for W1: it is a
principled, cheap way to pick *which* 20% of 250 items get human annotation.

**Reusable numbers:** flipping presentation order let Vicuna-13B "beat" ChatGPT on **66 of 80** queries. MEC + BPC
improve human alignment by **+9.8%** (GPT-4) and **+14.3%** (ChatGPT) accuracy. HITLC reaches human-level annotation
alignment with **20% human annotation cost**, a **39%** cost reduction.

**USE FOR: W3, W1.** ⚠️ Also use as the *citation for why position bias is out of scope* for EmbGen — see protocol.

---

### 2.2 Shi, Ma, Liang, Diao, Ma & Vosoughi (2025) — Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge
**Venue: AACL-IJCNLP 2025** (per arXiv v9 header). arXiv:2406.07791.
File: `B_Shi2025_PositionBiasJudges_AACL.pdf`

The largest position-bias study (15 judges, 22 tasks, MT-Bench + DevBench, >150k judgements). Its lasting contribution
for EmbGen is **not** the position finding but **Repetition Stability (RS)**: the percentage of the modal decision
across repeated identical queries, **measured at temperature = 1**, explicitly chosen "to generate nontrivial results."
This is the direct answer to W3 — EmbGen's temperature-0 × 10 runs is a degenerate protocol that measures nothing;
the accepted way to measure judge variance is repeated sampling at T ≥ 0.7. They also show position bias is **weakly**
related to prompt/response length but **strongly** related to the *quality gap* between candidates — meaning bias is
worst exactly where EmbGen's baselines are closest, i.e. on its headline comparison.

**Reusable numbers:** RS ≈ **0.87–0.93** for capable judges (below ~0.8 renders the evaluation invalid, marked red in
their Table 2); Llama-3.1-405B PC 0.93±0.10, Llama-3.1-8B PC 0.75±0.32. They use **bidirectional stepwise regression
with AIC** to identify bias drivers — a reusable analysis template.

**USE FOR: W3** (primary — the temperature argument), **W4.**

---

## 3. Verbosity / length bias and length-debiasing estimators (W5)

### 3.1 Dubois, Galambosi, Liang & Hashimoto (2024) — Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators
**Venue: COLM 2024.** arXiv:2404.04475. File: `B_Dubois2024_LengthControlledAlpacaEval_COLM.pdf`

**The estimator EmbGen should implement for W5.** They cast length as an undesirable *mediator* in a causal graph and
fit a GLM with a logit link:

> q(y=1 | z_m, z_b, m, b, x) = logistic[ (θ_m − θ_b) + φ_{m,b}·tanh( (len(z_m) − len(z_b)) / std(len(z_m) − len(z_b)) ) + (ψ_m − ψ_b)·γ_x ]

then **zeros the length term** to get the counterfactual "what if lengths matched" score. The three components — system
identity, standardised length difference (tanh-squashed, so diminishing returns), and per-item difficulty — map onto
EmbGen exactly: fit `logit P(BinaryAccuracy_i = 1) = θ_system + φ·tanh((len_i − len_ref_i)/σ) + ψ_item` over the 250×
{EmbGen, EntiGraph, InstructLab, Knowledge-Instruct, no-aug} grid, then report θ with the length term set to 0.
The `ψ_item` per-question difficulty term is also what buys the *precision* gain that W4 needs (paired design).
Fits with off-the-shelf GLM libraries; 3M + N parameters for M systems and N instructions.

**Reusable numbers:** raw AlpacaEval win rate for gpt4_1106_preview swings **22.9% → 64.3%** purely from
"be concise" vs. "answer with as much detail as possible" prompts; after length control the same swing is only
**41.9% → 51.6%**. Normalised std across the three verbosity prompts drops **25% → 10%**. Spearman correlation with
Chatbot Arena rises **0.94 → 0.98**. Length-*balanced* and length-*normalised* alternatives are shown to be strictly
dominated by the GLM approach.

**USE FOR: W5** (primary estimator), **W4** (item-difficulty term reduces variance).

---

### 3.2 Singhal, Goyal, Xu & Durrett (2024) — A Long Way to Go: Investigating Length Correlations in RLHF
**Venue: COLM 2024.** arXiv:2310.03716. File: `B_Singhal2024_LengthCorrelationsRLHF_COLM.pdf`

Provides the **second, non-parametric** length control — cheaper than a GLM and easier for a reviewer to read.
**Length-stratified analysis:** bucket outputs by length (they use **20-token buckets**), compute the score of each
system *within* each bucket, and define **Non-Length Reward Gain (NRG)** = the average within-bucket gain weighted by
bucket population. The headline diagnostic is the ratio **NRG / Δ(total)** = the fraction of the improvement that is
*not* explained by length. EmbGen should report exactly this for its 88.9% relative Binary-Accuracy uplift: if the
within-bucket ratio is small, the headline is a length artefact. They also give the strongest possible "so what":
a **purely length-based reward** reproduces most RLHF gains.

**Reusable numbers:** NRG/ΔR ratio = **2.0%** (WebGPT), **53.4%** (Stack), **27.2%** (RLCD) — i.e. 70–90% of the
improvement on two of three settings was pure length. A length-only PPO reward achieves **56% vs 58%** win rate against
standard PPO (WebGPT) and **64% vs 63%** (RLCD). "PPO improvements disappear if we restrict our comparison to similar
length outputs" on two of three settings. Significance by **paired bootstrap test, p < 0.05**.

**USE FOR: W5** (primary control condition), **W4.**

---

### 3.3 Saito, Wachi, Wataoka & Akimoto (2023) — Verbosity Bias in Preference Labeling by Large Language Models
**Venue: arXiv-only (CoRR 2023); presented in the NeurIPS 2023 Instruction-Tuning workshop line of work — flag as
non-peer-reviewed but the canonical formal definition.** arXiv:2310.10076.
File: `B_Saito2023_VerbosityBias_arXiv.pdf`

Gives the **fairness-theoretic formalisation** of verbosity bias that EmbGen can cite instead of hand-waving. Define a
sensitive attribute S = 1{answer A is longer than answer B}; verbosity bias is the violation of **accuracy parity**
(Hardt et al. 2016) with respect to S, i.e. the judge's human-agreement accuracy differs between the "longer answer is
right" and "shorter answer is right" strata. Their empirical finding is the one that should scare EmbGen: judge–human
agreement is **high when humans preferred the longer answer and collapses when humans preferred the shorter one** —
the judge is not tracking quality, it is tracking length and getting credit when length happens to correlate.
They also warn that the verbosity-response curve is *prompt-specific*, so post-hoc scalar correction is unsafe unless
you fit the curve — which is precisely Dubois's per-item ψ term.

**Reusable numbers:** verbosity-bias value (accuracy parity gap) **GPT-4 = 0.328**, **GPT-3.5 = 0.428**. Cites the
"repetitive list attack": GPT-4 success rate **<10%**, GPT-3.5 and Claude-v1 **>90%**. Human alignment drops to well
below 50% in the "human preferred the shorter answer" stratum.

**USE FOR: W5** (the stratified-agreement probe), **W1.**

---

### 3.4 Wu & Aji (2025) — Style Over Substance: Evaluation Biases for Large Language Models
**Venue: COLING 2025.** `2025.coling-main.21`. arXiv:2307.03025. File: `B_Wu2025_StyleOverSubstance_COLING.pdf`

The best **adversarial probe design** in this list, and cheap to replicate. They hand-curate answers with *controlled,
independent* defects — correct / one minor factual error / several minor / several major factual errors × {~100 words,
~50 words} × {spelling errors, grammatical errors} — and Elo-rate them with crowd, expert, and LLM judges. EmbGen can
build a 40–80 item version of this set from its own eval questions in an afternoon; it yields a *direct* measurement of
whether GPT-5's Completeness/Factual-Accuracy dimensions can separate length from truth. Their fix, **MERS
(Multi-Elo Rating System)** — score Accuracy, Helpfulness and Language in **independent** generations rather than
merging into one score — is also the correct answer to W7's "are the four dimensions independent?" question.

**Reusable numbers (GPT-4 Elo):** "Several Minor Factual Errors" at ~100 words = **1206**, beating "Correct + Short"
at ~50 words = **1096**. "Correct" long = 1482; "Correct + Short" = 1096 — a **386-point** penalty for brevity alone.
Every "+ Short" variant is rated below its long counterpart for both humans and LLMs. MERS significantly improves LLM
factual-accuracy evaluation; it does **not** help crowd annotators.

**USE FOR: W5, W6, W7** (this paper touches all three).

---

## 4. Bias taxonomies and bias benchmarks (W2, W5, W7)

### 4.1 Ye, Wang, Huang, Chen, Zhang, Moniz, Gao, Geyer, Huang, Chen, Chawla & Zhang (2025) — Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)
**Venue: ICLR 2025.** OpenReview `3GTtZFiajM`. arXiv:2410.02736. File: `B_Ye2025_JusticeOrPrejudice_ICLR.pdf`

**The best turnkey bias-probe framework for a pointwise judge.** CALM covers 12 bias types and — critically — measures
them by **content-preserving perturbation** rather than by pairwise swapping. For verbosity it prompts GPT-4o to
*"Expand the length of the answer provided below… Do not address or include information beyond the scope of the original
answer"*, then compares the judgement before and after. Two metrics, both label-free:
**Robustness Rate RR = (1/|D|) Σ 1[y_i = ŷ_i]** (judgement unchanged under the perturbation) and
**Consistency Rate CR = (1/|D|) Σ 1[y_i = y_i^rand]** (judgement unchanged under a *repeat with no perturbation*).
**CR is the honest replacement for EmbGen's temperature-0 × 10 runs**, and RR-verbosity is the length probe that works
for pointwise grading. Their explicit recommendation is quotable: *"Avoid using the same model to generate and judge
answers."*

**Reusable numbers (fact-related datasets, the closest to EmbGen's QA setting):** GPT-4o **RR_verbosity = 0.977**,
RR_fallacy 0.984, RR_sentiment 0.699, **CR = 0.998**; ChatGPT RR_verbosity 0.900, GPT-4-Turbo 0.915, Qwen2 0.884.
On alignment datasets (small quality gaps) robustness collapses — position RR drops **below 0.5** with 3–4 candidates.
Bias impact is **larger on datasets with small quality gaps** — precisely EmbGen's 0.068-vs-0.036 regime.
Self-enhancement bias found in most models **even when answer sources were anonymised**.

**USE FOR: W2, W3, W5** (primary probe framework for all three).

---

### 4.2 Koo, Lee, Raheja, Park, Kim & Kang (2024) — Benchmarking Cognitive Biases in Large Language Models as Evaluators (CoBBLEr)
**Venue: Findings of ACL 2024.** `2024.findings-acl.29`, DOI 10.18653/v1/2024.findings-acl.29. arXiv:2309.17012.
File: `B_Koo2024_CoBBLEr_FindingsACL.pdf`

Six named cognitive biases with operational definitions EmbGen can cite by name: **Order**, **Compassion Fade**
(behaviour changes when model *names* are revealed vs. anonymised aliases), **Egocentric** (prefers own output),
**Salience** (prefers longer output), **Bandwagon**, **Attentional**. The Compassion-Fade design is a probe EmbGen can
run cheaply and that reviewers will find persuasive: judge each answer twice, once with the producing system
anonymised and once with it named ("Model: EmbGen-Llama-3-8B" vs. "System A"), and report the delta.

**Reusable numbers:** biased comparisons ≈ **40%** of all comparisons across all 16 models. Human–machine
Rank-Biased Overlap = **44%**. GPT-4 **egocentric bias 0.78–0.80** (proportion of self-preferring comparisons) — the
highest of all models tested; **salience (length) bias 0.56–0.57** for GPT-4, 0.63–0.70 for ChatGPT/InstructGPT.
11/15 models show significant order bias; >40B models favour the first-ordered system in **over 50%** of comparisons.

**USE FOR: W2, W5, W7.**

---

### 4.3 Park, Jwa, Ren, Kim & Choi (2024) — OffsetBias: Leveraging Debiased Data for Tuning Evaluators (EvalBiasBench)
**Venue: Findings of EMNLP 2024.** `2024.findings-emnlp.57`, DOI 10.18653/v1/2024.findings-emnlp.57. arXiv:2407.06551.
File: `B_Park2024_OffsetBias_FindingsEMNLP.pdf`

Contributes **EvalBiasBench**, 160 hand-crafted test cases across six bias types — **Length**, **Concreteness**
(credits specific numbers, citations, jargon), **Empty Reference**, **Content Continuation**, **Nested Instruction**,
**Familiar Knowledge** — plus a debiasing preference dataset. *Concreteness bias* is the under-discussed one that
matters most for EmbGen: its cluster-specialised prompts produce entity-dense, numeric answers, which a judge may credit
independently of correctness. This is an **off-the-shelf benchmark EmbGen can run its judge on** and report a single
number, at essentially zero annotation cost.

**Reusable numbers (accuracy on EvalBiasBench, position-swap-augmented):** GPT-4o-0513 **86.9** overall, **91.2** on
Length, but only **50.0** on Empty Reference. GPT-3.5-0613 **45.0** overall, **20.6** on Length. Prometheus-2-7B
**34.4** overall, 17.6 on Length. Fine-tuning LLaMA3-8B-Instruct on OffsetBias raises it **51.2 → 85.0**, and
FsfairX-LLaMA3-RM on RewardBench Chat-Hard **65.1 → 80.7**.

**USE FOR: W5, W2, W7.**

---

### 4.4 Stureborg, Alikaniotis & Suhara (2024) — Large Language Models are Inconsistent and Biased Evaluators
**Venue: arXiv-only (CoRR 2024); widely cited — flag as non-peer-reviewed.** arXiv:2405.01724.
**Already present as `C_Stureborg2024_LLMsInconsistentBiasedEvaluators_arXiv.pdf`** (duplicate deleted).

**The paper for W7 and W3.** Three findings map one-to-one onto EmbGen's design flaws. (i) **Anchoring effect in
multi-attribute judgements**: when several attributes are scored in a *single* prompt, later attributes are contaminated
by earlier ones — exactly EmbGen's "Factual Accuracy, Completeness, Relevance, Clarity in one call" design.
(ii) **Skewed/compressed rating distributions**: LLM judges do not use the full scale and show round-number bias —
EmbGen's 3-level Strong/Adequate/Weak scale makes this *worse*, not better, and its categorical→ordinal→rounded
round-trip destroys resolution. (iii) **Low inter-sample (self-)agreement** — the judge disagrees with *itself*
across resamples more than human annotators disagree with each other. Also documents **familiarity bias** (preference
for low-perplexity text), corroborating Wataoka.

**Reusable numbers:** Kendall τ on Coherence degrades **0.400 → 0.391 → 0.359 → 0.368** as it is predicted 1st, 2nd,
3rd, 4th in the same prompt. Krippendorff's α: **human inter-annotator 0.659** vs. **GPT-4 inter-sample 0.587**.
Increasing score granularity improves performance (contra EmbGen's 3-level scale), subject to round-number bias.
Their combined "recipe" reaches Kendall τ = 0.220 on RoSE, statistically significantly above G-Eval.

**USE FOR: W7** (primary — cite this to justify *separate calls per dimension*), **W3**, **W2.**

---

### 4.5 Chen, Chen, Zhang, Xiong, Fan, Yu, Yang & Wang (2024) — Humans or LLMs as the Judge? A Study on Judgement Biases
**Venue: EMNLP 2024 (Main).** `2024.emnlp-main.474`, DOI 10.18653/v1/2024.emnlp-main.474. arXiv:2402.10669.
**Already present as `A_Chen2024_HumansOrLLMsAsTheJudge_EMNLP.pdf`** (not re-downloaded).

Contributes a reference-free, human-annotation-free bias-probing framework and, uniquely, benchmarks **humans and LLM
judges under the same perturbations**, so it supports the "humans aren't a clean gold standard either" rebuttal that
EmbGen will need for W6. Covers Misinformation Oversight, Authority, Beauty and Verbosity biases. The Misinformation
Oversight probe (inject a false claim into an otherwise good answer and see whether the judge notices) is the closest
analogue to EmbGen's Factual Accuracy dimension and is directly runnable on its 250-item sets.

**USE FOR: W1, W5, W6.**

---

## 5. Mitigation architectures — panels, debate, calibration, selective prediction (W1, W2, W4)

### 5.1 Chan, Chen, Su, Yu, Xue, Zhang, Fu & Liu (2024) — ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate
**Venue: ICLR 2024.** OpenReview `FQepisCUWu`. arXiv:2308.07201. File: `B_Chan2024_ChatEval_ICLR.pdf`

The reference for multi-agent-debate judging: a team of LLM referees with **diverse role prompts** discusses before
scoring, under one of three communication strategies (one-by-one, simultaneous-talk, simultaneous-talk-with-summariser).
Their negative result is the important one for EmbGen: **identical role descriptions across agents degrade performance** —
so a "panel" of ten GPT-5 calls with the same prompt (which is what EmbGen's 10 repeated runs effectively are) buys
nothing. Real diversity must come from different models or genuinely different personas. Evaluated on FairEval and
topical-chat with turn-level Spearman/Kendall against humans.

**USE FOR: W2, W3.** Cite as the *upper-cost* option; PoLL (1.5) is the cheaper one EmbGen should actually run.

---

### 5.2 Jung, Brahman & Choi (2025) — Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement
**Venue: ICLR 2025.** OpenReview `UHPnqSTBPO`. arXiv:2407.18370.
**Already present as `A_Jung2025_TrustOrEscalate_ICLR.pdf`** (duplicate deleted).

**Selective evaluation with a distribution-free guarantee**: given a user-specified risk α, it certifies
P(LLM judgement agrees with human | LLM chose to evaluate x) ≥ 1 − α, abstaining on the rest. Two components EmbGen can
use: **Simulated Annotators** (a confidence-estimation method that markedly improves judge calibration without training)
and **Cascaded Selective Evaluation** (cheap judge first, escalate to an expensive one only on low-confidence items).
For EmbGen this converts "we have no human labels" into "we have a small calibration set and a certified coverage
number", and pairs naturally with Wang et al.'s HITLC routing (2.1) and Agent C's PPI machinery.

**Reusable numbers:** on a Chatbot-Arena subset where **GPT-4 almost never reaches 80% human agreement**, cascaded
selective evaluation using **Mistral-7B** as the first-stage judge guarantees **>80% human agreement at ~80% coverage**.

**USE FOR: W1** (primary), **W4, W2.**

---

## 6. Rubric and scale design: pointwise vs. pairwise, granularity, CoT, fine-grained rubrics (W5, W6, W7)

### 6.1 Liu, Zhou, Guo, Shareghi, Vulić, Korhonen & Collier (2024) — Aligning with Human Judgement: The Role of Pairwise Preference in LLM Evaluators (PairS)
**Venue: COLM 2024.** arXiv:2403.16950. File: `B_Liu2024_PairwisePreferenceJudges_COLM.pdf`

The systematic head-to-head of **direct (pointwise) scoring vs. pairwise preference**, and the paper that says the
uncomfortable thing about EmbGen's design: pointwise LLM scores have a **prior distribution that does not match the
human score distribution**, and **existing calibration methods are insufficient to fix it**, because the misalignment
lies in the *evaluation standard* (the likelihood), not in a biased score prior. PairS reformulates evaluation as
uncertainty-guided pairwise ranking and beats direct scoring and G-Eval on most aspects/datasets. For EmbGen the
implication is concrete: report a **pairwise EmbGen-vs-baseline judgement as a robustness check** on the pointwise
Binary Accuracy headline; if the two disagree, the pointwise scale is the problem.

**Reusable numbers:** PairS-greedy needs only **~30%** of the comparisons of an Elo baseline for equal quality; calibrated
PairS beats the *upper bound* of exhaustive N(N−1) comparison baselines. Transitivity (Spearman ρ over 10 seeds,
coherence): GPT-3.5 beam **55.9 ± 0.72** (NewsRoom) / **41.7 ± 0.43** (SummEval) vs. greedy 54.6 / 36.2; Llama-2-7B
39.5 → 43.2. They flag the ceiling case: SummEval consistency, where **86.7%** of human labels are the same value —
a warning for EmbGen's compressed 3-level scale.

**USE FOR: W7** (primary), **W5, W1.**

---

### 6.2 Liu, Iter, Xu, Wang, Xu & Zhu (2023) — G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment
**Venue: EMNLP 2023 (Main).** `2023.emnlp-main.153`, DOI 10.18653/v1/2023.emnlp-main.153. arXiv:2303.16634.
**Already present as `D_Liu2023_GEval_EMNLP.pdf`** (duplicate deleted).

Two things EmbGen needs. (i) The **probability-weighted score**: instead of taking the argmax category, take
Σ_i p(s_i)·s_i over the score tokens. This is a **drop-in fix for EmbGen's W3 and W7** — it yields a continuous score
from a coarse ordinal rubric in *one* call, recovers the resolution destroyed by the "categorical → ordinal → rounded"
round-trip, and gives real per-item variance instead of ten identical temperature-0 samples.
(ii) The paper's own limitation section is the citation for **W6**: G-Eval-style judges show a documented
**preference for LLM-generated text over human-written text**, which the authors warn creates *self-reinforcement* when
the metric is used as a training/selection signal — exactly EmbGen's synthetic-reference situation.

**USE FOR: W3, W6, W7.**

---

### 6.3 Ye, Kim, Kim, Hwang, Kim, Jo, Thorne, Kim & Seo (2024) — FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets
**Venue: ICLR 2024 (Spotlight).** arXiv:2307.10928.
**Already present as `D_Ye2024_FLASK_ICLR.pdf`** (duplicate deleted).

The methodological precedent for decomposing a monolithic quality score into **instance-specific fine-grained skill
rubrics** rather than fixed global dimensions. Two things EmbGen can borrow: (a) evidence that fine-grained
skill-level scoring **improves judge–human correlation** over coarse holistic scoring, which is the constructive
version of the W7 critique; and (b) the practice of assigning *per-instance* required skills, which for EmbGen would
mean deriving each eval item's expected claim set from the source ED pairs rather than scoring "Completeness" against
an unstated ideal. That directly attacks the length confound: Completeness becomes "fraction of the k required claims
present", a **length-normalised, countable** quantity rather than an impression.

**USE FOR: W5, W6, W7.**

---

### 6.4 Kim, Shin, Cho, Jang, Longpre, Lee, Yun, Shin, Kim, Thorne & Seo (2024) — Prometheus: Inducing Fine-grained Evaluation Capability in Language Models
**Venue: ICLR 2024.** arXiv:2310.08491. **Already present as `D_Kim2024_Prometheus_ICLR.pdf`** (duplicate deleted).

### 6.5 Kim, Suk, Longpre, Lin, Shin, Welleck, Neubig, Lee, Lee & Seo (2024) — Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models
**Venue: EMNLP 2024 (Main).** `2024.emnlp-main.248`, DOI 10.18653/v1/2024.emnlp-main.248. arXiv:2405.01535.
**Already present as `D_Kim2024_Prometheus2_EMNLP.pdf`** (duplicate deleted).

Together these are the **open-weight, reference-based, user-defined-rubric judges** — the cheapest possible way for
EmbGen to break the teacher==judge confound. Prometheus 2 handles **both direct assessment (pointwise, with a reference
answer and a custom rubric — EmbGen's exact format) and pairwise ranking**, closely mirroring human and GPT-4
judgements across four direct-assessment and four pairwise benchmarks. Adding Prometheus-2-8x7B as a second judge costs
nothing per-token beyond compute and is from a completely disjoint lineage (Mistral) to GPT-5.
⚠️ Caveat to state honestly: Park et al. (4.3) measure Prometheus-2-7B at only **34.4** on EvalBiasBench (17.6 on the
Length subset), so it is a **de-confounding** judge, not a *better* judge — use it as a disagreement detector, not as
a replacement gold standard.

**USE FOR: W2** (primary — the practical way to add a non-GPT judge), **W1, W6.**

---

### 6.6 Zeng, Yu, Gao, Meng, Goyal & Chen (2024) — Evaluating Large Language Models at Evaluating Instruction Following (LLMBar)
**Venue: ICLR 2024.** OpenReview `tr0KidwPLc`. arXiv:2310.07641.
**Already present as `A_Zeng2024_LLMBar_ICLR.pdf`** (duplicate deleted).

The **adversarial meta-evaluation set with objectively correct labels**: each instance pairs a genuinely
instruction-following output against one that is **superficially more appealing** (longer, more fluent, better
formatted) but objectively worse. Because the labels are objective rather than preferential, it is a valid gold
standard for EmbGen's judge with *zero* new annotation, and its Natural/Adversarial split lets EmbGen report
"our judge's accuracy on adversarially-length-inflated pairs" as a one-line credibility statement. Park et al.
(4.3) report GPT-4-class judges dropping sharply on the GPTOut and Manual adversarial splits.

**USE FOR: W1, W5, W6.**

---

## Recommended bias-control protocol for EmbGen

**Scope correction first.** EmbGen grades **one answer at a time against a reference**, so classic position/order bias
(Wang et al., ACL 2024; Shi et al., AACL-IJCNLP 2025) — a property of *pairwise/list-wise* comparison — **does not
apply**. State this explicitly, or reviewers will assume it was ignored. What *does* apply to pointwise grading:
(a) **anchoring across the four dimensions scored in one prompt** (Stureborg et al. 2024: Kendall τ 0.400→0.368 from
1st to 4th attribute); (b) **verbosity/salience bias** (Koo et al., Findings ACL 2024: GPT-4 salience 0.56);
(c) **self-preference / preference leakage** (Li et al., ICLR 2026); (d) **ordinal-scale compression** (Stureborg;
Liu et al., COLM 2024).

**Step 1 — Real variance, not T=0×10 (W3).** Re-run at **T=1**, ≥5 samples, and report **Repetition Stability**
(Shi et al.; ≥0.87 healthy) or **CALM Consistency Rate** (Ye et al., ICLR 2025; GPT-4o CR = 0.998 on fact-like data).
Emit **G-Eval probability-weighted scores** (Liu et al., EMNLP 2023) so the 3-level rubric yields continuous values
instead of a rounded round-trip.

**Step 2 — One call per dimension (W7).** Justified by Stureborg's anchoring result and Wu & Aji's MERS (COLING 2025).
Report the inter-dimension correlation matrix; drop Clarity if redundant.

**Step 3 — Break teacher==judge (W2).** Compute the **Preference Leakage Score** (Li et al., ICLR 2026) by adding a
non-GPT judge — **Prometheus-2-8x7B** (Kim et al., EMNLP 2024) is open-weight, reference-based, and matches EmbGen's
format. Aggregate via **PoLL** max-voting (Verga et al. 2024: σ = 2.2 vs 6.1; κ = 0.763–0.906; 7–8× cheaper); report
the headline both ways. Also run **Panickssery et al.'s self-recognition probe** (NeurIPS 2024; GPT-4 baseline 73.5%)
and **Koo's Compassion-Fade probe**. An 8B student trained on ~100% synthetic GPT-5 data is Li et al.'s
maximum-risk configuration.

**Step 4 — Length-control Completeness / Binary Accuracy (W5).** Cheapest first: (i) **length-stratified NRG**
(Singhal et al., COLM 2024) — 20-token buckets, report the non-length share of the 88.9% uplift; (ii) the
**Dubois et al. GLM** (COLM 2024), `logit P(BinAcc=1) = θ_system + φ·tanh((len − len_ref)/σ) + ψ_item`, then zero the
length term (ψ_item also buys paired-design variance reduction for W4); (iii) **CALM's content-preserving expansion
probe** — lengthen answers without adding information, report RR_verbosity. Add **Saito et al.'s accuracy-parity gap**
(GPT-4 = 0.328) on any human slice.

**Step 5 — Zero-annotation external validity (W1/W6).** Run the judge on **EvalBiasBench** (Park et al., Findings
EMNLP 2024; GPT-4o = 86.9) and **LLMBar** (Zeng et al., ICLR 2024); both carry objective labels. Build a 40-item
**Wu & Aji flawed-answer set** from EmbGen's own questions — their GPT-4 result (several minor factual errors at
100 words = 1206 Elo > correct at 50 words = 1096) is the failure mode to test for. Spend human budget via **HITLC**
routing (Wang et al.: human-level alignment at 20% cost) or **Cascaded Selective Evaluation** (Jung et al., ICLR 2025:
>80% guaranteed agreement at ~80% coverage).
