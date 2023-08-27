import time
from pywinauto import Application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys


def sell(code, price, count):
    # 在全屏情况下点击卖出菜单
    click(coords=(40, 150))  # 在 (100, 200) 坐标处点击
    # 点击鼠标左键进入证券代码行
    click(coords=(300, 165))
    # 在文本框中输入全选与删除
    send_keys("^a")
    time.sleep(0.5)
    send_keys("{DELETE}")
    time.sleep(0.5)
    # 输入股票代码，这里是【变量】
    send_keys(code, pause=0.5)

    # 点击鼠标左键，进入卖出价格文本框
    click(coords=(300, 264))
    # 在文本框中输入全选与删除
    time.sleep(0.5)
    double_click(coords=(300, 264))
    time.sleep(0.5)
    send_keys("{DELETE}")
    time.sleep(0.5)
    # 输入卖出价格，这里是【变量】
    send_keys(price, pause=0.5)

    # 点击鼠标左键，进入卖出数量行
    click(coords=(300, 325))
    # 在文本框中输入全选与删除
    send_keys("^a")
    time.sleep(1)
    send_keys("{DELETE}")
    time.sleep(1)
    # 输入要卖出的数量，这里是【变量】
    send_keys(count, pause=0.5)
    # 点击鼠标左键，点击卖出按钮
    click(coords=(400, 400))
    time.sleep(0.5)
    # 点击鼠标左键，点击卖出按钮
    click(coords=(904, 607))
    time.sleep(0.5)
    # 点击鼠标左键，点击卖出完成确认按钮
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
    # sell("300482", "25.01", "100")
    # time.sleep(30)
    # sell("300482", "25.02", "100")
    # time.sleep(20)
    # sell("300482", "25.03", "100")
    # time.sleep(50)
    # sell("300482", "25.04", "100")
    # time.sleep(40)
    # sell("300482", "25.05", "100")
    minimize(title_str)
