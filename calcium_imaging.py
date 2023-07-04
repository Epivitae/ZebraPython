# 计算并调整基线

for name in dir():
    if not name.startswith('_'):
        del globals()[name]

import pandas as pd
import matplotlib.pyplot as plt

# 从文件中读取数据
data = pd.read_csv('Calculate.csv')

# 设置窗口大小和阈值分位点
win = 300
perc = 0.1
threshold = int(win * perc)

# 计算基线并绘图
fig, axes = plt.subplots(len(data.columns) // 3 + 1, 3, figsize=(15, 4 * (len(data.columns) // 3 + 1)))
for i, col in enumerate(data.columns):
    ax = axes[i // 3, i % 3]
    col_data = data[col]
    baseline = []
    for j in range(win // 2, len(col_data) - win // 2):
        data_win = col_data[j - win // 2: j + win // 2 + 1]
        s = data_win.sort_values()
        baseline.append(s.iloc[threshold])
    baseline = [baseline[0]] * (win // 2) + baseline
    baseline.extend([baseline[-1]] * (win // 2))
    ax.plot(col_data)
    ax.plot(pd.Series(baseline).rolling(500, center=True, min_periods=1).mean())
plt.show()




#减去基线dF/F0

import pandas as pd
import matplotlib.pyplot as plt

# 从文件中读取数据
data = pd.read_csv('Calculate.csv')

# 设置窗口大小和阈值分位点
win = 500
perc = 0.1
threshold = int(win * perc)

# 计算基线并绘图
dFF0_data = pd.DataFrame()
for col in data.columns:
    col_data = data[col]
    baseline = []
    for i in range(win // 2, len(col_data) - win // 2):
        data_win = col_data[i - win // 2: i + win // 2 + 1]
        s = data_win.sort_values()
        baseline.append(s.iloc[threshold])
    baseline = [baseline[0]] * (win // 2) + baseline
    baseline.extend([baseline[-1]] * (win // 2))
    baseline = pd.Series(baseline).rolling(500, center=True, min_periods=1).mean()
    dFF0_col_data = (col_data - baseline) / baseline
    dFF0_data[col] = dFF0_col_data

# 将结果保存到文件中
dFF0_data.to_csv('dFF0.csv', index=False)




# Ploting

# Plotting
#plotting

import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv('dFF0.csv')

# 获取列标题
columns = data.columns

# 设置图形大小
fig, axs = plt.subplots(len(columns), 1, figsize=(3, 3))

# 遍历每一列
for i, col in enumerate(columns):
 # 绘制折线图
 axs[i].plot(data[col], label=col, linewidth=.5)
 # axs[i].set_ylim(1, 8)
 
 # 设置折线颜色
 if 'GFP' in col:
     axs[i].lines[-1].set_color('green')
 elif 'BFP' in col:
     axs[i].lines[-1].set_color('cyan')
 elif 'BRET' in col:
     axs[i].lines[-1].set_color('grey')
 
 # 设置标题位置
 axs[i].text(-0.05, 0, col, transform=axs[i].transAxes, ha='right', va='bottom', fontsize=3)
 
 # 隐藏坐标轴
 axs[i].axis('off')

# 调整子图间距
plt.subplots_adjust(hspace=-0.5)
plt.savefig('Results_dFF0.pdf', format='pdf')
# 显示图形
plt.show()
