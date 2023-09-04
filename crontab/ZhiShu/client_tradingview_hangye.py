import time

import openpyxl
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

jsonDicCode1 = [('399001', '深证成指'), ('399006', '创业板指'), ('399231', '农林指数'), ('399232', '采矿指数'), ('399233', '制造指数'),
                ('399234', '水电指数'), ('399235', '建筑指数'), ('399236', '批零指数'), ('399237', '运输指数'), ('399238', '餐饮指数'),
                ('399239', 'IT指数'), ('399365', '国证农业'),
                ('399240', '金融指数'), ('399241', '地产指数'), ('399242', '商务指数'), ('399243', '科研指数'), ('399244', '公共指数'),
                ('399248', '文化指数'),
                ('399275', '创医药'), ('399276', '创科技'), ('399279', '云科技'),
                ('399280', '生物50'), ('399281', '电子50'), ('399282', '大数据50'), ('399283', '机器人50'), ('399285', '物联网50'),
                ('399286', '区块链50'),
                ('399353', '国证物流'),
                ('399360', '新硬件'), ('399363', '计算机指数'),
                ('399365', '国证粮食'),
                ('399368', '国证军工'), ('399382', '1000材料'), ('399394', '国证医药'), ('399395', '国证有色'),
                ('399396', '国证食品'), ('399397', '国证文化'), ('399412', '国证新能'), ('399432', '智能汽车'), ('399434', '国证传媒'),
                ('399435', '国证农牧'),
                ('399437', '国证证券'), ('399431', '国证银行'), ('399997', '中证白酒'), ('600519', '白酒_茅台'),
                ('399434', '国证传媒'), ('399435', '国证农林牧渔'), ('399441', '国证生物医药'), ('399693', '安防产业'),
                ('399804', '中证体育'), ('399807', '中证高铁'), ('399812', '中证养老'), ('399976', '中证新能源汽车'),
                ('399970', '中证移动互联网'), ('399989', '中证医疗'),
                ('399993', '中证生物科技'), ('399996', '中证智能家居'), ('399998', '中证煤炭'), ('601088', '煤炭_神华'),
                ('512480', '半导体ETF'), ('512760', '半导体50ETF'), ('512930', 'AIETF'), ('515050', '5GETF'),
                ('512690', '酒ETF'), ('518880', '黄金ETF'), ('515110', '一带一路国企ETF'), ('159995', '芯片ETF'),
                ('515000', '科技ETF'), ('515030', '新能源车ETF'), ('512170', '医疗ETF'), ('512660', '军工ETF'),
                ('515880', '通信ETF'), ('515980', '人工智能ETF')]

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
    send_keys(code, pause=0.1)
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

        for key, value in jsonDicCode1:
            codeItem = key
            image(codeItem)

        image(title_str)
        # 最小化窗口
        minimize(title_str)
    else:
        print("=====")
