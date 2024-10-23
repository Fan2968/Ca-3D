import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os


def plot_dynamic_3D(csv_file, output_video):
    # 定义连线规则 (0-15对应1-16)
    lines_to_draw = [
        [0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [3, 5],
        [4, 8], [4, 12], [4, 6], [5, 9], [5, 12], [5, 7],
        [6, 10], [6, 13], [6, 12], [7, 12], [7, 11], [7, 13],
        [13, 14], [14, 15]
    ]

    # 生成颜色渐变
    def generate_colors(num):
        return plt.cm.plasma(np.linspace(0, 1, num))

    # 读取 CSV 文件
    df = pd.read_csv(csv_file, header=None)
    num_frames = df.shape[0]

    # 提取所有坐标点
    x = df.iloc[:, 0::3].values
    y = df.iloc[:, 1::3].values
    z = df.iloc[:, 2::3].values

    # 计算 z 轴的范围
    z_min = np.min(z)
    z_max = np.max(z)
    z_range = [z_min, z_max * 3]

    # 计算差值
    diff = (3 * z_max - z_min) / 3

    # 创建 3D 图形
    fig = plt.figure(facecolor='black', figsize=(10.8, 10.8))  # 设置为1080p
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    # 设置坐标轴范围
    ax.set_xlim([-300, 300])
    ax.set_ylim([-300, 300])
    ax.set_zlim(z_range)

    # 隐藏坐标轴刻度
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.xaxis.set_pane_color((0, 0, 0, 0))
    ax.yaxis.set_pane_color((0, 0, 0, 0))
    ax.zaxis.set_pane_color((0, 0, 0, 0))

    colors = generate_colors(16)

    # 动画更新函数
    def update(frame):
        ax.cla()  # 清除当前图形
        ax.set_facecolor('black')
        ax.set_xlim([-300, 300])
        ax.set_ylim([-300, 300])
        ax.set_zlim(z_range)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        # 绘制当前帧的点
        for i in range(16):
            ax.scatter(x[frame, i], y[frame, i], z[frame, i], color=colors[i], marker='o', s=100)

        # 按规则连接线
        for line in lines_to_draw:
            ax.plot(x[frame, line], y[frame, line], z[frame, line], color='white', linewidth=2)

        # 绘制外轮廓线
        ax.plot([-300, 300], [-300, -300], [z_min], color='white', linewidth=3)  # X轴
        ax.plot([300, 300], [-300, 300], [z_min], color='white', linewidth=3)  # Y轴
        ax.plot([-300, -300], [-300, -300], [z_min, 3 * z_max], color='white', linewidth=3)  # Z轴

        # 绘制参考线
        for wanggex in [-200, -100, 0, 100, 200]:
            ax.plot([wanggex, wanggex], [-300, 300], [z_min, z_min], color='white', alpha=0.3, linewidth=3)
            ax.plot([wanggex, wanggex], [300, 300], [z_min, 3 * z_max], color='white', alpha=0.3, linewidth=3)

        for wanggey in [-200, -100, 0, 100, 200]:
            ax.plot([-300, 300], [wanggey, wanggey], [z_min, z_min], color='white', alpha=0.3, linewidth=3)
            ax.plot([-300, -300], [wanggey, wanggey], [z_min, 3 * z_max], color='white', alpha=0.3, linewidth=3)

        # 使用新计算的差值绘制新的 z 参考线
        for wanggez in [z_min, z_min + diff, z_min + 2 * diff]:
            ax.plot([-300, -300], [-300, 300], [wanggez, wanggez], color='white', alpha=0.3, linewidth=3)

        for wanggez in [z_min, z_min + diff, z_min + 2 * diff]:
            ax.plot([-300, 300], [300, 300], [wanggez, wanggez], color='white', alpha=0.3, linewidth=3)

        # 在X轴上绘制短横线
        for x_tick in [-200, -100, 0, 100, 200]:
            ax.plot([x_tick, x_tick], [-310, -300], [z_min, z_min], color='white', linewidth=3)

        # 在Y轴上绘制短横线
        for y_tick in [-200, -100, 0, 100, 200]:
            ax.plot([310, 300], [y_tick, y_tick], [z_min, z_min], color='white', linewidth=3)

        # 在Z轴上绘制短横线
        for z_tick in [z_min, z_min + diff, z_min + 2 * diff]:
            ax.plot([-300, -300], [-310, -300], [z_tick, z_tick], color='white', linewidth=3)

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='z', colors='white')
        ax.grid(False)

    # 创建动画
    ani = FuncAnimation(fig, update, frames=num_frames, interval=200)

    # 保存动画为AVI格式，设置dpi为高分辨率
    ani.save(output_video, writer='ffmpeg', fps=10, dpi=300)

    plt.close(fig)  # 关闭图形以释放资源


#if __name__ == "__main__":
    # 指定 3D.csv 的路径
   # csv_file = r'D:\20241014beh_data_analysis\plot\plotdata\3D.csv'  # 修改为实际路径

    # 提取目录路径
  #  output_directory = os.path.dirname(csv_file)

    # 输出第一个视频（3D重建）
  #  output_video_3D = os.path.join(output_directory, 'output_video_3D.avi')
 #   plot_dynamic_3D(csv_file, output_video_3D)
