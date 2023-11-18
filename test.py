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
map = Map("street","inputs/map_1.mp4",[(285,536),(339,1315),(1681,1085),(1539,357)])
# 填写角色名，角色视频路径和最大缩放成的像素大小
akane = Character("akane","inputs/akane.mp4", 280)
reisa = Character("reisa","inputs/reisa.mp4", 280)
wakamo = Character("wakamo","inputs/wakamo.mp4", 280)
momoi = Character("momoi","inputs/momoi.mp4", 280)

map.process()
akane.process()
reisa.process()
wakamo.process()
momoi.process()

# 填写数据集中图片最小含量
sythesizer = Sythesizer(map,[akane,reisa,wakamo,momoi],2000)
sythesizer.execute()
# 填写数据集名称
datasetCollator = DatasetCollator("dataset",sythesizer.labels,sythesizer._img_and_txt_folder)
datasetCollator.execute()

# shutil.rmtree('cache')

