import os
import cv2
from PIL import Image
from utils import is_green_range, get_image_resolution


class Material(object):
    def __init__(self, video_path) -> None:
        self.video_path = video_path

    def _split_video_to_images(self, img_folder):
        # 打开视频文件
        video = cv2.VideoCapture(self.video_path)

        # 检查视频文件是否成功打开
        if not video.isOpened():
            print("无法打开视频文件")
            return

        # 创建输出文件夹
        os.makedirs(img_folder, exist_ok=True)

        # 逐帧读取视频并保存为图片
        frame_count = 0
        while True:
            # 读取下一帧
            ret, frame = video.read()

            # 检查是否成功读取帧
            if not ret:
                break

            # 生成输出图片文件路径
            output_path = os.path.join(img_folder, f"frame_{frame_count:05d}.png")

            # 保存当前帧为图片
            cv2.imwrite(output_path, frame)

            frame_count += 1

        # 释放视频对象
        video.release()


# Map类：地图背景视频
class Map(Material):
    def __init__(self, name, video_path, floor_pos_range) -> None:
        # 从Material父类继承视频路径
        super(Map, self).__init__(video_path)
        # 地图名称
        self.name = name
        # 地图的角色放置范围，由四个坐标围成
        # 注意！！！：4个坐标值顺序必须是ABDC或ACDB
        #      A-----------B
        #      |           |
        #      |           |
        #      |           |
        #      C-----------D
        self.floor_pos_range = floor_pos_range
        # 工作文件夹和输出文件夹的父集目录
        self.__img_folder_tmp = "cache"
        # 输出文件夹
        self._img_folder = self.__img_folder_tmp + "/" + self.name
        # 图片大小
        self._img_size = None

    def __init_dir(self):
        os.makedirs(self._img_folder, exist_ok=True)

    # 封装继承过来的方法
    def __split_video_to_images(self):
        return super()._split_video_to_images(self._img_folder)

    # 该方法处理地图背景
    def process(self):
        # 1.创建输出文件夹
        self.__init_dir()
        # 2.将视频分割成图片
        self.__split_video_to_images()
        # 3.获取图片分辨率
        self._img_size = get_image_resolution(self._img_folder)


# Character类：角色绿幕视频
class Character(Material):
    def __init__(self, name, video_path) -> None:
        # 从Material父类继承视频路径
        super(Character, self).__init__(video_path)
        # 角色名称
        self.name = name
        # # 角色图片缩放后的最大像素
        # self.resize_to_what_size = resize_to_what_size
        # 工作文件夹和输出文件夹的父级目录
        self.__img_folder_tmp = "cache"
        # 工作文件夹1：放置视频分割后的图片
        self.__work_folder_1 = self.__img_folder_tmp + "/" + self.name + "_tmp_1"
        # 工作文件夹2：放置缩放后的图片
        self.__work_folder_2 = self.__img_folder_tmp + "/" + self.name + "_tmp_2"
        # 输出文件夹：放置去绿幕后的图片
        self._img_folder = self.__img_folder_tmp + "/" + self.name
        # 图片像素
        self._img_size = None

    def __init_dir(self):
        os.makedirs(self.__work_folder_1, exist_ok=True)
        os.makedirs(self.__work_folder_2, exist_ok=True)
        os.makedirs(self._img_folder, exist_ok=True)

    # 封装继承过来的方法
    def __split_video_to_images(self):
        return super()._split_video_to_images(self.__work_folder_1)

    # def __resize_images_in_folder(self):
    #     for filename in os.listdir(self.__work_folder_1):
    #         # 检查是否为图像文件
    #         if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".bmp")):
    #             input_image_path = os.path.join(self.__work_folder_1, filename)
    #             output_image_path = os.path.join(self.__work_folder_2, filename)

    #             original_image = Image.open(input_image_path)
    #             width, height = original_image.size

    #             ratio = 1  # 默认比例为1，表示不缩放
    #             if width > height and width > self.resize_to_what_size:
    #                 ratio = self.resize_to_what_size / width
    #             elif height > self.resize_to_what_size:
    #                 ratio = self.resize_to_what_size / height

    #             new_width = int(width * ratio)
    #             new_height = int(height * ratio)
    #             resized_image = original_image.resize((new_width, new_height))

    #             resized_image.save(output_image_path)

    # 因为是process的最后一步所以需要传入target_folder
    def __replace_green_range_with_transparent(self, target_folder):
        for filename in os.listdir(self.__work_folder_1):
            # 检查是否为图像文件
            if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".bmp")):
                input_image_path = os.path.join(self.__work_folder_1, filename)
                output_image_path = os.path.join(target_folder, filename)

                image = Image.open(input_image_path)
                # 将图片转换为RGBA模式
                image = image.convert("RGBA")

                # 获取图片的像素数据
                data = image.getdata()
                # 存储修改后的像素数据
                new_data = []

                for item in data:
                    # 判断当前像素的颜色是否在绿色范围内
                    if is_green_range(item[:3]):
                        # 将绿色像素修改为透明
                        new_data.append((item[0], item[1], item[2], 0))
                    else:
                        new_data.append(item)
                # 更新图片的像素数据
                image.putdata(new_data)
                # 保存修改后的图片
                image.save(output_image_path, "PNG")

    # 该方法处理角色绿幕视频
    def process(self):
        # 1.创建工作文件夹及输出文件夹
        self.__init_dir()
        # 2.将视频分割成图片
        self.__split_video_to_images()
        # # 3.将图片缩放
        # self.__resize_images_in_folder()
        # 4.将图片去绿幕
        self.__replace_green_range_with_transparent(self._img_folder)
        # 5.获取图片分辨率
        self._img_size = get_image_resolution(self._img_folder)
