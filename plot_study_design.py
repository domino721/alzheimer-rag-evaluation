"""Render the study design and dual scoring protocol diagram (Figure 1).

Matches the typography and color palette of plot_agreement.py.
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent


def draw_card(ax, x, y, w, h, fc="#ffffff", ec="#cbd5e1", lw=1.2, pad=0.012, ls="-", zorder=2):
    patch = FancyBboxPatch(
        (x + pad, y + pad),
        w - 2 * pad,
        h - 2 * pad,
        boxstyle=f"round,pad={pad},rounding_size=0.016",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        linestyle=ls,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def draw_arrow(ax, x0, y0, x1, y1, color="#475569", lw=1.5, rad=0.0):
    arr = FancyArrowPatch(
        (x0, y0),
        (x1, y1),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>,head_length=6,head_width=3.6",
        color=color,
        linewidth=lw,
        zorder=5,
    )
    ax.add_patch(arr)
    return arr


def draw_badge(ax, x, y, text, bg="#215e99", fg="#ffffff", fontsize=8.5):
    return ax.text(
        x,
        y,
        text,
        ha="left",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color=fg,
        bbox=dict(boxstyle="round,pad=0.26,rounding_size=0.35", fc=bg, ec="none"),
        zorder=6,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT.parent / "study_design.pdf")
    parser.add_argument("--verify", action="store_true", help="Assert text bounds fit inside parent cards")
    args = parser.parse_args()

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig, ax = plt.subplots(figsize=(11.6, 5.25))
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # Palette harmonized with Figure 2 (agreement_summary.pdf)
    BLUE = "#215e99"
    BLUE_BG = "#f1f6fb"
    BLUE_TAG = "#dceaf7"
    AMBER = "#b55b26"
    AMBER_BG = "#fdf5ef"
    AMBER_TAG = "#f9e3d2"
    SLATE = "#334155"
    SLATE_SUB = "#475569"
    GRAY_BG = "#f8fafc"
    GRAY_BORDER = "#cbd5e1"

    checks = []

    # =========================================================================
    # Section Headers (Top Row: y = 0.945)
    # =========================================================================
    ax.text(0.008, 0.955, "A  Shared Literature-RAG Archive", fontsize=11.5, fontweight="bold", color=SLATE, va="center")
    ax.text(0.352, 0.955, "B  Two Realised Scoring Protocols", fontsize=11.5, fontweight="bold", color=SLATE, va="center")
    ax.text(0.725, 0.955, "C  Paired Evaluation Analysis", fontsize=11.5, fontweight="bold", color=SLATE, va="center")

    # =========================================================================
    # Column A: Shared RAG Archive (x = 0.008 .. 0.305)
    # =========================================================================
    colA_x, colA_w = 0.008, 0.297
    draw_card(ax, colA_x, 0.03, colA_w, 0.89, fc=GRAY_BG, ec=GRAY_BORDER, lw=1.1, zorder=1)

    # Box A1: Query Pool & Corpus
    bA1 = draw_card(ax, 0.022, 0.665, 0.269, 0.23, fc="#ffffff", ec=GRAY_BORDER, lw=1.0, zorder=2)
    t = [
        ax.text(0.036, 0.852, "Query Pool & Corpus", fontsize=9.8, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.036, 0.798, "• 201 researcher-authored AD queries", fontsize=8.7, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.752, "• 50-query evaluation subset", fontsize=8.7, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.036, 0.706, "• ~18k PubMed abstracts (2015–2024)", fontsize=8.7, color=SLATE_SUB, va="center", zorder=4),
    ]
    checks.append(("Box A1", bA1, t))

    draw_arrow(ax, 0.1565, 0.665, 0.1565, 0.618, color=SLATE_SUB, lw=1.3)

    # Box A2: Eight Retrieval Configurations
    bA2 = draw_card(ax, 0.022, 0.365, 0.269, 0.25, fc="#ffffff", ec=GRAY_BORDER, lw=1.0, zorder=2)
    t = [
        ax.text(0.036, 0.573, "Eight Configurations (2 × 4)", fontsize=9.8, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.036, 0.520, "• Retriever: BM25 or DPR", fontsize=8.7, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.474, "• Modes: Naive | HyDE (no keyword)", fontsize=8.7, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.052, 0.431, "Keyword + HyDE | MeSH + HyDE", fontsize=8.7, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.390, "  (MeSH via prompt guidance only)", fontsize=8.0, style="italic", color="#64748b", va="center", zorder=4),
    ]
    checks.append(("Box A2", bA2, t))

    draw_arrow(ax, 0.1565, 0.365, 0.1565, 0.318, color=SLATE_SUB, lw=1.3)

    # Box A3: Two-Step Stream & Response Generation
    bA3 = draw_card(ax, 0.022, 0.055, 0.269, 0.26, fc="#ffffff", ec=SLATE_SUB, lw=1.15, zorder=2)
    t = [
        ax.text(0.036, 0.273, "Retrieval & Generation", fontsize=9.8, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.036, 0.222, "• 2-step stream: q* → d₁ → {q*, d₁} → d₂", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.177, "• Slots: 2 (no-kw) or 4 (kw; 10 in 2 cases)", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.132, "• Generator: GPT-4o-mini", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.036, 0.085, "→ 400 query–condition responses", fontsize=8.8, fontweight="bold", color=SLATE, va="center", zorder=4),
    ]
    checks.append(("Box A3", bA3, t))

    # =========================================================================
    # Column B: Two Realised Scoring Protocols (x = 0.352 .. 0.678)
    # =========================================================================
    colB_x, colB_w = 0.352, 0.326

    # Top Card: Expert Panel Protocol (Blue)
    bB1 = draw_card(ax, colB_x, 0.535, colB_w, 0.385, fc=BLUE_BG, ec=BLUE, lw=1.5, zorder=2)
    draw_badge(ax, colB_x + 0.016, 0.873, "Expert Panel Protocol", bg=BLUE, fg="#ffffff", fontsize=9.2)
    t = [
        ax.text(colB_x + 0.016, 0.808, "Raters: 5 AD biomedical researchers", fontsize=8.8, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.764, "  (7,939 observed / 61 missing scalar scores)", fontsize=8.2, color=SLATE_SUB, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.706, "Evidence: Query + Response + Abstracts", fontsize=8.7, fontweight="bold", color=BLUE, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.654, "Display: All 8 conditions side by side", fontsize=8.7, fontweight="bold", color=BLUE, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.610, "  (condition identities blinded at distribution)", fontsize=8.2, color=SLATE_SUB, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.564, "Rubric: Concise 1-sentence metric definitions", fontsize=8.4, color=SLATE_SUB, va="center", zorder=4),
    ]
    checks.append(("Box B1", bB1, t))

    # Center Contrast Callout Pill between B1 and B2
    pill = ax.text(
        colB_x + colB_w / 2,
        0.478,
        "Asymmetries: abstracts • display • rubric",
        ha="center",
        va="center",
        fontsize=8.1,
        style="italic",
        color="#475569",
        bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.4", fc="#f1f5f9", ec="#94a3b8", lw=0.85, ls="--"),
        zorder=6,
    )

    # Bottom Card: Automated GPT-4o Protocol (Amber)
    bB2 = draw_card(ax, colB_x, 0.03, colB_w, 0.39, fc=AMBER_BG, ec=AMBER, lw=1.5, zorder=2)
    b_badge2 = draw_badge(ax, colB_x + 0.016, 0.373, "Automated Judge Protocol", bg=AMBER, fg="#ffffff", fontsize=9.2)
    t = [
        ax.text(colB_x + 0.016, 0.308, "Judge: GPT-4o", fontsize=8.8, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.264, "  (1,600 complete scalar scores; 400 × 4)", fontsize=8.2, color=SLATE_SUB, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.206, "Evidence: Query + Response only (no abstracts)", fontsize=8.7, fontweight="bold", color=AMBER, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.154, "Display: 1 response scored per prompt call", fontsize=8.7, fontweight="bold", color=AMBER, va="center", zorder=4),
        ax.text(colB_x + 0.016, 0.110, "  (no cross-condition comparison context)", fontsize=8.2, color=SLATE_SUB, va="center", zorder=4),
        ax.text(colB_x + 0.064 - 0.048, 0.064, "Rubric: Detailed 1–5 anchor criteria per metric", fontsize=8.4, color=SLATE_SUB, va="center", zorder=4),
    ]
    checks.append(("Box B2", bB2, t))

    # Branching arrows from Box A3 to B1 & B2
    draw_arrow(ax, 0.291, 0.21, colB_x, 0.70, color=BLUE, lw=1.5, rad=0.14)
    draw_arrow(ax, 0.291, 0.14, colB_x, 0.21, color=AMBER, lw=1.5, rad=-0.06)

    # =========================================================================
    # Column C: Paired Evaluation Analysis (x = 0.725 .. 0.992)
    # =========================================================================
    colC_x, colC_w = 0.725, 0.267
    draw_card(ax, colC_x, 0.03, colC_w, 0.89, fc=GRAY_BG, ec=GRAY_BORDER, lw=1.1, zorder=1)

    # Top strip: Shared 4 Dimensions
    bC0 = draw_card(ax, 0.738, 0.745, 0.241, 0.15, fc="#ffffff", ec=GRAY_BORDER, lw=1.0, zorder=2)
    t = [
        ax.text(0.751, 0.854, "Four Dimensions (1–5 Likert)", fontsize=9.2, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.751, 0.806, "Factuality • Diversity", fontsize=8.6, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.751, 0.768, "Clarity • Insightfulness", fontsize=8.6, color=SLATE_SUB, va="center", zorder=4),
    ]
    checks.append(("Box C0", bC0, t))

    # Box C1: System Rankings (N = 8)
    bC1 = draw_card(ax, 0.738, 0.515, 0.241, 0.21, fc="#ffffff", ec=AMBER, lw=1.2, zorder=2)
    t = [
        ax.text(0.751, 0.684, "1. System Rankings (N = 8)", fontsize=9.2, fontweight="bold", color=AMBER, va="center", zorder=4),
        ax.text(0.751, 0.632, "• Config-mean rank order", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.751, 0.586, "• Spearman ρ = 0.67–0.93", fontsize=8.6, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.751, 0.543, "  (descriptive point estimates)", fontsize=8.0, color="#64748b", va="center", zorder=4),
    ]
    checks.append(("Box C1", bC1, t))

    # Box C2: Response-Level Association (N = 400)
    bC2 = draw_card(ax, 0.738, 0.285, 0.241, 0.21, fc="#ffffff", ec=BLUE, lw=1.2, zorder=2)
    t = [
        ax.text(0.751, 0.454, "2. Response Level (N = 400)", fontsize=9.2, fontweight="bold", color=BLUE, va="center", zorder=4),
        ax.text(0.751, 0.402, "• Panel mean vs. GPT-4o", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.751, 0.356, "• Spearman ρ = 0.27–0.52", fontsize=8.6, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.751, 0.313, "  (query-cluster 95% CI)", fontsize=8.0, color="#64748b", va="center", zorder=4),
    ]
    checks.append(("Box C2", bC2, t))

    # Box C3: Offsets, Reliability & Sensitivity
    bC3 = draw_card(ax, 0.738, 0.055, 0.241, 0.21, fc="#ffffff", ec=SLATE_SUB, lw=1.1, zorder=2)
    t = [
        ax.text(0.751, 0.224, "3. Offsets & Reliability", fontsize=9.2, fontweight="bold", color=SLATE, va="center", zorder=4),
        ax.text(0.751, 0.172, "• Scale offsets (Expert − GPT)", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.751, 0.126, "• Expert ICC(A,1) = 0.09–0.24", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
        ax.text(0.751, 0.083, "• Complete-case & rater checks", fontsize=8.5, color=SLATE_SUB, va="center", zorder=4),
    ]
    checks.append(("Box C3", bC3, t))

    # Converging arrows from B1 & B2 into Column C
    draw_arrow(ax, colB_x + colB_w, 0.70, colC_x, 0.62, color=BLUE, lw=1.5, rad=-0.06)
    draw_arrow(ax, colB_x + colB_w, 0.22, colC_x, 0.38, color=AMBER, lw=1.5, rad=0.06)

    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.01, top=0.99)

    if args.verify:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        pill_data = pill.get_bbox_patch().get_window_extent(renderer).transformed(ax.transData.inverted())
        assert pill_data.x0 > colB_x + 0.01 and pill_data.x1 < colB_x + colB_w - 0.01, f"Pill x overflow: {pill_data.bounds}"
        assert pill_data.y0 > 0.425 and pill_data.y1 < 0.530, f"Pill y overflow: {pill_data.bounds}"
        for name, box, texts in checks:
            bb_box = box.get_window_extent(renderer)
            for idx, txt in enumerate(texts):
                bb_txt = txt.get_window_extent(renderer)
                if (
                    bb_txt.x0 < bb_box.x0 - 2
                    or bb_txt.x1 > bb_box.x1 + 2
                    or bb_txt.y0 < bb_box.y0 - 2
                    or bb_txt.y1 > bb_box.y1 + 2
                ):
                    raise AssertionError(
                        f"Overflow in {name} text[{idx}] {txt.get_text()!r}: "
                        f"text={bb_txt.bounds} vs box={bb_box.bounds}"
                    )
                for idx2 in range(idx + 1, len(texts)):
                    bb2 = texts[idx2].get_window_extent(renderer)
                    if bb_txt.overlaps(bb2):
                        raise AssertionError(f"Vertical text overlap in {name}: {txt.get_text()!r} vs {texts[idx2].get_text()!r}")
        print(f"All containment & non-overlap checks PASSED (pill x={pill_data.x0:.3f}..{pill_data.x1:.3f}).")

    fig.savefig(args.output, bbox_inches="tight", metadata={"Creator": "Matplotlib", "CreationDate": None})
    plt.close(fig)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
