from material import Map, Character
import os
from PIL import Image
import shutil

from shapely.geometry import Polygon, box
from utils import (
    generate_txt_for_annotation,
    get_image_count,
    copy_image,
    add_directory,
    get_filenames_without_extension,
    generate_rectangles_in_polygon,
)

# Sythesizer类：合成器


# 一个合成器的输入为：
# 1.一个地图背景图片目录
# 2.若干个角色图片目录 TODO
## 支持单一角色的重复不同位置合成（例如总力战球的小兵） TODO
# 3.若干个、若干种特效图片目录 TODO
## 特效图片我暂且分为 绑定在地图背景的特效 与 绑定在角色附近或上方的特效 TODO
# 一个合成器的输出为：
# 输出目录（包含合成后的图片和一一对应的标注信息文本）


class Sythesizer(object):
    def __init__(self, map: Map, character_list, img_minimum_num_in_dataset) -> None:
        # 待合成的地图类
        self.map = map
        # 待合成角色列表
        self.character_list = character_list
        # 数据集中的最小图片数
        self.img_minimum_num_in_dataset = img_minimum_num_in_dataset
        # 标签列表
        self.labels = list()
        # 暂存的随机坐标列表
        self.__pos_list = None
        # 暂存的数据字典
        self.__annotation_dict = None
        # 输出目录的父目录
        self._img_folder_tmp = "cache"
        # 输出目录
        self._img_and_txt_folder = (
            self._img_folder_tmp + "/" + self.map.name + "_raw_dataset"
        )

    # 创建输出文件夹
    def __init_dir(self):
        os.makedirs(self._img_and_txt_folder, exist_ok=True)

    # 用character的name初始化标签列表
    def _init_labels(self):
        for character in self.character_list:
            self.labels.append(character.name)

    # 使各输入目录下图片数量一致
    def _supply_folders(self):
        folders = list()
        # 将所有的character图片目录加入待比较列表中
        for character in self.character_list:
            folders.append(character._img_folder)
        # 将map图片目录加入待比较列表中
        folders.append(self.map._img_folder)
        # 存储每个文件夹的图片数量
        counts = [get_image_count(folder) for folder in folders]
        # 计算最大图片数量
        max_count = max(counts)
        # 获取最小要求的图片数
        img_minimum_num_in_dataset = self.img_minimum_num_in_dataset
        # 先对齐所有文件夹图片数
        for folder, count in zip(folders, counts):
            difference = max_count - count
            for i in range(difference):
                source_file = os.path.join(
                    folder, f"frame_{str(i % count).zfill(5)}.png"
                )
                destination_file = os.path.join(
                    folder, f"frame_{str(count + i).zfill(5)}.png"
                )
                copy_image(source_file, destination_file)
        # 更新每个文件夹图片的数目
        counts = [get_image_count(folder) for folder in folders]
        # 如果未满足最小数量要求，继续添加图片
        if max_count < img_minimum_num_in_dataset:
            for folder, count in zip(folders, counts):
                difference_2 = img_minimum_num_in_dataset - max_count
                for i in range(difference_2):
                    source_file = os.path.join(
                        folder, f"frame_{str(i % count).zfill(5)}.png"
                    )
                    destination_file = os.path.join(
                        folder, f"frame_{str(count + i).zfill(5)}.png"
                    )
                    copy_image(source_file, destination_file)

    # 根据label和文件数量生成若干组随机坐标
    def _init_pos_list(self):
        pos_list = []
        polygon_coords = self.map.floor_pos_range
        polygon = Polygon(polygon_coords)
        label_num = len(self.labels)
        img_size = self.character_list[0]._img_size
        file_num = len(os.listdir(self.character_list[0]._img_folder))
        for i in range(file_num):
            rects_pos = generate_rectangles_in_polygon(label_num, img_size, polygon)
            pos_list.append(rects_pos)
        self.__pos_list = pos_list

    # 创建数据字典，并填入随机坐标：
    # "frame_00000":                   # 地图背景图片文件名
    #       0: (pos_x, pos_y),        # label_index: 坐标
    #       1: (pos_x, pos_y),
    #       ...
    # ,
    # "frame_00001":
    #       ...
    # ,
    # ...
    # 该数据字典为 生成标注文件 与 合成图片 提供依据
    def _init_annotation_dict(self):
        directories = {
            # label_index_1: ["frame_00000", "frame_00001"],
            # label_index_2: ["frame_00000", "frame_00001"]
        }
        img_name_list = get_filenames_without_extension(self.map._img_folder)
        # 初始化字典结构
        for character in self.character_list:
            label_index = self.labels.index(character.name)
            add_directory(directories, label_index, img_name_list)
        # 整理初始化后的数据字典
        manager = FileCoordinateManager(directories)
        pos_list = self.__pos_list
        for img_index, img_name in enumerate(img_name_list):
            for label_index in range(len(self.labels)):
                # 设置图片名，label下标，坐标
                # manager.set_coordinates("frame_00000", 0, (10, 20))
                manager.set_coordinates(
                    img_name, label_index, pos_list[img_index][label_index]
                )
        self.__annotation_dict = manager.data

    # 合成图片
    def _composite_imgs(self):
        # 获取数据字典
        annotation_dict = self.__annotation_dict
        # 从地图图片文件夹开始遍历
        for index, map_img_file in enumerate(os.listdir(self.map._img_folder)):
            map_img = Image.open(self.map._img_folder + "/" + map_img_file)
            map_img_name = os.path.splitext(map_img_file)[0]
            character_img_list = []
            # 获取一个地图图片对应的所有角色图片
            for character in self.character_list:
                character_img = Image.open(
                    character._img_folder
                    + "/"
                    + os.listdir(character._img_folder)[index]
                ).convert("RGBA")
                character_img_list.append(character_img)
            # 依次黏贴角色图片到地图图片
            # TODO: 随机顺序黏贴
            for index_2, character_img in enumerate(character_img_list):
                pos = annotation_dict[map_img_name][index_2]
                map_img.paste(character_img, pos, character_img)
                map_img.save(self._img_and_txt_folder + "/" + map_img_name + ".jpg")

    # 批量生成标注信息文本文件
    def _generate_txts_for_annotation(self):
        annotation_dict = self.__annotation_dict
        character_img_size = self.character_list[0]._img_size
        map_img_size = self.map._img_size
        # 遍历外层字典
        for file_name, positions_dict in annotation_dict.items():
            # 遍历内层字典
            for position_index, pos in positions_dict.items():
                generate_txt_for_annotation(
                    file_name,
                    position_index,
                    pos,
                    character_img_size,
                    map_img_size,
                    self._img_and_txt_folder,
                )

    # 封装方法
    def execute(self):
        self.__init_dir()
        self._init_labels()
        self._supply_folders()
        self._init_pos_list()
        self._init_annotation_dict()
        self._composite_imgs()
        self._generate_txts_for_annotation()


# FileCoordinateManager类：获取数据字典
class FileCoordinateManager:
    def __init__(self, directories):
        self.data = {}
        for label_index, files in directories.items():
            for file in files:
                if file not in self.data:
                    self.data[file] = {}
                # 初始化pos_x和pos_y的值，这里默认为0
                self.data[file][label_index] = (0, 0)

    def set_coordinates(self, file_name, label_index, pos: tuple):
        if file_name in self.data and label_index in self.data[file_name]:
            self.data[file_name][label_index] = pos
        else:
            print("File or directory not found.")

    def get_coordinates(self, file_name, label_index):
        if file_name in self.data and label_index in self.data[file_name]:
            return self.data[file_name][label_index]
        else:
            return "File or directory not found."


if __name__ == "__main__":
    shutil.rmtree('cache')
    shutil.rmtree('outputs')