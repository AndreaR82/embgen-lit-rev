# Paper manifest

Every paper in this repository, with a link to its canonical source.

**The `no-pdfs` branch does not contain the PDF files** — it holds the notes, the methodology document and the code only, so it clones in seconds inside a restricted environment. Use this manifest (or `fetch_papers.sh`) to obtain the PDFs on a machine that can reach the open web.

Detailed annotations for every paper — what it says and what EmbGen should take from it — are in [`claude-papers/notes/`](claude-papers/notes/).


## How to get the PDFs

```bash
# downloads all 110 search-collected papers into ./claude-papers/
bash claude-papers/fetch_papers.sh
```

The script skips files that already exist, sleeps between requests, and verifies each download is a real PDF. **Run it twice** — a few requests get transiently rate-limited on the first pass and succeed on the second. Four papers are behind publisher paywalls and are listed at the end for manual retrieval.


---

## Manually gathered — `llm-as-a-judge/papers/`

| Paper | Venue | Link |
|---|---|---|
| EmbGen: Teaching with Reassembled Corpora | arXiv preprint 2026 | [source](https://arxiv.org/abs/2605.19394) |
| Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | NeurIPS 2023 D&B | [source](https://arxiv.org/abs/2306.05685) |
| A Survey on LLM-as-a-Judge | arXiv preprint | [source](https://arxiv.org/abs/2411.15594) |
| A survey on LLM-as-a-judge (journal version) | The Innovation 2026 | [source](https://doi.org/10.1016/j.xinn.2025.101253) |
| An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability | arXiv 2025 | [source](https://arxiv.org/abs/2506.13639) |
| Explicit Reasoning Makes Better Judges: A Systematic Study on Accuracy, Efficiency, and Robustness | arXiv 2025 | [source](https://arxiv.org/abs/2509.13332) |
| From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge | EMNLP 2025, pp. 2757–2791 | [source](https://scholar.google.com/scholar?q=From+Generation+to+Judgment%3A+Opportunities+and+Challenges+of+LLM-as-a-judge) |
| Training an LLM-as-a-Judge Model: Pipeline, Insights, and Practical Lessons (Themis) | WWW 2025 | [source](https://arxiv.org/abs/2502.02988) |
| When the Judge Changes, So Does the Measurement: Auditing LLM-as-Judge Reliability | arXiv 2026 | [source](https://arxiv.org/abs/2607.08535) |

---

## Literature search — `llm-as-a-judge/claude-papers/`

110 papers across five research fronts. Filenames are prefixed `A_`–`E_` by front.


### A — Judge–human agreement (validating a judge)

*Annotated in [`notes/A-*.md`](claude-papers/notes/)* · 20 papers

| # | Paper | Venue | Link |
|---|---|---|---|
| 1 | RethinkingAgreementHumanEvaluation | COLING 2018 | [source](https://aclanthology.org/C18-1281/) |
| 2 | TruthIsALie | AIMagazine 2015 | [source](https://doi.org/10.1609/aimag) |
| 3 | InterCoderAgreement | ComputationalLinguistics 2008 | [source](https://aclanthology.org/J08-4004/) |
| 4 | LLMsInsteadOfHumanJudges | ACL 2025 | [source](https://arxiv.org/abs/2406.18403) |
| 5 | ReproducibilityCrisisHumanEval | ACL Findings 2023 | [source](https://aclanthology.org/2023.findings-acl.226/) |
| 6 | AlternativeAnnotatorTest | ACL 2025 | [source](https://arxiv.org/abs/2501.10970) |
| 7 | HumansOrLLMsAsTheJudge | EMNLP 2024 | [source](https://arxiv.org/abs/2402.10669) |
| 8 | FBIBlindSpots | EMNLP 2024 | [source](https://arxiv.org/abs/2406.13439) |
| 9 | LimitsScalableEvaluation | ICLR 2025 | [source](https://arxiv.org/abs/2410.13341) |
| 10 | JuStRank | ACL 2025 | [source](https://arxiv.org/abs/2412.09569) |
| 11 | TwentyYearsConfusingHumanEvaluation | INLG 2020 | [source](https://aclanthology.org/2020.inlg-1.23/) |
| 12 | TrustOrEscalate | ICLR 2025 | [source](https://arxiv.org/abs/2407.18370) |
| 13 | EvaluatingOpenDomainQA | ACL 2023 | [source](https://arxiv.org/abs/2305.06984) |
| 14 | RewardBench | NAACL Findings 2025 | [source](https://arxiv.org/abs/2403.13787) |
| 15 | Problem | EMNLP 2022 | [source](https://arxiv.org/abs/2211.02570) |
| 16 | WhoValidatesTheValidators | UIST 2024 | [source](https://arxiv.org/abs/2404.12272) |
| 17 | JudgeBench | ICLR 2025 | [source](https://arxiv.org/abs/2410.12784) |
| 18 | JudgingTheJudges | GEM Workshop ACL 2025 | [source](https://arxiv.org/abs/2406.12624) |
| 19 | LLMBar | ICLR 2024 | [source](https://arxiv.org/abs/2310.07641) |
| 20 | BestPracticesHumanEvaluation | INLG 2019 | [source](https://aclanthology.org/W19-8643/) |

### B — Judge bias (self-preference, leakage, verbosity)

*Annotated in [`notes/B-*.md`](claude-papers/notes/)* · 16 papers

| # | Paper | Venue | Link |
|---|---|---|---|
| 1 | ChatEval | ICLR 2024 | [source](https://arxiv.org/abs/2308.07201) |
| 2 | LengthControlledAlpacaEval | COLM 2024 | [source](https://arxiv.org/abs/2404.04475) |
| 3 | CoBBLEr | Findings ACL 2024 | [source](https://arxiv.org/abs/2309.17012) |
| 4 | PreferenceLeakage | ICLR 2026 | [source](https://arxiv.org/abs/2502.01534) |
| 5 | PairwisePreferenceJudges | COLM 2024 | [source](https://arxiv.org/abs/2403.16950) |
| 6 | SelfPreference | NeurIPS 2024 | [source](https://arxiv.org/abs/2404.13076) |
| 7 | OffsetBias | Findings EMNLP 2024 | [source](https://arxiv.org/abs/2407.06551) |
| 8 | VerbosityBias | arXiv 2023 | [source](https://arxiv.org/abs/2310.10076) |
| 9 | PositionBiasJudges | AACL 2025 | [source](https://arxiv.org/abs/2406.07791) |
| 10 | LengthCorrelationsRLHF | COLM 2024 | [source](https://arxiv.org/abs/2310.03716) |
| 11 | PanelOfLLMEvaluators | arXiv 2024 | [source](https://arxiv.org/abs/2404.18796) |
| 12 | NotFairEvaluators | ACL 2024 | [source](https://arxiv.org/abs/2305.17926) |
| 13 | SelfPreferenceBias | NeurIPSWorkshop 2024 | [source](https://arxiv.org/abs/2410.21819) |
| 14 | StyleOverSubstance | COLING 2025 | [source](https://arxiv.org/abs/2307.03025) |
| 15 | PridePrejudiceSelfBias | ACL 2024 | [source](https://arxiv.org/abs/2402.11436) |
| 16 | JusticeOrPrejudice | ICLR 2025 | [source](https://arxiv.org/abs/2410.02736) |

### C — Statistical rigour (CIs, paired tests, PPI)

*Annotated in [`notes/C-*.md`](claude-papers/notes/)* · 25 papers

| # | Paper | Venue | Link |
|---|---|---|---|
| 1 | PPI++: Efficient Prediction-Powered Inference | arXiv 2023 | [source](https://arxiv.org/abs/2311.01453) |
| 2 | Prediction-Powered Inference | Science 2023 | [source](https://arxiv.org/abs/2301.09633) |
| 3 | An Empirical Investigation of Statistical Significance in NLP | EMNLP 2012 | [source](https://aclanthology.org/D12-1091/) |
| 4 | Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints | ICML 2025 | [source](https://arxiv.org/abs/2503.01747) |
| 5 | AutoEval Done Right: Using Synthetic Data for Model Evaluation | ICML 2025 | [source](https://arxiv.org/abs/2403.07008) |
| 6 | Interval Estimation for a Binomial Proportion | StatSci 2001 | [source](https://doi.org/10.1214/ss/1009213286) |
| 7 | With Little Power Comes Great Responsibility | EMNLP 2020 | [source](https://aclanthology.org/2020.emnlp-main.745/) |
| 8 | The Price of Debiasing Automatic Metrics in Natural Language Evaluation | ACL 2018 | [source](https://aclanthology.org/P18-1060/) |
| 9 | Efficient Inference for Noisy LLM-as-a-Judge Evaluation | arXiv 2026 | [source](https://arxiv.org/abs/2601.05420) |
| 10 | Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference | ICML 2024 | [source](https://arxiv.org/abs/2403.04132) |
| 11 | Statistical Comparisons of Classifiers over Multiple Data Sets | JMLR 2006 | [source](https://www.jmlr.org/papers/v7/demsar06a.html) |
| 12 | A Statistical Analysis of Summarization Evaluation Metrics Using Resampling Methods | TACL 2021 | [source](https://aclanthology.org/2021.tacl-1.67/) |
| 13 | Re-Examining System-Level Correlations of Automatic Summarization Evaluation Metrics | NAACL 2022 | [source](https://aclanthology.org/2022.naacl-main.442/) |
| 14 | Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms | NeuralComp 1998 | [source](https://doi.org/10.1162/089976698300017197) |
| 15 | Replicability Analysis for Natural Language Processing: Testing Significance with Multiple Datasets | TACL 2017 | [source](https://aclanthology.org/Q17-1033/) |
| 16 | The Hitchhiker's Guide to Testing Statistical Significance in NLP | ACL 2018 | [source](https://aclanthology.org/P18-1128/) |
| 17 | Regression for the Mean: Auto-Evaluation and Inference with Few Labels through Post-hoc Regression | ICML 2025 | [source](https://arxiv.org/abs/2411.12665) |
| 18 | Statistical Significance Tests for Machine Translation Evaluation | EMNLP 2004 | [source](https://aclanthology.org/W04-3250/) |
| 19 | Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations | arXiv 2024 | [source](https://arxiv.org/abs/2411.00640) |
| 20 | Benchmark Agreement Testing Done Right: A Guide for LLM Benchmark Evaluation | NeurIPS2025ws | [source](https://arxiv.org/abs/2407.13696) |
| 21 | tinyBenchmarks: evaluating LLMs with fewer examples | ICML 2024 | [source](https://arxiv.org/abs/2402.14992) |
| 22 | Exploring LLM Autoscoring Reliability in Large-Scale Writing Assessments Using Generalizability Theory | arXiv 2025 | [source](https://arxiv.org/abs/2507.19980) |
| 23 | Large Language Models are Inconsistent and Biased Evaluators | arXiv 2024 | [source](https://arxiv.org/abs/2405.01724) |
| 24 | Active Statistical Inference | ICML 2024 | [source](https://arxiv.org/abs/2403.03208) |
| 25 | Cross-Prediction-Powered Inference | PNAS 2024 | [source](https://arxiv.org/abs/2309.16598) |

### D — Claim-level factuality (atomic-claim verification)

*Annotated in [`notes/D-*.md`](claude-papers/notes/)* · 23 papers

| # | Paper | Venue | Link |
|---|---|---|---|
| 1 | CorrectnessFaithfulnessQA | TACL 2024 | [source](https://aclanthology.org/2024.tacl-1.38/) |
| 2 | TICK | arXiv 2024 | [source](https://arxiv.org/abs/2410.03608) |
| 3 | RAGAS | EACL Demo 2024 | [source](https://aclanthology.org/2024.eacl-demo.16/) |
| 4 | QAFactEval | NAACL 2022 | [source](https://aclanthology.org/2022.naacl-main.187/) |
| 5 | FineTuningNewKnowledge | EMNLP 2024 | [source](https://arxiv.org/abs/2405.05904) |
| 6 | MolecularFacts | EMNLP Findings 2024 | [source](https://arxiv.org/abs/2406.20079) |
| 7 | TRUE | NAACL 2022 | [source](https://aclanthology.org/2022.naacl-main.287/) |
| 8 | Prometheus2 | EMNLP 2024 | [source](https://arxiv.org/abs/2405.01535) |
| 9 | Prometheus | ICLR 2024 | [source](https://arxiv.org/abs/2310.08491) |
| 10 | BiGGenBench | NAACL 2025 | [source](https://arxiv.org/abs/2406.05761) |
| 11 | HurdlesLongFormQA | NAACL 2021 | [source](https://aclanthology.org/2021.naacl-main.393/) |
| 12 | SummaC | TACL 2022 | [source](https://aclanthology.org/2022.tacl-1.10/) |
| 13 | HaluEval | EMNLP 2023 | [source](https://arxiv.org/abs/2305.11747) |
| 14 | GEval | EMNLP 2023 | [source](https://arxiv.org/abs/2303.16634) |
| 15 | FActScore | EMNLP 2023 | [source](https://arxiv.org/abs/2305.14251) |
| 16 | ARES | NAACL 2024 | [source](https://aclanthology.org/2024.naacl-long.20/) |
| 17 | VeriScore | EMNLP Findings 2024 | [source](https://arxiv.org/abs/2406.19276) |
| 18 | MiniCheck | EMNLP 2024 | [source](https://arxiv.org/abs/2404.10774) |
| 19 | ClaimDecomposition | StarSEM 2024 | [source](https://arxiv.org/abs/2403.11903) |
| 20 | LongFormFactuality | NeurIPS 2024 | [source](https://arxiv.org/abs/2403.18802) |
| 21 | CriticalEvalLongFormQA | ACL 2023 | [source](https://aclanthology.org/2023.acl-long.181/) |
| 22 | FLASK | ICLR 2024 | [source](https://arxiv.org/abs/2307.10928) |
| 23 | AlignScore | ACL 2023 | [source](https://arxiv.org/abs/2305.16739) |

### E — Eval-set validity, multi-hop controls, prior work

*Annotated in [`notes/E-*.md`](claude-papers/notes/)* · 26 papers

| # | Paper | Venue | Link |
|---|---|---|---|
| 1 | Physics of Language Models: Part 3.1, Knowledge Storage and Extraction | ICML 2024 | [source](https://arxiv.org/abs/2309.14316) |
| 2 | Physics of Language Models: Part 3.2, Knowledge Manipulation | ICLR 2025 | [source](https://arxiv.org/abs/2309.14402) |
| 3 | LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks | ACL 2025 | [source](https://aclanthology.org/2025.acl-long.183/) |
| 4 | AlpaGasus: Training a Better Alpaca with Fewer Data | ICLR 2024 | [source](https://arxiv.org/abs/2307.08701) |
| 5 | On the Diversity of Synthetic Data and its Impact on Training Large Language Models | arXiv 2024 | [source](https://arxiv.org/abs/2410.15226) |
| 6 | Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps | COLING 2020 | [source](https://aclanthology.org/2020.coling-main.580/) |
| 7 | Measurement and Fairness | FAccT 2021 | [source](https://arxiv.org/abs/1912.05511) |
| 8 | Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation | NAACL 2025 | [source](https://aclanthology.org/2025.naacl-long.243/) |
| 9 | From Quantity to Quality: Boosting LLM Performance with Self-Guided Data Selection for Instruction Tuning | NAACL 2024 | [source](https://aclanthology.org/2024.naacl-long.421/) |
| 10 | AutoBencher: Towards Declarative Benchmark Construction | ICLR 2025 | [source](https://arxiv.org/abs/2407.08351) |
| 11 | Are We Learning Yet? A Meta-Review of Evaluation Failures Across Machine Learning | NeurIPS Datasets & Benchmarks 2021 | [source](https://scholar.google.com/scholar?q=Are+We+Learning+Yet%3F+A+Meta-Review+of+Evaluation+Failures+Across+Machine+Learning) |
| 12 | Injecting New Knowledge into Large Language Models via Supervised Fine-tuning | arXiv 2024 | [source](https://arxiv.org/abs/2404.00213) |
| 13 | Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs | EMNLP 2024 | [source](https://aclanthology.org/2024.emnlp-main.15/) |
| 14 | Knowledge-Instruct: Effective Continual Pre-training from Limited Data using Instructions | arXiv 2025 | [source](https://arxiv.org/abs/2504.05571) |
| 15 | QuALITY: Question Answering with Long Input Texts, Yes! | NAACL 2022 | [source](https://aclanthology.org/2022.naacl-main.391/) |
| 16 | Discovering Language Model Behaviors with Model-Written Evaluations | ACL Findings 2023 | [source](https://aclanthology.org/2023.findings-acl.847/) |
| 17 | AI and the Everything in the Whole Wide World Benchmark | NeurIPS Datasets & Benchmarks 2021 | [source](https://arxiv.org/abs/2111.15366) |
| 18 | NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark | EMNLP Findings 2023 | [source](https://aclanthology.org/2023.findings-emnlp.722/) |
| 19 | It Takes Two to Tango: Navigating Conceptualizations of NLP Tasks and Measurements of Performance | ACL Findings 2023 | [source](https://aclanthology.org/2023.findings-acl.202/) |
| 20 | LAB: Large-Scale Alignment for ChatBots | arXiv 2024 | [source](https://arxiv.org/abs/2403.01081) |
| 21 | MuSiQue: Multihop Questions via Single-hop Question Composition | TACL 2022 | [source](https://aclanthology.org/2022.tacl-1.31/) |
| 22 | Self-Instruct: Aligning Language Models with Self-Generated Instructions | ACL 2023 | [source](https://aclanthology.org/2023.acl-long.754/) |
| 23 | HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | EMNLP 2018 | [source](https://aclanthology.org/D18-1259/) |
| 24 | Synthetic Continued Pretraining | ICLR 2025 | [source](https://arxiv.org/abs/2409.07431) |
| 25 | Task Me Anything | NeurIPS Datasets & Benchmarks 2024 | [source](https://arxiv.org/abs/2406.11775) |
| 26 | FanOutQA: A Multi-Hop, Multi-Document Question Answering Benchmark for Large Language Models | ACL 2024 | [source](https://aclanthology.org/2024.acl-short.2/) |

---

## Paywalled — retrieve manually

These four have no open direct PDF; the link goes to the publisher or a title search.

| Paper | Link |
|---|---|
| TruthIsALie | [source](https://doi.org/10.1609/aimag) |
| Interval Estimation for a Binomial Proportion | [source](https://doi.org/10.1214/ss/1009213286) |
| Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms | [source](https://doi.org/10.1162/089976698300017197) |
| Are We Learning Yet? A Meta-Review of Evaluation Failures Across Machine Learning | [source](https://scholar.google.com/scholar?q=Are+We+Learning+Yet%3F+A+Meta-Review+of+Evaluation+Failures+Across+Machine+Learning) |
| A survey on LLM-as-a-judge (journal version) | [doi.org/10.1016/j.xinn.2025.101253](https://doi.org/10.1016/j.xinn.2025.101253) |
| From Generation to Judgment (EMNLP 2025) | [search](https://scholar.google.com/scholar?q=From+Generation+to+Judgment+LLM-as-a-judge) |
