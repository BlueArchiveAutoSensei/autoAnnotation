# autoAnnotation

## 此部分为 “动态剪贴画”计划的实现尝试

使用ae抠出小人的绿幕素材，此素材遍历不同摄像机下的小人的所有基本动作，作为“剪下来的动态图画”。将这些素材与背景地图相合成。合成方式由算法得出。

进阶操作：绿幕素材可包含常见特效，例如体香的蓝盾等各种光污染；合成方式不局限于小人普通地合成在地图上，可包含多个小人的多种互相遮挡等。

### 操作指南

1. 在工作目录创建inputs文件夹，并在其中添加需要合成的前景视频（foreground_video_raw.mp4）与背景视频（background_video.mp4）
2. foreground_video_raw.mp4建议分辨率为1080*1350，时长为20秒内，内容为学生加绿幕，可使用ae与clipchamp制作。示例见下方
3. background_video.mp4建议分辨率为2560*1440，时长为20秒内，内容为空的地图背景，可使用ae制作。示例见下方
4. 运行test.py，在cache/result_pic目录中可查看合成出的图片，格式为frame__xxxx.png
5. 如有将合成出的图片生成视频的需求，请创建outputs文件夹，并运行generate_video.py

![foreground_video_raw.mp4图片示例](https://github.com/BlueArchiveAutoSensei/autoAnnotation/blob/dev/foreground_video_raw_example.png)

![background_video.mp4图片示例](https://github.com/BlueArchiveAutoSensei/autoAnnotation/blob/dev/background_video_example.png)

### v0.0.1

已实现：

1. 视频分割图片
2. 前景图片处理
    1. 去绿幕
    2. 缩放
3. 前景图片与背景图片的简单合成
    1. 随机坐标生成

待实现：

1. 去绿幕算法改进
2. 生成yolov8标注文件
3. 线程优化，运行速度优化
4. 支持更长视频
5. 自定义分割帧数
6. 随机坐标生成算法改进
7. 支持多个前景（更多学生、光效、血条、掩体等）合成到背景
