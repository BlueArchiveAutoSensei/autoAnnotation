import os
import threading
from config import Config
from PIL import Image

from processForegroundPic import process_foreground_pic
from splitVideoToImages import split_video_to_images
from supplyPic import supply_pic
from generateRandomPos import generate_random_pos


def video_to_compound_pic(foreground_video,background_video):
#1.将视频分割为图片
    config = Config()
    
    def code1():
        split_video_to_images(background_video, config.background_pic_path)

    def code2():
        split_video_to_images(foreground_video,config.foreground_pic_raw_1_path)
        file_names_1 = os.listdir(config.foreground_pic_raw_1_path)
        file_names = [config.foreground_pic_raw_1_path + '/' + item for item in file_names_1]
        for item in file_names:
            process_foreground_pic(item)
    
    thread1 = threading.Thread(target=code1)
    thread2 = threading.Thread(target=code2)
    # 启动线程
    thread1.start()
    thread2.start()

    # 等待线程执行结束
    thread1.join()
    thread2.join()
#2.补足图片
    supply_pic(config.background_pic_path,config.foreground_pic_path)

#3.合成图片
    # 指定文件夹路径
    folder_path = config.foreground_pic_path
    #获取文件夹中所有文件的列表
    file_list = os.listdir(folder_path)
    # 使用列表推导式筛选出扩展名为 '.png' 的文件
    png_files = [file for file in file_list if file.endswith('.png')]
    # 获取 PNG 图片数量
    png_count = len(png_files)
    for i in range(png_count):
        background_pic = Image.open(config.background_pic_path+f"/frame_{str(i).zfill(4)}.png")
        foreground_pic = Image.open(config.foreground_pic_path+f"/frame_{str(i).zfill(4)}.png")  # 要合成的图片，可以是任何支持的格式
        # 将要合成的图片粘贴到背景图片上
        background_pic.paste(foreground_pic, generate_random_pos(), foreground_pic)
        target_path = config.result_pic_path
        # 保存合成后的图片
        background_pic.save(target_path+f"/frame_{str(i).zfill(4)}.png")
        #print(f"/frame_{str(i).zfill(4)}.png  合成完成")
    