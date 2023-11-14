import os
import shutil


# 获取文件夹内的图片数量
def get_image_count(folder_path):
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.endswith('.png')]
    return len(image_files)

# 获取文件名的编号部分
def get_file_number(file_name):
    return int(file_name.split('.')[0][-4:])

# 复制图片
def copy_image(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def supply_pic(folder_a, folder_b):
    # folder_a = "cache/background_pic"  # 第一个文件夹路径
    # folder_b = "cache/foreground_pic"  # 第二个文件夹路径
    # 获取文件夹a和文件夹b内的图片数量
    count_a = get_image_count(folder_a)
    count_b = get_image_count(folder_b)
    # 计算差额
    difference = count_b - count_a
    #print(difference)
    # 补足图片
    if difference > 0:  # 补足文件夹a的图片
        for i in range(difference):
            source_file = os.path.join(folder_a, f"frame_{str(i).zfill(4)}.png")
            destination_file = os.path.join(folder_a, f"frame_{str(count_a+i).zfill(4)}.png")
            copy_image(source_file, destination_file)
            #print('在  '+folder_a+f"  用  frame_{str(i).zfill(4)}.png  "f"补足了  frame_{str(count_a+i+1).zfill(4)}.png")
    elif difference < 0:  # 补足文件夹b的图片
        for i in range(abs(difference)):
            source_file = os.path.join(folder_b, f"frame_{str(i).zfill(4)}.png")
            destination_file = os.path.join(folder_b, f"frame_{str(count_b+i).zfill(4)}.png")
            copy_image(source_file, destination_file)
            #print('在  '+folder_b+f"  用  frame_{str(i).zfill(4)}.png  "f"补足了  frame_{str(count_a+i+1).zfill(4)}.png")

    #print("图片补足完成！")







