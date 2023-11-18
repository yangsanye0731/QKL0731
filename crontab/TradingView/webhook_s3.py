# encoding=utf-8
import numpy as num
import talib as ta
import tushare as ts
import time
from tabulate import tabulate
import random

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common_image
import common
import common_mysqlUtil
from datetime import datetime, timedelta
import logging
import warnings
import threading
import Notiontt.zx_autobuy as zx_autobuy
import Notiontt.zx_autosell as zx_autosell
import Notiontt.client as client
import Notiontt.zx_client as zx_client

warnings.filterwarnings("ignore")

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)
import common_notion
import pygame

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
dic = common_notion.find_config_item_from_database("18fcc6b54f574e97b1d6fe907260d37a")
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
                ('399434', '国证传媒'), ('399435', '国证农林牧渔'), ('399440', '国证钢铁'), ('399441', '国证生物医药'), ('399693', '安防产业'),
                ('399804', '中证体育'), ('399807', '中证高铁'), ('399812', '中证养老'), ('399976', '中证新能源汽车'),
                ('399970', '中证移动互联网'), ('399989', '中证医疗'),
                ('399993', '中证生物科技'), ('399996', '中证智能家居'), ('399998', '中证煤炭'), ('601088', '煤炭_神华'),
                ('512480', '半导体ETF'), ('512760', '半导体50ETF'), ('512930', 'AIETF'), ('515050', '5GETF'),
                ('512690', '酒ETF'), ('518880', '黄金ETF'), ('515110', '一带一路国企ETF'), ('159995', '芯片ETF'),
                ('515000', '科技ETF'), ('515030', '新能源车ETF'), ('512170', '医疗ETF'), ('512660', '军工ETF'),
                ('515880', '通信ETF'), ('515980', '人工智能ETF')]


#######################################################################################################################
###########################################################################################################跨域5周线策略
def exec(codeItem):
    if codeItem.startswith("399") or codeItem.startswith("51"):
        for key, value in jsonDicCode1:
            if key == codeItem:
                codeName = value

    data = common_mysqlUtil.select_all_code_one(codeItem)
    if len(data) > 0:
        codeName = data[0][1]

    zhangdiefu, price = common.zhangdiefu_and_price(codeItem)
    logging.debug("编码： %s,名称：%s", codeItem, codeName)

    # 日线
    table_item_data = exec_d(codeItem, zhangdiefu, price, codeName)

    # 发送钉钉消息
    time_str_1 = time.strftime("%H:%M", time.localtime())
    # 卖出策略_当触发高线，并下跌超过0.5%时卖出
    sell_strategy1(table_item_data, codeItem, codeName, price, zhangdiefu)
    # 卖出策略_当触发线路反转时全部卖出
    sell_strategy2(table_item_data, codeItem, codeName, price, zhangdiefu)
    return table_item_data


def sell_strategy1(table_item_data, codeItem, codeName, price, zhangdiefu):
    # 当触发高线，并下跌超过0.5%时卖出
    xiadielv_h = (table_item_data[13] - float(price)) / table_item_data[13] > 0.005
    xiadielv_d = (table_item_data[14] - float(price)) / table_item_data[14] > 0.005
    if ("高线" in table_item_data[11] and xiadielv_h) or ("高线" in table_item_data[12] and xiadielv_d):
        common.dingding_markdown_msg_03(
            '🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:' +
            table_item_data[6] + 'D:' +
            table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12],
            '🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:' +
            table_item_data[6] + 'D:' +
            table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12])

        # 是否自动操作
        if "true" in get_auto_state("auto_sell"):
            logging.info('🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:'
                         + table_item_data[6] + 'D:' +
                         table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12])
            autosell(codeItem)


def sell_strategy2(table_item_data, codeItem, codeName, price, zhangdiefu):
    # 当触发线路反转时全部卖出
    if "顶部" in table_item_data[6]:
        common.dingding_markdown_msg_03(
            '🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:' +
            table_item_data[6] + 'D:' +
            table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12],
            '🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:' +
            table_item_data[6] + 'D:' +
            table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12])

        logging.info('🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:'
                     + table_item_data[6] + 'D:' +
                     table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12])

        # 是否自动操作
        if "true" in get_auto_state("auto_sell"):
            logging.info('🔋🔋【自动卖出】🔋🔋' + codeName + codeItem + '当:' + price + ' ' + zhangdiefu + ' H:'
                         + table_item_data[6] + 'D:' +
                         table_item_data[10] + ' 唐H:' + table_item_data[11] + ' 唐日:' + table_item_data[12])
            autosell(codeItem)


def exec_d(codeItem, zhangdiefu, price, codeName):
    # ======================================================60分钟数据
    data_history_60 = ts.get_k_data(codeItem, ktype='60')

    closeArray_60 = num.array(data_history_60['close'])
    doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')

    highArray_60 = num.array(data_history_60['high'])
    doubleHighArray_60 = num.asarray(highArray_60, dtype='double')

    lowArray_60 = num.array(data_history_60['low'])
    doubleLowArray_60 = num.asarray(lowArray_60, dtype='double')

    # 均线
    ma10_60 = ta.SMA(doubleCloseArray_60, timeperiod=10)
    sma10_60 = ta.EMA(ma10_60, timeperiod=10)
    state_60 = state(ma10_60, sma10_60)

    # 60分钟操作机会1：触碰到唐奇安底线
    state_dc_h = ""
    dc_high_60 = ta.MAX(doubleHighArray_60, timeperiod=20)
    dc_low_60 = ta.MIN(doubleLowArray_60, timeperiod=20)
    if doubleLowArray_60[-1] == dc_low_60[-1]:
        logging.debug("【交易机会】" + codeItem + codeName + "将触碰到唐奇安小时线底线")
        state_dc_h = "时底线"
    if doubleHighArray_60[-1] == dc_high_60[-1]:
        logging.debug("【交易机会】" + codeItem + codeName + "将触碰到唐奇安小时线高线")
        state_dc_h = "时高线📌"

    # ======================================================日线数据
    data_history = ts.get_k_data(codeItem, ktype='D')

    closeArray = num.array(data_history['close'])
    doubleCloseArray = num.asarray(closeArray, dtype='double')

    highArray = num.array(data_history['high'])
    doubleHighArray = num.asarray(highArray, dtype='double')

    lowArray = num.array(data_history['low'])
    doubleLowArray = num.asarray(lowArray, dtype='double')

    # 均线
    ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
    sma10 = ta.EMA(ma10, timeperiod=10)
    state_D = state(ma10, sma10)

    # 日线操作机会1：触碰到唐奇安底线
    dc_high = ta.MAX(doubleHighArray, timeperiod=20)
    dc_low = ta.MIN(doubleLowArray, timeperiod=20)
    state_dc_d = ""
    if doubleLowArray[-1] == dc_low[-1] or (doubleLowArray[-1] - dc_low[-1]) / dc_low[-1] < 0.01:
        logging.debug("【交易机会】" + codeItem + codeName + "将触碰到唐奇安日线底线")
        state_dc_d = "日线底线"
        # 自动买入
        # autobuy(codeItem)
    if doubleHighArray[-1] == dc_high[-1] or (dc_high[-1] - doubleHighArray[-1]) / dc_high[-1] < 0.01:
        logging.debug("【交易机会】" + codeItem + codeName + "将触碰到唐奇安日线高线")
        state_dc_d = "日线高线📌"

    # ======================================================周线数据
    data_history_W = ts.get_k_data(codeItem, ktype='W')

    closeArray_W = num.array(data_history_W['close'])
    doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')

    highArray_W = num.array(data_history_W['high'])
    doubleHighArray_W = num.asarray(highArray_W, dtype='double')

    lowArray_W = num.array(data_history_W['low'])
    doubleLowArray_W = num.asarray(lowArray_W, dtype='double')

    # 均线
    ma10_W = ta.SMA(doubleCloseArray_W, timeperiod=10)
    sma10_W = ta.EMA(ma10_W, timeperiod=10)
    state_W = state(ma10_W, sma10_W)

    table_item_data = [codeName, zhangdiefu, price, ma10_60[-3], ma10_60[-2], ma10_60[-1], state_60, ma10[-3], ma10[-2],
                       ma10[-1], state_D, state_dc_h, state_dc_d, dc_high_60[-1], dc_high[-1], state_W]

    return table_item_data


def state(ma10, sma10):
    item_state = ""
    if ma10[-3] < ma10[-2] < ma10[-1]:
        item_state = "上升"
    if ma10[-3] < ma10[-2] > ma10[-1]:
        item_state = "顶部"
    if ma10[-3] > ma10[-2] > ma10[-1]:
        item_state = "下降"
    if ma10[-3] > ma10[-2] < ma10[-1]:
        item_state = "底部"
    if ma10[-1] > sma10[-1] and ma10[-2] < sma10[-2]:
        item_state = "上穿"
    if ma10[-1] < sma10[-1] and ma10[-2] > sma10[-2]:
        item_state = "下穿"
    return item_state


def list_sell():
    code_list = []
    data = common_mysqlUtil.select_sell()
    for i in range(len(data)):
        codeItem = str(data[i][0])
        code_list.append(codeItem)
    return code_list


def get_auto_state(config_key):
    data = common_mysqlUtil.get_config(config_key)
    result = ""
    for i in range(len(data)):
        config_value = str(data[i][2])
        if config_value is not None:
            result = config_value
    return result


def main(choice):
    if choice == '1':
        data = []
        headers = ["name", "ZDF", "JG", "ma10_60[-3]", "ma10_60[-2]", "ma10_60[-1]", "state_60", "ma10[-3]", "ma10[-2]",
                   "ma10[-1]", "state_d", "state_dc_h", "state_dc_d", "dc_high_60[-1]", "dc_high[-1]", "state_W"]
        # 从Notion配置项中获取数据
        # my_list = dic.get('chicang_list').split(",")
        # 从数据库中获取数据
        my_list = list_sell()
        index = 0
        while index < len(my_list):
            table_item_data1 = exec(my_list[index])
            data.append(table_item_data1)
            index += 1
        table = tabulate(data, headers, tablefmt="grid")
    elif choice == '2':
        data = []
        headers = ["name", "ZDF", "JG", "ma10_60[-3]", "ma10_60[-2]", "ma10_60[-1]", "state_60", "ma10[-3]", "ma10[-2]",
                   "ma10[-1]", "state_d", "state_dc_h", "state_dc_d", "dc_high_60[-1]", "dc_high[-1]", "state_W"]
        table_item_data = exec("300482")
        data.append(table_item_data)
        table = tabulate(data, headers, tablefmt="grid")

    # logging.info(table)
    return data


# 定义一个函数，作为线程要执行的操作
def another_operation(param):
    try:
        common_mysqlUtil.acquire_lock()
        logging.debug("获取锁成功")
        # 获取当前时间
        start_time = time.time()
        title = "触发一级响应,进入一级响应SOP"
        text = "触发一级响应,进入一级响应SOP"
        while time.time() - start_time < 3600:
            logging.debug("消息发送中，%s", str(time.time() - start_time))
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(5)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(1)
            common.dingding_markdown_msg_04(title, text)
            time.sleep(60)
        common_mysqlUtil.release_lock()
        logging.debug("释放锁成功")
    except (IOError, TypeError, NameError, IndexError, Exception) as e:
        logging.debug("获取锁失败")


def autobuy(code):
    if "true" in get_auto_state("auto_sell"):
        zx_result = dic.get('zx_auto_list')
        if zx_result is not None and code in zx_result:
            zhangdiefu, price = common.zhangdiefu_and_price(code)
            zx_client.auto_operate(p_type="b", p_code=code, p_price=price, p_count=1000)

        result = dic.get('auto_list')
        if result is not None and code in result:
            zhangdiefu, price = common.zhangdiefu_and_price(code)
            client.auto_operate(p_type="b", p_code=code, p_price=price, p_count=1000)


def autosell(code):
    if "true" in get_auto_state("auto_sell"):
        zhangdiefu, price = common.zhangdiefu_and_price(code)
        data = common_mysqlUtil.select_sell()
        for i in range(len(data)):
            codeItem = str(data[i][0])
            if codeItem == code:
                if data[i][2] == '中信证券' and data[i][3] > 100:
                    playsound()
                    time.sleep(30)
                    zhangdiefu, price = common.zhangdiefu_and_price(code)
                    zx_client.auto_operate(p_type="s", p_code=code, p_price=price, p_count=data[i][3])
                    common_mysqlUtil.update_sell(data[i][4], "0")

                if data[i][2] == '东方财富' and data[i][3] > 100:
                    playsound()
                    time.sleep(30)
                    zhangdiefu, price = common.zhangdiefu_and_price(code)
                    client.auto_operate(p_type="s", p_code=code, p_price=price, p_count=data[i][3])
                    common_mysqlUtil.update_sell(data[i][4], "0")


def playsound():
    pygame.init()

    # 初始化音频
    pygame.mixer.init()
    # 加载音频文件
    sound = pygame.mixer.Sound('D:\\workspace\\python\\QKL0731\\crontab\\TradingView\\y1871.wav')

    # 播放音频
    sound.play()
    # 暂停音频
    pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频结束
    pygame.mixer.quit()


#######################################################################################################################
##############################################################################################################主执行程序
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            data = main('1')
            # my_list = dic.get('tixing_list').split(";")
            # text = "【触发Tips】" + random.choice(my_list)
            # time.sleep(2)
            # common.dingding_markdown_msg_03(text, text)
        elif sys.argv[1] == '2':
            data = main('1')
            for row in data:
                name, zhangdiefu, price, ma10_60_3, ma10_60_2, ma10_60, state_60, ma10_3, ma10_2, ma10, state_D, state_dc_D = row
                c1 = "顶部" in state_60 or "底部" in state_60 or "上穿" in state_60 or "下穿" in state_60
                c2 = "顶部" in state_D or "底部" in state_D or "上穿" in state_D or "下穿" in state_D

                if c1 or c2:
                    param_value = "一级响应启动"
                    # 创建一个线程，并指定要执行的函数
                    thread = threading.Thread(target=another_operation, args=(param_value,))
                    # 启动线程
                    thread.start()
                    break

            my_list = dic.get('tixing_list').split(";")
            text = "【触发Tips】" + random.choice(my_list)
            time.sleep(2)
            common.dingding_markdown_msg_03(text, text)
        else:
            exec(sys.argv[1])
    else:
        print("==============操作系统面板命令行==================")
        print("(0) 注意信息")
        print("(1) 当前情况")
        print("===============================================")

        choice = input("请输入命令编号: ").strip().lower()
        main(choice)
