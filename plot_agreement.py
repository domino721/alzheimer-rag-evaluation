"""Render the manuscript summary from reproduced CSV estimates.

Run after the two primary analysis scripts. Optional: --output path/to/figure.pdf
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
METRICS = ["factuality", "diversity", "clarity", "insightfulness"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "agreement_summary.pdf")
    args = parser.parse_args()
    pairs = pd.read_csv(ROOT / "query_cluster_bootstrap.csv").set_index("metric").loc[METRICS]
    ranks = pd.read_csv(ROOT / "condition_rank_agreement.csv").set_index("metric").loc[METRICS]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13,
                         "pdf.fonttype": 42, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.8), gridspec_kw={"width_ratios": [1.2, 1]})
    y = np.arange(4)
    ax = axes[0]
    values = pairs.spearman_rho.to_numpy()
    ax.errorbar(values, y + .12,
                xerr=np.array([values-pairs.spearman_ci95_low, pairs.spearman_ci95_high-values]),
                fmt="o", color="#215e99", capsize=3, markersize=6,
                label="Response level (400 pairs; 95% CI)")
    ax.scatter(ranks.spearman_rho, y - .12, color="#b55b26", marker="D", s=35,
               label="System level (8 means; point estimate)")
    ax.set(xlim=(0, 1.03), ylim=(3.5, -.5), yticks=y,
           yticklabels=[m.title() for m in METRICS], xlabel="Spearman correlation",
           title="A  Association at two levels")
    ax.legend(loc="upper left", bbox_to_anchor=(-.24, -.22), frameon=False, fontsize=11)
    ax = axes[1]
    values = pairs.human_minus_gpt_mean.to_numpy()
    ax.axvline(0, color="#777777", lw=1, ls="--")
    ax.errorbar(values, y,
                xerr=np.array([values-pairs.bias_ci95_low, pairs.bias_ci95_high-values]),
                fmt="o", color="#215e99", capsize=3, markersize=6)
    for yi, val, upper in zip(y, values, pairs.bias_ci95_high):
        ax.text(upper+.045, yi, f"{val:+.2f}", va="center", fontsize=11)
    ax.set(xlim=(-.82, 1.05), ylim=(3.5, -.5), yticks=y,
           yticklabels=[m.title() for m in METRICS],
           xlabel="Expert minus GPT score (1–5 scale)",
           title="B  Directional score offsets")
    ax.text(0, -.29, "Points: means; bars: query-cluster 95% CI", transform=ax.transAxes,
            fontsize=11)
    for ax in axes:
        ax.grid(axis="x", color="#dddddd", lw=.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=.115, right=.985, bottom=.28, top=.87, wspace=.43)
    fig.savefig(args.output, bbox_inches="tight", metadata={"Creator": "Matplotlib", "CreationDate": None})
    plt.close(fig)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
