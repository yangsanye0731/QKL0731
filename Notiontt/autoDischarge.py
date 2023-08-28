import time
from pywinauto import Application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys
import random

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


# 撤卖
def discharge_sell():
    # 点击撤销
    click(coords=(50, 180))  # 在 (100, 200) 坐标处点击
    time.sleep(0.3)
    # 撤卖
    click(coords=(466, 108))
    time.sleep(0.4)
    click(coords=(938, 563))
    # 点击确定
    time.sleep(0.2)
    click(coords=(1015, 557))

    # 发送钉钉消息
    send_dingding_msg("撤卖")


# 撤买
def discharge_buy():
    # 点击撤销
    click(coords=(50, 180))  # 在 (100, 200) 坐标处点击
    time.sleep(0.4)
    # 撤买
    click(coords=(392, 113))
    time.sleep(0.2)
    click(coords=(975, 563))
    # 点击确定
    time.sleep(0.3)
    click(coords=(1015, 557))
    # 发送钉钉消息
    send_dingding_msg("撤买")



def send_dingding_msg(type):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    common.dingding_markdown_msg_03(
        time_str + '触发自动插销' + '类型：' + type,
        time_str + '触发自动撤销' + '类型：' + type)


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
    discharge_sell()
    time.sleep(random.randrange(10))
    discharge_buy()
    minimize(title_str)
