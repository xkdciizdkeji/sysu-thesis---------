import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Global font settings
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 16

# --- 1. Data from the thesis table (chap03, main results) ---
case_labels = [
    "18_1", "18_2", "18_3", "18_4", "18_5", "18_6", "18_7", "18_8", "18_9", "18_10",
    "19_1", "19_2", "19_3", "19_4", "19_5", "19_6", "19_7", "19_8", "19_9", "19_10",
    "18_5m", "18_8m", "18_10m", "19_7m", "19_8m", "19_9m",
    "ariane51", "ariane68", "bsg", "mempool", "nvdla",
]

wl_cugr2 = [
    409081, 7603188, 8531627, 25620922, 26719280, 34220480, 62761893, 62964888, 52494024, 65090544,
    601511, 23943128, 774750, 25287922, 4220085, 63649578, 117043233, 180606119, 272442799, 268638004,
    25555635, 58877869, 62480282, 101591635, 166178884, 254881352,
    18593148, 18895608, 116192206, 16820490, 42556632,
]
wl_dgr = [
    409081, 7603188, 8531627, 25635707, 26740190, 34241555, 62817858, 63029328, 52502349, 65154399,
    601511, 23955842, 774930, 25658050, 4254615, 63702168, 117206163, 180803724, 272513104, 268780621,
    25703970, 59282854, 62833202, 101996635, 166808599, 255467552,
    18626426, 18970596, 116649953, 16866961, 42917424,
]
wl_ours = [
    409081, 7603188, 8531627, 25635647, 26740460, 34253465, 62824848, 63042633, 52499784, 65187579,
    601511, 23959649, 774930, 25861815, 4257945, 63728853, 117242118, 180787644, 272519239, 268785745,
    25709175, 59346019, 62983817, 102138325, 166996084, 255691772,
    18629236, 18969990, 116782852, 16874116, 43086075,
]

via_cugr2 = [
    32454, 357967, 360466, 772767, 896347, 1347248, 2206523, 2251453, 2241545, 2368014,
    38499, 808496, 65079, 755438, 156680, 2045541, 3808931, 6298931, 10488012, 9646345,
    873683, 2171062, 2260680, 3787758, 6236992, 10396151,
    1004753, 956737, 6319828, 1135001, 1452197,
]
via_dgr = [
    32454, 357967, 360454, 772777, 896803, 1347311, 2207719, 2252852, 2242142, 2370408,
    38499, 808731, 65103, 761515, 157145, 2047428, 3818624, 6299926, 10491391, 9647443,
    876918, 2178494, 2268622, 3803429, 6249606, 10413501,
    1007282, 960909, 6337012, 1139491, 1458950,
]
via_ours = [
    32454, 357967, 360454, 772746, 896795, 1347210, 2207628, 2252911, 2242107, 2370994,
    38499, 808740, 65103, 764535, 157235, 2047201, 3818762, 6300058, 10491625, 9647812,
    876921, 2180373, 2271584, 3807167, 6253175, 10417961,
    1008121, 962133, 6341978, 1141860, 1461924,
]

of_cugr2 = [
    0, 0, 0, 1174, 75, 428, 27862, 27876, 1011, 1796,
    0, 324, 7, 214888, 29060, 36860, 14401, 20059, 361, 23318,
    63993, 116252, 46630, 137601, 353260, 346328,
    5430, 22159, 224133, 5689, 300135,
]
of_dgr = [
    0, 0, 0, 0, 0, 71, 8783, 8771, 31, 5947,
    0, 71, 4, 186082, 21128, 8739, 33020, 145, 206, 7318,
    43113, 81451, 102268, 124958, 288230, 290530,
    382, 2427, 119506, 3074, 167646,
]
of_ours = [
    0, 0, 0, 0, 0, 0, 1058, 960, 0, 6069,
    0, 14, 4, 147072, 20585, 1210, 14747, 0, 0, 6094,
    37995, 53893, 101799, 114034, 252105, 264645,
    66, 754, 52542, 1814, 52154,
]

# Normalized wirelength per case (relative to ours)
wl_cugr2_norm = [c / o for c, o in zip(wl_cugr2, wl_ours)]
wl_dgr_norm = [d / o for d, o in zip(wl_dgr, wl_ours)]
wl_ours_norm = [1.0] * len(wl_ours)

# Normalized overflow by total ours overflow to keep a stable scale
total_of_ours = sum(of_ours) if sum(of_ours) > 0 else 1.0
of_cugr2_norm = [v / total_of_ours for v in of_cugr2]
of_dgr_norm = [v / total_of_ours for v in of_dgr]
of_ours_norm = [v / total_of_ours for v in of_ours]

# Normalized via per case (relative to ours)
via_cugr2_norm = [c / o for c, o in zip(via_cugr2, via_ours)]
via_dgr_norm = [d / o for d, o in zip(via_dgr, via_ours)]
via_ours_norm = [1.0] * len(via_ours)

# Append average row values from the thesis table (already normalized)
labels = case_labels + ["Avg."]
wl_cugr2_norm.append(0.997168)
wl_dgr_norm.append(0.999355)
wl_ours_norm.append(1.0)
via_cugr2_norm.append(0.998059)
via_dgr_norm.append(0.999604)
via_ours_norm.append(1.0)
of_cugr2_norm.append(1.789204)
of_dgr_norm.append(1.331341)
of_ours_norm.append(1.0)

# --- 2. Plot ---
fig, axes = plt.subplots(3, 1, figsize=(16, 8), sharex=True)

x = np.arange(len(labels))
width = 0.25

# Wirelength subplot
axes[0].bar(x - width, wl_cugr2_norm, width, color="lightblue", edgecolor="black")
axes[0].bar(x, wl_dgr_norm, width, color="tab:blue", edgecolor="black")
axes[0].bar(x + width, wl_ours_norm, width, color="navy", edgecolor="black")
axes[0].set_ylabel("Normalized Wirelength", fontsize=20, fontfamily="Times New Roman", fontweight="bold", color="tab:blue")
axes[0].set_ylim(0.90, 1.05)
axes[0].set_yticks(np.arange(0.90, 1.051, 0.02))
axes[0].tick_params(axis="y", labelcolor="tab:blue", labelsize=14)
axes[0].legend(
    handles=[
        Patch(facecolor="lightblue", edgecolor="black", label="CUGR2"),
        Patch(facecolor="tab:blue", edgecolor="black", label="DGR"),
        Patch(facecolor="navy", edgecolor="black", label="Ours"),
    ],
    loc="upper center",
    # bbox_to_anchor=(0.5, 1.12),
    ncol=3,
    fontsize=12,
    frameon=True,
    prop={"family": "Times New Roman", "weight": "bold"},
)

# Via subplot
axes[1].bar(x - width, via_cugr2_norm, width, color="#B7E4C7", edgecolor="black")
axes[1].bar(x, via_dgr_norm, width, color="#74C69D", edgecolor="black")
axes[1].bar(x + width, via_ours_norm, width, color="#40916C", edgecolor="black")
axes[1].set_ylabel("Normalized Via", fontsize=20, fontfamily="Times New Roman", fontweight="bold", color="#40916C")
axes[1].set_ylim(0.90, 1.05)
axes[1].set_yticks(np.arange(0.90, 1.051, 0.02))
axes[1].tick_params(axis="y", labelcolor="#40916C", labelsize=14)
axes[1].legend(
    handles=[
        Patch(facecolor="#B7E4C7", edgecolor="black", label="CUGR2"),
        Patch(facecolor="#74C69D", edgecolor="black", label="DGR"),
        Patch(facecolor="#40916C", edgecolor="black", label="Ours"),
    ],
    loc="upper center",
    # bbox_to_anchor=(0.5, 1.12),
    ncol=3,
    fontsize=12,
    frameon=True,
    prop={"family": "Times New Roman", "weight": "bold"},
)

# Overflow subplot
axes[2].bar(x - width, of_cugr2_norm, width, color="#CD5C5C", edgecolor="black")
axes[2].bar(x, of_dgr_norm, width, color="#8B0000", edgecolor="black")
axes[2].bar(x + width, of_ours_norm, width, color="red", edgecolor="black")
axes[2].set_ylabel("Normalized Overflow", fontsize=20, fontfamily="Times New Roman", fontweight="bold", color="#8B0000")
axes[2].set_ylim(0.0, 2.0)
axes[2].set_yticks(np.arange(0.0, 2.01, 0.5))
axes[2].tick_params(axis="y", labelcolor="#8B0000", labelsize=14)
axes[2].legend(
    handles=[
        Patch(facecolor="#CD5C5C", edgecolor="black", label="CUGR2"),
        Patch(facecolor="#8B0000", edgecolor="black", label="DGR"),
        Patch(facecolor="red", edgecolor="black", label="Ours"),
    ],
    loc="upper center",
    # bbox_to_anchor=(0.5, 1.12),
    ncol=3,
    fontsize=12,
    frameon=True,
    prop={"family": "Times New Roman", "weight": "bold"},
)

# Shared X axis
axes[2].set_xticks(x)
axes[2].set_xticklabels(labels, fontsize=16, fontfamily="Times New Roman", rotation=60, fontweight="bold")

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
plt.savefig("three_dim_to_one_dim_chart_main_result.png", dpi=300)
plt.savefig("three_dim_to_one_dim_chart_main_result.pdf")
plt.show()
