#!/usr/bin/env python3
"""Generate Chapter 4 SA optimization curve figures for PPT (half-height)."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


@dataclass
class RoundSeries:
    round_index: int
    iter_begin: int
    iter_end: int
    iterations: list[int]
    net_lengths: list[float]
    temperatures: list[float]
    start_iter: int
    start_net: float
    min_iter: int
    min_net: float


def configure_matplotlib() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "Noto Sans CJK JP",
        "Noto Serif CJK JP",
        "Noto Sans CJK SC",
        "Noto Serif CJK SC",
        "SimHei",
        "Microsoft YaHei",
        "WenQuanYi Zen Hei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["font.size"] = 18
    plt.rcParams["axes.titlesize"] = 26
    plt.rcParams["axes.labelsize"] = 22
    plt.rcParams["xtick.labelsize"] = 18
    plt.rcParams["ytick.labelsize"] = 18
    plt.rcParams["legend.fontsize"] = 18


def parse_inner_log(log_path: Path) -> RoundSeries:
    samples: list[tuple[int, float, float]] = []
    with log_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("iteration"):
                continue

            parts = [item.strip() for item in line.split(",")]
            if len(parts) < 11:
                continue

            try:
                iteration = int(float(parts[0]))
                total_net_length = float(parts[-10])
                temperature = float(parts[-5])
            except ValueError:
                continue

            samples.append((iteration, total_net_length, temperature))

    if not samples:
        raise ValueError(f"No valid rows found in {log_path}")

    samples.sort(key=lambda item: item[0])

    start_iter = samples[0][0]
    round_index = start_iter // 20 + 1
    iter_begin = (round_index - 1) * 20 + 1
    iter_end = round_index * 20

    iterations = [item[0] for item in samples]
    net_lengths = [item[1] for item in samples]
    temperatures = [item[2] for item in samples]

    min_iter, min_net, _ = min(samples, key=lambda item: item[1])

    return RoundSeries(
        round_index=round_index,
        iter_begin=iter_begin,
        iter_end=iter_end,
        iterations=iterations,
        net_lengths=net_lengths,
        temperatures=temperatures,
        start_iter=iterations[0],
        start_net=net_lengths[0],
        min_iter=min_iter,
        min_net=min_net,
    )


def save_round_plot(series: RoundSeries, out_dir: Path, out_format: str) -> Path:
    fig_width = 14.0
    fig_height = 7.2 / 2
    fig, ax_left = plt.subplots(figsize=(fig_width, fig_height))

    ax_left.plot(
        series.iterations,
        series.net_lengths,
        color="#E67E22",
        marker="o",
        linewidth=4.8,
        markersize=5.8,
        label="总线长",
    )
    ax_left.set_xlabel("迭代次数")
    ax_left.set_ylabel("总线长")
    ax_left.grid(axis="both", linestyle="--", alpha=0.30)

    x_min = min(series.iterations)
    x_max = max(series.iterations)
    ax_left.set_xlim(x_min - 0.5, x_max + 0.5)
    tick_count = x_max - x_min + 1
    tick_step = 1 if tick_count <= 12 else 2
    ax_left.set_xticks(list(range(x_min, x_max + 1, tick_step)))
    ax_left.xaxis.set_major_formatter(FormatStrFormatter("%d"))

    net_min = min(series.net_lengths)
    net_max = max(series.net_lengths)
    y_pad = max((net_max - net_min) * 0.15, 1.0)
    ax_left.set_ylim(net_min - y_pad, net_max + y_pad)

    ax_left.set_title(f"b20 第{series.round_index}轮模拟退火：总线长变化曲线", pad=18)
    ax_left.text(
        0.01,
        0.98,
        f"本轮迭代区间：{series.iter_begin}-{series.iter_end}",
        transform=ax_left.transAxes,
        ha="left",
        va="top",
        fontsize=22,
        color="#444444",
    )

    ax_left.legend(
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        frameon=False,
        borderaxespad=0.0,
    )

    min_ratio = (series.min_net / series.start_net) * 100.0

    ax_left.scatter([series.start_iter], [series.start_net], color="#A04000", s=70, zorder=5)
    ax_left.scatter([series.min_iter], [series.min_net], color="#922B21", s=70, zorder=5)

    def pick_offset(x_val: int, y_val: float) -> tuple[int, int, str, str]:
        x_left = x_min
        x_right = x_max
        y_bottom, y_top = ax_left.get_ylim()

        x_norm = (x_val - x_left) / max(x_right - x_left, 1)
        y_norm = (y_val - y_bottom) / max(y_top - y_bottom, 1e-9)

        if x_norm <= 0.20:
            dx, dy, ha, va = 34, -38, "left", "top"
        elif x_norm >= 0.80:
            dx = -34
            ha = "right"
            if y_norm <= 0.45:
                dy, va = 38, "bottom"
            else:
                dy, va = -38, "top"
        else:
            if y_norm >= 0.5:
                dx, ha = -34, "right"
                dy, va = -38, "top"
            else:
                dx, ha = 34, "left"
                dy, va = 38, "bottom"

        return dx, dy, ha, va

    start_dx, start_dy, start_ha, start_va = pick_offset(series.start_iter, series.start_net)
    min_dx, min_dy, min_ha, min_va = pick_offset(series.min_iter, series.min_net)

    ax_left.annotate(
        f"起点: {series.start_net:.3f}",
        xy=(series.start_iter, series.start_net),
        xytext=(start_dx, start_dy),
        textcoords="offset points",
        fontsize=26,
        ha=start_ha,
        va=start_va,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B0B0B0", alpha=0.9),
        arrowprops=dict(arrowstyle="->", color="#666666", lw=1.0),
    )

    ax_left.annotate(
        f"最低点: {series.min_net:.3f}\n相对初始: {min_ratio:.2f}%",
        xy=(series.min_iter, series.min_net),
        xytext=(min_dx, min_dy),
        textcoords="offset points",
        fontsize=26,
        ha=min_ha,
        va=min_va,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#B0B0B0", alpha=0.9),
        arrowprops=dict(arrowstyle="->", color="#666666", lw=1.0),
    )

    fig.tight_layout()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"chap4_b20_sa_round{series.round_index}_curve.{out_format}"
    fig.savefig(out_path, dpi=300, format=out_format, facecolor="white")
    plt.close(fig)
    return out_path


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    parser = argparse.ArgumentParser(description="Generate b20 SA curve figures for PPT.")
    parser.add_argument(
        "--log-dir",
        default=repo_root / "论文基础/b20模拟退火log",
        type=Path,
        help="Directory containing b20 SA logs",
    )
    parser.add_argument(
        "--format",
        choices=["png", "svg"],
        default="png",
        help="Output image format",
    )
    args = parser.parse_args()

    configure_matplotlib()

    log_dir = args.log_dir
    out_dir = script_dir

    inner_logs = [path for path in log_dir.glob("*.txt") if "dynamic_global" not in path.name]
    if not inner_logs:
        raise ValueError(f"No inner SA logs found in {log_dir}")

    rounds = [parse_inner_log(path) for path in inner_logs]
    rounds.sort(key=lambda item: item.round_index)

    for series in rounds:
        out_path = save_round_plot(series, out_dir, args.format)
        ratio = (series.min_net / series.start_net) * 100.0
        print(
            f"Round {series.round_index}: start={series.start_net:.3f}, "
            f"min={series.min_net:.3f} @ iter {series.min_iter}, "
            f"ratio={ratio:.2f}% -> {out_path}"
        )


if __name__ == "__main__":
    main()
