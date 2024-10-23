# main.py
from video_processing import extract_video_segments
from extract_3D2 import extract_3D_data
from plot_dynamic_3D_and_2D import plot_dynamic_3D_and_2D
from line_3D import plot_dynamic_line_chart
from tiff import extract_video_frames
from dffvideo import process_dff_data
import os

if __name__ == "__main__":
    # 定义输入视频路径
    input_video_path = r'D:\20241014beh_data_analysis\plot\3Dvideo'

    # 定义输出视频路径
    output_video_path = r'D:\20241014beh_data_analysis\plot\plotdata'

    # 确保输出路径存在
    os.makedirs(output_video_path, exist_ok=True)

    # 定义3D数据路径
    three_d_path = r'D:\20241014beh_data_analysis\plot\3D'  # 3D 数据的路径--dff体态帧数对应的文件
    orgin3D_path = r'D:\20241014beh_data_analysis\plot\3Dorgin'
    start_row = 2000  # 起始帧数
    end_row = 2600  # 结束帧数

    # 调用提取3D数据的函数，并获取 start_frame 和 stop_frame--从3D文件中提取想要画图的帧数范围同步对应的体态视频帧数，在结果中会保存为新的3D文件，返回 start_frame 和 stop_frame
    start_frame, stop_frame = extract_3D_data(three_d_path, output_video_path, start_row, end_row, orgin3D_path)

    # 调用提取视频段的函数，使用从提取的3D数据中获取的 start_frame 和 stop_frame--从原始视频中提取所需范围内的视频（四个视角）
    extract_video_segments(input_video_path, output_video_path, start_frame, stop_frame)

    # 指定 CSV 文件的路径
    csv_file = r'D:\20241014beh_data_analysis\plot\plotdata\3D_data.csv'  # 修改为实际路径
    output_directory = os.path.dirname(csv_file)

    # 输出视频文件名
    output_video_3D = os.path.join(output_directory, '3D_video.avi.avi')
    output_video_xy = os.path.join(output_directory, 'xy_video.avi.avi')

    # 调用合并后的函数
    plot_dynamic_3D_and_2D(csv_file, output_video_3D, output_video_xy)

    # 输出视频文件名
    output_video_line = os.path.join(output_directory, '3D_data_line_video.avi')

    # 调用折线图函数
    plot_dynamic_line_chart(csv_file, output_video_line)

    # tiff-avi
    extract_video_frames(start_row, end_row, r'D:\20241014beh_data_analysis\plot\calcium_video',
                         r'D:\20241014beh_data_analysis\plot\plotdata')

    # dff trace
    input_folder = r'D:\20241014beh_data_analysis\plot\dff'  # 输入文件夹路径
    output_path = r'D:\20241014beh_data_analysis\plot\plotdata\新建文件夹 (2)'  # 输出文件夹路径
    process_dff_data(start_row, end_row, input_folder, output_path)