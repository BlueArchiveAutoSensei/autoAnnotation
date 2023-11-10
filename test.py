from config import Config,init
from composite_pic import video_to_compound_pic

config = Config()
try:
    init(config)#生成缓存目录
except FileExistsError:
    pass

foreground_video = config.input_foreground_video
background_video = config.input_background_video

video_to_compound_pic(foreground_video,background_video)