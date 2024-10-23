import pandas as pd
import os
import glob

def extract_3D_data(three_d_path, output_path, start, end, orgin3D_path):
    # 获取文件夹中唯一的 CSV 文件
    csv_files = glob.glob(os.path.join(three_d_path, '*.csv'))

    if not csv_files:
        raise FileNotFoundError("没有找到 CSV 文件。")

    if len(csv_files) > 1:
        raise ValueError("文件夹中存在多个 CSV 文件，请确保只有一个。")

    csv_file = csv_files[0]  # 获取唯一的 CSV 文件

    # 读取 CSV 文件，不将第一行作为标题
    df = pd.read_csv(csv_file, header=None)

    # 查找 start 和 end 行对应的 frame
    start_rows = df.loc[df[0] == start, 1]
    stop_rows = df.loc[df[0] == end, 1]

    # 检查是否找到对应的行
    if start_rows.empty:
        raise ValueError(f"未找到 start 行匹配: {start}")

    if stop_rows.empty:
        raise ValueError(f"未找到 end 行匹配: {end}")

    start_frame = start_rows.values[0]
    stop_frame = stop_rows.values[0]

    print(f"Start Frame: {start_frame}, Stop Frame: {stop_frame}")

    # 在 orgin3D_path 查找 CSV 文件
    orgin3D_files = glob.glob(os.path.join(orgin3D_path, '*.csv'))

    if not orgin3D_files:
        raise FileNotFoundError("没有找到 orgin3D 文件夹中的 CSV 文件。")

    # 假设只处理第一个文件
    orgin3D_file = orgin3D_files[0]

    # 读取 orgin3D CSV 文件，忽略前三行
    orgin_df = pd.read_csv(orgin3D_file, header=3)  # 从第四行开始读取

    # 检查是否有足够的行
    if start_frame < 0 or stop_frame >= len(orgin_df):
        raise ValueError(f"start_frame 或 stop_frame 超出有效范围: start_frame={start_frame}, stop_frame={stop_frame}")

    # 提取从 start_frame 行到 stop_frame 行的数据
    extracted_data = orgin_df.iloc[start_frame:stop_frame + 1]

    # 保存为新的 CSV 文件
    output_file = os.path.join(output_path, '3D_data.csv')
    extracted_data.to_csv(output_file, index=False, header=False)  # 不写入标题

    print(f"提取的数据已保存到: {output_file}")

    return start_frame, stop_frame  # 返回 start_frame 和 stop_frame
