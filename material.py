import os
import cv2
import json
from PIL import Image
from utils import is_green_range, get_image_resolution

with open('materialData.json', 'r') as json_file:
    materialData = json.load(json_file)

class Material(object):
    def __init__(self,video_path) -> None:
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

    def _replace_green_range_with_transparent(self, target_folder):
        for filename in os.listdir(self.video_path):
            # 检查是否为图像文件
            if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".bmp")):
                input_image_path = os.path.join(self.video_path, filename)
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


# Map类：地图背景视频
class Map(Material):
    def __init__(self, name) -> None:
        # 地图名称
        self.name = name
        # 视频路径
        super(Map,self).__init__(materialData["map_data"][name]["video_path"])
        # 地图可标注范围
        self._annotation_area = materialData["map_data"][name]["annotation_area"]
        # 工作文件夹父目录
        self.__work_parent_folder = materialData["foundamental_data"]["work_parent_folder"]
        # 输出文件夹
        self._img_folder = self.__work_parent_folder + "/" + self.name
        # 图片大小
        self._img_size = None

    # 初始化文件夹
    def __init_dir(self):
        os.makedirs(self._img_folder, exist_ok=True)

    # 封装继承过来的方法
    def __split_video_to_images(self):
        return super()._split_video_to_images(self._img_folder)

    # 背景视频没有绿幕
    def _replace_green_range_with_transparent(self, target_folder):
        pass

    def process(self):
        # 1.创建输出文件夹
        self.__init_dir()
        # 2.将视频分割成图片
        self.__split_video_to_images()
        # 3.获取图片分辨率
        self._img_size = get_image_resolution(self._img_folder)



class Character(Material):
    def __init__(self, name) -> None:
        # 角色名称
        self.name = name
        # 根据角色名称从json中获取相关数据
        # TODO:获取所有动作的视频和标注区域
        super(Character, self).__init__(materialData["character_data"][name]["run"])
        # 工作文件夹父目录
        self.__work_parent_folder = materialData["foundamental_data"]["work_parent_folder"]
        # 工作文件夹：放置视频分割后的图片
        self.__work_folder_1 = self.__work_parent_folder + "/" + self.name + "_tmp_1"
        # 输出文件夹：放置去绿幕后的图片
        self._img_folder = self.__work_parent_folder + "/" + self.name
        # 图片像素
        self._img_size = None
        # TODO:可标注区域列表存储；动作比例

    def __init_dir(self):
        os.makedirs(self.__work_folder_1, exist_ok=True)
        os.makedirs(self._img_folder, exist_ok=True)

    # 封装继承过来的方法
    def __split_video_to_images(self):
        return super()._split_video_to_images(self.__work_folder_1)

    def __replace_green_range_with_transparent(self):
        return super()._replace_green_range_with_transparent(self._img_folder)

    # 该方法处理角色绿幕视频
    def process(self):
        # 1.创建工作文件夹及输出文件夹
        self.__init_dir()
        # 2.将视频分割成图片
        self.__split_video_to_images()
        # 3.将图片去绿幕
        self.__replace_green_range_with_transparent()
        # 4.获取图片分辨率
        self._img_size = get_image_resolution(self._img_folder)
        


if __name__=="__main__":
    map = Map("map_1")
    print(map._annotation_area)