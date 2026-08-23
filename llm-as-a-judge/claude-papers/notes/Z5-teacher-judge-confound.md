# The teacher = judge confound, and why it is entangled with EmbGen's headline variable

## The setup

From Appendix A.8 and §5.2.2:

| Dataset | Heterogeneity | Teacher `M_teach` | Judge | Relatedness (Li et al., ICLR 2026 taxonomy) |
|---|---|---|---|---|
| Pop-QA-Cities-20 | lowest | **GPT-5** | GPT-5 | **same model** (strongest) |
| SQuAD-20 | intermediate | **GPT-5** | GPT-5 | **same model** (strongest) |
| Wikitext-10 | **highest** | **gpt-4o-mini** | GPT-5 | same *family* (weaker) |

## Why this matters

Li et al., *Preference Leakage: A Contamination Problem in LLM-as-a-Judge* (**ICLR 2026**) define exactly
three relatedness levels between the synthetic-data generator and the judge — **same model**, inheritance,
and same family — and empirically confirm that judges are biased toward student models trained on data from
related generators. They note this contamination is *"harder to detect compared to previously identified
biases."* EmbGen sits in the strongest category (same model) on two of three corpora.

**Partial mitigation already present:** the teacher is held fixed across *methods* within a dataset, so
EmbGen and its baselines are all downstream of the same generator. Between-method comparisons are therefore
partly protected. Say this explicitly in the paper — it is a real defence and costs nothing.

**The unprotected part — and this is the serious one.** The no-augmentation Llama-3-8B-Instruct baseline was
never trained on GPT-5 data, so it is systematically disadvantaged by leakage. More importantly:

> **Teacher identity is confounded with the paper's central independent variable.**

EmbGen's thesis is *"EmbGen's advantage grows with corpus heterogeneity."* But the highest-heterogeneity
corpus (Wikitext-10) is also **the only one with a different, weaker teacher** (gpt-4o-mini rather than
GPT-5). So an alternative explanation for the headline result is available to any reviewer:

> *The Wikitext-10 result differs from the others not because heterogeneity is higher, but because the
> teacher was a smaller model and the judge–generator relatedness was weaker.*

With three datasets and two teacher models, heterogeneity and teacher identity cannot be separated from the
existing experiments. This is the most likely reason for a reviewer to reject the paper's core claim, and
it is not currently acknowledged anywhere.

## What to do in the available week

**Minimum (hours, no training).** Re-judge the **Wikitext-10 @ 20M** cell — the headline — with a
**non-OpenAI judge** (Claude, Gemini, or an open-weight judge such as Prometheus-2). Report the
EmbGen-vs-baseline ranking under both judges. If the ranking survives a judge from a different family, the
leakage objection is answered for the claim that actually matters. This is inference-only over 250×2
answers, and it simultaneously addresses W2 *and* the single-judge objection (W2 + part of W3).

**Strongly recommended (also hours).** Re-judge **one GPT-5-teacher cell** (Pop-QA @ 20M) with the same
non-OpenAI judge and report the *change in the gap*. The difference-in-differences between the
GPT-5-teacher cell and the gpt-4o-mini-teacher cell is a direct, quantitative estimate of preference
leakage in your own setup — a genuinely novel measurement for a workshop paper on evaluation, and exactly
the kind of result CFP topic #9 is asking for.

**If time allows.** Regenerate Wikitext-10 data with GPT-5 as teacher (or Pop-QA with gpt-4o-mini) to break
the confound properly. This needs a generation + training run, so it is probably out of scope this week —
but it is the right answer, and naming it as future work is far better than leaving the confound unstated.

**Non-negotiable regardless of time.** Add the teacher-model column to the dataset table, and state the
confound in Limitations. A reviewer who discovers it in Appendix A.8 unaided will treat it as concealment;
a reviewer who reads it in your Limitations will treat it as rigour.
