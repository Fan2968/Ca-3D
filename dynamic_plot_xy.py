import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
def plot_xy_projection(csv_file, output_video_xy):
    def generate_colors(num_colors):
        """生成指定数量的颜色，用于绘制散点图"""
        colors = plt.cm.viridis(range(num_colors))
        return colors

    # 读取 CSV 文件
    df = pd.read_csv(csv_file, header=None)
    num_frames = df.shape[0]

    # 提取所有坐标点
    x = df.iloc[:, 0::3].values
    y = df.iloc[:, 1::3].values

    # 定义连线规则 (0-15对应1-16)
    lines_to_draw = [
        [0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [3, 5],
        [4, 8], [4, 12], [4, 6], [5, 9], [5, 12], [5, 7],
        [6, 10], [6, 13], [6, 12], [7, 12], [7, 11], [7, 13],
        [13, 14], [14, 15]
    ]

    # 创建 2D 图形
    fig, ax = plt.subplots(figsize=(1080 / 100, 1080 / 100))  # 设置为1080p
    fig.patch.set_facecolor('black')  # 设置整个图形背景为黑色
    ax.set_facecolor('black')  # 设置坐标轴背景为黑色


    # 设置坐标轴范围
    ax.set_xlim([-300, 300])
    ax.set_ylim([-300, 300])

    # 隐藏坐标轴刻度
    ax.set_xticks([])
    ax.set_yticks([])

    # 动画更新函数
    colors = generate_colors(16)  # 生成16种颜色

    def update(frame):
        ax.cla()  # 清除当前图形
        ax.set_facecolor('black')

        # 设置坐标轴范围
        ax.set_xlim([-300, 300])
        ax.set_ylim([-300, 300])

        # 隐藏坐标轴刻度
        ax.set_xticks([])
        ax.set_yticks([])

        # 绘制当前帧的投影点
        for i in range(16):
            ax.scatter(x[frame][i], y[frame][i], color=colors[i], marker='o', s=100)

        # 按规则连接线的投影
        for line in lines_to_draw:
            ax.plot(x[frame][line], y[frame][line], color='white', linewidth=2)

        # 绘制外轮廓线
        ax.plot([-300, 300], [-300, -300], color='white', linewidth=3)  # 底边
        ax.plot([-300, 300], [300, 300], color='white', linewidth=3)  # 顶边
        ax.plot([300, 300], [-300, 300], color='white', linewidth=3)  # 右边
        ax.plot([-300, -300], [-300, 300], color='white', linewidth=3)  # 左边

        # 绘制参考线
        for wanggex in [-200, -100, 0, 100, 200]:
            ax.plot([wanggex, wanggex], [-300, 300], color='white', alpha=0.3, linewidth=3)

        for wanggey in [-200, -100, 0, 100, 200]:
            ax.plot([-300, 300], [wanggey, wanggey], color='white', alpha=0.3, linewidth=3)

        # 在X轴上绘制短横线
        for x_tick in [-200, -100, 0, 100, 200]:
            ax.plot([x_tick, x_tick], [-300, -290], color='white', linewidth=3)
            ax.plot([x_tick, x_tick], [290, 300], color='white', linewidth=3)

        # 在Y轴上绘制短横线
        for y_tick in [-200, -100, 0, 100, 200]:
            ax.plot([290, 300], [y_tick, y_tick], color='white', linewidth=3)
            ax.plot([-300, -290], [y_tick, y_tick], color='white', linewidth=3)

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(False)

    # 创建动画
    ani = FuncAnimation(fig, update, frames=num_frames, interval=200)

    # 保存动画为AVI格式，设置dpi为高分辨率
    ani.save(output_video_xy, writer='ffmpeg', fps=10, dpi=300)

    plt.close(fig)  # 关闭图形以释放资源


if __name__ == "__main__":
    # 指定 3D.csv 的路径
    csv_file = r'D:\20241014beh_data_analysis\plot\plotdata\3D.csv'  # 修改为实际路径

    # 提取目录路径
    output_directory = os.path.dirname(csv_file)

    output_video_xy = os.path.join(output_directory, 'output_video_xy.avi')
    plot_xy_projection(csv_file, output_video_xy)
