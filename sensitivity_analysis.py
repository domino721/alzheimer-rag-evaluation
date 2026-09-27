"""Descriptive robustness checks on archived ratings; no new model calls.

Run after reproduce_analysis.py. No significance tests or causal interpretation.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

ROOT = Path(__file__).resolve().parent
KEYS = ["query_id", "retriever", "condition"]
METRICS = ["factuality", "diversity", "clarity", "insightfulness"]


def main():
    human = pd.read_csv(ROOT / "human_ratings_anonymized.csv")
    matched = pd.read_csv(ROOT / "arxiv_human_gpt_anonymized.csv").set_index(KEYS).sort_index()
    assert matched.index.is_unique and len(matched) == 400
    rows = []
    for metric in METRICS:
        panel = human.pivot(index=KEYS, columns="rater_id", values=metric + "_human").reindex(matched.index)
        assert panel.shape == (400, 5)
        gpt = matched[metric + "_gpt"]
        assert np.allclose(panel.mean(axis=1), matched[metric + "_human_mean"])

        def record(check, group, h, g):
            assert h.index.equals(g.index) and not h.isna().any() and not g.isna().any()
            rows.append(dict(metric=metric, check=check, group=group, n=len(h),
                             pearson_r=pearsonr(h, g).statistic,
                             spearman_rho=spearmanr(h, g).statistic,
                             human_minus_gpt_mean=(h - g).mean()))

        record("pooled", "all", panel.mean(axis=1), gpt)
        complete = panel.notna().all(axis=1)
        record("complete_case", "five_ratings", panel.loc[complete].mean(axis=1), gpt.loc[complete])
        for rater in panel.columns:
            record("leave_one_rater_out", rater, panel.drop(columns=rater).mean(axis=1), gpt)
        for (retriever, condition), block in panel.groupby(level=["retriever", "condition"]):
            record("within_condition", retriever + "/" + condition, block.mean(axis=1), gpt.loc[block.index])
    result = pd.DataFrame(rows)
    result.to_csv(ROOT / "sensitivity_results.csv", index=False)
    print(result.groupby(["metric", "check"]).agg(n_comparisons=("n", "size"),
          pearson_min=("pearson_r", "min"), pearson_max=("pearson_r", "max")).to_string())


if __name__ == "__main__":
    main()
