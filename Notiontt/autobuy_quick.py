# encoding=utf-8
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
import common_constants


def buy(code, price, count):
    # 在全屏模式下点击买入菜单
    click(coords=(70, 120))  # 在 (100, 200) 坐标处点击
    time.sleep(random.randint(2, 6))
    # 点击鼠标左键，进入证券代码文本输入框
    click(coords=(300, 165))
    # 在证券代码输入全选，并删除
    send_keys("^a")
    time.sleep(0.1)
    send_keys("{DELETE}")
    time.sleep(round(random.uniform(0.2, 1), 1))
    send_keys(code, pause=round(random.uniform(0.2, 1), 1))
    time.sleep(1)

    # 点击鼠标左键，进入买入价格文本框
    click(coords=(300, 264))
    # 在文本框中双击并删除
    time.sleep(0.2)
    double_click(coords=(300, 264))
    send_keys("{DELETE}")
    # 输入买入价格，这里是【变量】
    send_keys(price, pause=round(random.uniform(0.2, 0.5), 1))

    # 点击鼠标左键，进入买入数量行
    click(coords=(300, 325))
    # 在文本框中输入全选与删除
    send_keys("^a")
    send_keys("{DELETE}")
    time.sleep(0.3)
    # 输入要卖出的数量，这里是【变量】
    send_keys(count, pause=round(random.uniform(0.2, 0.5), 1))
    # 点击鼠标左键，点击卖出按钮
    click(coords=(400, 400))
    # 点击鼠标左键，点击卖出按钮
    click(coords=(904, 607))
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


def minimize(title_str):
    app = Application(backend='uia')
    app.connect(title=title_str, timeout=120)
    app[title_str].wrapper_object().minimize()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        price = sys.argv[2]
        price_float = float(price)
        count = sys.argv[3]
        level = sys.argv[4]
        count_int = int(count)
        level_int = int(level)

        title_str = common_constants.global_variable_dong_fang_cai_fu
        # 最大化窗口
        maximize(title_str)

        fenshu = count_int
        if count_int >= 1000:
            fenshu = 100 * level_int

        quotient, remainder = divmod(count_int, fenshu)
        for num in range(0, quotient):
            youxiaoshu = 2
            if price_float < 1:
                youxiaoshu = 3
            price_buy = round(price_float * (1 - 0.001 * num), youxiaoshu)
            buy(code, str(price_buy), str(fenshu))

        # 最小化窗口
        minimize(title_str)
    else:
        print("=====")
