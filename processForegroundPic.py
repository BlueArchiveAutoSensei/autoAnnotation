from PIL import Image
from config import Config


# 前景图片等比例缩放
# 1080*1350的学生图片建议max_size为280
def resize_image(input_image_path, output_image_path, max_size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size

    # 计算缩放比例
    if width > height:
        if width > max_size:
            ratio = max_size / width
    else:
        if height > max_size:
            ratio = max_size / height

    # 根据缩放比例调整图片大小
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    resized_image = original_image.resize((new_width, new_height))

    # 保存缩放后的图片
    resized_image.save(output_image_path)


def replace_green_range_with_transparent(input_image_path, output_image_path):
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


def is_green_range(color):
    # 定义颜色范围的上下界
    lower_bound = (0, 130, 0)
    upper_bound = (110, 255, 110)

    # 超级答辩的绿色判断算法，但是还挺管用？
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


def process_foreground_pic(foreground_pic_raw_1: str):
    config = Config()
    filename = foreground_pic_raw_1[27:37]
    foreground_pic = config.foreground_pic_path + "/" + filename + ".png"
    foreground_pic_raw_2 = config.foreground_pic_raw_2_path + "/" + filename + ".png"
    replace_green_range_with_transparent(foreground_pic_raw_1, foreground_pic_raw_2)
    resize_image(foreground_pic_raw_2, foreground_pic, 280)


if __name__ == "__main__":
    process_foreground_pic("frame_0000.png")