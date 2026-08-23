# Agent A — Meta-evaluation of LLM judges: validating a judge against humans

Scope: the protocol, statistics and evidence EmbGen needs to (a) validate its GPT-5 judge against human
annotators on a small budget, (b) choose and defend the agreement statistic, and (c) argue honestly about
what human labels can and cannot certify.

All PDFs live in `/Users/andreanicastro/Documents/repos/embgen-lit-rev/llm-as-a-judge/claude-papers/`.
All 20 files were verified (`>50KB`, magic bytes `%PDF-`). No broken downloads; nothing dropped.

Venue verification method: ACL Anthology landing pages / camera-ready PDF headers / OpenReview / ICLR
proceedings pages. Where the PDF header itself states the venue, I quote it.

---

## 1. Core meta-evaluation protocol (how to certify a judge with few human labels)

### 1.1 Calderon, Reichart & Dror (2025). *The Alternative Annotator Test for LLM-as-a-Judge: How to Statistically Justify Replacing Human Annotators with LLMs.*
**Venue (verified from camera-ready header): ACL 2025, Long Papers, pp. 16051–16081.** arXiv:2501.10970.
File: `A_Calderon2025_AlternativeAnnotatorTest_ACL.pdf`

This is **the single most useful paper for EmbGen's W1**. It proposes the *alt-test*: a leave-one-annotator-out
procedure that asks, for each human annotator *j*, whether the LLM predicts the *remaining* annotators better
than annotator *j* does. Each comparison yields a p-value; Benjamini–Hochberg FDR control is applied across
annotators; the **winning rate ω** is the fraction of annotators the LLM beats. If **ω ≥ 0.5** the LLM may be
used in place of humans. A cost–benefit discount **ε** handicaps the LLM (they use ε = 0.1 for crowd-workers,
ε = 0.15 for skilled annotators, **ε = 0.2 for experts**). They also report the **average advantage probability
ρ** as a continuous, interpretable judge-quality score. Crucially, §"how many annotated instances" and Figure 2
show the test stabilises with **three annotators and 50–100 items**, and Table 3 reports full bootstrapped
results for exactly the "3 annotators × 100 instances" regime.
- **Reusable numbers**: minimum viable design = **≥3 annotators, 50–100 items**; decision threshold **ω ≥ 0.5**;
  ε = 0.2 for expert annotators; MT-Bench and SummEval are datasets where **no** LLM passed the alt-test
  (a useful cautionary comparison); GPT-4o passed on 4/10 datasets.
- **USE FOR: W1** (primary), **W4** (it is a hypothesis test with FDR control, so it delivers significance,
  not just a correlation), **W2** (the test penalises a judge that is merely self-consistent rather than human-like).

### 1.2 Bavaresco et al. (2025). *LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks.*
**Venue (verified, ACL Anthology 2025.acl-short.20): ACL 2025, Short Papers, pp. 238–255.** arXiv:2406.18403.
File: `A_Bavaresco2025_LLMsInsteadOfHumanJudges_ACL.pdf`

Builds JUDGE-BENCH: 20 datasets with **human annotations**, and asks 11 LLMs to replicate them. Their
methodology is exactly the template EmbGen should copy: **Cohen's κ for categorical annotations, Spearman's ρ
for graded annotations**, and — the key move — an explicit **human upper bound (UB)** computed by bootstrapping
a *single* human rater against the *aggregate* of the remaining raters. That UB is what makes a κ of 0.28
interpretable. Their conclusion is explicitly the recommendation EmbGen must adopt: *"We recommend validation
and calibration of LLMs against task-specific human judgments prior to their deployment as evaluators."*
- **Reusable numbers**: best judge (GPT-4o) averages **Cohen's κ = 0.28 ± 0.32** on categorical tasks and
  **Spearman ρ = 0.50 ± 0.21** on graded tasks across 20 tasks; typically **3 human judgments per item**;
  agreement is *lower* on machine-generated text than on human text (Figure 4) — directly relevant to EmbGen,
  whose items are all machine-generated.
- **USE FOR: W1** (the UB methodology and the headline κ = 0.28 as the field-wide baseline EmbGen must beat),
  **W6** (their human-vs-machine-generated-text split is evidence that judging LLM-generated text is harder).

### 1.3 Jung, Brahman & Choi (2025). *Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement.*
**Venue (verified from PDF header "Published as a conference paper at ICLR 2025"): ICLR 2025.** arXiv:2407.18370.
File: `A_Jung2025_TrustOrEscalate_ICLR.pdf`

Introduces **selective evaluation**: the judge emits a confidence estimate and only issues a verdict when
confident, escalating (abstaining, or deferring to a stronger judge / human) otherwise. Under this framework
they derive a **provable lower bound on human agreement** for the non-abstained subset, calibrated with a small
human-labelled set. They also propose *Simulated Annotators* (in-context simulation of multiple annotator
personas) to get better-calibrated confidence without extra human labels, and a cascaded judge pipeline.
- **Reusable methodology**: EmbGen can report judge accuracy *conditional on confidence* with a certified
  agreement floor (e.g. "≥80% human agreement on the 70% of items the judge is confident on"), which is far
  more defensible than an unconditional 250-item score.
- **USE FOR: W1, W4** (this is the only paper here that gives a *guarantee* rather than a point estimate),
  **W3** (confidence estimation is the right substitute for the degenerate temperature-0 × 10 repeat protocol).

### 1.4 Shankar, Zamfirescu-Pereira, Hartmann, Parameswaran & Arawjo (2024). *Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences.*
**Venue (verified, ACM DL 10.1145/3654777.3676450 / dblp conf/uist/ShankarZHPA24): UIST 2024** (37th ACM Symp. on
User Interface Software and Technology). arXiv:2404.12272. File: `A_Shankar2024_WhoValidatesTheValidators_UIST.pdf`

Presents **EvalGen**, a mixed-initiative system that generates candidate evaluator implementations (LLM grader
prompts and Python assertions), asks a human to grade a *small subset* of outputs, and then **selects the
evaluator implementation that best aligns with those human grades**. The qualitative study surfaces
**criteria drift**: users cannot fully specify grading criteria a priori — grading outputs is what teaches them
the criteria. This is a direct threat to EmbGen's four fixed dimensions defined before any human ever looked
at the outputs.
- **Reusable methodology**: align-then-report loop on a small human sample; report *coverage* and *false failure
  rate* of the judge rubric rather than only accuracy. Cite criteria drift as the justification for a pilot
  annotation round that **revises** the Strong/Adequate/Weak rubric before the main round.
- **USE FOR: W1, W7** (criteria drift and criteria-dependence is the best available argument that the four
  dimensions need empirical validation, not assertion).

### 1.5 Dorner, Nastl & Hardt (2025). *Limits to Scalable Evaluation at the Frontier: LLM as Judge Won't Beat Twice the Data.*
**Venue (verified, ICLR 2025 proceedings; announced by MPI-IS as an ICLR 2025 **Oral**): ICLR 2025.** arXiv:2410.13341. Local file is the ICLR camera-ready.
File: `A_Dorner2025_LimitsScalableEvaluation_ICLR.pdf`

A theory paper on the exact question EmbGen faces: *can a few human labels debias a large number of judge
labels?* Main theorem: **when the judge is no more accurate than the evaluated model, no debiasing method can
reduce the required number of ground-truth labels by more than a factor of two.** It also formalises how
self-preferencing distorts model comparisons.
- **Reusable number**: the **factor-of-2 ceiling** — cite it to pre-empt "why not just use PPI/CPPI and claim a
  huge effective sample size?", and to set honest expectations about how much a 100-item human set can buy.
- **USE FOR: W1, W2** (formal statement of the self-preference distortion), **W4** (bounds the achievable
  variance reduction). Complements Agent C's prediction-powered-inference papers (`C_Angelopoulos*`, `C_Eyre*`,
  `C_Boyeau*`) — **this is the paper that says how far those methods can go.**

---

## 2. Meta-evaluation benchmarks (what "a good judge" looks like, and where judges break)

### 2.1 Zeng, Yu, Gao, Meng, Goyal & Chen (2024). *Evaluating Large Language Models at Evaluating Instruction Following* (LLMBar).
**Venue (verified, iclr.cc/virtual/2024/poster/17598): ICLR 2024.** arXiv:2310.07641. File: `A_Zeng2024_LLMBar_ICLR.pdf`

The canonical meta-evaluation benchmark for LLM evaluators. 419 instances (100 NATURAL + 319 ADVERSARIAL) with
**objective** preference labels, where the dispreferred output deliberately has appealing superficial qualities
(length, formatting, apparent authority). The key methodological contribution for EmbGen is the framing:
a meta-evaluation set is only meaningful if the *human* labels themselves are reliable.
- **Reusable numbers (very citable)**: LLMBar's **expert annotator agreement = 94%**, versus
  **AlpacaFarm human agreement 66%** and **MT-Bench human agreement 63%**, against a 50% random baseline. This is
  the single best justification for EmbGen restricting its human validation to *objectively checkable* dimensions
  (Factual Accuracy, Completeness) rather than Clarity. Also: prompting strategies (rules + metrics + reference +
  swapped-position ensembling) measurably improve evaluator agreement.
- **USE FOR: W1** (target agreement level), **W5** (adversarial set is explicitly built around superficial
  quality / verbosity attractors), **W7** (argues for objective, verifiable criteria).

### 2.2 Tan, Zhuang, Montgomery, Tang, Cuadron, Wang, Popa & Stoica (2025). *JudgeBench: A Benchmark for Evaluating LLM-Based Judges.*
**Venue (verified from PDF header "Published as a conference paper at ICLR 2025"): ICLR 2025.** arXiv:2410.12784.
File: `A_Tan2025_JudgeBench_ICLR.pdf`

Converts existing hard datasets (knowledge, reasoning, math, coding) into response pairs whose preference labels
reflect **objective correctness**, not human taste — so a judge's score is a factuality-detection score, not a
preference-mimicry score. Finding: many strong models (incl. GPT-4o) perform **only slightly better than random**.
- **Reusable methodology**: the "derive labels from verifiable correctness rather than from annotator preference"
  trick is directly transferable to EmbGen — for Pop-QA-Cities-20 the entity attributes are checkable, so a
  subset of the human validation set can be built from *verifiable* gold rather than opinion.
- **USE FOR: W1, W6** (an answer to "your references were LLM-generated": ground a subset in verifiable facts).

### 2.3 Lambert, Pyatkin, Morrison, Miranda, Lin, Chandu, Dziri, Kumar, Zick, Choi, Smith & Hajishirzi (2025). *RewardBench: Evaluating Reward Models for Language Modeling.*
**Venue (verified, ACL Anthology 2025.findings-naacl.96): Findings of NAACL 2025, pp. 1755–1797.** arXiv:2403.13787.
File: `A_Lambert2025_RewardBench_NAACL-Findings.pdf`

The reference meta-evaluation harness for reward models / preference scorers, with an explicit taxonomy
(Chat, Chat-Hard, Safety, Reasoning) and **prior-set / length-controlled subsets**. Methodologically it is the
best template for how to *report* judge quality: per-category accuracies with a length-bias diagnostic rather
than a single aggregate.
- **USE FOR: W1, W5** (its length/verbosity diagnostics), **W2** (it documents family-level correlation between
  scorer and scored model).

### 2.4 Gera, Boni, Perlitz, Bar-Haim, Eden & Yehudai (2025). *JuStRank: Benchmarking LLM Judges for System Ranking.*
**Venue (verified from camera-ready header; ACL Anthology 2025.acl-long.34): ACL 2025, Long Papers, pp. 682–712.** IBM Research. arXiv:2412.09569.
File: `A_Gera2025_JuStRank_ACL.pdf`

Argues that instance-level judge accuracy is the *wrong* target when the claim is about *systems*. They score
**63 systems × 500 Arena-Hard-v0.1 questions** with 10 LLM judges and 8 reward models, then compare the induced
**system ranking** to the human-based ranking. They introduce per-judge, per-system **bias** (systematic
positive/negative offset toward a given system) and **decisiveness** (how sharply the judge separates systems).
- **Reusable methodology**: EmbGen's claim *is* a system-ranking claim (EmbGen > EntiGraph > InstructLab > none).
  JuStRank says: report rank correlation with a human ranking, and report **per-system judge bias** — which is
  exactly the measurement that would expose whether GPT-5-as-judge favours GPT-5-teacher-derived outputs.
- **USE FOR: W2** (the per-system bias decomposition is *the* quantitative test for self/familial preference),
  **W1**, **W4** (system-level vs instance-level uncertainty).

### 2.5 Thakur, Choudhary, Ramayapally, Vaidyanathan & Hupkes (2025). *Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges.*
**Venue (verified from camera-ready header): 4th Workshop on Generation, Evaluation and Metrics (GEM² 2025),
co-located with ACL 2025, pp. 404–430.** *Note: peer-reviewed **workshop**, not main conference; but heavily cited
and the canonical reference for the "percent agreement is not enough" argument.* arXiv:2406.12624.
File: `A_Thakur2025_JudgingTheJudges_GEM-Workshop-ACL.pdf`

13 judge models × 9 exam-taker models on TriviaQA, in a deliberately *clean* setting (high human alignment) so
that judge failure cannot be blamed on task ambiguity. The headline methodological result is exactly EmbGen's
statistic problem: **"judges with high agreement can still assign vastly different scores"**, so **percent
agreement must not be the reported metric**; they use **Scott's π** instead and show it discriminates judges
that percent agreement cannot.
- **Reusable numbers (excellent)**: human–human alignment **96% percent agreement**; best judges reach
  **Scott's π ≈ 87–88** (GPT-4 Turbo, Llama-3-70B, Llama-3.1-70B), still below the human ceiling; weaker judges
  fall to π = 26–34. Judges differ from human-assigned scores by **up to 5 points** even when aligned; high
  percent agreement can coexist with **10–20 point** score differences. Also documents a **leniency bias** and
  sensitivity to prompt complexity.
- **USE FOR: W1** (this is the citation for *why* EmbGen must report a chance-corrected coefficient),
  **W4** (score-level divergence despite agreement ⇒ error bars needed).

### 2.6 Chen, Chen, Liu, Jiang & Wang (2024). *Humans or LLMs as the Judge? A Study on Judgement Bias.*
**Venue (verified, ACL Anthology 2024.emnlp-main.474): EMNLP 2024 Main, pp. 8301–8327.** arXiv:2402.10669.
File: `A_Chen2024_HumansOrLLMsAsTheJudge_EMNLP.pdf`

A reference-free **intervention study**: they perturb answers (inject a factual error, gender-biased content,
fake references, "rich content") and measure whether judges' scores move as they should. Four biases:
**Misinformation Oversight, Gender, Authority, Beauty**. Both human and LLM judges are vulnerable; humans are
*not* uniformly better. Because it needs no gold labels, it is cheap.
- **Reusable methodology (cheap and high-value for EmbGen)**: run the **Misinformation Oversight** probe —
  inject a known factual error into a sample of otherwise-correct answers and check the GPT-5 judge downgrades
  Factual Accuracy from Strong. This is a *validity* check that costs zero human annotation.
- **USE FOR: W1** (validity without human labels), **W5** ("rich content" perturbation is a verbosity probe),
  **W7** (shows dimensions do not respond independently to targeted perturbations).

### 2.7 Doddapaneni, Khan, Verma & Khapra (2024). *Finding Blind Spots in Evaluator LLMs with Interpretable Checklists* (FBI).
**Venue (verified, ACL Anthology 2024.emnlp-main.911): EMNLP 2024 Main, pp. 16279–16309.** *(EMNLP 2024 best-paper
award listing.)* arXiv:2406.13439. File: `A_Doddapaneni2024_FBIBlindSpots_EMNLP.pdf`

Same perturbation logic as above but systematised: **2,400 perturbed answers across 22 perturbation categories**
targeting factual accuracy, instruction following, long-form coherence and reasoning, evaluated by 5 evaluator
LLMs under several strategies.
- **Reusable numbers (the money quote for EmbGen's related work)**: evaluator LLMs **failed to identify quality
  drops in over 50% of cases on average**; single-answer and pairwise evaluation were notably weak, while
  **reference-based evaluation performed comparatively better**. That last clause is a *defence* of EmbGen's
  reference-based pointwise design — cite it explicitly.
- **USE FOR: W1** (perturbation-based validity suite), **W6** (justifies reference-based grading as the least-bad
  option), **W7** (per-ability checklists = the fine-grained alternative to 4 coarse dimensions).

---

## 3. The right agreement statistic

### 3.1 Artstein & Poesio (2008). *Inter-Coder Agreement for Computational Linguistics.*
**Venue (verified, ACL Anthology J08-4004): Computational Linguistics 34(4), pp. 555–596.**
File: `A_ArtsteinPoesio2008_InterCoderAgreement_ComputationalLinguistics.pdf`

The canonical CL survey of agreement coefficients — **exactly the citation EmbGen needs for its statistic
choice**. It derives and contrasts S, Scott's **π**, Cohen's **κ**, Fleiss/Carletta **K** and Krippendorff's
**α**, explains why **observed (percent) agreement alone is uninterpretable** because it ignores chance and
marginal distributions, and — critically for EmbGen's **ordinal** Strong/Adequate/Weak scale — develops the
**weighted coefficients** (weighted κ, α with a distance metric) that credit near-misses. It documents the
convention that **α/κ ≥ 0.8 indicates reliability and 0.67 ≤ α < 0.8 licenses only tentative conclusions**,
while also cautioning that these thresholds are borrowed conventions, not laws.
- **Reusable numbers/rules**: report a **weighted, chance-corrected** coefficient for ordinal data; the
  **0.67 / 0.8 thresholds**; report both κ and π/K when marginals differ (Di Eugenio & Glass's recommendation,
  discussed in §2.4–3.1) since the choice can move a value across the 0.67 line.
- **USE FOR: W1** (statistic selection and its defence), **W7** (weighted α per dimension exposes which
  dimensions carry no reliable signal).

### 3.2 Amidei, Piwek & Willis (2018). *Rethinking the Agreement in Human Evaluation Tasks.*
**Venue (verified from camera-ready header; ACL Anthology C18-1281): COLING 2018, pp. 3318–3329** (position paper). File: `A_Amidei2018_RethinkingAgreementHumanEvaluation_COLING.pdf`

The necessary counterweight to §3.1. Argues that in NLG human evaluation, **maximising inter-annotator agreement
is not automatically the goal**: legitimate variation in judgement is signal, and agreement can be inflated
artificially by coarsening the scale. They give the concrete example that collapsing word senses from an average
of 7.6 to 4 per noun raised average κ from **0.463 to 0.862** — i.e. a 3-point ordinal scale like EmbGen's
mechanically buys agreement that a finer scale would not.
- **USE FOR: W1** (pre-empts the reviewer who says "your κ is only 0.5"), **W7** (direct warning that EmbGen's
  Strong/Adequate/Weak collapse inflates apparent reliability — must be acknowledged).

---

## 4. Human annotation as an imperfect gold standard

### 4.1 Aroyo & Welty (2015). *Truth Is a Lie: Crowd Truth and the Seven Myths of Human Annotation.*
**Venue (verified, DOI 10.1609/aimag.v36i1.2564): AI Magazine 36(1), pp. 15–24.** *(Peer-reviewed journal;
CC-BY copy from research.vu.nl.)* File: `A_AroyoWelty2015_TruthIsALie_AIMagazine.pdf`

Dismantles the assumption of a single correct annotation for semantic-interpretation tasks and enumerates seven
myths (one truth; one is enough; experts are better; all examples are equal; disagreement is bad; detail hurts;
one gold set is forever). Proposes **CrowdTruth**: model disagreement rather than suppress it, and treat
annotation as a distribution.
- **USE FOR: W1** (frames judge-human disagreement as expected, not disqualifying), **W6** (the sharpest
  available argument that "no canonical human gold set exists" is a property of the task, not a defect of EmbGen).

### 4.2 Plank (2022). *The "Problem" of Human Label Variation: On Ground Truth in Data, Modeling and Evaluation.*
**Venue (verified, ACL Anthology 2022.emnlp-main.731): EMNLP 2022 Main.** arXiv:2211.02570.
File: `A_Plank2022_HumanLabelVariation_EMNLP.pdf`

The modern NLP position paper on the same theme. Distinguishes annotator error from genuine **human label
variation** (ambiguity, subjectivity, legitimate differences in interpretation) and argues evaluation should
model the label *distribution* rather than a majority-vote point.
- **Reusable methodology**: instead of forcing a majority label, EmbGen can report judge agreement against the
  **full human label distribution** (e.g. soft agreement / cross-entropy against the 3-annotator distribution),
  which is more honest at N = 100 and more favourable to the judge.
- **USE FOR: W1, W6**.

### 4.3 Kamalloo, Dziri, Clarke & Rafiei (2023). *Evaluating Open-Domain Question Answering in the Era of Large Language Models.*
**Venue (verified from camera-ready header; ACL Anthology 2023.acl-long.307): ACL 2023, Long Papers, pp. 5591–5606.** arXiv:2305.06984.
File: `A_Kamalloo2023_EvaluatingOpenDomainQA_ACL.pdf`

Manually re-judges answer correctness for open-domain QA and shows that lexical-match metrics (EM/F1) badly
**underestimate** LLM answer correctness — precisely EmbGen's motivation for using a judge alongside BLEU/ROUGE.
Its annotation study is the closest available **human–human ceiling for exactly EmbGen's task** (deciding
whether a free-form answer to a factoid question is correct).
- **Reusable numbers (the best ceiling in this bibliography)**: **Fleiss' κ = 0.728** between two annotators on
  answer-correctness judgements, with **202 disagreements out of 1,490 cases (13.6%)**; a third annotator
  adjudicated. Disagreements concentrate in **ambiguous, list-style and time-dependent** questions.
- **USE FOR: W1** (a judge–human κ near 0.7 on factual-accuracy judgements is *at the human ceiling*, not a
  failure — this reframes the whole validation result), **W6** (evidence that reference-based lexical matching
  is the weaker gold, not the judge).

---

## 5. Human evaluation protocol design in NLG

### 5.1 van der Lee, Gatt, van Miltenburg, Wubben & Krahmer (2019). *Best Practices for the Human Evaluation of Automatically Generated Text.*
**Venue (verified, ACL Anthology W19-8643): INLG 2019.** File: `A_vanderLee2019_BestPracticesHumanEvaluation_INLG.pdf`

Bibliometric survey of NLG human evaluation plus an actionable checklist: report participant numbers and
recruitment, report the scale used, **report inter-annotator agreement**, **report confidence intervals via
bootstrap resampling**, run statistical tests, and release materials. Documents that 5-point Likert is the modal
scale (14 papers) with 3-point used in only 5 — so EmbGen's 3-level ordinal scale is unusual and needs a stated
justification.
- **USE FOR: W1** (protocol checklist to comply with), **W4** (bootstrap CIs are explicitly recommended here for
  generation metrics).

### 5.2 Howcroft, Belz, Clinciu, Gkatzia, Hasan, Mahamood, Mille, van Miltenburg, Santhanam & Rieser (2020). *Twenty Years of Confusion in Human Evaluation: NLG Needs Evaluation Sheets and Standardised Definitions.*
**Venue (verified from camera-ready header): INLG 2020, pp. 169–182.** File: `A_Howcroft2020_TwentyYearsConfusingHumanEvaluation_INLG.pdf`

Surveys two decades of NLG human evaluations and finds a proliferation of inconsistently-named, undefined
quality criteria that makes cross-paper comparison and meta-evaluation impossible. Proposes normalised criterion
definitions and **evaluation datasheets**.
- **Reusable methodology**: EmbGen's four dimensions (Factual Accuracy, Completeness, Relevance, Clarity) are
  precisely the kind of ad-hoc criterion set this paper criticises. Map them onto Howcroft et al.'s normalised
  taxonomy (e.g. *correctness of outputs relative to input* vs *goodness of outputs in their own right*) and
  ship an evaluation sheet in the appendix. Cheap, and it directly answers W7.
- **USE FOR: W7** (primary), **W1**.

### 5.3 Belz, Thomson, Reiter & Mille (2023). *Non-Repeatable Experiments and Non-Reproducible Results: The Reproducibility Crisis in Human Evaluation in NLP.*
**Venue (verified from camera-ready header; ACL Anthology 2023.findings-acl.226): Findings of ACL 2023, pp. 3676–3687.**
File: `A_Belz2023_ReproducibilityCrisisHumanEval_ACL-Findings.pdf`

Reports a coordinated attempt to reproduce prior NLP human evaluations and finds the overwhelming majority are
**not repeatable and/or not reproducible and/or too flawed to be worth reproducing** — in the companion study (Belz et al., *Insights from Negative Results* 2023.insights-1.1, not downloaded)
only **13%** of papers had low enough barriers to even attempt reproduction. The remedy is full reporting of
annotator recruitment/expertise, instructions verbatim, item sampling, and released raw per-annotator labels.
- **USE FOR: W1** (justifies releasing the raw per-annotator label matrix and the verbatim annotator
  instructions as an appendix — a very cheap way to look rigorous to a reviewer).

---

## Overlap notes

- Agent C is covering prediction-powered inference / few-label debiasing (`C_Angelopoulos2023_*`,
  `C_Eyre2024_*`, `C_Boyeau2024_*`, `C_Chaganty2018_*`). **Dorner et al. 2025 (§1.5) is the theoretical
  ceiling for all of those** and should be cited alongside them.
- Papers already in `papers/` (MT-Bench, both Gu et al. surveys, Li et al., Yamauchi et al., Themis,
  "When the Judge Changes", "Explicit Reasoning Makes Better Judges") were not re-downloaded.
- Not obtained: a dedicated Gwet's AC1 methodology paper. Artstein & Poesio (§3.1) plus Amidei et al. (§3.2)
  cover the paradox that motivates AC1 (high observed agreement + skewed marginals ⇒ deflated κ), which is the
  only reason EmbGen would need AC1. Recommend citing Gwet's 2008 *Br. J. Math. Stat. Psychol.* paper by
  reference only if the marginals turn out badly skewed (they will: most answers will be "Strong").

---

## Recommended protocol from this literature

**Design.** Sample **150 items** stratified across the three corpora (50 each) and across systems (EmbGen,
EntiGraph, InstructLab, no-augmentation), sampling *within* strata proportionally so the human set spans the
score range rather than only the disputed middle. Recruit **3 annotators** who each label **all 150 items** —
this is the minimum configuration Calderon et al. (2025) show is sufficient for the alt-test, and it matches the
3-judgements-per-item norm in Bavaresco et al. (2025). Run a **pilot of 20 items first** and revise the rubric
afterwards: Shankar et al. (2024) show criteria drift makes an unrevised a-priori rubric unreliable.

**What to annotate.** Only **Factual Accuracy** and **Completeness**, on the same Strong/Adequate/Weak scale, plus
the derived **Binary Accuracy** label. Do *not* spend budget on Clarity — LLMBar (Zeng et al., 2024) shows human
agreement collapses to 63–66% on subjective criteria versus 94% on objective ones, so a low κ on Clarity would
tell you nothing. Blind annotators to system identity and randomise presentation order.

**Statistics to report.**
1. **Krippendorff's α with ordinal weights** for human–human reliability, and **weighted Cohen's κ** (or Scott's
   π) for judge–human, per dimension. Artstein & Poesio (2008) is the citation for using a *weighted,
   chance-corrected* coefficient on an ordinal scale; Thakur et al. (2025) is the citation for *never* reporting
   raw percent agreement, since judges with matching percent agreement can differ by 10–20 score points.
2. **The human upper bound**, computed Bavaresco-style: bootstrap each single annotator against the aggregate of
   the other two and report the mean. Report judge–human agreement **as a fraction of that ceiling**.
3. **The alt-test** (Calderon et al., 2025): leave-one-annotator-out, BH-FDR across the 3 annotators, ε = 0.2
   (expert annotators), report winning rate ω and average advantage probability ρ. **ω ≥ 0.5 is the pass mark**
   and is the strongest single sentence EmbGen can put in the paper.
4. **Bootstrap 95% CIs** on every judge-derived number, and a **paired bootstrap / McNemar test** on the
   EmbGen-vs-baseline Binary Accuracy difference (van der Lee et al., 2019).

**What counts as acceptable.** Do not target α ≥ 0.8. For free-form QA answer-correctness the realistic human
ceiling is **Fleiss' κ ≈ 0.73** (Kamalloo et al., 2023, ACL); the best judges in the field average **κ ≈ 0.28**
(Bavaresco et al., 2025) and top out at Scott's π ≈ 0.88 against a 96% human ceiling in a *clean* setting
(Thakur et al., 2025). So: judge–human weighted κ in the **0.6–0.75** band on Factual Accuracy, reported against
the measured human ceiling, plus **ω ≥ 0.5** on the alt-test, is a defensible and honest claim. Frame residual
disagreement with Plank (2022) and Aroyo & Welty (2015) as label variation, not judge failure — and note
Amidei et al. (2018) as the reason the 3-level scale inflates agreement relative to a finer one.

**Two free add-ons (no human labels needed).** (i) A **misinformation-oversight probe** (Chen et al., 2024;
Doddapaneni et al., 2024): inject known factual errors into ~50 correct answers and measure the rate at which
the judge downgrades Factual Accuracy — evaluator LLMs miss >50% of such drops on average, so a good number here
is a real result. (ii) A **per-system judge-bias decomposition** (Gera et al., 2025) to test whether the GPT-5
judge systematically favours GPT-5-teacher-derived outputs (W2).
