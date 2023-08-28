import time
from pywinauto import Application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys
import random

#######################################################################################################################
# ############################################################################################### 配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
import common


def buy(code, price, count):
    # 在全屏模式下点击买入菜单
    click(coords=(70, 120))  # 在 (100, 200) 坐标处点击
    # 点击鼠标左键，进入证券代码文本输入框
    click(coords=(300, 165))
    # 在证券代码输入全选，并删除
    send_keys("^a")
    time.sleep(0.4)
    send_keys("{DELETE}")
    time.sleep(0.3)
    send_keys(code, pause=0.5)

    # 点击鼠标左键，进入买入价格文本框
    click(coords=(300, 264))
    # 在文本框中双击并删除
    time.sleep(0.2)
    double_click(coords=(300, 264))
    time.sleep(0.4)
    send_keys("{DELETE}")
    time.sleep(0.5)
    # 输入买入价格，这里是【变量】
    send_keys(price, pause=0.5)

    # 点击鼠标左键，进入买入数量行
    click(coords=(300, 325))
    # 在文本框中输入全选与删除
    send_keys("^a")
    time.sleep(0.6)
    send_keys("{DELETE}")
    time.sleep(0.3)
    # 输入要卖出的数量，这里是【变量】
    send_keys(count, pause=0.5)
    # 点击鼠标左键，点击卖出按钮
    click(coords=(400, 400))
    time.sleep(0.4)
    # 点击鼠标左键，点击卖出按钮
    click(coords=(904, 607))
    time.sleep(0.6)
    # 点击鼠标左键，点击卖出完成确认按钮
    click(coords=(1015, 557))

    # 点击ESC
    send_keys("{ESC}")

    # 发送消息
    send_dingding_msg(code, price, count)


def send_dingding_msg(code, price, count):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    common.dingding_markdown_msg_03(
        time_str + '触发自动买入' + code + '当前价格：' + price + ' 数量：' + count,
        time_str + '触发自动买入' + code + '当前价格：' + price + ' 数量：' + count)


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
    buy("159819", "0.755", "100")
    time.sleep(random.randrange(10))
    buy("159819", "0.755", "100")
    time.sleep(random.randrange(10))
    buy("159819", "0.755", "100")
    time.sleep(random.randrange(10))
    buy("159819", "0.755", "100")
    minimize(title_str)
