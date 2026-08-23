# Agent E — Validity of LLM-generated evaluation sets, multi-hop QA benchmarks, knowledge-injection eval protocols

All PDFs live in `/Users/andreanicastro/Documents/repos/embgen-lit-rev/llm-as-a-judge/claude-papers/`.
All 26 files verified: `head -c 5` == `%PDF-` and size > 50 KB. **Zero broken downloads.**

---

## Workshop CFP

Source: <https://pretrain2posttrain.github.io/call.html> (fetched 2026-08-22; homepage <https://pretrain2posttrain.github.io/> confirms the same framing).

**Workshop:** "Transitioning from Pre-Training to Post-Training" — *First edition · NeurIPS 2026 · Sydney, Australia · December 11, 2026 · Livestreamed & recorded · Non-archival · OpenReview*

### Verbatim facts

| Field | Verbatim text | Source |
|---|---|---|
| **Submission deadline** | "Aug 29 '26 (Anywhere on Earth)" — under *Important dates*, "All deadlines are 11:59 PM Anywhere on Earth (AoE)." | call.html |
| Portal opens | "August 1, 2026 — Submission portal opens" | call.html |
| **Author notification** | "Sep 29 '26 (Anywhere on Earth)" | call.html |
| Workshop day | "December 11, 2026" | call.html |
| **Tracks** | "Short and long papers" | call.html |
| **Format / template** | "NeurIPS style" ("formatted in NeurIPS paper style") | call.html |
| **Page limit** | "**Short papers:** 4–5 pages. **Long papers:** the chosen format's main-conference page limit. Page limits exclude references and appendices for both tracks." | call.html |
| **Archival status** | "Submissions are non-archival; work already published at NeurIPS or other major ML conferences is not eligible." Eligibility row: "No work already published at NeurIPS or other major ML venues" | call.html |
| **Review process** | "Each submission must nominate a reciprocal reviewer, who may be contacted to review if additional reviewers are needed" | call.html |
| Submission portal | "OpenReview submission portal" → <https://openreview.net/group?id=NeurIPS.cc/2026/Workshop/Pre-to-Post> | index.html nav |
| Recording | "All talks will be livestreamed and recorded." | call.html |

**NOT FOUND (do not invent):**
- **Anonymity / double-blind policy** — NOT FOUND. The CFP says nothing about whether submissions are anonymous. Assume nothing; check the OpenReview form.
- **Dual-submission policy for papers under review elsewhere** — NOT FOUND. Only *already published* at NeurIPS/major ML venues is stated as ineligible. Whether concurrent submission to another venue is allowed is unstated.
- **Explicit page count for the long track** — the CFP defers to "the chosen format's main-conference page limit" without naming a number (NeurIPS 2026 main-conference limit would apply; the CFP itself does not state it).
- **Camera-ready deadline** — NOT FOUND.
- **Reviewer count per paper / rebuttal phase** — NOT FOUND.
- **Supplementary material / code policy** — NOT FOUND.

### Full topic list (verbatim headings + descriptions)

> "We solicit theoretical, empirical, and methodological work across the following areas. This list is not exhaustive."

1. **Foundations laid during pre-training** — "How data mixtures, curricula, continued or mid-training, learning-rate decay, and other late-stage pre-training decisions shape downstream capabilities."
2. **The mechanics of post-training** — "Comparisons across supervised fine-tuning, reinforcement learning from human or AI feedback, reinforcement learning with verifiable rewards, and distillation; how these methods sharpen, broaden, suppress, or reorganize capabilities."
3. **The development of model behaviors across training** — "Identifying when alignment, reasoning, instruction following, refusal, persona, and other behaviors emerge during specific stages of post-training, and distinguishing changes created by post-training from capabilities already present after pre-training."
4. **Interactions between pre-training and post-training data** — "How particular pre-training data mixtures, domains, curricula, or objectives make subsequent post-training more or less effective; whether post-training outcomes depend on related knowledge, behaviors, or representations being established during pre-training."
5. **Failure modes and fundamental limits** — "Mode or entropy collapse, reward hacking, capability forgetting, alignment taxes, and theoretical or empirical limits on what post-training can recover or change."
6. **Data and optimization across the training transition** — "Synthetic data, scaling laws for supervised, preference, and reinforcement-learning data, optimizer-state inheritance, learning-rate schedules, regularization, and curriculum design across training stages."
7. **Predicting post-training outcomes from pre-training** — "Developing metrics, representations, or behavioral signals during pre-training that forecast later trainability, alignment, robustness, and capability gains."
8. **Reimagining the training pipeline** — "Folding traditionally post-training data and objectives into pre-training, jointly designing training stages, and allocating data and compute across the full pipeline."
9. **Evaluation and open science** — "Evaluating post-training beyond benchmark improvements through causal experiments, standardized protocols, intermediate checkpoints, and openly reproducible training studies."

**Positioning note for EmbGen.** Topic 6 ("Synthetic data … across training stages") is EmbGen's home topic. Topic 9 ("Evaluation and open science … standardized protocols") is *exactly* the reviewer-facing weakness list W1–W7 — a paper that fixes its own evaluation protocol and reports it transparently is squarely on-topic, not a distraction. The 4–5 page short track is the realistic target; the eval-validity work below should be compressible into ~1 page + appendix (appendices are excluded from the limit).

---

## Annotated bibliography

### Part 1a — LLM-generated / automatically-constructed benchmarks and their validation

**1. Li, Kaiyom, Liu, Mai, Liang, Hashimoto (2025). "AutoBencher: Towards Declarative Benchmark Construction." ICLR 2025.** OpenReview `ymt4crbbXh`; arXiv 2407.08351. → `E_Li2025_AutoBencher_ICLR.pdf`
Casts benchmark construction as an optimisation over dataset *descriptions*, maximising a weighted sum of novelty, difficulty and separability subject to a salience constraint. The critical mechanism for EmbGen is **privileged information**: the evaluator LM generates (question, answer) pairs conditioned on source documents that the *candidate* models never see, so answers are grounded in a reliable source and an information asymmetry makes the questions harder than the generator's own unaided capability. They explicitly name the two failure modes EmbGen inherits — "*Example correctness*: since we use LM_evaluator to construct the dataset, the generated answers might be incorrect due to model hallucination" and "*Example difficulty*". They then **audit with Mechanical Turk**: overall **5% label error rate**, broken out as 3% (math, economics), 6.7% (history), 7.2% (science), and benchmark this against the **1–5% label error rate present in human-constructed datasets** (Chong et al. 2022) — the single most quotable sentence in this whole search. A second MTurk pass collects *salience* labels.
**USE FOR: W6** (justifies LLM-written references by auditing them and comparing to human-dataset error floors); **W4** (gives an error-rate figure to report alongside N=250).

**2. Perez, Ringer, Lukošiūtė, et al. (2023). "Discovering Language Model Behaviors with Model-Written Evaluations." Findings of ACL 2023**, pp. 13387–13434. → `E_Perez2023_ModelWrittenEvaluations_ACL-Findings.pdf`
The canonical peer-reviewed defence of model-written evaluation sets. They generate **154 datasets** and validate them with crowdworkers: "*We have crowdworkers manually validate 100+ examples in each generated dataset. A vast majority of examples are correctly-labeled (e.g., **95.7% of the time over 133 evaluations**), as well as relevant to the evaluation description.*" They also run **head-to-head comparisons between LM-written and human-written versions of the same evaluation**, finding LM-written data "approach the quality of human-written ones, sometimes even exceeding them", while honestly reporting limitations (lower quality for certain labels, and on more complex topics). Their conclusion is the framing EmbGen should adopt: LMs "are not a silver bullet for creating arbitrary evaluations but rather … should be strongly considered before embarking on manual data creation."
**USE FOR: W6, W1.** Gives EmbGen (a) a precedent for a **100-example-per-dataset** human audit — an affordable budget at 250 QA pairs, i.e. a 40% audit rate — and (b) the head-to-head LM-vs-human eval-set design (EmbGen's SQuAD-20 native eval set is exactly such a control).

**3. Zhang, Huang, Ma, Michel, He, Gupta, Ma, Farhadi, Kembhavi, Krishna (2024). "Task Me Anything." NeurIPS 2024 Datasets & Benchmarks Track.** arXiv 2406.11775. → `E_Zhang2024_TaskMeAnything_NeurIPS-DB.pdf`
A *programmatic* benchmark-generation engine: a taxonomy of assets (113K images, 10K videos, 2K 3D assets, 365 object categories, 655 attributes, 335 relationships) is combined with task templates to generate **750M question–answer pairs**, plus algorithms that answer user queries about model performance within a compute budget. **Caveat: this is multimodal (MLM), not text QA**, so it is a methodological citation, not a drop-in benchmark. What EmbGen reuses is the *argument*: when the generator is template/graph-driven rather than free-form, correctness is guaranteed by construction and the eval set can be scaled and sliced on demand. EmbGen's proximity-graph sampling is structurally analogous — worth making explicit.
**USE FOR: W6** (generation-by-construction reduces the hallucinated-reference risk); framing for the "benchmark as a generator, not a fixed set" position.

**4. Wang, Kordi, Mishra, Liu, Smith, Khashabi, Hajishirzi (2023). "Self-Instruct: Aligning Language Models with Self-Generated Instructions." ACL 2023** (`2023.acl-long.754`). → `E_Wang2023_SelfInstruct_ACL.pdf`
The precursor for the whole "LLM writes its own training/eval data" line, and the paper every reviewer expects cited when a pipeline generates instructions from a model. It also contains an under-used artefact: a **human evaluation of the generated data's quality** with a graded error taxonomy (instruction valid / input appropriate / output correct), showing most instructions are meaningful while a sizeable minority of *outputs* contain errors. That decomposition — question is well-posed vs reference answer is correct — is precisely the two-axis audit EmbGen needs.
**USE FOR: W6.** Adopt its error taxonomy verbatim as the audit rubric for the 250-item sets.

### Part 1b — Construct / measurement validity for ML benchmarks

**5. Raji, Bender, Paullada, Denton, Hanna (2021). "AI and the Everything in the Whole Wide World Benchmark." NeurIPS 2021 Datasets & Benchmarks Track.** arXiv 2111.15366. → `E_Raji2021_EverythingWholeWideWorldBenchmark_NeurIPS-DB.pdf`
The standard critique of *construct validity* in ML benchmarks: benchmarks marketed as measuring "general" capability in fact measure a narrow, task-specific, dataset-bound construct, and the gap between the claimed construct and the operationalised measure is rarely argued. For EmbGen the relevant lesson is defensive framing: **do not claim the 250 LLM-generated QA pairs measure "knowledge internalisation" in general** — claim they measure *cross-document recall over this specific corpus*, and say so.
**USE FOR: W6, W7.** Directly supports narrowing the claim and motivates checking whether the four judge dimensions actually correspond to distinct constructs.

**6. Liao, Taori, Raji, Schmidt (2021). "Are We Learning Yet? A Meta-Review of Evaluation Failures Across Machine Learning." NeurIPS 2021 Datasets & Benchmarks Track.** → `E_Liao2021_AreWeLearningYet_NeurIPS-DB.pdf`
Meta-reviews **107 survey papers** across NLP, RecSys, CV, RL, comp-bio and graph learning, and distils a taxonomy of evaluation failure modes organised, following measurement theory, into **internal validity** (does the comparison isolate the claimed cause within the study?) and **external validity** (does the result transfer outside it?). This is the cleanest single citation for structuring EmbGen's own limitations section as a validity argument rather than an apology.
**USE FOR: W4, W5, W6.** Internal validity → the length/verbosity confound (W5) and the missing significance tests (W4) are named failure modes; external validity → motivates adding a human-authored benchmark.

**7. Subramonian, Yuan, Daumé III, Blodgett (2023). "It Takes Two to Tango: Navigating Conceptualizations of NLP Tasks and Measurements of Performance." Findings of ACL 2023** (`2023.findings-acl.202`). → `E_Subramonian2023_ItTakesTwoToTango_ACL-Findings.pdf`
Argues that disagreement about "which metric is right" is usually disagreement about how the *task itself* is conceptualised, and that a metric can only be validated relative to an explicit conceptualisation. Gives EmbGen the vocabulary to say what "Factual Accuracy / Completeness / Relevance / Clarity" are supposed to operationalise, and why the binary composition rule (`FA==Strong AND Completeness ∈ {Strong, Adequate}`) is a *conceptualisation choice* that must be defended, not a neutral aggregation.
**USE FOR: W7, W6.** The paper to cite when justifying (or dropping) the Clarity dimension.

**8. Jacobs & Wallach (2021). "Measurement and Fairness." ACM FAccT 2021.** arXiv 1912.05511. → `E_Jacobs2021_MeasurementAndFairness_FAccT.pdf`
Imports measurement-modelling from the social sciences into ML: unobservable constructs must be linked to observable measurements by an explicit measurement model, then tested for **construct reliability** and **construct validity** (face, content, convergent, discriminant, predictive, hypothesis, consequential). This is the source of the specific tests EmbGen should run: **convergent validity** (do judge scores correlate with lexical metrics / with human labels?) and **discriminant validity** (are the four dimensions distinguishable, or is Clarity redundant?).
**USE FOR: W7 (primary), W1, W6.** One inter-dimension correlation matrix + a sentence naming "discriminant validity" answers W7 at near-zero cost. *Note: FAccT is peer-reviewed ACM; the local PDF is the arXiv version of the same paper.*

**9. Sainz, Campos, García-Ferrero, Etxaniz, de Lacalle, Agirre (2023). "NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark." Findings of EMNLP 2023** (`2023.findings-emnlp.722`). → `E_Sainz2023_DataContaminationEachBenchmark_EMNLP-Findings.pdf`
Position paper: closed-model evaluation is broken because benchmark data leaks into pretraining, and the community must measure and report contamination *per benchmark* rather than assume it away. EmbGen has a specific, mirror-image version of this problem — **the eval set is generated from the same corpus that is used to build the SFT data**, so the eval set is by construction "contaminated" with respect to the training signal (that is the point), but it also means an EmbGen-flavoured question may be distributionally closer to EmbGen's training data than to a baseline's. That is a *fairness-of-comparison* risk, not a leakage risk, and it must be named explicitly.
**USE FOR: W6, W2.** Cite when arguing that the eval-set generator (Claude-Sonnet-4.5) is deliberately *disjoint* from both the teacher (GPT-5 / gpt-4o-mini) and the judge — turn this into a stated design principle.

### Part 1c — Established multi-hop / cross-document QA benchmarks (candidate external controls)

**10. Yang, Qi, Zhang, Bengio, Cohen, Salakhutdinov, Manning (2018). "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering." EMNLP 2018** (`D18-1259`). → `E_Yang2018_HotpotQA_EMNLP.pdf`
**113k** crowd-sourced Wikipedia-based multi-hop QA pairs with **sentence-level supporting facts**, plus comparison questions; distractor and full-wiki settings. The supporting-facts annotation is the useful part for EmbGen: it lets you *verify* that a question needs ≥2 documents by ablating the supporting sentences. Widely known to be partially solvable by shortcuts (see MuSiQue), so cite it as the historical anchor, not the primary control.
**USE FOR: W6** (external human-authored control); the supporting-facts design motivates EmbGen's single-chunk ablation.

**11. Trivedi, Balasubramanian, Khot, Sabharwal (2022). "MuSiQue: Multihop Questions via Single-hop Question Composition." TACL 2022** (`2022.tacl-1.31`). → `E_Trivedi2022_MuSiQue_TACL.pdf`
**The best external control for EmbGen.** Built bottom-up by composing *connected* single-hop questions, with filters explicitly targeting **disconnected reasoning** (answering without actually chaining). **MuSiQue-Ans: 25K 2–4 hop questions**; relative to prior datasets it is "more difficult overall (**3× increase in human–machine gap**), and harder to cheat via disconnected reasoning (**a single-hop model has a 30-point drop in F1**)". **MuSiQue-Full** adds unanswerable contrast questions. The "single-hop model F1 drop" is precisely the diagnostic EmbGen should replicate on its own generated sets.
**USE FOR: W6 (primary external control), and the multi-hop-genuineness ablation.**

**12. Ho, Duong Nguyen, Sugawara, Aizawa (2020). "Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps" (2WikiMultiHopQA). COLING 2020** (`2020.coling-main.580`), pp. 6609–6625. → `E_Ho2020_2WikiMultiHopQA_COLING.pdf`
**192,606** questions built from Wikipedia + Wikidata using templates and logical rules, each annotated with **evidence triples giving the full reasoning path**, average ~12.6 evidence items. The construction pipeline "guarantees the multi-hop steps and the quality of the questions" by design — structurally the closest published analogue to EmbGen's entity-description graph + proximity sampling, and therefore the best citation for "a graph-structured generator can guarantee multi-hop-ness by construction".
**USE FOR: W6.** Methodological precedent for EmbGen's own generator; also a ready external control.

**13. Zhu, Hwang, Dugan, Callison-Burch (2024). "FanOutQA: A Multi-Hop, Multi-Document Question Answering Benchmark for Large Language Models." ACL 2024 (Short)** (`2024.acl-short.2`), pp. 18–37. → `E_Zhu2024_FanOutQA_ACL.pdf`
"Fan-out" questions requiring aggregation over *many* entities: **1,034 top-level questions and 7,305 human-written sub-question decompositions** over English Wikipedia, split 30% dev (310) / 70% test (724), questions paired with up to ~172k tokens of context. Three benchmark settings (closed-book, open-book, evidence-provided) across 7 LLMs incl. GPT-4, LLaMA-2, Claude-2.1, Mixtral-8x7B. The **human-written decompositions** are gold for EmbGen: they are the human-authored analogue of "this question genuinely requires k documents".
**USE FOR: W6.** External control with an explicit multi-document requirement and a closed-book setting matching EmbGen's.

**14. Krishna, Krishna, Mohananey, Schwarcz, Stambler, Upadhyay, Faruqui (2025). "Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation" (FRAMES). NAACL 2025** (`2025.naacl-long.243`), pp. 4745–4759. → `E_Krishna2025_FRAMES_NAACL.pdf`
**824** challenging multi-hop questions requiring integration across multiple Wikipedia sources, evaluating factuality + retrieval + reasoning end-to-end. Baselines: **0.408 accuracy without retrieval**, rising to **0.66 with a multi-step retrieval pipeline (>50% improvement)**. The no-retrieval vs multi-step-retrieval gap is a directly reusable *difficulty certificate*: if a question set is genuinely multi-hop, closed-book accuracy should be far below oracle-context accuracy.
**USE FOR: W6.** Supplies the oracle/closed-book gap metric and a modern, small (824-item) external control comparable in size to EmbGen's 250.

**15. Pang, Parrish, Joshi, Nangia, Phang, Chen, Padmakumar, Ma, Thompson, He, Bowman (2022). "QuALITY: Question Answering with Long Input Texts, Yes!" NAACL 2022** (`2022.naacl-main.391`), pp. 5336–5358. → `E_Pang2022_QuALITY_NAACL.pdf`
Multiple-choice QA over passages averaging **~5,000 tokens**, written *and validated* by annotators who read the whole passage. Crucially, **"only half of the questions are answerable by annotators working under tight time constraints"** — an explicit, quantified guarantee that skimming/search is insufficient. Baselines **55.4%** vs human **93.5%**. This is the corpus EntiGraph uses, so it is also the direct comparability bridge to EmbGen's closest baseline.
**USE FOR: W6, W4.** The time-constrained-annotator design is a cheap, citable way to certify that questions need real reading; the 93.5% human ceiling is the kind of number EmbGen currently lacks entirely.

**16. Bai, Tu, Zhang, Wu, Wen, Lai, et al. (2025). "LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks." ACL 2025** (`2025.acl-long.183`), pp. 3639–3664. → `E_Bai2025_LongBenchV2_ACL.pdf`
The recent (2024–2026) long-context/cross-document control the brief asked for. **503 multiple-choice questions**, contexts from **8k to 2M words**, six categories including **multi-document QA**; data from ~100 highly educated annotators with both automated and manual review. Human experts reach only **53.7% under a 15-minute constraint**; best direct-answering model **50.1%**; o1-preview **57.7%**. Its MCQ format makes judge-free scoring possible, which sidesteps W1–W3 entirely on that slice.
**USE FOR: W6, W1.** A modern external control that requires *no LLM judge at all* — the cleanest possible rebuttal to "your metric is an LLM".

### Part 1d — Knowledge-injection / domain-adaptation evaluation protocols

**17. Yang, Band, Li, Candès, Hashimoto (2025). "Synthetic Continued Pretraining" (EntiGraph). ICLR 2025.** arXiv 2409.07431. → `E_Yang2025_EntiGraph_ICLR.pdf`
EmbGen's closest baseline; **read their eval protocol carefully because it is the community norm EmbGen is being judged against.** Corpus = **QuALITY, 265 articles/short books, ~5,000 tokens each, 1.3M tokens total**, synthesised up to **455M tokens**. Test set = the **10–20 human-written MCQs per article, "contextualized"** by prefixing "In the context of article {name} by {author}…" to remove reading-comprehension presupposition → **4,609 unambiguous queries**. Scoring = **4-choice single-answer accuracy, 5-shot chain-of-thought — no LLM judge, no human judging needed.** Results: Llama-3-8B-Base 39.49% → EntiGraph CPT **56.22%** (log-linear in synthetic tokens); Raw CPT 38.15% (worse than base); GPT-3.5 44.81%, GPT-4 51.30% closed-book. **Corpus-obscurity check:** GPT-3.5 72.60% / GPT-4 86.09% *open-book* vs 44.81/51.30 closed-book — the ~30-point gap is used to argue the corpus is niche enough to be a valid testbed. **Open-ended eval (§4.3):** closed-book summarisation scored by an **automated pyramid-style claim metric** — GPT-4 (1) splits the summary into atomic claims, (2) judges each true/false, (3) judges whether true claims are salient — then **normalises counts of false and salient claims by the corresponding counts from the human-written summary**. **RAG control (§5):** EntiGraph CPT + RAG 62.60% (Recall@8 99.63) vs Llama-3-8B + RAG 60.35%, with **GPT-4 + Oracle RAG 86.09%** as a perfect-retriever upper bound. **They report no human validation of the GPT-4 claim judge and no confidence intervals.**
**USE FOR: W1, W4, W6.** Three concrete transplants: (a) the **contextualisation trick** for de-ambiguating generated questions; (b) **claim-level pyramid scoring normalised to a reference**, which converts "agreement with an LLM reference" into "count of atomic claims", partially defusing W6; (c) the **oracle-RAG upper bound**, which is EmbGen's single-chunk/oracle-context control.

**18. Ovadia, Brief, Mishaeli, Elisha (2024). "Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs." EMNLP 2024** (`2024.emnlp-main.15`), pp. 237–250. → `E_Ovadia2024_FineTuningOrRetrieval_EMNLP.pdf`
Two eval families: (i) selected **MMLU** subject sets (anatomy, astronomy, college biology, prehistory) to avoid single-domain overfitting; (ii) a purpose-built **"current events"** task over Wikipedia articles from **Aug–Nov 2023**, i.e. strictly *after* the models' cutoffs, so the injected knowledge is provably new. **Eval-set construction is the direct precedent for EmbGen:** GPT-4 was prompted to write four highly specific single-answer MCQs per chunk, then to select the two most specific, **"followed by a manual evaluation and verification step. In total, this resulted in 910 new questions."** Scoring = **log-likelihood MCQ accuracy** (append each option, take argmax log-prob) via **LM-Evaluation-Harness** — deterministic, judge-free, reproducible. They also generate paraphrase augmentations (240 chunks × 2 paraphrases held out as a hyperparameter-tuning validation set).
**USE FOR: W6 (primary), W1, W2.** This is the peer-reviewed EMNLP citation for "LLM-generated eval set + human verification pass" — exactly the protocol EmbGen should adopt and cite.

**19. Ovadia, Brief, Lemberg, Sheetrit (2025). "Knowledge-Instruct: Effective Continual Pre-training from Limited Data using Instructions." arXiv 2504.05571** — *arXiv-only; flagged. Canonical because it is a named EmbGen baseline.* → `E_Ovadia2025_KnowledgeInstruct_arXiv.pdf`
Three eval corpora: **Companies** (23 *entirely fictional* companies generated by GPT-4o — guarantees zero prior knowledge), **PopQA** long-tail subset, and **MultiHop-RAG** (an existing external multi-hop benchmark). Deliberately **open-ended questions only, "to avoid any guessing that multiple choice questions may enable."** Scoring = **LLM-as-a-Judge (GPT-4o)** using the judge and prompt of Brief et al. (2024), on a **{0,1,2} scale, binarised: correct only if it scores a strict 2**, normalised by dividing by two. **No human validation of the judge is reported.** Two design details EmbGen should steal: the **PopQA filtering rule** — keep only questions GPT-4o answers correctly *when given the relevant Wikipedia article*, yielding **1,935 verified pairs** (an automated answerability guarantee); and an explicit **"Oracle" condition** (relevant ground-truth documents in context) reported as a separate column, plus a Table-3 **Oracle-vs-Reconstruct gap** (PopQA 99.0 vs 97.1, gap 1.9; Companies 98.4 vs 95.5, gap 2.9). General-capability regression is checked on MMLU / MMLU-Pro / TriviaQA / GSM8K via LM-Evaluation-Harness.
**USE FOR: W6, W1, W3.** The **oracle-answerability filter** is the cheapest possible defence of a generated eval set and can be run over all 250 items automatically before any human audit.

**20. Sudalairaj, Bhandwaldar, Pareja, Xu, Cox, Padhi (2024). "LAB: Large-Scale Alignment for ChatBots" (InstructLab). arXiv 2403.01081** — *arXiv-only; flagged. Canonical because it is a named EmbGen baseline and the basis of InstructLab.* → `E_Sudalairaj2024_LAB_InstructLab_arXiv.pdf`
Taxonomy-driven synthetic generation (1.2M samples: 617k knowledge + 588k skills) with a **teacher-as-evaluator filtering stage** — the teacher model is repurposed to score each generated instruction and each instruction–response pair against a rubric and drop failures. Evaluation is entirely **off-the-shelf general benchmarks**: **MT-Bench** (GPT-4 judge, 1–10, "average of 3 runs"), MMLU, ARC, HellaSwag, Winogrande, GSM8K. MERLINITE-7B: MT-Bench **7.66**, MMLU **64.88**; LABRADORITE-13B: MT-Bench **7.23**, MMLU 58.89. Comparison numbers for other models are "taken from the LMSYS Chatbot Arena Leaderboard". **No corpus-specific eval set, no human validation of the MT-Bench judge.**
**USE FOR: W3, W1.** Note the "average of 3 runs" convention — LAB reports repeated judge runs *at nonzero temperature*, which is the meaningful version of what EmbGen does with temperature 0 × 10 runs (W3). Also the strongest evidence that the community norm in this subfield is *no judge validation at all* — EmbGen doing any validation is above norm.

**21. Mecklenburg, Lin, Chen, Yang, Byun, et al. (2024). "Injecting New Knowledge into Large Language Models via Supervised Fine-tuning." arXiv 2404.00213** — *arXiv-only; flagged.* → `E_Mecklenburg2024_InjectingNewKnowledgeSFT_arXiv.pdf`
Compares **token-based** vs **fact-based** (atomic-fact-decomposed) QA dataset generation on six recent-sporting-event documents, fine-tuning GPT-4 with LoRA. Eval sets are generated by the **same procedure as the training sets, at 1× token scale**, and correctness is assessed by **querying GPT-4 for a binary judgement** — no human validation. Two reusable controls: (a) a **contamination sanity check** — the pre-cutoff 2018 FIFA World Cup document yields base-model accuracy **0.712** vs a **maximum of 0.242** for the five post-cutoff documents, proving the other corpora are genuinely out-of-domain; (b) a **RAG baseline** reported purely to contextualise (SFT lands within 16% of RAG). Fact-based generation beats token-based; 10× token scaling shows diminishing/negative returns attributed to lack of question diversity.
**USE FOR: W6, W2.** The base-model-accuracy sanity check is a two-line experiment that tells a reviewer the eval set is not answerable from Llama-3-8B's priors — EmbGen's "no-augmentation" baseline already gives this number, it just needs to be *framed* as a corpus-obscurity certificate.

**22. Allen-Zhu & Li (2024). "Physics of Language Models: Part 3.1, Knowledge Storage and Extraction." ICML 2024**, PMLR 235:1067–1077. → `E_AllenZhu2024_PhysicsLM3-1_KnowledgeStorageExtraction_ICML.pdf`
Controlled synthetic-biography experiments showing a **strong correlation between knowledge *extractability* and diversity measures of the training data**: knowledge must be sufficiently augmented (paraphrasing, sentence shuffling, entity permutation) *during pretraining* to become extractable; without augmentation it is memorised but **0% extractable**, and no amount of downstream instruction fine-tuning recovers it. This is the theoretical justification for EmbGen's entire premise (rewriting a corpus into diverse forms), and it also warns that **the form of the eval question matters as much as the fact** — an eval set written in one style measures extraction-in-that-style.
**USE FOR: W6, W5.** Motivates asking the same fact in ≥2 surface forms as a robustness check, which doubles as a verbosity/style control.

**23. Allen-Zhu & Li (2025). "Physics of Language Models: Part 3.2, Knowledge Manipulation." ICLR 2025.** arXiv 2309.14402. → `E_AllenZhu2025_PhysicsLM3-2_KnowledgeManipulation_ICLR.pdf`
Studies four manipulation tasks — retrieval, classification, comparison, inverse search. Models excel at **retrieval** but fail at classification/comparison **unless chain-of-thought is used at both training and inference time**, and inverse search is **~0%**. Direct implication for EmbGen: multi-hop/cross-document questions are *manipulation*, not retrieval, so measured gains are bounded by a known architectural limitation, and prompting format (CoT or not) will move the numbers substantially. EmbGen must report its inference prompt format and, ideally, ablate CoT.
**USE FOR: W6, W4.** Explains why absolute accuracies are low (0.068 vs 0.036) without conceding the comparison is meaningless — and argues for a CoT-vs-direct ablation.

### Part 1e — Synthetic data quality / diversity evaluation (data-side analysis)

**24. Li, Zhang, He, Li, Chen, Sun, et al. (2024). "From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selection for Instruction Tuning" (Cherry LLM / IFD). NAACL 2024** (`2024.naacl-long.421`). → `E_Li2024_IFD_CherryLLM_NAACL.pdf`
Introduces the **Instruction-Following Difficulty (IFD)** score — the ratio of the model's loss on a response given its instruction to its loss on the response alone — as a self-guided, reference-free measure of how much an instruction actually *teaches*. High-IFD "cherry" samples let a model trained on a small fraction of the data match or beat full-data training.
**USE FOR:** data-side analysis (a new contribution, not a W-fix). EmbGen can compute IFD over its generated SFT data and over the baselines' data, giving a **model-independent quality comparison** that does not route through the judge at all — a strong answer to "your only evidence is an LLM judge."

**25. Chen, Li, Yan, Wang, Gunaratna, Yadav, Tang, Srinivasan, Zhou, Huang, Jin (2024). "AlpaGasus: Training a Better Alpaca with Fewer Data." ICLR 2024.** arXiv 2307.08701. → `E_Chen2024_AlpaGasus_ICLR.pdf`
Uses a strong LLM (ChatGPT) to score and filter instruction data, keeping **9k of Alpaca's 52k** and beating the full-data model. Establishes the peer-reviewed precedent for **LLM-based quality filtering of synthetic SFT data**, and — importantly for EmbGen — documents that widely used synthetic IFT sets "contain many low-quality instances with incorrect or irrelevant responses."
**USE FOR: W6.** Precedent for adding an automated quality-filter stage to EmbGen's generator *and* to its eval-set generator; also honest evidence that unfiltered LLM output has a nontrivial error rate.

**26. Chen, Waheed, Li, Wang, Wang, Raj, Abdin (2024). "On the Diversity of Synthetic Data and its Impact on Training Large Language Models." arXiv 2410.15226** — *arXiv-only; flagged (preprint).* → `E_Chen2024_DiversitySyntheticData_arXiv.pdf`
Introduces the **LLM cluster-agent** diversity metric for synthetic corpora and shows, in controlled 350M and 1.4B-parameter experiments, that this cluster-based diversity score **correlates positively with both pre-training and supervised fine-tuning performance**, and that pre-training diversity has an outsized effect on later SFT. EmbGen is *literally a clustering pipeline* (UMAP + KMeans/HDBSCAN), so it can compute this metric almost for free and turn its clustering machinery into an explanatory variable.
**USE FOR:** data-side analysis. Lets EmbGen argue *why* it wins (higher generated-data diversity) rather than only *that* it wins, which is the more robust claim when N=250.

---

## How the closest prior work evaluates

The community norm in EmbGen's own subfield. This table is the single most useful artefact from this search: it shows **not one of the four closest baselines validates its judge against humans, and not one reports confidence intervals.**

| | **EntiGraph** (Yang et al., ICLR 2025) | **InstructLab / LAB** (Sudalairaj et al., arXiv 2024) | **Knowledge-Instruct** (Ovadia et al., arXiv 2025) | **Ovadia et al.** (EMNLP 2024) |
|---|---|---|---|---|
| **Primary metric** | 4-choice MCQ accuracy, 5-shot CoT | MT-Bench score (1–10); MMLU/ARC/HellaSwag/Winogrande/GSM8K accuracy | Binary correctness from a {0,1,2} judge score, strict-2 = correct | Log-likelihood MCQ accuracy (argmax over appended options) |
| **Eval set** | QuALITY's own **human-written** 10–20 MCQs/article, "contextualized" → **4,609 queries** | Off-the-shelf public benchmarks only; **no corpus-specific eval set** | Companies (synthetic, 23 fictional firms), PopQA long-tail (**1,935** filtered pairs), **MultiHop-RAG** (external) | Selected MMLU subjects + purpose-built "current events" set: **910** GPT-4-written MCQs |
| **Who wrote the eval questions** | Humans (QuALITY crowdworkers) | Humans (benchmark authors) | GPT-4o (Companies); humans (PopQA); pipeline (MultiHop-RAG) | **GPT-4**, 4 generated per chunk → 2 selected |
| **Human verification of the eval set** | N/A (inherited human benchmark) | N/A | **No** human pass; instead an **automated oracle filter** (keep only items GPT-4o answers correctly given the source article) | **Yes** — "followed by a manual evaluation and verification step" (rate/annotator count not reported) |
| **LLM judge used?** | Only for the open-ended summarisation eval: **GPT-4 atomic-claim decomposition + truth + salience**, normalised to a human summary | **Yes** — MT-Bench GPT-4 judge, "average of 3 runs" | **Yes** — GPT-4o, judge/prompt from Brief et al. (2024) | **No** — deterministic log-prob scoring via LM-Evaluation-Harness |
| **Judge validated against humans?** | **No** | **No** | **No** | N/A (no judge) |
| **Repeated judge runs / variance?** | Not reported | 3 runs averaged (no variance reported) | Not reported | Deterministic |
| **Confidence intervals / significance tests** | **None** | **None** | **None** | **None** |
| **Contamination / obscurity control** | **Yes** — GPT-3.5/GPT-4 closed-book (44.81 / 51.30) vs open-book (72.60 / 86.09); ~30-pt gap argues corpus is niche | No | Yes — fictional companies; long-tail PopQA filter (popularity sum < 2500) | **Yes** — events strictly after model cutoffs (Aug–Nov 2023) |
| **Oracle-context / retrieval control** | **Yes** — RAG (62.60 w/ EntiGraph vs 60.35 base, Recall@8 99.63) and **GPT-4 + Oracle RAG 86.09** as upper bound | No | **Yes** — explicit "Oracle" column; Oracle-vs-Reconstruct gap table (99.0/97.1; 98.4/95.5) | Implicitly via RAG arm |
| **General-capability regression check** | Not central | Yes (6 benchmarks) | **Yes** — MMLU, MMLU-Pro, TriviaQA, GSM8K via LM-Eval-Harness | Yes (MMLU) |
| **Headline number** | 39.49% → **56.22%** (455M synthetic tokens) | MERLINITE-7B MT-Bench **7.66**, MMLU **64.88** | >80% accuracy on Companies; largest gaps on MultiHop-RAG | RAG consistently > unsupervised fine-tuning |

**What this means for the paper.** (1) EmbGen's reviewers cannot demand a standard EmbGen fails to meet without also indicting all four baselines — but the *reviewer will still ask*, so the cheap wins below are worth taking. (2) Three of four use **judge-free or MCQ-based scoring** on at least one eval slice; EmbGen uses an LLM judge on *every* slice, which is its genuine outlier property and its biggest exposure. (3) **Three of four run an obscurity/contamination control and two run an oracle-context control** — these are the norms EmbGen is currently *missing*, and they are far cheaper than human annotation.

---

## Recommended eval-set validity protocol for EmbGen

**1. Run the automated answerability filter first (zero human cost, whole set).** Following Knowledge-Instruct, re-ask every one of the 250 questions to a *third* model (not the teacher, not the judge) **with the source chunks in context** and keep only items it answers correctly against the reference. Report the pass rate as an **oracle-answerability rate**; Knowledge-Instruct's comparable Oracle scores are 99.0 (PopQA) and 98.4 (Companies), so anything below ~90% is itself a finding. Items that fail are either unanswerable or have a wrong reference — either way they should be excised or flagged, and the filtered set becomes the headline eval set with the unfiltered result reported in an appendix.

**2. Human spot-check with a two-axis rubric and a reported audit rate.** Audit a stratified random sample — **100 of 250 per corpus (40% audit rate)**, matching Perez et al.'s "100+ examples in each generated dataset". Two independent binary judgements per item, borrowed from Self-Instruct's taxonomy: **(a) is the question well-posed and answerable from the corpus?** and **(b) is the LLM-written reference answer correct and complete?** Report both rates with Wilson intervals, and **benchmark them against AutoBencher's 5% label-error rate and the 1–5% error rate of human-constructed datasets** — that comparison is the whole rhetorical move. Two annotators on ~30 overlapping items gives a Cohen's κ for the audit itself at trivial cost.

**3. Add one external, human-authored multi-hop control — yes, do this.** It is the highest-leverage single addition. Priority order: **MuSiQue-Ans** (built explicitly against disconnected reasoning; 25K 2–4 hop) or **LongBench v2** (503 MCQs, judge-free scoring, contains a multi-document QA category). A ~200–500 item subset is enough. This converts "your benchmark is circular" into "our benchmark agrees with an independent human-authored one", and LongBench v2's MCQ format lets EmbGen report *one number that involves no LLM judge at all*.

**4. Prove the questions genuinely need multiple documents — three ablations, all cheap.**
- **Single-chunk ablation:** answer each question with only the single highest-similarity chunk in context. If accuracy barely drops, the question was never multi-hop. This is MuSiQue's "single-hop model drops 30 F1" diagnostic, transplanted.
- **Oracle-context ceiling:** answer with *all* gold chunks in context (EntiGraph's GPT-4 + Oracle RAG = 86.09%; FRAMES: 0.408 no-retrieval → 0.66 multi-step). The closed-book-to-oracle gap is the difficulty certificate.
- **Corpus-obscurity floor:** report base Llama-3-8B-Instruct accuracy on each eval set as a contamination check — EmbGen's existing no-augmentation baseline *is* this number; reframe it as Mecklenburg et al. do (0.712 pre-cutoff vs ≤0.242 post-cutoff).

**5. State the construct narrowly.** Following Raji et al. and Liao et al., claim the sets measure *cross-document factual recall over this specific corpus*, not "knowledge internalisation". And per Jacobs & Wallach, report the **inter-dimension correlation matrix** for the four judge dimensions as a discriminant-validity check — one table, and W7 is answered.
