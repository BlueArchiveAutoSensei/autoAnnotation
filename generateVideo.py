import cv2
import os

# 图片文件夹路径
image_folder = "cache/result_pic"

# 视频输出文件路径
video_name = "outputs/output_video.mp4"

# 获取图片文件夹中的所有图片文件名
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

# 获取第一张图片的宽度和高度
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# 创建视频编码器
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(video_name, fourcc, 24, (width, height))

# 将每张图片逐帧写入视频
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

# 关闭视频编码器
video.release()
