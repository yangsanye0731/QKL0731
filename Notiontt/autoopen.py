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


def maximize(title_str):
    app = Application(backend='uia')
    app.connect(title=title_str, timeout=120)
    app[title_str].wrapper_object().maximize()
    print(app.windows())
    time.sleep(2)


def minimize(title_str):
    app = Application(backend='uia')
    app.connect(title=title_str, timeout=120)
    app[title_str].wrapper_object().minimize()


if __name__ == "__main__":
    # 打开应用
    # app = Application().start("D:\\eastmoney\\swc8\\maintrade.exe")
    app = Application().start("C:\\eastmoney\\dfcfzq\\maintrade.exe")
    time.sleep(random.randint(5, 10))
    click(coords=(958, 686))
    send_keys("{ESC}")
    time.sleep(random.randint(5, 10))
    # 提示信息退出
    send_keys("{ESC}")
    # 输入密码
    click(coords=(859, 531))  # 在 (100, 200) 坐标处点击
    time.sleep(random.randint(2, 5))
    send_keys("888888", pause=round(random.uniform(0.2, 1), 1))
    # 点击确定
    click(coords=(960, 630))
    time.sleep(random.randint(10, 15))
    # 清理弹框
    send_keys("{ESC}")

    # title_str = "东方财富终端"
    title_str = "东方财富证券交易"
    # 最小化窗口
    minimize(title_str)
