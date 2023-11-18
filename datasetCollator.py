import os
import random
import shutil
from utils import rename_file_extension

# DatasetCollator类：数据集整理器
# 一个数据集整理器的输入为：
# 包含了合成后的图片和标注信息文本的目录
# 输出为：
# 可训练的yolov8标准数据集


class DatasetCollator(object):
    def __init__(self, name, labels, input_folder) -> None:
        # 数据集名称
        self.dataset_name = name
        # 未整理数据集输入目录
        self.input_folder = input_folder
        # 整理后数据集输出目录
        self._output_folder = "outputs" + "/" + self.dataset_name
        # 标签列表
        self.labels = labels

    def __init_dir(self):
        os.makedirs(self._output_folder, exist_ok=True)
        for dataset in [
            self._output_folder + "/" + "train",
            self._output_folder + "/" + "valid",
            self._output_folder + "/" + "test",
        ]:
            os.makedirs(os.path.join(dataset, "images"), exist_ok=True)
            os.makedirs(os.path.join(dataset, "labels"), exist_ok=True)

    def __move_pngs_and_txts(self):
        files = [f for f in os.listdir(self.input_folder) if f.endswith(".jpg")]
        pairs = [(f, f.replace(".jpg", ".txt")) for f in files]

        # 打乱文件顺序
        random.shuffle(pairs)

        # 计算分配比例
        total_files = len(pairs)
        train_count = int(total_files * 0.7)
        valid_count = int(total_files * 0.2)

        # 分配文件
        train_files = pairs[:train_count]
        valid_files = pairs[train_count : train_count + valid_count]
        test_files = pairs[train_count + valid_count :]

        # 移动文件的函数
        def move_files(file_pairs, dataset):
            for img_file, txt_file in file_pairs:
                shutil.move(
                    os.path.join(self.input_folder, img_file),
                    os.path.join(dataset, "images", img_file),
                )
                shutil.move(
                    os.path.join(self.input_folder, txt_file),
                    os.path.join(dataset, "labels", txt_file),
                )

        move_files(train_files, self._output_folder + "/" + "train")
        move_files(valid_files, self._output_folder + "/" + "valid")
        move_files(test_files, self._output_folder + "/" + "test")

    def __generate_yaml(self):
        # 文本内容
        text_content =  f"test: ../test/images\ntrain: ../train/images\nval: ../valid/images\nnc: {len(self.labels)}\nnames: {self.labels}"
        # 创建并写入文本文件
        with open(self._output_folder + "/" + "data.txt", "w", encoding="utf-8") as file:
            file.write(text_content)
        # 修改扩展名为yaml
        rename_file_extension(self._output_folder + "/" + "data.txt", "yaml")
            

    def execute(self):
        self.__init_dir()
        self.__move_pngs_and_txts()
        self.__generate_yaml()
