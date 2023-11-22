from material import Map,Character
from synthesizer import Sythesizer
from datasetCollator import DatasetCollator

# 在materialData.json中填写背景地图视频路径和角色摆放边界
# 注意！！！：角色摆放边界4个坐标值顺序必须是ABDC或ACDB
#      A-----------B
#      |           |
#      |           |
#      |           |
#      C-----------D
map = Map("map_1")
map.process()
# 在materialData.json中填写角色名，角色视频路径
# 暂只支持一个动作视频且不支持填写标注范围，请在"run"中填写
character_1 = Character("akane")
character_1.process()

# 填写数据集中图片最小含量
sythesizer = Sythesizer(map,[character_1],4000)
sythesizer.execute()
# 填写数据集名称
datasetCollator = DatasetCollator("dataset_1",sythesizer.labels,sythesizer._img_and_txt_folder)
datasetCollator.execute()

# shutil.rmtree('cache')

