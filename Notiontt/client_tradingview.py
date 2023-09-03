import time
from pywinauto import application
from pywinauto.mouse import click, double_click, right_click, move
from pywinauto.keyboard import send_keys
from pywinauto import findwindows
import random
from PIL import ImageGrab

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


def image(code):
    # 在全屏情况下点击搜索图标
    time.sleep(random.randint(2, 5))
    click(coords=(68, 58))  # 在 (100, 200) 坐标处点击
    time.sleep(random.randint(2, 5))
    # 在搜索栏中输入代号
    click(coords=(609, 295))
    # 在文本框中输入全选与删除
    send_keys("^a")
    time.sleep(round(random.uniform(0.2, 1), 1))
    send_keys("{DELETE}")
    time.sleep(round(random.uniform(0.2, 1), 1))
    # 输入股票代码，这里是【变量】
    send_keys(code, pause=round(random.uniform(0.2, 1), 1))
    time.sleep(round(random.uniform(0.2, 1), 1))
    send_keys("{ENTER}")
    time.sleep(2)
    # 截取整个屏幕
    screenshot = ImageGrab.grab()
    # 保存截图为文件
    screenshot.save("screenshot.png")
    # 关闭截图
    screenshot.close()
    time.sleep(16)


def send_dingding_msg(code, price, count):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    common.dingding_markdown_msg_03(
        time_str + '触发自动卖出' + code + '当前价格：' + price + ' 数量：' + count,
        time_str + '触发自动卖出' + code + '当前价格：' + price + ' 数量：' + count)


def maximize(title_str):
    windows = findwindows.find_windows(title_re=title_str + "")
    if windows:
        app = application.Application().connect(handle=windows[0])
        # window_title = app.top_window().window_text()
        app.top_window().wrapper_object().maximize()


def minimize(title_str):
    windows = findwindows.find_windows(title_re=title_str + "")
    if windows:
        app = application.Application().connect(handle=windows[0])
        # window_title = app.top_window().window_text()
        app.top_window().wrapper_object().minimize()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        title_str = "300482"
        # 最大化窗口
        maximize(title_str)
        image("XAUUSD")
        image("600547")

        image("XAGUSD")
        image("000426")

        image("COPPER")
        image("000630")

        image(title_str)
        # 最小化窗口
        minimize(title_str)
    else:
        print("=====")
