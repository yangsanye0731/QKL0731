import time
from pywinauto import Application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys

# 点击买入
click(coords=(70, 120))  # 在 (100, 200) 坐标处点击
# 进入证券代码行
click(coords=(300, 165))
# 输入全选与删除
send_keys("^a")
time.sleep(2)
send_keys("{DELETE}")
time.sleep(2)
send_keys("300482", pause=1)

# # 模拟鼠标
# click(coords=(100, 200))  # 在 (100, 200) 坐标处点击
#
# # 模拟鼠标双击
# double_click(coords=(150, 250))  # 在 (150, 250) 坐标处双击
#
# # 模拟鼠标右键点击
# right_click(coords=(200, 300))  # 在 (200, 300) 坐标处右键点击
#
# # 移动鼠标到指定坐标
# move(coords=(300, 400))