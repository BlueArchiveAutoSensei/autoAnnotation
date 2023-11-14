from config import Config, init
from compositePic import video_to_compound_pic

config = Config()
try:
    # 生成缓存目录
    init(config)
except FileExistsError:
    pass

foreground_video = config.input_foreground_video
background_video = config.input_background_video
video_to_compound_pic(foreground_video, background_video)
