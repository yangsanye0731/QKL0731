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


def maximize():
    app = Application(backend='uia')
    app.connect(title='东方财富终端')
    app['东方财富终端'].wrapper_object().maximize()
    time.sleep(20)


def minimize():
    app = Application(backend='uia')
    app.connect(title='东方财富终端')
    app['东方财富终端'].wrapper_object().minimize()
    time.sleep(20)


if __name__ == "__main__":
    maximize()
    discharge()
    minimize()
