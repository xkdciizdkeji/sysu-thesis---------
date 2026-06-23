#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon


def pick_cjk_font() -> str | None:
    candidates = [
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "Source Han Sans CN",
        "Source Han Sans SC",
        "WenQuanYi Zen Hei",
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    for name in candidates:
        try:
            fm.findfont(name, fallback_to_default=False)
            return name
        except Exception:
            continue
    return None


def add_process(ax, center, text, width, height, fc="#f2f2f2", font_size=9):
    x, y = center
    rect = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4,
        edgecolor="black",
        facecolor=fc,
        zorder=2,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=font_size, zorder=3)


def add_decision(ax, center, text, width, height, fc="#f2f2f2", font_size=9):
    x, y = center
    points = [
        (x, y + height / 2),
        (x + width / 2, y),
        (x, y - height / 2),
        (x - width / 2, y),
    ]
    diamond = Polygon(
        points,
        closed=True,
        linewidth=1.4,
        edgecolor="black",
        facecolor=fc,
        zorder=2,
    )
    ax.add_patch(diamond)
    ax.text(x, y, text, ha="center", va="center", fontsize=font_size, zorder=3)


def add_arrow(ax, start, end, text=None, text_offset=(0.0, 0.3), font_size=9, align="center"):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.3,
        color="black",
        zorder=1,
    )
    ax.add_patch(arrow)
    if text:
        mx = (start[0] + end[0]) / 2 + text_offset[0]
        my = (start[1] + end[1]) / 2 + text_offset[1]
        ax.text(mx, my, text, ha=align, va="center", fontsize=font_size)


def add_poly_arrow(ax, points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color="black", linewidth=1.3, zorder=1)
    arrow = FancyArrowPatch(
        points[-2],
        points[-1],
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.3,
        color="black",
        zorder=1,
    )
    ax.add_patch(arrow)


def build_flowchart(width, height, output_path, dpi, out_format):
    font_name = pick_cjk_font()
    if font_name:
        mpl.rcParams["font.sans-serif"] = [font_name]
    mpl.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(width, height))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03)
    ax.set_aspect("equal")
    ax.axis("off")

    proc_w = 4.0
    proc_h = 1.0
    dec_w = 2.4
    dec_h = 1.0
    font_size = 9

    x_start = -21.0
    step = 4.2
    y_main = 0.0

    node_order = [
        ("in", "proc", "输入：初始约束与网表信息"),
        ("parse", "proc", "约束解析与边界合法化"),
        (
            "init",
            "proc",
            "初始化：\n" + r"$C_{\mathrm{best}}\leftarrow C_0,\ r\leftarrow 1,\ T\leftarrow T_0$",
        ),
        ("neighbor", "proc", "邻域扰动生成（五类操作）"),
        ("eval", "proc", "调用后端工具评估并计算\n" + r"$J(C_{\mathrm{new}})$"),
        ("accept", "proc", "Metropolis 接受/拒绝\n并更新本轮最优"),
        ("cool", "proc", "温度更新与迭代计数"),
        ("inner", "decision", "内层迭代结束？"),
        ("update", "proc", "更新全局最优并准备下一轮重启"),
        ("outer", "decision", "外层轮次结束？\n或连续无改进？"),
        ("out", "proc", "输出最优约束"),
    ]

    nodes = {}
    for idx, (key, kind, text) in enumerate(node_order):
        x = x_start + idx * step
        center = (x, y_main)
        if kind == "proc":
            nodes[key] = {"center": center, "width": proc_w, "height": proc_h}
            add_process(ax, center, text, proc_w, proc_h, font_size=font_size)
        else:
            nodes[key] = {"center": center, "width": dec_w, "height": dec_h}
            add_decision(ax, center, text, dec_w, dec_h, font_size=font_size)

    def top_of(key):
        x, y = nodes[key]["center"]
        return (x, y + nodes[key]["height"] / 2)

    def bottom_of(key):
        x, y = nodes[key]["center"]
        return (x, y - nodes[key]["height"] / 2)

    def left_of(key):
        x, y = nodes[key]["center"]
        return (x - nodes[key]["width"] / 2, y)

    def right_of(key):
        x, y = nodes[key]["center"]
        return (x + nodes[key]["width"] / 2, y)

    for i in range(len(node_order) - 1):
        key_a = node_order[i][0]
        key_b = node_order[i + 1][0]
        label = None
        if key_a == "inner" and key_b == "update":
            label = "是"
        if key_a == "outer" and key_b == "out":
            label = "是"
        add_arrow(
            ax,
            right_of(key_a),
            left_of(key_b),
            text=label,
            text_offset=(0.0, 0.35),
            font_size=font_size,
            align="center",
        )

    inner_x, inner_y = nodes["inner"]["center"]
    neighbor_x, neighbor_y = nodes["neighbor"]["center"]
    loop_inner_y = -2.8
    add_poly_arrow(
        ax,
        [
            bottom_of("inner"),
            (inner_x, loop_inner_y),
            (neighbor_x, loop_inner_y),
            bottom_of("neighbor"),
        ],
    )
    ax.text(inner_x + 0.2, (bottom_of("inner")[1] + loop_inner_y) / 2, "否", ha="left", va="center", fontsize=font_size)
    ax.text(
        (inner_x + neighbor_x) / 2,
        loop_inner_y - 0.35,
        "内层闭环",
        ha="center",
        va="center",
        fontsize=font_size,
    )

    outer_x, outer_y = nodes["outer"]["center"]
    init_x, init_y = nodes["init"]["center"]
    loop_outer_y = -4.6
    add_poly_arrow(
        ax,
        [
            bottom_of("outer"),
            (outer_x, loop_outer_y),
            (init_x, loop_outer_y),
            bottom_of("init"),
        ],
    )
    ax.text(outer_x + 0.2, (bottom_of("outer")[1] + loop_outer_y) / 2, "否", ha="left", va="center", fontsize=font_size)
    ax.text(
        (outer_x + init_x) / 2,
        loop_outer_y - 0.35,
        "外层闭环",
        ha="center",
        va="center",
        fontsize=font_size,
    )

    x_extents = [
        nodes[key]["center"][0] - nodes[key]["width"] / 2 for key in nodes
    ] + [
        nodes[key]["center"][0] + nodes[key]["width"] / 2 for key in nodes
    ]
    y_extents = [
        nodes[key]["center"][1] - nodes[key]["height"] / 2 for key in nodes
    ] + [
        nodes[key]["center"][1] + nodes[key]["height"] / 2 for key in nodes
    ]
    x_min = min(x_extents) - 0.8
    x_max = max(x_extents) + 0.8
    y_min = min(y_extents + [loop_outer_y]) - 0.8
    y_max = max(y_extents) + 0.8
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    fig.savefig(output_path, dpi=dpi, format=out_format, facecolor="white")
    plt.close(fig)


def main():
    script_dir = Path(__file__).resolve().parent
    default_out = script_dir / "chap4_sa_closed_loop_flow.png"

    parser = argparse.ArgumentParser(description="Draw the SA closed-loop flowchart for PPT.")
    parser.add_argument("--out", type=Path, default=default_out, help="Output image path")
    parser.add_argument("--format", choices=["png", "svg", "jpg"], default=None)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--width", type=float, default=13.5, help="Figure width (inches)")
    parser.add_argument("--height", type=float, default=7.5, help="Figure height (inches)")
    args = parser.parse_args()

    if args.width <= args.height:
        raise ValueError("width must be greater than height for PPT landscape layout")

    out_path = args.out
    out_format = args.format or out_path.suffix.lstrip(".") or "png"
    if out_path.suffix == "":
        out_path = out_path.with_suffix("." + out_format)

    build_flowchart(args.width, args.height, out_path, args.dpi, out_format)


if __name__ == "__main__":
    main()
