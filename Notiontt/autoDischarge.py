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


def maximize(title_str):
    app = Application(backend='uia')
    app.connect(title=title_str, timeout=120)
    app[title_str].wrapper_object().maximize()
    print(app.windows())
    time.sleep(1)


def minimize(title_str):
    app = Application(backend='uia')
    app.connect(title=title_str, timeout=120)
    app[title_str].wrapper_object().minimize()


if __name__ == "__main__":
    # title_str = "东方财富终端"
    title_str = "东方财富证券交易"
    maximize(title_str)
    discharge()
    minimize(title_str)
