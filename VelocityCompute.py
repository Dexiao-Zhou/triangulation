import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import csv

from scipy.interpolate import make_interp_spline

def edge_extend(arr, extend_size=1):
    """对数组进行边缘扩展"""
    front = [arr[0]] * extend_size
    end = [arr[-1]] * extend_size
    return np.concatenate([front, arr, end])

def moving_average(y, window_size):
    """计算移动平均"""
    return np.convolve(y, np.ones(window_size) / window_size, mode='same')

def calculate_speeds(points, time_interval):
    """
    根据一系列点及相邻两点之间的时间间隔计算每段的速度。

    :param points: 一个包含多个(x, y)坐标的列表，表示一系列点。
    :param time_interval: 相邻两点之间的时间间隔。
    :return: 每两个连续点之间的速度列表。
    """
    speeds = []
    # 遍历点列表，除了最后一个点
    for i in range(len(points) - 1):
        point1 = points[i]
        point2 = points[i + 1]
        # 计算两点之间的距离
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        # 计算速度并添加到列表中
        speed = distance / time_interval
        speeds.append(speed)
    return speeds


# 读取CSV文件
df1 = pd.read_csv('/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/triangles.csv', delimiter=',', quotechar='"')
df2 = pd.read_csv('/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/rectangles.csv', delimiter=',', quotechar='"')

# 通过不同颜色找出目标点
# 选择感兴趣的行，这里假设我们关注索引为4的行（即第5行）
T_x1, T_y1 = df1.iloc[1, 1], df1.iloc[1, 2]  # iloc使用的是基于位置的索引，索引从0开始，所以第4列的索引是3
T_x2, T_y2 = df1.iloc[1, 3], df1.iloc[1, 4]
T_x3, T_y3 = df1.iloc[1, 5], df1.iloc[1, 6]

R_x1, R_y1 = df2.iloc[1, 3], df2.iloc[1, 4]  # iloc使用的是基于位置的索引，索引从0开始，所以第4列的索引是3
R_x2, R_y2 = df2.iloc[1, 5], df2.iloc[1, 6]
R_x3, R_y3 = df2.iloc[1, 7], df2.iloc[1, 8]
R_x4, R_y4 = df2.iloc[1, 9], df2.iloc[1, 10]

# 绘制该行的数据。由于行数据是按列索引排序的，我们可以直接绘制。
plt.scatter(T_x1, T_y1, color='red')
plt.scatter(T_x2, T_y2, color='green')
plt.scatter(T_x3, T_y3, color='black')
plt.scatter([R_x1, R_x2, R_x3, R_x4], [R_y1, R_y2, R_y3, R_y4], color='blue')


plt.xlim(0, 1920)
plt.ylim(1080,0)

plt.title('Plot of the Point from First Row')
plt.xlabel('Column 5 Value')
plt.ylabel('Column 6 Value')
plt.grid(True)
plt.show()

P2_x = df1.iloc[:, 3].values  # 获取第4列的所有数据
P2_y = df1.iloc[:, 4].values  # 获取第5列的所有数据

P2_x_extended = edge_extend(P2_x, extend_size=5)
P2_y_extended = edge_extend(P2_y, extend_size=5)

# 创建用于绘制的平滑点
x_smooth = moving_average(P2_x_extended, window_size=3)
y_smooth = moving_average(P2_y_extended, window_size=3)
# 去除扩展的边缘部分
x_smooth = x_smooth[1:-1]
y_smooth = y_smooth[1:-1]

# 使用zip将P2_x和P2_y组合成点的列表，然后将其转换为列表类型
points = list(zip(x_smooth, y_smooth))

time_interval = 0.0333
# 假设这是你计算得到的速度列表
speeds = calculate_speeds(points, time_interval)

# 创建速度的索引列表，用于x轴
# speed_indices = range(1, len(speeds) + 1)
N = len(speeds)
total_time = 10  # 总时间为10秒
# 生成对应每个速度点的时间戳列表
time_stamps = np.linspace(1, total_time, N)

# 将数据保存到CSV文件中
with open('/Users/zhoudexiao/Desktop/Project/triangulation/frames 3/SpeedData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Index', 'Value'])  # 写入标题行
    for i, value in enumerate(speeds, 1):  # 枚举数据并写入CSV
        writer.writerow([i, value])

# speeds_smooth = moving_average(speeds, window_size=3)
# 绘制速度图像
plt.plot(time_stamps, speeds, marker='o', linestyle='-', color='b', label='Speed')
# 添加图表标题和坐标轴标签
plt.title('Speed between Consecutive Points')
plt.xlabel('Segment Number')
plt.ylabel('Speed (units per second)')

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)

# 显示图表
plt.show()
