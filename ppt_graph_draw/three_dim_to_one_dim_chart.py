import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体为Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16

# --- 1. 数据准备 ---
# 根据您提供的实际数据
labels = ['b11', 'b12', 'b13', 'b14', 'b15', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'SA3x3', 'SA4x4', 'SA5x5', 'Avg.']

# 我们的方法数据
our_data = {
    'Average Density': [0.651923077, 0.701585366, 0.701136364, 0.699394464, 0.702978723, 0.706256351, 0.717715709, 0.710104841, 0.701616488, 0.705285714, 0.703362045, 0.690702479, 0.693938523, 0.700717109, 0.699051232],
    'Density Standard Deviation': [0.378589006, 0.355441908, 0.355474816, 0.356937638, 0.34783296, 0.344203257, 0.372257276, 0.347937857, 0.354139299, 0.35803976, 0.347574983, 0.358711425, 0.353901431, 0.364460079, 0.35682155]
}

# 基线方法数据
baseline_data = {
    'Average Density': [0.650641026, 0.702682927, 0.701136364, 0.698226644, 0.700851064, 0.703403977, 0.712440991, 0.709109429, 0.702929885, 0.70155102, 0.703014726, 0.691193182, 0.694570526, 0.700845821, 0.698042684],
    'Density Standard Deviation': [0.385306537, 0.360612787, 0.350538866, 0.350896485, 0.342458919, 0.330654343, 0.327936843, 0.330221376, 0.349189379, 0.347218749, 0.340103318, 0.355134886, 0.351705078, 0.360829418, 0.348771927]
}
# labels = ['b17', 'b18', 'b19', 'CNN_ACC', 'booth', 'eth_top', 'Avg.']
# # 我们的方法数据
# our_data = {
# 'Average Density': [0.706641022, 0.717715709, 0.710104841, 0.707159984, 0.673007309, 0.723314924, 0.706323965],
# 'Density Standard Deviation': [0.348770974, 0.372257276, 0.347937857, 0.392689475, 0.333595707, 0.383778545, 0.363171639]
# }
# # 基线方法数据
# baseline_data = {
# 'Average Density': [0.703403977, 0.712440991, 0.709109429, 0.706165487, 0.674011589, 0.718975248, 0.704017787],
# 'Density Standard Deviation': [0.330654343, 0.327936843, 0.330221376, 0.347328809, 0.314894512, 0.340468891, 0.331917462]
# }


# labels = ['b11', 'b12', 'b13', 'b14', 'b15', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'Avg.']
# # 我们的方法数据
# our_data = {
# 'Average Density': [0.651923077, 0.701585366, 0.701136364, 0.698615917, 0.712341486, 0.706641022, 0.717715709, 0.710104841, 0.701454839, 0.705285714, 0.702653515, 0.700859805],
# 'Density Standard Deviation': [0.378589006, 0.355441908, 0.358446031, 0.355040065, 0.3432209, 0.348770974, 0.372257276, 0.347937857, 0.357795592, 0.35803976, 0.352817682, 0.357123368]
# }
# # 基线方法数据
# baseline_data = {
# 'Average Density': [0.650641026, 0.702682927, 0.701136364, 0.698226644, 0.700851064, 0.703403977, 0.712440991, 0.709109429, 0.702929885, 0.70155102, 0.703014726, 0.698726187],
# 'Density Standard Deviation': [0.385306537, 0.360612787, 0.350538866, 0.350896485, 0.342458919, 0.330654343, 0.327936843, 0.330221376, 0.349189379, 0.347218749, 0.340103318, 0.346830691]
# }





# labels = ['b11', 'b12', 'b13', 'b14', 'b15', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'SA3x3', 'SA4x4', 'SA5x5', 'R0', 'R1', 'R2', 'R3', 'R4', 'Avg.']
# # 我们的方法数据
# our_data = {
#     'Average Density': [0.651923077, 0.701585366, 0.701136364, 0.698615917, 0.712341486, 0.706641022, 0.717715709, 0.710104841, 0.701454839, 0.705285714, 0.702653515, 0.690702479, 0.693938523, 0.700717109, 0.651411879, 0.708060678, 0.723314924, 0.707159984, 0.673007309, 0.697777407],
#     'Density Standard Deviation': [0.378589006, 0.355441908, 0.358446031, 0.355040065, 0.3432209, 0.348770974, 0.372257276, 0.347937857, 0.357795592, 0.35803976, 0.352817682, 0.358711425, 0.353901431, 0.364460079, 0.380102464, 0.341411823, 0.383778545, 0.392689475, 0.333595707, 0.359842526]
# }
# # 基线方法数据
# baseline_data = {
#     'Average Density': [0.650641026, 0.702682927, 0.701136364, 0.698226644, 0.700851064, 0.703403977, 0.712440991, 0.709109429, 0.702929885, 0.70155102, 0.703014726, 0.691193182, 0.694570526, 0.700845821, 0.650503083, 0.708268888, 0.718975248, 0.706165487, 0.674011589, 0.696343257],
#     'Density Standard Deviation': [0.385306537, 0.360612787, 0.350538866, 0.350896485, 0.342458919, 0.330654343, 0.327936843, 0.330221376, 0.349189379, 0.347218749, 0.340103318, 0.355134886, 0.351705078, 0.360829418, 0.373506643, 0.320687711, 0.340468891, 0.347328809, 0.314894512, 0.34629966]
# }


'''

'''
'''
设计名称	components_num	avg_density	density_std	baseline_avg_density	baseline_density_std
b11	268	0.651923077	0.378589006	0.650641026	0.385306537
b12	660	0.701585366	0.355441908	0.702682927	0.360612787
b13	190	0.701136364	0.358446031	0.701136364	0.350538866
b14	2224	0.698615917	0.355040065	0.698226644	0.350896485
b15	4163	0.712341486	0.3432209	0.700851064	0.342458919
b17	12757	0.706641022	0.348770974	0.703403977	0.330654343
b18	29143	0.717715709	0.372257276	0.712440991	0.327936843
b19	56679	0.710104841	0.347937857	0.709109429	0.330221376
b20	4812	0.701454839	0.357795592	0.702929885	0.349189379
b21	4803	0.705285714	0.35803976	0.70155102	0.347218749
b22	7030	0.702653515	0.352817682	0.703014726	0.340103318
PE_array_3x3	3098	0.690702479	0.358711425	0.691193182	0.355134886
PE_array_4x4	5596	0.693938523	0.353901431	0.694570526	0.351705078
PE_array_5x5	8822	0.700717109	0.364460079	0.700845821	0.360829418
wb_dma_top	2064	0.651411879	0.380102464	0.650503083	0.373506643
tv80s	3493	0.708060678	0.341411823	0.708268888	0.320687711
eth_top	35659	0.723314924	0.383778545	0.718975248	0.340468891
CNN_ACC	37573	0.707159984	0.392689475	0.706165487	0.347328809
booth	117195	0.673007309	0.333595707	0.674011589	0.314894512
NVDLA	352764	0.704555622	0.156864072	0.704745783	0.135513147
ac97_top        7344   0.63586     0.198553872     0.63525      0.191759495  
aes_cipher_top  10091  0.7291      0.165873687     0.54323      0.284187996 
aes             3844   0.60937     0.239844659     0.60916      0.235220988 
des             1925   0.51962     0.280163808     0.51946      0.270063435 
pci_bridge32    10888  0.62905     0.192178648     0.62902      0.181481481
Avg.	28923.4	0.698660572	0.250875408	0.695629278	0.230349936


'''
# labels = ['b11', 'b12', 'b13', 'b14', 'b15', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'PE_array_3x3', 'PE_array_4x4', 'PE_array_5x5', 'wb_dma_top', 'tv80s', 'eth_top', 'CNN_ACC', 'booth', 'NVDLA', 'ac97_top', 'aes_cipher_top', 'aes', 'des', 'pci_bridge32', 'Avg.']
labels = ['b11', 'b12', 'b13', 'b14', 'b15', 'b17', 'b18', 'b19', 'b20', 'b21', 'b22', 'SA3x3', 'SA4x4', 'SA5x5', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', ' I0', 'I1', 'I2', 'I3', 'I4', 'Avg.']
# 我们的方法数据
our_data = {
    'Average Density': [0.651923077, 0.701585366, 0.701136364, 0.698615917, 0.712341486, 0.706641022, 0.717715709, 0.710104841, 0.701454839, 0.705285714, 0.702653515, 0.690702479, 0.693938523, 0.700717109, 0.651411879, 0.708060678, 0.723314924, 0.707159984, 0.673007309, 0.704555622, 0.63586, 0.7291, 0.60937, 0.51962, 0.62905, 0.698660572],
    'Density Standard Deviation': [0.378589006, 0.355441908, 0.358446031, 0.355040065, 0.3432209, 0.348770974, 0.372257276, 0.347937857, 0.357795592, 0.35803976, 0.352817682, 0.358711425, 0.353901431, 0.364460079, 0.380102464, 0.341411823, 0.383778545, 0.392689475, 0.333595707, 0.156864072, 0.198553872, 0.165873687, 0.239844659, 0.280163808, 0.192178648, 0.250875408]
}
# 基线方法数据
baseline_data = {
    'Average Density': [0.650641026, 0.702682927, 0.701136364, 0.698226644, 0.700851064, 0.703403977, 0.712440991, 0.709109429, 0.702929885, 0.70155102, 0.703014726, 0.691193182, 0.694570526, 0.700845821, 0.650503083, 0.708268888, 0.718975248, 0.706165487, 0.674011589, 0.704745783, 0.63525, 0.54323, 0.60916, 0.51946, 0.62902, 0.695629278],
    'Density Standard Deviation': [0.385306537, 0.360612787, 0.350538866, 0.350896485, 0.342458919, 0.330654343, 0.327936843, 0.330221376, 0.349189379, 0.347218749, 0.340103318, 0.355134886, 0.351705078, 0.360829418, 0.373506643, 0.320687711, 0.340468891, 0.347328809, 0.314894512, 0.135513147, 0.191759495, 0.284187996, 0.235220988, 0.270063435, 0.181481481, 0.230349936]
}





# --- 2. 图表绘制 ---
# 设置图表的总体布局 - 单个图表
fig, ax = plt.subplots(1, 1, figsize=(10, 4))

# 定义柱状图的宽度和位置
x = np.arange(len(labels))  # 标签位置
width = 0.2  # 柱子宽度，缩小以容纳4个柱子

# 提取数据
avg_density_baseline = baseline_data['Average Density']
avg_density_slime = our_data['Average Density']
density_std_baseline = baseline_data['Density Standard Deviation']
density_std_slime = our_data['Density Standard Deviation']

# 绘制4组柱状图
# 1. Average Density - Baseline (浅蓝色) - 无纹理
for j, (pos, height) in enumerate(zip(x - 1.5*width, avg_density_baseline)):
    ax.bar(pos, height, width, color='lightblue', edgecolor='black')

# 2. Average Density - Slime (深蓝色)
for j, (pos, height) in enumerate(zip(x - 0.5*width, avg_density_slime)):
    ax.bar(pos, height, width, color='tab:blue', edgecolor='black')

# 3. Density Std - Baseline (浅暗红色) - 根据右Y轴缩放，无纹理
density_std_baseline_scaled = [h * 2 for h in density_std_baseline]  # 右Y轴范围是0-0.5，左Y轴是0-1，所以乘以2
for j, (pos, height) in enumerate(zip(x + 0.5*width, density_std_baseline_scaled)):
    ax.bar(pos, height, width, color='#CD5C5C', edgecolor='black')

# 4. Density Std - Slime (深暗红色) - 根据右Y轴缩放
density_std_slime_scaled = [h * 2 for h in density_std_slime]  # 右Y轴范围是0-0.5，左Y轴是0-1，所以乘以2
for j, (pos, height) in enumerate(zip(x + 1.5*width, density_std_slime_scaled)):
    ax.bar(pos, height, width, color='#8B0000', edgecolor='black')

# 创建双Y轴
ax2 = ax.twinx()

# 设置左Y轴 (Average Density)
ax.set_ylabel('Average Density', fontsize=22, fontfamily='Times New Roman', fontweight='bold',color='tab:blue')
ax.set_ylim(0, 1.0)
ax.set_yticks(np.arange(0, 1.01, 0.2))
ax.tick_params(axis='y', labelcolor='tab:blue', labelsize=16)

# 设置右Y轴 (Density Standard Deviation)
ax2.set_ylabel('Density Stan-\ndard Deviation', fontsize=22, fontfamily='Times New Roman', fontweight='bold', color='#8B0000')
ax2.set_ylim(0, 0.5)
ax2.set_yticks(np.arange(0, 0.51, 0.1))
ax2.tick_params(axis='y', labelcolor='#8B0000', labelsize=16)

# 设置X轴
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=19, fontfamily='Times New Roman', rotation=60, fontweight='bold')

# 设置坐标轴刻度标签字体
for tick in ax.get_xticklabels():
    tick.set_fontfamily('Times New Roman')
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontfamily('Times New Roman')
    tick.set_fontweight('bold')
for tick in ax2.get_yticklabels():
    tick.set_fontfamily('Times New Roman')
    tick.set_fontweight('bold')

# 添加垂直分割线
for j in range(len(x) - 1):
    ax.axvline(x[j] + 0.5, color='gray', linestyle='-', alpha=0.3, linewidth=0.8)

# 显示网格线
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
ax.set_axisbelow(True) # 将网格线置于底层

# 创建图例：放在图表外侧上方，2行2列，四种颜色分别表示四组数据
from matplotlib.patches import Patch

legend_handles = [
    Patch(facecolor='lightblue', edgecolor='black', label='Avg. Density (Baseline)'),
    Patch(facecolor='tab:blue', edgecolor='black', label='Avg. Density (Slime)'),
    Patch(facecolor='#CD5C5C', edgecolor='black', label='Density Std (Baseline)'),
    Patch(facecolor='#8B0000', edgecolor='black', label='Density Std (Slime)'),
]

legend = ax.legend(
    handles=legend_handles,
    loc='lower center',
    bbox_to_anchor=(0.5, 1),
    ncol=2,
    fontsize=16,
    frameon=True,
    prop={'family': 'Times New Roman', 'weight': 'bold'},
    handlelength=1.5,
    handleheight=0.8,
    handletextpad=0.5,
    columnspacing=1.2,
    borderpad=0.4,
)

# --- 3. 显示图表 ---
plt.tight_layout(rect=[0, 0, 1, 0.85])
plt.show()

# --- 4. 保存图表 ---
# 保存为pdf
plt.savefig("density_comparison_b11-I4.pdf")