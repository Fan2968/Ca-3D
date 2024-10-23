import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import glob
import subprocess
import cv2

def create_video(data, start_frame, end_frame, output_path, video_index):
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(5, 7), facecolor='black')

    ax_heatmap.set_facecolor('black')  # 设置背景为黑色
    data_min = np.min(data)
    data_max = np.max(data)

    # 创建热图并初始化颜色条（只在第一帧创建）
    im = ax_heatmap.imshow(data.T, aspect='auto', cmap='gray', vmin=data_min, vmax=data_max)
    cbar = plt.colorbar(im, ax=ax_heatmap, orientation='horizontal', pad=0.1)
    cbar.set_label('ΔF/F', color='white', labelpad=10)
    cbar.set_ticks([])  # 如果不需要具体的刻度，可以将其清空
    cbar.outline.set_edgecolor('white')

    def update(frame):
        ax_heatmap.cla()  # 清空当前轴
        t = frame + start_frame

        # 提取要显示的数据范围
        start_frame_range = max(0, t - 1500)
        end_frame_range = min(data.shape[0], t + 1500)
        displayed_data = data[start_frame_range:end_frame_range, :]

        # 更新热图
        im = ax_heatmap.imshow(displayed_data.T, aspect='auto', cmap='gray', vmin=data_min, vmax=data_max)

        # 设置标题和轴
        ax_heatmap.set_title(f'Frame: {t}, Time: {t / 10:.2f}s', color='white')
        ax_heatmap.set_xlim(t - 150, t + 151)

        x_ticks = np.arange(t - 150, t + 151)
        x_ticks_divisible_by_50 = x_ticks[x_ticks % 50 == 0]  # 找到能被50整除的刻度
        ax_heatmap.set_xticks(x_ticks_divisible_by_50)

        # 将帧数转化为秒并添加单位 's'
        x_tick_labels = [f'{frame // 10}s' for frame in x_ticks_divisible_by_50]
        ax_heatmap.set_xticklabels(x_tick_labels, color='white')

        ax_heatmap.set_yticks(np.arange(0, displayed_data.shape[1], 20))
        ax_heatmap.set_yticklabels(np.arange(0, displayed_data.shape[1], 20), color='white')
        ax_heatmap.spines['bottom'].set_color('white')
        ax_heatmap.spines['left'].set_color('white')
        ax_heatmap.spines['right'].set_color('white')
        ax_heatmap.axvline(x=t, color='white', linestyle='--')

    # 创建动画
    num_frames = end_frame - start_frame
    ani = FuncAnimation(fig_heatmap, update, frames=num_frames, interval=100)

    # 保存为视频
    output_file = os.path.join(output_path, f'heatmap_video_{video_index}.avi')  # 设置保存路径和文件名
    ani.save(output_file, writer='ffmpeg', fps=10, dpi=300)
    plt.close(fig_heatmap)  # 关闭图形窗口以释放资源
    print(f"视频已保存到: {output_file}")

# 在调用时
# create_video(data, start_frame, end_frame, output_path, video_index, colorbar_height=0.1)

def combine_videos(output_path, num_videos):
    output_file = os.path.join(output_path, 'dff_video.avi')

    # 获取第一个视频的属性
    first_video_path = os.path.join(output_path, f"heatmap_video_0.avi")
    first_video = cv2.VideoCapture(first_video_path)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = first_video.get(cv2.CAP_PROP_FPS)
    width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # 逐个读取视频并写入输出文件
    for i in range(num_videos):
        video_path = os.path.join(output_path, f"heatmap_video_{i}.avi")
        video = cv2.VideoCapture(video_path)

        while True:
            ret, frame = video.read()
            if not ret:
                break
            out.write(frame)

        video.release()

    out.release()
    first_video.release()

    print(f"合并完成，最终视频为: {output_file}")


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
    threshold = mean + 2 * sd
    print(f"计算阈值: {threshold}")

    # 替换数据
    print("替换数据...")
    new_data = np.where(data > threshold, data, threshold)
    print("数据替换完成。")

    # 分段处理视频
    frames_per_video = 200
    num_videos = (new_data.shape[0] + frames_per_video - 1) // frames_per_video  # 计算视频数量

    for i in range(num_videos):
        start_frame = i * frames_per_video
        end_frame = min((i + 1) * frames_per_video, new_data.shape[0])
        print(f"生成视频 {i + 1}/{num_videos}: 帧 {start_frame} 到 {end_frame}")
        create_video(new_data, start_frame, end_frame, output_path, i)

    # 合并所有视频
    combine_videos(output_path, num_videos)


if __name__ == "__main__":
    # 调用函数
    input_folder = r'D:\20241014beh_data_analysis\plot\dff'  # 输入文件夹路径
    output_path = r'D:\20241014beh_data_analysis\plot\plotdata\新建文件夹 (2)'  # 输出文件夹路径
    process_dff_data(500, 1500, input_folder, output_path)
