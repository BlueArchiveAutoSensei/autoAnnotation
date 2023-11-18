import os
import random
import shutil
from shapely.geometry import box
from PIL import Image

# 判断是否是绿色
def is_green_range(color):
    # 定义颜色范围的上下界
    lower_bound = (0, 130, 0)
    upper_bound = (110, 255, 110)

    if (
        (color[1] > color[0] and color[1] > color[2])
        and (color[1] - color[0] >= 50 or color[1] - color[2] >= 50)
        and (
            (color[0] <= 100 and color[2] <= 100)
            or (
                color[1] >= 220
                and color[1] - color[0] >= 80
                and color[1] - color[2] >= 80
            )
        )
    ):
        return True

        # 分别比较红色、绿色和蓝色分量
    for c, lower, upper in zip(color, lower_bound, upper_bound):
        if not lower <= c <= upper:
            return False

    return True

# 获取图片分辨率
def get_image_resolution(img_folder):
        for file in os.listdir(img_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                try:
                    with Image.open(os.path.join(img_folder, file)) as img:
                            return img.size
                except IOError:
                    print(f"无法打开文件：{file}")
                    continue
        return None

# 生成标注用的文本文件
def generate_txt_for_annotation(
    fileName, foregroundNameIndex, pos, foreground_size, background_size, target_folder
):
    foreground_x, foreground_y = pos  # 替换为实际坐标
    foreground_width, foreground_height = foreground_size

    # 背景图片的尺寸
    background_width, background_height = background_size

    # 计算中心点坐标
    center_x = foreground_x + (foreground_width / 2)
    center_y = foreground_y + (foreground_height / 2)

    # 归一化坐标
    norm_center_x = center_x / background_width
    norm_center_y = center_y / background_height
    norm_width = foreground_width / background_width
    norm_height = foreground_height / background_height

    # 类别索引
    class_index = foregroundNameIndex

    # 写入标注文件
    with open(target_folder + "/" + fileName + ".txt", "a") as file:
        file.write(
            f"{class_index} {norm_center_x} {norm_center_y} {norm_width} {norm_height}\n"
        )

# 获取文件夹内图片数量
def get_image_count(folder_path):
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.endswith(".png")]
    return len(image_files)

# 拷贝图片
def copy_image(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

# 添加到字典
def add_directory(dir_dict, dir_name, files):
    if dir_name not in dir_dict:
        dir_dict[dir_name] = files
    else:
        print(f"Directory {dir_name} already exists.")

# 获取文件名
def get_filenames_without_extension(directory):
    filenames = []
    for file in os.listdir(directory):
        # 检查是否为文件
        if os.path.isfile(os.path.join(directory, file)):
            # 去除扩展名
            file_name = os.path.splitext(file)[0]
            filenames.append(file_name)
    return filenames

# 在多边形内生成若干随机矩形，每个重叠面积不超过30%，且不能超过多边形边界
def generate_rectangles_in_polygon(num_rectangles, rectangle_size, polygon):
    rectangles = []

    # 辅助函数：生成一个随机矩形
    def generate_random_rectangle():
        minx, miny, maxx, maxy = polygon.bounds
        x = random.uniform(minx, maxx - rectangle_size[0])
        y = random.uniform(miny, maxy - rectangle_size[1])
        return box(x, y, x + rectangle_size[0], y + rectangle_size[1])

    # 辅助函数：检查重叠
    def check_overlap(new_rect):
        for rect in rectangles:
            if new_rect.intersection(rect).area > 0.3 * new_rect.area:
                return True
        return False

    while len(rectangles) < num_rectangles:
        new_rect = generate_random_rectangle()
        if polygon.contains(new_rect) and not check_overlap(new_rect):
            rectangles.append(new_rect)

    # 返回矩形的左下角坐标
    return [(int(rect.bounds[0]), int(rect.bounds[1])) for rect in rectangles]

# 修改文件后缀名
def rename_file_extension(original_file_name, new_extension):
    # 确保新扩展名以点开头
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    # 分离原始文件名和扩展名
    base_name, _ = os.path.splitext(original_file_name)

    # 创建新文件名
    new_file_name = base_name + new_extension

    # 重命名文件
    os.rename(original_file_name, new_file_name)