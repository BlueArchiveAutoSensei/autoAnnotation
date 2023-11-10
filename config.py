import os

class Config:
    def __init__(self) -> None:
        #背景视频
        self.input_foreground_video = 'inputs/foreground_video_raw.mp4'
        #前景视频
        self.input_background_video = 'inputs/background_video.mp4'
        #待加工（去绿幕、缩放）的前景图片1（由前景视频分割得出）存放目录
        self.foreground_pic_raw_1_path = 'cache/foreground_pic_raw_1'
        #待加工（缩放）的前景图片2（由前景图片1加工得出）存放目录
        self.foreground_pic_raw_2_path = 'cache/foreground_pic_raw_2' 
        #前景图片（由前景图片2加工得出）存放目录
        self.foreground_pic_path = 'cache/foreground_pic' 
        #背景图片（由背景视频分割得出）存放目录   
        self.background_pic_path = 'cache/background_pic'
        #合成图片（由前景图片和背景图片合成得出）存放目录
        self.result_pic_path = 'cache/result_pic'    

def init(config:Config):
    os.makedirs('cache')
    os.makedirs(config.background_pic_path)
    os.makedirs(config.foreground_pic_path)
    os.makedirs(config.foreground_pic_raw_1_path)
    os.makedirs(config.foreground_pic_raw_2_path)
    os.makedirs(config.result_pic_path)

def releaseCache(config:Config):
    os.remove(config.background_pic_path)
    os.remove(config.foreground_pic_path)
    os.remove(config.foreground_pic_raw_1_path)
    os.remove(config.foreground_pic_raw_2_path)
    os.remove(config.result_pic_path)