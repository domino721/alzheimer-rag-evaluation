"""Query-cluster bootstrap for the exploratory human--GPT comparison.

The unit resampled is the researcher query.  All eight shared conditions are
retained together within each bootstrap replicate, avoiding the assumption
that the 400 query--condition rows are independent observations.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata


ANALYSIS_DIR = Path(__file__).resolve().parent
PRIVATE_INPUT_FILE = ANALYSIS_DIR / "human_gpt_matched.csv"
PUBLIC_INPUT_FILE = ANALYSIS_DIR / "arxiv_human_gpt_anonymized.csv"
OUTPUT_FILE = ANALYSIS_DIR / "query_cluster_bootstrap.csv"
METRICS = ["factuality", "diversity", "clarity", "insightfulness"]
N_BOOTSTRAP = 2_000
SEED = 20_260_807


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def main() -> None:
    input_file = PUBLIC_INPUT_FILE if PUBLIC_INPUT_FILE.exists() else PRIVATE_INPUT_FILE
    data = pd.read_csv(input_file, encoding="utf-8-sig")
    data = data.sort_values(["query_id", "retriever", "condition"])

    # Create a public, text-free analysis table when running from the private
    # matched file. It contains no evaluator IDs, query text, generated text,
    # or retrieved abstracts.
    if input_file == PRIVATE_INPUT_FILE:
        query_map = {
            query_id: f"Q{index:03d}"
            for index, query_id in enumerate(data["query_id"].drop_duplicates(), start=1)
        }
        public_columns = ["query_id", "retriever", "condition"]
        for metric in METRICS:
            public_columns.extend(
                [
                    f"{metric}_human_mean",
                    f"{metric}_human_std",
                    f"{metric}_human_count",
                    f"{metric}_gpt",
                ]
            )
        public_data = data[public_columns].copy()
        public_data["query_id"] = public_data["query_id"].map(query_map)
        public_data.to_csv(PUBLIC_INPUT_FILE, index=False, encoding="utf-8-sig")

    per_query = data.groupby("query_id").size()
    if data["query_id"].nunique() != 50 or not per_query.eq(8).all():
        raise ValueError("Expected 50 queries with eight shared conditions each")

    human = np.stack(
        [
            data[f"{metric}_human_mean"].to_numpy().reshape(50, 8)
            for metric in METRICS
        ],
        axis=2,
    )
    gpt = np.stack(
        [data[f"{metric}_gpt"].to_numpy().reshape(50, 8) for metric in METRICS],
        axis=2,
    )

    rng = np.random.default_rng(SEED)
    pearson_samples = np.empty((N_BOOTSTRAP, len(METRICS)))
    spearman_samples = np.empty_like(pearson_samples)
    bias_samples = np.empty_like(pearson_samples)

    for bootstrap_id in range(N_BOOTSTRAP):
        query_indices = rng.integers(0, 50, 50)
        human_sample = human[query_indices].reshape(-1, len(METRICS))
        gpt_sample = gpt[query_indices].reshape(-1, len(METRICS))
        bias_samples[bootstrap_id] = (human_sample - gpt_sample).mean(axis=0)

        for metric_id in range(len(METRICS)):
            h = human_sample[:, metric_id]
            g = gpt_sample[:, metric_id]
            pearson_samples[bootstrap_id, metric_id] = correlation(h, g)
            spearman_samples[bootstrap_id, metric_id] = correlation(
                rankdata(h), rankdata(g)
            )

    rows = []
    for metric_id, metric in enumerate(METRICS):
        h = human[:, :, metric_id].ravel()
        g = gpt[:, :, metric_id].ravel()
        pearson_ci = np.quantile(
            pearson_samples[:, metric_id], [0.025, 0.975]
        )
        spearman_ci = np.quantile(
            spearman_samples[:, metric_id], [0.025, 0.975]
        )
        bias_ci = np.quantile(bias_samples[:, metric_id], [0.025, 0.975])
        rows.append(
            {
                "metric": metric,
                "n_queries": 50,
                "n_query_condition_pairs": 400,
                "pearson_r": correlation(h, g),
                "pearson_ci95_low": pearson_ci[0],
                "pearson_ci95_high": pearson_ci[1],
                "spearman_rho": correlation(rankdata(h), rankdata(g)),
                "spearman_ci95_low": spearman_ci[0],
                "spearman_ci95_high": spearman_ci[1],
                "human_minus_gpt_mean": float((h - g).mean()),
                "bias_ci95_low": bias_ci[0],
                "bias_ci95_high": bias_ci[1],
                "bootstrap_replicates": N_BOOTSTRAP,
                "seed": SEED,
            }
        )

    result = pd.DataFrame(rows).round(4)
    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))
    print(f"Public analysis data: {PUBLIC_INPUT_FILE}")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
