from material import Map,Character
from synthesizer import Sythesizer
from datasetCollator import DatasetCollator

# 填写背景地图视频路径和角色摆放边界
# 注意！！！：传入的4个坐标值顺序必须是ABDC或ACDB
#      A-----------B
#      |           |
#      |           |
#      |           |
#      C-----------D
map = Map("street","inputs/map_3.mp4",[(706,304),(609,773),(1598,601),(1447,113)])
map.process()
# 填写角色名，角色视频路径和最大缩放成的像素大小
aris = Character("aris","inputs/aris_1.mp4")
aru = Character("aru","inputs/aru_1.mp4")
azusa = Character("azusa","inputs/azusa_1.mp4")
toki = Character("toki","inputs/toki_1.mp4")
aris.process()
aru.process()
azusa.process()
toki.process()

# 填写数据集中图片最小含量
sythesizer = Sythesizer(map,[aris,aru,azusa,toki],2000)
sythesizer.execute()
# 填写数据集名称
datasetCollator = DatasetCollator("dataset",sythesizer.labels,sythesizer._img_and_txt_folder)
datasetCollator.execute()

# shutil.rmtree('cache')

