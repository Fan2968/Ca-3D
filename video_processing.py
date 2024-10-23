import cv2
import os


def extract_video_segments(path, output_path, start_frame, stop_frame):
    # 获取路径下的所有文件
    all_files = os.listdir(path)

    # 筛选出以 .avi 结尾且包含 "camera" 的文件
    camera_files = [f for f in all_files if f.endswith('.avi') and 'camera' in f]

    if not camera_files:
        print("没有找到符合条件的摄像头视频文件。")
        return

    print(f"找到 {len(camera_files)} 个视频文件，开始处理...")

    # 处理每个视频
    for i, camera_file in enumerate(camera_files):
        camera_file_path = os.path.join(path, camera_file)

        print(f"正在处理文件: {camera_file_path} ...")  # 提示正在处理的文件

        if os.path.exists(camera_file_path):
            cap = cv2.VideoCapture(camera_file_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # 确保开始帧和停止帧在视频的范围内
            start_frame = max(0, start_frame)
            stop_frame = min(stop_frame, total_frames)

            # 定义输出文件
            output_file = os.path.join(output_path, f"seg_{camera_file}")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

            # 截取指定帧范围
            for frame_idx in range(total_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                if start_frame <= frame_idx < stop_frame:
                    out.write(frame)

            # 释放资源
            cap.release()
            out.release()
            print(f"成功提取: {camera_file_path} 到 {output_file}")  # 提示成功提取的文件
        else:
            print(f"文件 {camera_file_path} 不存在。")
