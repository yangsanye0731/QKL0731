import time
from pywinauto import Application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys


# 撤卖
def discharge():
    # 点击撤销
    click(coords=(50, 180))  # 在 (100, 200) 坐标处点击
    time.sleep(1)
    # 进入证券代码行
    click(coords=(466, 108))
    click(coords=(938, 563))
    # 点击确定
    click(coords=(1015, 557))


if __name__ == "__main__":
    discharge()
