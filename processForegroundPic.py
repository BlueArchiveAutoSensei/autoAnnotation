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

def replace_green_range_with_transparent(input_image_path, output_image_path, tolerance):
    image = Image.open(input_image_path)
    image = image.convert("RGBA")  # 将图片转换为RGBA模式

    data = image.getdata()  # 获取图片的像素数据
    new_data = []  # 存储修改后的像素数据

    for item in data:
        # 判断当前像素的颜色是否在绿色范围内
        if is_green_range(item[:3], tolerance):
            new_data.append((item[0], item[1], item[2], 0))  # 将绿色像素修改为透明
        else:
            new_data.append(item)

    image.putdata(new_data)  # 更新图片的像素数据
    image.save(output_image_path, "PNG")  # 保存修改后的图片

def is_green_range(color, tolerance):
    # 定义绿色范围的上下限
    lower_green = (10, 200, 0)
    upper_green = (50, 255, 0)

    # 判断颜色是否在绿色范围内
    for c, lower, upper in zip(color, lower_green, upper_green):
        if c < lower - tolerance or c > upper + tolerance:
            return False
    return True

def process_foreground_pic(foreground_pic_raw_1:str):
    config = Config()
    filename = foreground_pic_raw_1[27:37]
    foreground_pic = config.foreground_pic_path + '/' + filename + '.png'
    foreground_pic_raw_2 = config.foreground_pic_raw_2_path + '/' + filename + '.png'
    replace_green_range_with_transparent(foreground_pic_raw_1,foreground_pic_raw_2,70)
    resize_image(foreground_pic_raw_2,foreground_pic, 280)