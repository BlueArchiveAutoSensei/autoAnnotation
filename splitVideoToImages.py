import os
import cv2


def split_video_to_images(video_path, output_folder):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)

    # 检查视频文件是否成功打开
    if not video.isOpened():
        print("无法打开视频文件")
        return

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 逐帧读取视频并保存为图片
    frame_count = 0
    while True:
        # 读取下一帧
        ret, frame = video.read()

        # 检查是否成功读取帧
        if not ret:
            break

        # 生成输出图片文件路径
        output_path = os.path.join(output_folder, f"frame_{frame_count:04d}.png")

        # 保存当前帧为图片
        cv2.imwrite(output_path, frame)

        frame_count += 1

    # 释放视频对象
    video.release()
