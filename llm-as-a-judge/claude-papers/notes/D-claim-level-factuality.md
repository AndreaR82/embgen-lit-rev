# Agent D — Fine-grained, decomposition-based factuality evaluation without canonical labels

Scope: literature that lets EmbGen replace/augment its single 3-level "Factual Accuracy" label with
**claim-level verification against the actual source corpus**, plus cheap grounded verifiers, RAG/QA
reference-free evaluation, fine-grained rubric judges, and knowledge-injection hallucination evidence.

All venues below were **verified** against DBLP and/or the ACL Anthology landing page (title check) on
2026-08-22. arXiv-only items are explicitly labelled. 23 papers, all downloaded and byte-verified
(`%PDF` header, all >200KB) into `/Users/andreanicastro/Documents/repos/embgen-lit-rev/llm-as-a-judge/claude-papers/`.

EmbGen weakness codes used in "USE FOR" lines: W1 no human validation of judge; W2 single judge /
teacher-judge overlap; W3 degenerate temp-0 repeats; W4 no uncertainty/significance; W5 verbosity
confound; W6 synthetic reference answers; W7 no inter-dimension validity.

---

## 1. Atomic-claim decomposition and verification

### 1.1 Min et al. (2023) — FActScore
**Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke
Zettlemoyer, Hannaneh Hajishirzi. "FActScore: Fine-grained Atomic Evaluation of Factual Precision in
Long Form Text Generation." EMNLP 2023 (Main), pp. 12076–12100.** Anthology `2023.emnlp-main.741`;
arXiv:2305.14251. File: `D_Min2023_FActScore_EMNLP.pdf`.

The canonical decomposition-based factuality metric: break a generation into **atomic facts** (short,
single-proposition sentences), then label each Supported / Not-Supported **against a designated
knowledge source** (they use Wikipedia; the source is a free parameter). FActScore of a response is
simply the fraction of atomic facts that are Supported, averaged over prompts, with an explicit
abstention/response-rate handling. Their automated estimator (retrieve-then-LM, plus a non-parametric
probability "NP" variant, ensembled) approximates human FActScore with an **error rate < 2%**; the
paper's own case study shows applying it to a *non-Wikipedia* knowledge source (ACL Anthology, 10
prompts about NLP papers) gives ER = 7.41 (human 66.20 vs model 73.61) — i.e. **the recipe transfers to
a custom corpus, which is exactly EmbGen's situation**. Reported cost: evaluating 6,500 generations
from 13 LMs would have cost **$26K** in human annotation and was done automatically instead; typical
110–150 word biographies yield **26–41 atomic facts**. EmbGen can reuse the decomposition prompt
(InstructGPT few-shot, Appendix), the Supported/Not-Supported verification prompt, and the
`pip install factscore` package directly, swapping Wikipedia for the ED-pair/chunk corpus.
**USE FOR: W6 (grounds scoring in the real corpus, not an LLM-written reference), W1 (gives a unit of
annotation — the claim — that a human can label cheaply), W7 (splits "Factual Accuracy" into precision
over claims).**

### 1.2 Wei et al. (2024) — SAFE / LongFact / F1@K
**Jerry Wei, Chengrun Yang, Xinying Song, Yifeng Lu, Nathan Hu, Jie Huang, Dustin Tran, Daiyi Peng,
Ruibo Liu, Da Huang, Cosmo Du, Quoc V. Le. "Long-form factuality in large language models."
NeurIPS 2024 (Advances in Neural Information Processing Systems 37).** arXiv:2403.18802.
File: `D_Wei2024_LongFormFactuality_SAFE_NeurIPS.pdf`.

SAFE = Search-Augmented Factuality Evaluator: an LLM agent splits a response into individual facts,
**revises each into a self-contained (decontextualised) form**, discards non-verifiable ones, then
issues multi-step search queries and rates each fact supported/irrelevant/not-supported. Crucially for
EmbGen, this paper supplies the **aggregation formula**: precision = #supported / #(supported +
unsupported); recall = min(#supported / K, 1) where K is a *hyperparameter for the user's preferred
number of facts*; **F1@K** is their harmonic mean. That is a principled, length-aware alternative to
EmbGen's Binary Accuracy and directly defuses the verbosity confound (extra unsupported claims lower
precision; K caps the reward for length). Validation numbers to cite: on **~16k individual facts SAFE
agrees with crowdworkers 72% of the time**, and on 100 sampled disagreements SAFE was judged correct
**76%** of the time by expert re-adjudication, at **>20x lower cost than human annotators**. Benchmarks
13 LMs across 4 families on LongFact (38 topics, GPT-4-generated prompts) — also a precedent for
LLM-generated evaluation sets.
**USE FOR: W5 (F1@K explicitly controls length/verbosity), W6, W4 (claim counts give a much larger
effective n than 250 answers), W1.**

### 1.3 Wanner et al. (2024) — A Closer Look at Claim Decomposition / DecompScore
**Miriam Wanner, Seth Ebner, Zhengping Jiang, Mark Dredze, Benjamin Van Durme. "A Closer Look at Claim
Decomposition." *SEM 2024 (13th Joint Conference on Lexical and Computational Semantics), pp.
153–175.** Anthology `2024.starsem-1.13`; arXiv:2403.11903. File: `D_Wanner2024_ClaimDecomposition_StarSEM.pdf`.

The essential critique to pre-empt a reviewer: **FActScore-style metrics are sensitive to *which*
decomposition method is used**, and the metric silently attributes decomposition error to the generator
being evaluated. They introduce **DecompScore**, an adaptation of FActScore that measures decomposition
quality itself (roughly, the number of supported subclaims produced, controlling for redundancy), and
propose an LLM decomposition prompt grounded in logical atomism / neo-Davidsonian event semantics that
yields better decompositions than FActScore's and than naive sentence splitting. EmbGen must (a) fix
and *publish* one decomposition prompt, (b) run at least one decomposition-ablation showing the ranking
of EmbGen vs EntiGraph/InstructLab is stable across two decomposers, citing this paper as the reason.
**USE FOR: W6, W3 (a real robustness/variance ablation with substantive variation, unlike temp-0 x10),
W1.**

### 1.4 Gunjal & Durrett (2024) — Molecular Facts
**Anisha Gunjal, Greg Durrett. "Molecular Facts: Desiderata for Decontextualization in LLM Fact
Verification." Findings of EMNLP 2024, pp. 3751–3768.** Anthology `2024.findings-emnlp.215`;
arXiv:2406.20079. File: `D_Gunjal2024_MolecularFacts_EMNLP-Findings.pdf`.

Argues that **fully atomic facts are the wrong granularity**: stripped propositions lose the context
needed to interpret them (ambiguous entity references especially), while big chunks are hard to check.
Defines two criteria — **decontextuality** (can it stand alone?) and **minimality** (how little extra
context was added?) — and gives a baseline method for generating "molecular facts" that adds exactly
the disambiguating context needed. Shows molecular facts beat both atomic facts and heavier
decontextualisation methods on verification accuracy in ambiguous settings. This matters a lot for
EmbGen because its QA pairs are **multi-hop / cross-document by design**, so atomic claims will
routinely contain dangling references ("the city", "its founder") that cannot be verified against a
corpus chunk. Reuse their decontextualisation prompt as step 2 of the pipeline.
**USE FOR: W6, W7 (makes claim-level factuality actually well-defined for multi-hop answers).**

### 1.5 Song et al. (2024) — VeriScore
**Yixiao Song, Yekyung Kim, Mohit Iyyer. "VeriScore: Evaluating the factuality of verifiable claims in
long-form text generation." Findings of EMNLP 2024, pp. 9447–9474.** Anthology `2024.findings-emnlp.552`;
arXiv:2406.19276. File: `D_Song2024_VeriScore_EMNLP-Findings.pdf`.

Fixes the assumption in FActScore/SAFE that *every* extracted claim is verifiable; VeriScore extracts
only **verifiable** claims (in context, with the sentence + surrounding window given to the extractor),
which is essential for free-form answers that mix facts with hedges, framing and opinion. Human study:
three annotators, 360 judgements, **Fleiss κ = 0.766** (substantial); VeriScore's extracted claims were
preferred over SAFE's across 8 long-form tasks (SAFE preferred only 26/360 times). Also the cheap-and-
reproducible route: they distil the extractor and verifier into **fine-tuned Mistral-7B-Instruct-v0.2 /
Llama-3-8B-Instruct** from 13,403 GPT-4-generated examples, with the fine-tuned Mistral roughly matching
GPT-4 on claim extraction in a blind comparison (37%/34% GPT-4 vs 34%/41% Mistral preference,
Cohen's κ = 0.432). Evaluates 16 models; VeriScore on one task does not predict VeriScore on another —
a warning against reporting one aggregate factuality number.
**USE FOR: W2 (open-weight extractor/verifier breaks the GPT-5-teacher = GPT-5-judge loop), W6, W1.**

---

## 2. Efficient / grounded fact-verification models (cheap alternatives to a big judge)

### 2.1 Tang et al. (2024) — MiniCheck + LLM-AggreFact
**Liyan Tang, Philippe Laban, Greg Durrett. "MiniCheck: Efficient Fact-Checking of LLMs on Grounding
Documents." EMNLP 2024 (Main), pp. 8818–8847.** Anthology `2024.emnlp-main.499`; arXiv:2404.10774.
File: `D_Tang2024_MiniCheck_EMNLP.pdf`.

**The single most cost-effective drop-in verifier for EmbGen.** Small models trained on synthetic
GPT-4-generated factual errors that check a claim against a grounding document. **MiniCheck-FT5 is 770M
parameters, reaches GPT-4-level accuracy (74.7 vs 75.3 average balanced accuracy on the LLM-AggreFact
benchmark of 10 datasets) at ~400x lower cost**: their Table 4/Table 6 cost comparison over the 13K-example
test set is **$0.24 for MiniCheck-FT5 vs $107 for GPT-4** ($161 with decontextualisation, $212 with
decomposition; Claude-3 Opus $165; AlignScore 70.4 BAcc, QAFactEval ~66, SummaC-ZS ~68). They also report
that **claim decomposition does not help MiniCheck** (Table 5: −1.4 on average) because it was trained to
handle multi-sentence synthesis internally — an important design choice to report honestly. Includes a
paired bootstrap test (1000 runs, p<0.05) for comparing verifiers, which EmbGen should copy.
**USE FOR: W2 (a non-GPT judge component), W4 (cheap enough to bootstrap/score every claim), W6.**

### 2.2 Zha et al. (2023) — AlignScore
**Yuheng Zha, Yichi Yang, Ruichen Li, Zhiting Hu. "AlignScore: Evaluating Factual Consistency with A
Unified Alignment Function." ACL 2023 (Long), pp. 11328–11348.** Anthology `2023.acl-long.634`;
arXiv:2305.16739. File: `D_Zha2023_AlignScore_ACL.pdf`.

A single **355M-parameter** RoBERTa-based alignment function trained on **4.7M examples from 7 tasks**
(NLI, QA, paraphrase, fact verification, IR, STS, summarisation), evaluated on 22 datasets (19 unseen).
It scores "is text b supported by text a" for arbitrary text pairs with a splitting/aggregation scheme
for long contexts, and **matches or beats ChatGPT/GPT-4-based metrics that are orders of magnitude
larger**. For EmbGen it is a zero-API-cost, fully reproducible second opinion on claim ⊂ corpus-chunk
entailment, usable as an agreement check against the LLM verifier (its 70.4 BAcc on LLM-AggreFact is
below MiniCheck's 74.7, so use it as a corroborating rather than primary signal).
**USE FOR: W2, W4 (free to run over bootstrap resamples), W6.**

### 2.3 Fabbri et al. (2022) — QAFactEval
**Alexander R. Fabbri, Chien-Sheng Wu, Wenhao Liu, Caiming Xiong. "QAFactEval: Improved QA-Based Factual
Consistency Evaluation for Summarization." NAACL-HLT 2022, pp. 2587–2601.** Anthology `2022.naacl-main.187`.
File: `D_Fabbri2022_QAFactEval_NAACL.pdf`.

Systematic component study of QA-based factual-consistency metrics (answer selection, question
generation, question answering, answerability classification, answer overlap), yielding an optimised
metric that is **+14% on average over previous QA-based metrics on the SummaC benchmark** and beats the
best entailment metric; also shows entailment- and QA-based signals are **complementary and improve when
combined**. The relevant methodological transfer for EmbGen: the QA-based decomposition is an
alternative "unit of factuality" to atomic claims (generate questions from the answer, answer them from
the corpus, compare) and the complementarity result justifies reporting two independent verifiers.
1.4B total parameters, $1.87 to run the LLM-AggreFact test set (per MiniCheck's cost table).
**USE FOR: W7 (independent factuality signal to correlate with the rubric dimension), W2.**

### 2.4 Laban et al. (2022) — SummaC
**Philippe Laban, Tobias Schnabel, Paul N. Bennett, Marti A. Hearst. "SummaC: Re-Visiting NLI-based
Models for Inconsistency Detection in Summarization." TACL 2022, vol. 10, pp. 163–177.** Anthology
`2022.tacl-1.10`. File: `D_Laban2022_SummaC_TACL.pdf`.

Diagnoses the **granularity mismatch** that also threatens EmbGen: NLI models are trained on
sentence-pairs but were being applied document-level, which is why earlier work concluded NLI "doesn't
work" for consistency. Their fix — segment the document into sentence units, compute a pairwise
NLI matrix between source sentences and generated sentences, and aggregate (SummaC-ZS = max over source
sentences; SummaC-Conv = learned convolution over the score histogram) — reaches **74.4% balanced
accuracy, +5% over prior work**, with models as small as **60M (ALBERT-XL)**. The max-over-source-chunks
aggregation is precisely the operator EmbGen needs to verify one claim against many retrieved corpus
chunks.
**USE FOR: W6 (defines claim-vs-corpus-chunk aggregation), W2, W4 (60M model, negligible cost).**

### 2.5 Honovich et al. (2022) — TRUE
**Or Honovich, Roee Aharoni, Jonathan Herzig, Hagai Taitelbaum, Vered Cohen, Doron Kukliansky, Thomas
Scialom, Idan Szpektor, Avinatan Hassidim, Yossi Matias. "TRUE: Re-evaluating Factual Consistency
Evaluation." NAACL-HLT 2022, pp. 3905–3920.** Anthology `2022.naacl-main.287`.
File: `D_Honovich2022_TRUE_NAACL.pdf`.

The meta-evaluation paper for this whole family. It standardises 11 datasets across summarisation,
dialogue, paraphrase and fact verification into **binary example-level annotations** and argues
explicitly that the field's habit of reporting **system-level correlations hides example-level
accuracy** — a criticism that lands directly on EmbGen's aggregate Binary Accuracy. Recommends
**ROC-AUC on example-level binary labels** as the meta-evaluation statistic, and finds large-scale NLI
and QG/QA approaches strongest and complementary. EmbGen should adopt its protocol for validating its
own judge: collect binary human labels on a sample, report **ROC-AUC / balanced accuracy of the judge
against them**, not just a correlation.
**USE FOR: W1 (exact meta-evaluation protocol on a small budget), W7, W4.**

---

## 3. Reference-free / retrieval-grounded QA and RAG evaluation

### 3.1 Es et al. (2024) — RAGAS
**Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert. "RAGAs: Automated Evaluation of
Retrieval Augmented Generation." EACL 2024 System Demonstrations, pp. 150–158.** Anthology
`2024.eacl-demo.16`. File: `D_Es2024_RAGAS_EACL-Demo.pdf`.

The most-cited **reference-free** RAG evaluation suite: Faithfulness (decompose the answer into
statements with an LLM, then verify each against the retrieved context; score = #supported/#statements
— structurally identical to FActScore but with the *provided context* as the knowledge source), Answer
Relevance (generate questions from the answer and measure embedding similarity to the original
question) and Context Relevance (fraction of context sentences the LLM extracts as necessary). Validated
on **WikiEval** (50 Wikipedia pages, post-2022 events, ChatGPT-generated Q/A pairs, human pairwise
annotation): agreement with human annotators **0.95 faithfulness / 0.78 answer relevance / 0.70 context
relevance**, versus GPT-Score 0.72/0.52/0.63 and GPT-Ranking 0.54/0.40/0.52. Two direct lessons for
EmbGen: (i) the faithfulness prompt is a ready-made decomposition+verification prompt; (ii) WikiEval is
a published precedent for building an LLM-generated evaluation set and then validating it with humans
(W6 defence).
**USE FOR: W6, W1, W7 (decomposes "quality" into orthogonal, separately validated axes).**

### 3.2 Saad-Falcon et al. (2024) — ARES
**Jon Saad-Falcon, Omar Khattab, Christopher Potts, Matei Zaharia. "ARES: An Automated Evaluation
Framework for Retrieval-Augmented Generation Systems." NAACL-HLT 2024 (Long), pp. 338–354.** Anthology
`2024.naacl-long.20`. File: `D_SaadFalcon2024_ARES_NAACL.pdf`.

Fine-tunes **lightweight open LM judges** (DeBERTa-v3-Large scale) on *synthetic* query/passage/answer
training data for context relevance, answer faithfulness and answer relevance, then — the part EmbGen
must copy — **debiases the judges' aggregate score with prediction-powered inference (PPI; Angelopoulos
et al. 2023) using only ~150 human-annotated datapoints, producing statistical confidence intervals for
each RAG system's score**. Evaluated across 8 KILT/SuperGLUE/AIS tasks and shown robust to domain shift.
**Flag for the write-up: ARES is the paper that makes PPI standard practice in this exact setting** —
it is the cleanest published justification for "small human sample + LLM judge = valid CI", which is
simultaneously the fix for W1 and W4 and lets EmbGen keep N=250 while reporting defensible error bars.
**USE FOR: W1 + W4 (PPI confidence intervals from ~150 human labels), W2 (open-weight judges).**

### 3.3 Adlakha et al. (2024) — Correctness and Faithfulness for QA
**Vaibhav Adlakha, Parishad BehnamGhader, Xing Han Lu, Nicholas Meade, Siva Reddy. "Evaluating
Correctness and Faithfulness of Instruction-Following Models for Question Answering." TACL 2024, vol.
12, pp. 681–699.** Anthology `2024.tacl-1.38`. File: `D_Adlakha2024_CorrectnessFaithfulnessQA_TACL.pdf`.

**The most directly transferable paper in this whole set.** Human analysis of **1,800 model responses**
on NQ, HotpotQA and TopiOCQA, correlating every common automatic metric with human judgements of
correctness. Headline table (Spearman ρ / Kendall τ, x100): **EM 27.3/27.3, F1 47.3/40.2, ROUGE-L
45.9/38.8, METEOR 48.2/39.8, BERTScore-F1 31.9/26.1, BEM 53.7/43.9, Recall 60.0/55.6, GPT-3.5-Eval
61.4/61.4, GPT-4-Eval 67.5/67.5.** Two results EmbGen needs: (i) **token-level Recall** (fraction of
reference tokens present in the response) is by far the best *lexical* metric and beats BERTScore/BEM,
precisely **because it does not penalise the extra verbosity of instruction-following models** — this is
the principled fix for EmbGen's BLEU/ROUGE table and its verbosity confound; (ii) for faithfulness they
propose **K-Precision** — the fraction of response tokens that appear in the *knowledge source* — which
is a near-zero-cost corpus-grounded faithfulness proxy EmbGen can compute for all 250x4 answers today.
Also confirms an LLM judge tops the correlation table (67.5), which supports keeping the rubric judge as
well.
**USE FOR: W5 (recall is verbosity-robust; EM/F1 are not), W6 (K-Precision is grounded in the corpus,
not the synthetic reference), W1 (their 1,800-response human protocol is a template).**

### 3.4 Xu et al. (2023) — A Critical Evaluation of Evaluations for LFQA
**Fangyuan Xu, Yixiao Song, Mohit Iyyer, Eunsol Choi. "A Critical Evaluation of Evaluations for
Long-form Question Answering." ACL 2023 (Long), pp. 3225–3245.** Anthology `2023.acl-long.181`.
File: `D_Xu2023_CriticalEvalLongFormQA_ACL.pdf`.

Hires **domain experts in 7 areas** to give pairwise preferences plus free-form justifications over
long-form answers, then tests automatic metrics against them: **no existing automatic metric is
predictive of human preference**, though some correlate with individual fine-grained aspects (e.g.
coherence). Their closing recommendation is verbatim the argument EmbGen needs: **"move away from a
single overall score of the answer and adopt a multi-faceted evaluation, targeting aspects such as
factuality and completeness."** They also surface *comprehensiveness* as an aspect experts actually use.
Cite this both to justify having a rubric at all and to justify not trusting the aggregate.
**USE FOR: W7 (multi-faceted evaluation is the field's recommendation), W1, W5.**

### 3.5 Krishna et al. (2021) — Hurdles to Progress in LFQA
**Kalpesh Krishna, Aurko Roy, Mohit Iyyer. "Hurdles to Progress in Long-form Question Answering."
NAACL-HLT 2021, pp. 4940–4957.** Anthology `2021.naacl-main.393`. File: `D_Krishna2021_HurdlesLongFormQA_NAACL.pdf`.

The classic cautionary result: a system can top the ELI5 leaderboard while (1) its answers are **not
actually grounded in the retrieved documents** — conditioning on random documents barely changes ROUGE;
(2) **at least 81% of validation questions appear in paraphrased form in training**, i.e. train/eval
contamination; (3) **ROUGE-L is uninformative and trivially gameable** (a trivial retrieval baseline
beats the SOTA model); and (4) human evaluations for LFQA are unreliable without careful design. For
EmbGen this is a required citation for (a) why the BLEU/ROUGE table cannot carry the argument, and (b)
an explicit **train/eval leakage check** between the EmbGen-generated SFT data and the
Claude-Sonnet-4.5-generated eval sets — a reviewer will ask, and this is the paper that makes it a
standard obligation.
**USE FOR: W6 (eval-set contamination/leakage check), W5, W4.**

---

## 4. Fine-grained rubric judges (open-source, reproducible alternatives to GPT-5)

### 4.1 Kim et al. (2024) — Prometheus
**Seungone Kim, Jamin Shin, Yejin Cho, Joel Jang, Shayne Longpre, Hwaran Lee, Sangdoo Yun, Seongjin
Shin, Sungdong Kim, James Thorne, Minjoon Seo. "Prometheus: Inducing Fine-Grained Evaluation Capability
in Language Models." ICLR 2024** (OpenReview `8euJaTveKw`; arXiv:2310.08491 — PDF downloaded from arXiv
because OpenReview blocks scripted download). File: `D_Kim2024_Prometheus_ICLR.pdf`.

Trains a **13B open evaluator LLM** on the FEEDBACK COLLECTION (GPT-4-generated feedback for 1K
fine-grained score rubrics, 20K instructions, 100K responses) that scores a response 1–5 given a
**user-supplied custom rubric plus a reference answer**. Key number: **Pearson 0.897 with human
evaluators across 45 customised rubrics, on par with GPT-4 (0.882) and far above ChatGPT (0.392)**; also
correlates 0.897 with GPT-4 across 1,222 rubrics on 4 benchmarks, and works as a reward model. EmbGen
can run Prometheus as a **second, non-GPT-family judge** on the same 4-dimension rubric and report
judge-judge agreement — the cheapest possible mitigation of the GPT-5-teacher/GPT-5-judge circularity.
The 1–5 rubric-with-descriptors format is also a strictly better-specified scale than Strong/Adequate/Weak.
**USE FOR: W2 (independent open judge), W3 (real cross-judge variance), W7, W1.**

### 4.2 Kim et al. (2024) — Prometheus 2
**Seungone Kim, Juyoung Suk, Shayne Longpre, Bill Yuchen Lin, Jamin Shin, Sean Welleck, Graham Neubig,
Moontae Lee, Kyungjae Lee, Minjoon Seo. "Prometheus 2: An Open Source Language Model Specialized in
Evaluating Other Language Models." EMNLP 2024 (Main), pp. 4334–4353.** Anthology `2024.emnlp-main.248`;
arXiv:2405.01535. File: `D_Kim2024_Prometheus2_EMNLP.pdf`.

7B and 8x7B open evaluators, obtained by **weight-merging a direct-assessment-trained model with a
pairwise-ranking-trained model**, that handle both grading formats and both reference-based and
reference-free rubrics. Numbers to quote: on **FLASK, human–GPT-4 correlation is 0.679; the best prior
open evaluator (Prometheus-13B) reached 0.449; Prometheus-2-8x7B reaches 0.555, halving the gap**; it
also achieves the highest agreement with human/proprietary judges among open models on all 4 pairwise
benchmarks. This is the concrete, deployable answer to "your judge is GPT-5 and so was your teacher":
re-run the rubric with Prometheus-2-8x7B and report the agreement.
**USE FOR: W2, W3, W1.**

### 4.3 Ye et al. (2024) — FLASK
**Seonghyeon Ye, Doyoung Kim, Sungdong Kim, Hyeonbin Hwang, Seungone Kim, Yongrae Jo, James Thorne,
Juho Kim, Minjoon Seo. "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets."
ICLR 2024** (OpenReview `CYmF38ysDa`; arXiv:2307.10928 — arXiv PDF used). File: `D_Ye2024_FLASK_ICLR.pdf`.

Decomposes coarse "response quality" into **4 primary abilities / 12 fine-grained skills** (Logical
Thinking: correctness, robustness, efficiency; Background Knowledge: **factuality**, commonsense;
Problem Handling: comprehension, insightfulness, **completeness**, metacognition; User Alignment:
conciseness, readability, harmlessness), assigns **instance-wise, per-instruction skill sets and
difficulty levels**, and scores each 1–5. Directly relevant: FLASK's skill set *contains EmbGen's
Factual Accuracy and Completeness as separate, independently validated skills*, so EmbGen can cite it
as prior art for its dimension choice — and FLASK's analysis of **which skills the model-based
evaluator can and cannot judge reliably** is the template for the missing inter-dimension validity
analysis (in particular it shows fine-grained scoring raises both reliability and human-judge
correlation relative to a single overall score).
**USE FOR: W7 (validated dimension taxonomy + evidence that fine-grained > single score), W1, W5
(conciseness is scored separately from completeness).**

### 4.4 Kim et al. (2025) — The BiGGen Bench
**Seungone Kim, Juyoung Suk, Ji Yong Cho, Shayne Longpre, Chaeeun Kim, Dongkeun Yoon, Guijin Son,
Yejin Cho, Sheikh Shafayat, Jinheon Baek, Sue Hyun Park, Hyeonbin Hwang, Jinkyung Jo, Hyowon Cho,
Haebin Shin, Seongyun Lee, Hanseok Oh, Noah Lee, Namgyu Ho, Se June Joo, Miyoung Ko, Yoonjoo Lee,
Hyungjoo Chae, Jamin Shin, Joel Jang, Seonghyeon Ye, Bill Yuchen Lin, Sean Welleck, Graham Neubig,
Moontae Lee, Kyungjae Lee, Minjoon Seo. "The BiGGen Bench: A Principled Benchmark for Fine-grained
Evaluation of Language Models with Language Models." NAACL 2025 (Long), pp. 5877–5919.** Anthology
`2025.naacl-long.303`; arXiv:2406.05761. File: `D_Kim2025_BiGGenBench_NAACL.pdf`.

Argues abstract criteria (helpfulness, harmlessness) lack the granularity of human assessment, and
builds a benchmark of **9 capabilities across 77 tasks with instance-specific evaluation criteria**
(a bespoke rubric per instance rather than one global rubric), evaluating **103 frontier LMs with 5
evaluator LMs**, and reporting human-annotation-based validation of the evaluator LMs. For EmbGen the
transferable idea is **instance-specific rubrics**: for each of the 250 eval questions, the rubric
should name the specific facts required, which is far more checkable than "Factual Accuracy: Strong".
It also provides the multi-evaluator agreement methodology (5 judges) that answers W2/W3 head-on.
**USE FOR: W2 (5-judge design), W7 (instance-specific criteria), W1.**

### 4.5 Liu et al. (2023) — G-Eval
**Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, Chenguang Zhu. "G-Eval: NLG Evaluation
using GPT-4 with Better Human Alignment." EMNLP 2023 (Main), pp. 2511–2522.** Anthology
`2023.emnlp-main.153`; arXiv:2303.16634. File: `D_Liu2023_GEval_EMNLP.pdf`.

Chain-of-thought + form-filling LLM evaluation with **probability-weighted score aggregation** (weight
each discrete score by its output token probability instead of taking the argmax) — this is the correct
fix for EmbGen's degenerate "temperature 0 x 10 runs, categorical → ordinal → rounded" scheme, which
destroys exactly the fine-grained signal G-Eval recovers. **Spearman 0.514 with humans on SummEval
summarisation**, well above prior metrics. Critically for EmbGen, G-Eval also documents the **bias of
LLM evaluators towards LLM-generated text** — a reviewer will cite this against EmbGen's GPT-5-judge /
GPT-5-teacher / Claude-generated-reference setup, so it should be pre-empted and cited by EmbGen itself.
**USE FOR: W3 (probability-weighted scores instead of temp-0 repeats), W2 + W6 (documents self/LLM-text
preference bias), W1.**

### 4.6 Cook et al. (2024) — TICK / STICK  *(arXiv-only — flagged; widely cited)*
**Jonathan Cook, Tim Rocktäschel, Jakob Foerster, Dennis Aumiller, Alex Wang. "TICKing All the Boxes:
Generated Checklists Improve LLM Evaluation and Generation." arXiv:2410.03608 (2024). NOT peer-reviewed
— label as preprint if cited.** File: `D_Cook2024_TICK_arXiv.pdf`.

The judge decomposes each *instruction* into an instruction-specific **checklist of YES/NO questions**,
then evaluates a response question-by-question. Reported gain: exact agreement between LLM judgements
and human preferences rises **46.4% → 52.2%** versus direct scoring; self-refinement against the
checklist (STICK) gives **+7.8% absolute on LiveBench reasoning** and Best-of-N selection **+6.3% on
WildBench**. This is the *instruction-side* analogue of claim decomposition and pairs naturally with the
answer-side decomposition: for an EmbGen multi-hop question, the checklist enumerates the required sub-
answers, giving a natural **claim-recall denominator** that is more defensible than the synthetic
reference answer.
**USE FOR: W7, W6 (checklist defines required facts without a gold answer), W5 (checklist items are
length-invariant), W1.**

---

## 5. Hallucination and knowledge-injection evaluation

### 5.1 Li et al. (2023) — HaluEval
**Junyi Li, Xiaoxue Cheng, Wayne Xin Zhao, Jian-Yun Nie, Ji-Rong Wen. "HaluEval: A Large-Scale
Hallucination Evaluation Benchmark for Large Language Models." EMNLP 2023 (Main), pp. 6449–6464.**
Anthology `2023.emnlp-main.397`; arXiv:2305.11747. File: `D_Li2023_HaluEval_EMNLP.pdf`.

35,000 hallucinated/normal samples (30K task-specific from QA/dialogue/summarisation via a
**sampling-then-filtering** framework, 5K general ChatGPT responses with human annotation). Findings to
reuse: **~19.5% of ChatGPT responses contain unverifiable/fabricated content**, and LLMs are poor at
*recognising* hallucination — but **providing external knowledge or explicit reasoning steps
substantially improves recognition**. That last result is the empirical justification for giving
EmbGen's factuality judge the retrieved corpus chunks rather than only a reference answer. The
sampling-then-filtering recipe is also a cheap way for EmbGen to build **synthetic negative controls**
(deliberately corrupted answers) and show its judge detects them — a poor-man's judge validation with
zero human annotation.
**USE FOR: W1 (negative-control validation of the judge), W6, W2.**

### 5.2 Gekhman et al. (2024) — Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?
**Zorik Gekhman, Gal Yona, Roee Aharoni, Matan Eyal, Amir Feder, Roi Reichart, Jonathan Herzig. "Does
Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?" EMNLP 2024 (Main), pp. 7765–7784.**
Anthology `2024.emnlp-main.444`; arXiv:2405.05904. File: `D_Gekhman2024_FineTuningNewKnowledge_EMNLP.pdf`.

**The most important related-work paper for EmbGen's thesis, and the biggest threat to it.** Controlled
closed-book QA setup varying the proportion of SFT examples that introduce knowledge **new** to the
model, categorised by a SLIKNOW/`Unknown` taxonomy built from few-shot sampling of the base model.
Findings: (i) examples introducing new knowledge are **learned significantly more slowly** than examples
consistent with existing knowledge — LLMs struggle to acquire new facts via fine-tuning; (ii) once those
examples *are* fitted, they **linearly increase the model's tendency to hallucinate** on previously known
questions; (iii) conclusion: knowledge is mostly acquired in pre-training and fine-tuning teaches
*usage*. EmbGen is doing exactly knowledge-injection SFT, so it **must** cite this and show the
counter-evidence: a claim-level metric that separates (a) newly-injected corpus facts correctly produced
from (b) degradation on pre-existing knowledge. Reuse their `Known`/`Unknown` categorisation procedure
to stratify the 250-item eval sets, and their early-stopping analysis as a training-side control.
**USE FOR: W6, W4 (stratified analysis gives a much sharper effect than one aggregate 88.9% uplift),
W7.**

---

## Downloaded files (all verified `%PDF`, all >200KB)

| File | Venue (verified) |
|---|---|
| `D_Min2023_FActScore_EMNLP.pdf` | EMNLP 2023 |
| `D_Wei2024_LongFormFactuality_SAFE_NeurIPS.pdf` | NeurIPS 2024 |
| `D_Wanner2024_ClaimDecomposition_StarSEM.pdf` | *SEM 2024 |
| `D_Gunjal2024_MolecularFacts_EMNLP-Findings.pdf` | Findings of EMNLP 2024 |
| `D_Song2024_VeriScore_EMNLP-Findings.pdf` | Findings of EMNLP 2024 |
| `D_Tang2024_MiniCheck_EMNLP.pdf` | EMNLP 2024 |
| `D_Zha2023_AlignScore_ACL.pdf` | ACL 2023 |
| `D_Fabbri2022_QAFactEval_NAACL.pdf` | NAACL-HLT 2022 |
| `D_Laban2022_SummaC_TACL.pdf` | TACL 2022 |
| `D_Honovich2022_TRUE_NAACL.pdf` | NAACL-HLT 2022 |
| `D_Es2024_RAGAS_EACL-Demo.pdf` | EACL 2024 (System Demos) |
| `D_SaadFalcon2024_ARES_NAACL.pdf` | NAACL-HLT 2024 |
| `D_Adlakha2024_CorrectnessFaithfulnessQA_TACL.pdf` | TACL 2024 |
| `D_Xu2023_CriticalEvalLongFormQA_ACL.pdf` | ACL 2023 |
| `D_Krishna2021_HurdlesLongFormQA_NAACL.pdf` | NAACL-HLT 2021 |
| `D_Kim2024_Prometheus_ICLR.pdf` | ICLR 2024 |
| `D_Kim2024_Prometheus2_EMNLP.pdf` | EMNLP 2024 |
| `D_Ye2024_FLASK_ICLR.pdf` | ICLR 2024 |
| `D_Kim2025_BiGGenBench_NAACL.pdf` | NAACL 2025 |
| `D_Liu2023_GEval_EMNLP.pdf` | EMNLP 2023 |
| `D_Cook2024_TICK_arXiv.pdf` | **arXiv preprint only** |
| `D_Li2023_HaluEval_EMNLP.pdf` | EMNLP 2023 |
| `D_Gekhman2024_FineTuningNewKnowledge_EMNLP.pdf` | EMNLP 2024 |

Deliberately excluded: Lee et al. "CheckEval" (arXiv:2403.18771) — DBLP shows no peer-reviewed venue,
and TICK already covers checklist-based judging with stronger numbers.

---

## Recommended claim-level protocol for EmbGen

**Design goal.** Add a *second, corpus-grounded judge* — **CorpusFActScore** — that never sees the
LLM-written reference answer. It scores each model answer by decomposing it into claims and verifying
each against the **actual source corpus** EmbGen already owns (the three corpora plus the ED pairs and
chunk index built during data generation). It complements rather than replaces the 4-dimension rubric:
the rubric keeps Completeness, Relevance and Clarity; factuality moves to non-synthetic ground truth.

**Step 1 — Decompose.** Prompt an open-weight extractor to emit atomic claims, one proposition each
(FActScore, Min et al. 2023, EMNLP), keeping **only verifiable** claims rather than hedges or framing
(VeriScore, Song et al. 2024, Findings of EMNLP; their fine-tuned Mistral-7B extractor is a drop-in and
matches GPT-4 on extraction). Since EmbGen's questions are multi-hop, **decontextualise each claim to
molecular granularity** (Gunjal & Durrett 2024, Findings of EMNLP). Because decomposition choice shifts
scores, **fix and publish one prompt and run a two-decomposer ablation** showing the ranking is stable
(Wanner et al. 2024, *SEM).

**Step 2 — Retrieve from the corpus, not the reference.** Retrieve top-k (k=5) chunks per claim using
the embedding index EmbGen already built for ED pairs: FActScore's retrieve→LM design with Wikipedia
swapped for the domain corpus, which FActScore itself validates (ER = 7.41 on an ACL-Anthology source).

**Step 3 — Verify.** Label each claim Supported / Not-Supported with **MiniCheck-FT5 (770M; 74.7 vs
GPT-4's 75.3 BAcc on LLM-AggreFact, ~400x cheaper — $0.24 vs $107 for 13K checks)** (Tang et al. 2024,
EMNLP), aggregating over the k chunks with SummaC's max operator (Laban et al. 2022, TACL). Corroborate
with **AlignScore (355M)** (Zha et al. 2023, ACL); the two families are complementary (Honovich et al.
2022, NAACL; Fabbri et al. 2022, NAACL).

**Step 4 — Score.** Claim **precision** = supported / (supported + unsupported). For **recall** you need
a denominator that is not the synthetic reference: derive it per question from a **TICK-style checklist
of required sub-answers generated from the question + its source ED pairs** (Cook et al. 2024, arXiv
preprint), or fall back to SAFE's length-capped **recall = min(#supported / K, 1)** with K set to the
median claim count across systems. Report **F1@K** as the headline (Wei et al. 2024, NeurIPS). Also
report **K-Precision** — fraction of answer tokens appearing in the corpus — as a free, zero-model
faithfulness proxy, and swap ROUGE for token-level **Recall**, which correlates with humans at ρ=0.600
versus F1's 0.473 and EM's 0.273 (Adlakha et al. 2024, TACL).

**Why this beats Binary Accuracy.** Binary Accuracy thresholds one GPT-5 label measuring agreement with
a Claude-written reference (W6); F1@K measures agreement with the corpus. It moves the unit of analysis
from ~250 answers to ~250 x 10–30 claims, giving bootstrap CIs and paired tests real power (W4);
precision penalises unsupported additions while K caps the reward for length (W5); and it runs on
non-GPT models, breaking the teacher/judge overlap (W2).

**Cost.** Extraction over 4 systems x 250 answers ≈ 1,000 generations (minutes on one GPU); verifying
~20k claims with MiniCheck-FT5 costs under **$1**. Validate on **~150 human-labelled claims**, reporting
judge–human balanced accuracy/ROC-AUC (Honovich et al. 2022) plus **PPI confidence intervals** (ARES,
Saad-Falcon et al. 2024, NAACL) — a few hours of human effort, and the whole W1/W4 fix.
