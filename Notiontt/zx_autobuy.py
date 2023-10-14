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
    click(coords=(37, 76))  # 在 (100, 200) 坐标处点击
    time.sleep(1)
    # 点击鼠标左键，进入证券代码文本输入框
    double_click(coords=(310, 111))
    # 在证券代码输入全选，并删除
    time.sleep(0.1)
    send_keys("{DELETE}")
    time.sleep(round(random.uniform(0.2, 0.3), 1))
    send_keys(code, pause=round(random.uniform(0.2, 0.3), 1))
    time.sleep(1)

    # 点击鼠标左键，进入买入价格文本框
    click(coords=(322, 153))
    # 在文本框中双击并删除
    double_click(coords=(311, 155))
    send_keys("{DELETE}")
    # 输入买入价格，这里是【变量】
    send_keys(price, pause=round(random.uniform(0.2, 0.3), 1))

    # 点击鼠标左键，进入买入数量行
    click(coords=(327, 200))
    # 在文本框中输入全选与删除8
    send_keys("^a")
    time.sleep(round(random.uniform(0.2, 0.3), 1))
    send_keys("{DELETE}")
    time.sleep(0.3)
    # 输入要卖出的数量，这里是【变量】
    send_keys(count, pause=round(random.uniform(0.2, 0.3), 1))
    # 点击鼠标左键，点击买入按钮
    click(coords=(332, 250))
    time.sleep(round(random.uniform(0.2, 0.3), 1))
    # 点击鼠标左键，点击买入完成确认按钮
    click(coords=(900, 644))
    time.sleep(round(random.uniform(0.2, 0.3), 1))
    # 点击鼠标左键，买入完成，关闭对话框
    click(coords=(951, 598))

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


def auto_operate(p_code, p_price, p_count):
    title_str = "中信证券至胜全能版"
    # 最大化窗口
    maximize(title_str)

    fenshu = p_count
    if p_count >= 1000:
        fenshu = 100
    if p_count >= 3000:
        fenshu = 200

    p_price = float(p_price)
    quotient, remainder = divmod(p_count, fenshu)
    for num in range(0, quotient):
        youxiaoshu = 2
        if p_price < 1:
            youxiaoshu = 3
        price_buy = round(p_price * (1 - 0.001 * num), youxiaoshu)
        buy(p_code, str(price_buy), str(fenshu))

    # 最小化窗口
    minimize(title_str)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        price = sys.argv[2]
        price_float = float(price)
        count = sys.argv[3]
        count_int = int(count)
        auto_operate(code, price_float, count_int)
    else:
        print("=====")
