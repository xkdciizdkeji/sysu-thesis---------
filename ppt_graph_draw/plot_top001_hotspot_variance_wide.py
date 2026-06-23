#!/usr/bin/env python3
"""Generate a wide, PPT-friendly top-0.1% hotspot variance chart.

Bars are vertical (cases along X) to produce a wide aspect ratio.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# (case, CUGR2, DGR, DGR Dynamic / Initial-routing workflow)
RAW_VARIANCE_DATA = [
    ("ispd18_test1", 0.0, 0.0, 0.0),
    ("ispd18_test2", 0.0, 0.0, 0.0),
    ("ispd18_test3", 0.002954, 0.002911, 0.002911),
    ("ispd18_test4", 0.478744, 0.183275, 0.183575),
    ("ispd18_test5", 0.099713, 0.086805, 0.086805),
    ("ispd18_test6", 0.455318, 0.297576, 0.269986),
    ("ispd18_test7", 27.599318, 7.205359, 0.12138),
    ("ispd18_test8", 27.264154, 7.688613, 0.148349),
    ("ispd18_test9", 1.37048, 0.233442, 0.225255),
    ("ispd18_test10", 0.606387, 17.41427, 6.538063),
    ("ispd19_test1", 0.0, 0.0, 0.0),
    ("ispd19_test2", 0.17731, 0.046588, 0.035484),
    ("ispd19_test3", 0.060352, 0.057961, 0.057961),
    ("ispd19_test4", 117.169531, 297.090094, 35.828338),
    ("ispd19_test5", 2.040019, 1.021479, 1.206489),
    ("ispd19_test6", 30.228375, 3.383759, 0.211399),
    ("ispd19_test7", 3.520162, 12.736848, 4.232374),
    ("ispd19_test8", 2.409848, 0.041119, 0.027365),
    ("ispd19_test9", 0.049072, 0.032242, 0.020581),
    ("ispd19_test10", 0.522657, 0.216799, 0.313512),
    ("ispd18_test5_metal5", 3.537208, 4.337662, 4.774059),
    ("ispd18_test8_metal5", 31.263657, 33.872799, 28.007952),
    ("ispd18_test10_metal5", 1.230266, 140.246639, 28.734771),
    ("ispd19_test7_metal5", 16.193711, 53.298422, 30.839764),
    ("ispd19_test8_metal5", 8.052888, 8.301968, 8.494682),
    ("ispd19_test9_metal5", 10.840905, 12.525667, 8.824261),
    ("ariane133_51", 0.936457, 0.018048, 0.009177),
    ("ariane133_68", 3.203282, 0.226382, 0.075453),
    ("bsg_chip", 46.829871, 20.824924, 16.536126),
    ("mempool_tile", 1.572264, 1.083579, 0.591742),
    ("nvdla", 73.207433, 42.770859, 9.647749),
]


def normalize_casewise(data):
    """Drop all-zero cases and normalize each case by its local max to 100%."""
    kept = []
    dropped = []
    for case, cugr, dgr, flow in data:
        if cugr == 0.0 and dgr == 0.0 and flow == 0.0:
            dropped.append(case)
            continue
        scale = max(cugr, dgr, flow)
        kept.append((case, cugr / scale * 100.0, dgr / scale * 100.0, flow / scale * 100.0))
    return kept, dropped


def configure_fonts():
    # Prefer a CJK font for Chinese labels while keeping robust fallbacks.
    matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Noto Sans", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False


def render_chart(normalized_data, output_pdf, output_png):
    cases = [row[0] for row in normalized_data]
    vals_c = [row[1] for row in normalized_data]
    vals_d = [row[2] for row in normalized_data]
    vals_f = [row[3] for row in normalized_data]

    n = len(cases)
    x = np.arange(n)
    width = 0.24

    fig_w = max(16.0, n * 0.45 + 6.0)
    fig_h = 6.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor="white")
    ax.set_facecolor("white")

    ax.bar(x - width, vals_c, width=width, color="#4C78A8", label="CUGR2")
    ax.bar(x, vals_d, width=width, color="#F58518", label="DGR")
    ax.bar(x + width, vals_f, width=width, color="#54A24B", label="本文方法")

    ax.set_ylabel("归一化方差对比（%）", fontname="Noto Sans CJK JP", fontsize=20, color="black", labelpad=10)
    ax.set_ylim(0, 105)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.tick_params(axis="y", labelsize=14, colors="black")

    ax.set_xticks(x)
    ax.set_xticklabels(cases, fontsize=10, rotation=45, ha="right", color="black")

    ax.grid(axis="y", linestyle="--", alpha=0.28, color="gray")

    for spine_name in ("left", "bottom", "top", "right"):
        ax.spines[spine_name].set_color("black")
        ax.spines[spine_name].set_linewidth(1.0)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        ncol=3,
        fontsize=14,
        frameon=True,
        facecolor="white",
        edgecolor="black",
        handlelength=2.6,
        handletextpad=0.7,
        columnspacing=2.0,
        borderpad=0.6,
    )

    fig.subplots_adjust(left=0.06, right=0.995, top=0.82, bottom=0.24)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_pdf, format="pdf")
    fig.savefig(output_png, format="png", dpi=300)


def main():
    configure_fonts()

    normalized, dropped = normalize_casewise(RAW_VARIANCE_DATA)

    repo_root = Path(__file__).resolve().parents[1]
    output_pdf = repo_root / "top001_hotspot_variance_normalized_barv.pdf"
    output_png = repo_root / "top001_hotspot_variance_normalized_barv.png"

    render_chart(normalized, output_pdf, output_png)

    print(f"Saved PDF: {output_pdf}")
    print(f"Saved PNG: {output_png}")
    print(f"Kept cases: {len(normalized)}")
    print(f"Dropped all-zero cases: {dropped}")


if __name__ == "__main__":
    main()
