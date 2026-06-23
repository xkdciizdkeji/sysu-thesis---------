import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Global font settings
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 16

# --- 1. Data from the thesis runtime table (chap03) ---
case_labels = [
    "18_1", "18_2", "18_3", "18_4", "18_5", "18_6", "18_7", "18_8", "18_9", "18_10",
    "19_1", "19_2", "19_3", "19_4", "19_5", "19_6", "19_7", "19_8", "19_9", "19_10",
    "18_5m", "18_8m", "18_10m", "19_7m", "19_8m", "19_9m",
    "ariane51", "ariane68", "bsg", "mempool", "nvdla",
]

template_dgr = [
    0.406, 2.449, 3.960, 8.102, 9.970, 11.481, 20.980, 21.452, 18.547, 24.852,
    0.594, 8.566, 1.347, 12.242, 2.883, 23.178, 48.208, 45.531, 72.277, 87.520,
    9.525, 26.336, 23.532, 39.872, 49.075, 71.800,
    11.098, 13.737, 83.150, 12.295, 36.782,
]

template_ours = [
    0.385, 1.974, 2.988, 9.085, 7.287, 11.316, 22.589, 23.536, 17.061, 38.808,
    0.416, 9.327, 2.718, 27.684, 4.884, 24.068, 53.710, 47.037, 70.102, 69.749,
    16.659, 44.830, 54.194, 53.806, 78.097, 105.283,
    13.910, 14.236, 111.166, 14.165, 43.522,
]

total_dgr = [
    0.771, 4.438, 6.628, 14.505, 16.479, 19.968, 39.438, 42.418, 33.700, 48.740,
    0.867, 15.794, 1.985, 28.157, 4.760, 40.585, 85.605, 87.059, 138.643, 169.474,
    17.827, 50.760, 56.098, 87.752, 107.168, 156.127,
    23.369, 26.481, 162.301, 23.919, 72.248,
]

total_ours = [
    0.583, 3.520, 4.699, 13.951, 12.495, 17.291, 36.520, 37.731, 28.286, 56.058,
    0.622, 14.394, 3.110, 38.278, 6.198, 38.347, 79.901, 79.077, 122.374, 127.147,
    22.711, 62.391, 80.623, 91.396, 128.112, 177.494,
    24.676, 23.929, 168.232, 22.416, 64.782,
]

# Normalized runtime per case (relative to ours)
template_dgr_norm = [d / o for d, o in zip(template_dgr, template_ours)]
template_ours_norm = [1.0] * len(template_ours)

total_dgr_norm = [d / o for d, o in zip(total_dgr, total_ours)]
total_ours_norm = [1.0] * len(total_ours)

# Append average row values from the thesis table (already normalized)
labels = case_labels + ["Avg."]
template_dgr_norm.append(0.806)
template_ours_norm.append(1.0)
total_dgr_norm.append(0.998)
total_ours_norm.append(1.0)

# --- 2. Plot ---
fig, axes = plt.subplots(2, 1, figsize=(16, 8), sharex=True)

x = np.arange(len(labels))
width = 0.3
avg_idx = len(labels) - 1

# Template routing runtime subplot
axes[0].bar(x - width / 2, template_dgr_norm, width, color="lightblue", edgecolor="black")
axes[0].bar(x + width / 2, template_ours_norm, width, color="tab:blue", edgecolor="black")
axes[0].set_ylabel("Normalized Pattern Routing Runtime", fontsize=15, fontfamily="Times New Roman", fontweight="bold", color="tab:blue")
axes[0].set_ylim(0.4, 1.4)
axes[0].set_yticks(np.arange(0.4, 1.41, 0.2))
axes[0].tick_params(axis="y", labelcolor="tab:blue", labelsize=14)
axes[0].text(
    avg_idx - width / 2,
    template_dgr_norm[-1] + 0.03,
    f"{template_dgr_norm[-1]:.3f}",
    ha="center",
    va="bottom",
    fontsize=11,
    fontweight="bold",
    rotation=90,
)
axes[0].text(
    avg_idx + width / 2,
    template_ours_norm[-1] + 0.03,
    f"{template_ours_norm[-1]:.3f}",
    ha="center",
    va="bottom",
    fontsize=11,
    fontweight="bold",
    rotation=90,
)
axes[0].legend(
    handles=[
        Patch(facecolor="lightblue", edgecolor="black", label="DGR"),
        Patch(facecolor="tab:blue", edgecolor="black", label="Ours"),
    ],
    loc="upper center",
    # bbox_to_anchor=(0.5, 1.12),
    ncol=2,
    fontsize=12,
    frameon=True,
    prop={"family": "Times New Roman", "weight": "bold"},
)

# Total runtime subplot
axes[1].bar(x - width / 2, total_dgr_norm, width, color="#B0C4DE", edgecolor="black")
axes[1].bar(x + width / 2, total_ours_norm, width, color="#1E90FF", edgecolor="black")
axes[1].set_ylabel("Normalized Total Runtime", fontsize=15, fontfamily="Times New Roman", fontweight="bold", color="#1E90FF")
axes[1].set_ylim(0.4, 1.5)
axes[1].set_yticks(np.arange(0.4, 1.51, 0.2))
axes[1].tick_params(axis="y", labelcolor="#1E90FF", labelsize=14)
axes[1].text(
    avg_idx - width / 2,
    total_dgr_norm[-1] + 0.03,
    f"{total_dgr_norm[-1]:.3f}",
    ha="center",
    va="bottom",
    fontsize=11,
    fontweight="bold",
    rotation=90,
)
axes[1].text(
    avg_idx + width / 2,
    total_ours_norm[-1] + 0.03,
    f"{total_ours_norm[-1]:.3f}",
    ha="center",
    va="bottom",
    fontsize=11,
    fontweight="bold",
    rotation=90,
)
axes[1].legend(
    handles=[
        Patch(facecolor="#B0C4DE", edgecolor="black", label="DGR"),
        Patch(facecolor="#1E90FF", edgecolor="black", label="Ours"),
    ],
    loc="upper center",
    # bbox_to_anchor=(0.5, 1.12),
    ncol=2,
    fontsize=12,
    frameon=True,
    prop={"family": "Times New Roman", "weight": "bold"},
)

# Shared X axis
axes[1].set_xticks(x)
axes[1].set_xticklabels(labels, fontsize=16, fontfamily="Times New Roman", rotation=60, fontweight="bold")

# Tick label fonts and gridlines
for ax in axes:
    for tick in ax.get_yticklabels():
        tick.set_fontfamily("Times New Roman")
        tick.set_fontweight("bold")
    ax.yaxis.grid(True, linestyle="--", which="major", color="grey", alpha=0.25)
    ax.set_axisbelow(True)
    for j in range(len(x) - 1):
        ax.axvline(x[j] + 0.5, color="gray", linestyle="-", alpha=0.3, linewidth=0.8)

# --- 3. Save and show ---
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("three_dim_to_one_dim_chart_run_time.png", dpi=300)
plt.savefig("three_dim_to_one_dim_chart_run_time.pdf")
plt.show()
