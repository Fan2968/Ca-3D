import cv2
import os


def extract_video_frames(start_row, end_row, calcium_video_path, output_path):
    # 构建输入视频文件的完整路径
    video_path = os.path.join(calcium_video_path, "CellVideo.avi")

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 获取视频的帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 将 end_row 限制在视频的总帧数范围内
    end_row = min(end_row, total_frames)

    # 输出视频的设置
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 编码
    output_video_path = os.path.join(output_path, "dff_video.avi")
    out = cv2.VideoWriter(output_video_path, fourcc, 10.0, (int(cap.get(3)), int(cap.get(4))))

    # 提取并写入指定范围的帧
    for i in range(start_row, end_row):
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame {i}.")
            break

        # 写入输出视频
        out.write(frame)

    # 释放资源
    cap.release()
    out.release()
    print(f"Video saved at {output_video_path}")

# 示例调用
extract_video_frames(1, 1000, r'D:\20241014beh_data_analysis\plot\calcium_video', r'D:\20241014beh_data_analysis\plot\plotdata')
