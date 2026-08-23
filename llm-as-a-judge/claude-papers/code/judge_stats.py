"""
judge_stats.py — statistics toolkit for the EmbGen LLM-as-a-judge evaluation.

Everything here runs on data the EmbGen authors ALREADY have: the per-item, per-run
judge outputs. No new model training and no new judge calls are required for
sections 1-4. Section 5 (PPI) needs a small human-annotated subsample.

Expected input: a tidy CSV/DataFrame with one row per (item, method, judge_run):
    item_id      str   evaluation question id (shared across methods -- this is what makes
                       the comparison PAIRED, which is where the statistical power comes from)
    dataset      str   'popqa' | 'squad' | 'wikitext'
    budget       str   '5M' | '20M'
    method       str   'EmbGen' | 'InstructLab' | 'EntiGraph' | 'KnowledgeInstruct' | 'Baseline'
    run          int   0..9  (the 10 repeated judge runs)
    factual      str   'Strong' | 'Adequate' | 'Weak'
    completeness str   'Strong' | 'Adequate' | 'Weak'
    relevance    str   ...
    clarity      str   ...
    answer       str   the model's generated answer (needed for the length control)

Install: pip install numpy pandas scipy statsmodels krippendorff ppi-python
         (PPI: `pip install ppi-python` provides ppi_py)
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.multitest import multipletests

ORD = {"Weak": 1, "Adequate": 2, "Strong": 3}
DIMS = ["factual", "completeness", "relevance", "clarity"]


# ---------------------------------------------------------------- 0. the metric
def binary_accuracy_flag(factual: str, completeness: str) -> int:
    """EmbGen's Binary Accuracy rule, applied per item per run (paper section 5.2.2)."""
    return int(factual == "Strong" and completeness in ("Strong", "Adequate"))


def per_item_outcomes(df: pd.DataFrame, aggregate: str = "majority") -> pd.DataFrame:
    """Collapse the 10 judge runs to one binary outcome per (item, method).

    aggregate='majority' -> item is correct if >5/10 runs say so (recommended: it is a
                            decision rule, and it keeps the outcome binary so McNemar applies)
    aggregate='mean'     -> keeps the fraction of runs (use for the graded analysis)
    """
    d = df.copy()
    d["correct"] = [binary_accuracy_flag(f, c)
                    for f, c in zip(d["factual"], d["completeness"])]
    g = d.groupby(["dataset", "budget", "method", "item_id"])["correct"].mean().reset_index()
    if aggregate == "majority":
        g["correct"] = (g["correct"] > 0.5).astype(int)
    return g


# ------------------------------------------- 1. judge stability across the 10 runs
def judge_stability(df: pd.DataFrame) -> pd.DataFrame:
    """Does the temperature-0 judge actually repeat itself?

    NOTE: the reported Binary Accuracy values in Tables 3-4 are not expressible as k/250,
    which already implies the answer is NO. This quantifies it.

    Returns, per dataset/budget/method/dimension:
      unanimity   fraction of items where all 10 runs gave the identical label
      alpha       Krippendorff's alpha (ordinal) treating the 10 runs as 10 coders
    """
    try:
        import krippendorff
    except ImportError:
        raise SystemExit("pip install krippendorff")
    out = []
    for (ds, bu, me), grp in df.groupby(["dataset", "budget", "method"]):
        for dim in DIMS:
            wide = grp.pivot_table(index="run", columns="item_id", values=dim,
                                   aggfunc="first")
            mat = wide.replace(ORD).to_numpy(dtype=float)   # coders x units
            alpha = krippendorff.alpha(reliability_data=mat,
                                       level_of_measurement="ordinal")
            unan = float(np.mean([len(set(mat[:, j][~np.isnan(mat[:, j])])) == 1
                                  for j in range(mat.shape[1])]))
            out.append(dict(dataset=ds, budget=bu, method=me, dimension=dim,
                            unanimity=unan, krippendorff_alpha=alpha))
    # also the derived binary metric
    d = df.copy()
    d["correct"] = [binary_accuracy_flag(f, c)
                    for f, c in zip(d["factual"], d["completeness"])]
    for (ds, bu, me), grp in d.groupby(["dataset", "budget", "method"]):
        wide = grp.pivot_table(index="run", columns="item_id", values="correct",
                               aggfunc="first").to_numpy(dtype=float)
        unan = float(np.mean([len(set(wide[:, j][~np.isnan(wide[:, j])])) == 1
                              for j in range(wide.shape[1])]))
        out.append(dict(dataset=ds, budget=bu, method=me, dimension="BinaryAccuracy",
                        unanimity=unan, krippendorff_alpha=np.nan))
    return pd.DataFrame(out)


# --------------------------------------------------- 2. confidence intervals
def ba_with_ci(items: pd.DataFrame, method_col="method") -> pd.DataFrame:
    """Wilson 95% CI for Binary Accuracy. Wilson (not Wald) because base rates on
    Wikitext-10 are ~0.07 and Wald intervals are badly wrong in that regime
    (Brown, Cai & DasGupta, Statistical Science 2001)."""
    rows = []
    for (ds, bu, me), g in items.groupby(["dataset", "budget", method_col]):
        k, n = int(g["correct"].sum()), len(g)
        lo, hi = proportion_confint(k, n, alpha=0.05, method="wilson")
        rows.append(dict(dataset=ds, budget=bu, method=me, k=k, n=n,
                         ba=k / n, ci_lo=lo, ci_hi=hi))
    return pd.DataFrame(rows)


# --------------------------------------------------- 3. paired significance tests
def mcnemar_exact(b: int, c: int) -> float:
    """Exact (binomial) McNemar. Use the exact form, not the chi-square approximation:
    discordant counts here are small (Dietterich, Neural Computation 1998)."""
    n = b + c
    if n == 0:
        return 1.0
    return float(min(1.0, 2 * stats.binom.cdf(min(b, c), n, 0.5)))


def paired_comparisons(items: pd.DataFrame, focal="EmbGen") -> pd.DataFrame:
    """McNemar focal-vs-each-baseline on the SAME item ids, plus the paired
    bootstrap CI for the difference. Holm-corrects across the whole table."""
    rows = []
    for (ds, bu), g in items.groupby(["dataset", "budget"]):
        piv = g.pivot_table(index="item_id", columns="method", values="correct")
        if focal not in piv.columns:
            continue
        for other in piv.columns:
            if other == focal:
                continue
            sub = piv[[focal, other]].dropna()
            a, o = sub[focal].to_numpy(), sub[other].to_numpy()
            b = int(np.sum((a == 1) & (o == 0)))   # focal only
            c = int(np.sum((a == 0) & (o == 1)))   # baseline only
            p = mcnemar_exact(b, c)
            diff = a.mean() - o.mean()
            lo, hi = paired_bootstrap_ci(a, o)
            rows.append(dict(dataset=ds, budget=bu, focal=focal, baseline=other,
                             n=len(sub), b_focal_only=b, c_base_only=c,
                             diff=diff, boot_lo=lo, boot_hi=hi, p_raw=p))
    out = pd.DataFrame(rows)
    if len(out):
        out["p_holm"] = multipletests(out["p_raw"], method="holm")[1]
        out["sig_holm"] = out["p_holm"] < 0.05
    return out


def paired_bootstrap_ci(a, o, B=10000, seed=0):
    """Bootstrap over ITEMS (resample item indices, keeping both methods' outcomes
    together) -- this respects the pairing. Berg-Kirkpatrick et al., EMNLP 2012.

    CAVEAT -- report this as secondary, not primary. Bowyer et al. (ICML 2025, Position
    track) show that at N ~ 100 with few successes the bootstrap is calibrated just as
    badly as a CLT/Wald interval (~92.5% coverage for a nominal 95%). Only **Wilson** and
    **Bayesian Beta** intervals hold nominal coverage in this regime. EmbGen's N=250 with
    9-17 successes on Wikitext-10 is squarely inside that failure regime.
    Primary interval for a single proportion  -> Wilson (see ba_with_ci).
    Primary test for a paired difference      -> McNemar exact (see mcnemar_exact).
    Use this bootstrap for the effect-size interval only, and say so."""
    rng = np.random.default_rng(seed)
    n = len(a)
    idx = rng.integers(0, n, size=(B, n))
    d = a[idx].mean(1) - o[idx].mean(1)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


# --------------------------------------------------- 4. the verbosity control
def length_controlled(items: pd.DataFrame, answers: pd.DataFrame,
                      focal="EmbGen", baseline="InstructLab") -> pd.DataFrame:
    """Is the win a completeness effect or just a length effect?

    Fits  correct ~ method + log(answer_tokens)  with item random-effect-free
    logistic regression, clustered SEs by item. If the method coefficient survives
    conditioning on length, the verbosity objection is answered.
    (Same logic as Length-Controlled AlpacaEval, Dubois et al., COLM 2024.)
    """
    import statsmodels.formula.api as smf
    d = items.merge(answers, on=["dataset", "budget", "method", "item_id"])
    d = d[d["method"].isin([focal, baseline])].copy()
    d["ntok"] = d["answer"].str.split().str.len().clip(lower=1)
    d["loglen"] = np.log(d["ntok"])
    d["is_focal"] = (d["method"] == focal).astype(int)
    rows = []
    for (ds, bu), g in d.groupby(["dataset", "budget"]):
        naive = smf.logit("correct ~ is_focal", data=g).fit(disp=0)
        ctrl = smf.logit("correct ~ is_focal + loglen", data=g).fit(
            disp=0, cov_type="cluster", cov_kwds={"groups": g["item_id"]})
        rows.append(dict(
            dataset=ds, budget=bu,
            len_focal=g.loc[g.is_focal == 1, "ntok"].mean(),
            len_base=g.loc[g.is_focal == 0, "ntok"].mean(),
            beta_naive=naive.params["is_focal"], p_naive=naive.pvalues["is_focal"],
            beta_lencontrolled=ctrl.params["is_focal"], p_lencontrolled=ctrl.pvalues["is_focal"],
            beta_loglen=ctrl.params["loglen"], p_loglen=ctrl.pvalues["loglen"]))
    return pd.DataFrame(rows)


# --------------------------------------------------- 5. PPI: few human labels, valid CIs
def ppi_binary(human_idx, y_human, yhat_labelled, yhat_unlabelled, alpha=0.05,
               tune_lambda=True):
    r"""PPI++ for a PROPORTION (Angelopoulos, Duchi & Zrnic, PPI++; Boyeau et al., ICML 2025).

    Combines a small human-labelled subsample with the full LLM-judged set to get an estimate
    that is UNBIASED EVEN IF THE JUDGE IS BIASED -- the judge only needs to be *correlated*
    with humans to buy precision.

        theta_hat(lam) = (lam/|U|) * sum_U f_i  +  (1/n) * sum_L [ y_i - lam * f_i ]

    The tuned lambda matters. Plain PPI (lam = 1) can be WORSE than just using the human
    labels when n is small -- Eyre & Madras (ICML 2025) put that regime at n <~ 50-100, which
    is exactly EmbGen's likely annotation budget. With lam tuned, lam_hat -> 0 recovers the
    human-only estimator exactly, so PPI++ is never worse than classical inference.
    THIS IS WHY YOU SHOULD USE tune_lambda=True.

    Args:
        y_human         (n,) human 0/1 labels on the annotated subsample
        yhat_labelled   (n,) judge 0/1 labels on those SAME items
        yhat_unlabelled (N,) judge 0/1 labels on everything else
    """
    y = np.asarray(y_human, float)
    f_l = np.asarray(yhat_labelled, float)
    f_u = np.asarray(yhat_unlabelled, float)
    n, N = len(y), len(f_u)

    if tune_lambda and n > 1 and N > 0 and f_l.var(ddof=1) > 0:
        lam = (np.cov(f_l, y, ddof=1)[0, 1] / f_l.var(ddof=1)) * (N / (N + n))
        lam = float(np.clip(lam, 0.0, 1.0))
    else:
        lam = 1.0 if N > 0 else 0.0

    theta = lam * f_u.mean() + np.mean(y - lam * f_l) if N > 0 else y.mean()
    var = (lam ** 2) * f_u.var(ddof=1) / N + (y - lam * f_l).var(ddof=1) / n if N > 0 \
        else y.var(ddof=1) / n
    z = stats.norm.ppf(1 - alpha / 2)
    half = z * np.sqrt(var)

    cl_half = z * np.sqrt(y.var(ddof=1) / n)
    return dict(ppi_estimate=float(theta),
                ppi_ci=(float(theta - half), float(theta + half)),
                ppi_halfwidth=float(half), lam=lam,
                classical_estimate=float(y.mean()),
                classical_ci=(float(y.mean() - cl_half), float(y.mean() + cl_half)),
                classical_halfwidth=float(cl_half),
                effective_gain=float((cl_half / half) ** 2) if half > 0 else np.nan,
                n_human=n, n_judge_only=N)


def rogan_gladen(p_judge, sens, spec):
    """Sanity cross-check on the PPI estimate: correct an observed judge rate for known
    sensitivity/specificity.  p_corr = (p_judge + Sp - 1) / (Se + Sp - 1)"""
    denom = sens + spec - 1
    if abs(denom) < 1e-9:
        return np.nan
    return float(np.clip((p_judge + spec - 1) / denom, 0.0, 1.0))


def stratified_annotation_sample(items: pd.DataFrame, n_per_cell=40, seed=0):
    """Which items to send to human annotators.

    Stratify on (dataset, budget, judge verdict) so both judge-correct and judge-wrong
    items are represented -- otherwise on Wikitext-10 (BA~0.07) a uniform sample gives
    you almost no positives and the rectifier is estimated from nothing.
    """
    rng = np.random.default_rng(seed)
    picks = []
    for (ds, bu, corr), g in items.groupby(["dataset", "budget", "correct"]):
        take = min(n_per_cell, len(g))
        picks.append(g.iloc[rng.choice(len(g), take, replace=False)])
    return pd.concat(picks).reset_index(drop=True)


# --------------------------------------------------- 6. judge-human agreement
def judge_human_agreement(y_human_ord, y_judge_ord):
    """Report ALL of these -- reviewers disagree about which one matters.
    Inputs are ordinal 1/2/3 arrays (or 0/1 for the binary metric)."""
    try:
        import krippendorff
    except ImportError:
        raise SystemExit("pip install krippendorff")
    from sklearn.metrics import cohen_kappa_score  # pip install scikit-learn
    h, j = np.asarray(y_human_ord), np.asarray(y_judge_ord)
    return dict(
        raw_agreement=float((h == j).mean()),
        cohen_kappa=float(cohen_kappa_score(h, j)),
        cohen_kappa_quadratic=float(cohen_kappa_score(h, j, weights="quadratic")),
        krippendorff_alpha_ordinal=float(
            krippendorff.alpha(reliability_data=np.vstack([h, j]).astype(float),
                               level_of_measurement="ordinal")),
        spearman=float(stats.spearmanr(h, j).statistic),
    )


if __name__ == "__main__":
    print(__doc__)
