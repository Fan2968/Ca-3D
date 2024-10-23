import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import glob


def process_dff_data(start_row, end_row, input_folder, output_path):
    print("开始读取数据...")

    # 找到唯一的xlsx文件
    dff_files = glob.glob(os.path.join(input_folder, '*.xlsx'))
    if not dff_files:
        print("未找到xlsx文件。")
        return
    dff_path = dff_files[0]

    # 读取数据
    df = pd.read_excel(dff_path, skiprows=1)  # 忽略第一行
    print("数据读取完成。")

    # 提取所需数据
    print(f"提取数据行: {start_row} 到 {end_row}...")
    data = df.iloc[start_row:end_row].to_numpy()
    print("数据提取完成。")

    # 计算均值和标准差
    print("计算均值和标准差...")
    mean = np.mean(data)
    sd = np.std(data)
    print(f"均值: {mean}, 标准差: {sd}")

    # 计算阈值
    threshold = mean + 3 * sd
    print(f"计算阈值: {threshold}")

    # 替换数据
    print("替换数据...")
    new_data = np.where(data > threshold, data, threshold)
    print("数据替换完成。")

    # 创建视频
    print("开始创建视频...")

    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 5), facecolor='black')
    ax_heatmap.set_facecolor('black')  # 设置背景为黑色

    # 获取 z 数据的最小值和最大值
    data_min = np.min(new_data)
    data_max = np.max(new_data)

    def update(frame):
        ax_heatmap.cla()

        # 定义当前帧
        t = frame  # 当前帧
        start_frame = max(0, t - 150)
        end_frame = min(new_data.shape[0], t + 150)

        displayed_data = new_data[start_frame:end_frame, :]  # 提取显示的数据

        # 绘制热图
        im = ax_heatmap.imshow(displayed_data.T, aspect='auto', cmap='gray', vmin=data_min, vmax=data_max)

        # 设置标题
        ax_heatmap.set_title(f'Frame: {t}, Time: {t / 10:.2f}s', color='white')

        # 设置 X 轴的范围
        ax_heatmap.set_xlim(t - 150, t + 150)

        # 设置 X 轴的刻度
        x_ticks = np.arange(t - 150, t + 151)
        x_ticks_divisible_by_50 = x_ticks[x_ticks % 50 == 0]  # 找到能被50整除的刻度
        ax_heatmap.set_xticks(x_ticks_divisible_by_50)

        # 将帧数转化为秒并添加单位 's'
        x_tick_labels = [f'{frame // 10}s' for frame in x_ticks_divisible_by_50]
        ax_heatmap.set_xticklabels(x_tick_labels, color='white')

        # 设置 Y 轴的标签
        y_ticks = np.arange(0, displayed_data.shape[1], 20)
        ax_heatmap.set_yticks(y_ticks)
        ax_heatmap.set_yticklabels(y_ticks, color='white')

        # 设置轴的颜色
        ax_heatmap.spines['bottom'].set_color('white')
        ax_heatmap.spines['left'].set_color('white')
        ax_heatmap.spines['right'].set_color('white')

        # 在时刻 t 画一条白色虚线
        ax_heatmap.axvline(x=t, color='white', linestyle='--')

        # 设置颜色条
        cbar = plt.colorbar(im, ax=ax_heatmap)
        cbar.set_label('ΔF/F', color='white', labelpad=10)
        cbar.set_ticks([])
        cbar.outline.set_edgecolor('white')

    # 创建动画
    num_frames = new_data.shape[0]
    ani = FuncAnimation(fig_heatmap, update, frames= num_frames, interval=1000 / 10)

    # 保存视频，设置 fps=10 和 dpi=300
    ani.save(os.path.join(output_path, 'heatmap_video.avi'), writer='ffmpeg', fps=10, dpi=300)

    print("视频生成完成。")
    plt.close(fig_heatmap)  # 关闭折线图以释放资源

if __name__ == "__main__":
    # 调用函数
    input_folder = r'D:\20241014beh_data_analysis\plot\dff'  # 输入文件夹路径
    output_path = r'D:\20241014beh_data_analysis\plot\plotdata'  # 输出文件夹路径
    process_dff_data(100, 1000, input_folder, output_path)
