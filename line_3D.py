import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os


def generate_colors(num):
    """生成指定数量的颜色，用于绘制折线图"""
    return plt.cm.plasma(np.linspace(0, 1, num))


def plot_dynamic_line_chart(csv_file, output_video_line):
    # 读取 CSV 文件
    print(f"读取数据文件: {csv_file}")
    df = pd.read_csv(csv_file, header=None)

    # 确保数据有48列
    if df.shape[1] != 48:
        raise ValueError("数据文件必须包含48列。")

    num_frames = df.shape[0]

    # 提取所有坐标点
    z = df.values  # 直接获取所有数据
    num_columns = z.shape[1]  # 列数应为48
    num_color_groups = num_columns // 3  # 每三列使用同一种颜色

    # 生成16种颜色
    colors = generate_colors(num_color_groups)

    # 获取 z 数据的最小值和最大值
    data_min = np.min(z)
    data_max = np.max(z)

    ### 创建折线图 ###
    print("开始创建折线图动画...")

    # 输出总折线数
    print(f"总折线数: {num_columns}")

    fig_line, ax_line = plt.subplots(figsize=(10, 5), facecolor='black')

    # 设置 Y 轴范围
    ax_line.set_ylim(data_min - 5, data_max + 5)  # 稍微增加一些缓冲
    ax_line.set_facecolor('black')  # 设置背景为黑色

    # 设置 Y 轴的颜色为白色
    ax_line.spines['left'].set_color('none')  # 左侧 Y 轴不显示
    ax_line.spines['top'].set_color('none')  # 上侧边框不显示
    ax_line.spines['right'].set_color('none')  # 右侧不显示
    ax_line.yaxis.set_visible(False)  # 完全隐藏 Y 轴
    ax_line.spines['bottom'].set_color('white')  # X 轴底边框颜色


    print(f"数据最小值: {data_min}, 数据最大值: {data_max}")

    def update_line(frame):
        ax_line.cla()
        ax_line.set_facecolor('black')
        ax_line.set_ylim(data_min - 5, data_max + 5)

        # 当前帧数
        t = frame

        # 设置 X 轴范围
        ax_line.set_xlim(t - 150, t + 150)

        # 在当前帧位置添加灰色虚线
        ax_line.axvline(t, color='white', linestyle='--')

        # 计算时间范围
        start_frame = max(0, t - 150)
        end_frame = min(num_frames, t + 150)

        # 绘制数据
        for i in range(num_columns):
            if start_frame < end_frame:
                # 绘制每个系列的折线，按组的颜色
                color_index = i // 3  # 每三列使用同一种颜色
                ax_line.plot(range(start_frame, end_frame), z[start_frame:end_frame, i], color=colors[color_index])

        ax_line.set_title(f'Frame: {frame}, Time: {frame / 30:.2f}s', color='white')

        # 设置 X 轴的刻度
        ticks = np.arange(t - 150, t + 151, 1)  # 每一帧都有刻度
        ax_line.set_xticks(ticks)

        # 生成刻度标签，仅在能被60整除的帧数上显示
        labels = [f"{(tick / 30):.0f}s" if tick % 60 == 0 else "" for tick in ticks]
        ax_line.set_xticklabels(labels, color='white')

        # 设置 X 轴的 ticks 样式
        ax_line.tick_params(axis='x', which='both', length=6, color='white')

        # 只显示 ticks 在能被60整除的刻度位置
        for tick in ticks:
            if tick % 60 != 0:
                ax_line.xaxis.get_major_ticks()[np.where(ticks == tick)[0][0]].set_visible(False)

    # 创建折线图动画
    ani_line = FuncAnimation(fig_line, update_line, frames=num_frames, interval=1000 / 30)
    ani_line.save(output_video_line, writer='ffmpeg', fps=30, dpi=300)

    print(f"折线图动画已保存为: {output_video_line}")
    plt.close(fig_line)  # 关闭折线图以释放资源


if __name__ == "__main__":
    # 指定 CSV 文件的路径
    csv_file = r'D:\20241014beh_data_analysis\plot\plotdata\3D.csv'  # 修改为实际路径
    output_directory = os.path.dirname(csv_file)

    # 输出视频文件名
    output_video_line = os.path.join(output_directory, '3D_data_line_video.avi')

    # 调用折线图函数
    plot_dynamic_line_chart(csv_file, output_video_line)
