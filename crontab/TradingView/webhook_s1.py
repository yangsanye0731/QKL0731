# encoding=utf-8
import numpy as num
import talib as ta
import tushare as ts
import time
from tabulate import tabulate

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
warnings.filterwarnings("ignore")

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


#######################################################################################################################
###########################################################################################################跨域5周线策略
def exec(codeItem):
    data = common_mysqlUtil.select_all_code_one(codeItem)
    if len(data) > 0:
        codeName = data[0][1]

    if codeItem == '399006':
        codeName = "创业板指"
    image_path = common_image.plt_image_geGuZhiBiao_tradingview(codeItem, codeName)
    image_url = "http://" + "8.218.97.91:8080" + "/" + image_path[6:]

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    zhangdiefu, price = common.zhangdiefu_and_price(codeItem)
    logging.debug("编码： %s,名称：%s", codeItem, codeName)

    # 日线
    table_item_data = exec_d(codeItem, zhangdiefu, price)

    logging.debug("ZDF： %s,  JG：%s", zhangdiefu, price)
    # 发送钉钉消息
    common.dingding_markdown_msg_03(
        time_str + '触发TradingView策略' + codeName + '(' + codeItem + ')' + '当前价格：' + price + ' 涨跌幅：' + zhangdiefu,
        time_str + '触发TradingView策略' + codeName + '(' + codeItem + ')' + '当前价格：' + price + ' 涨跌幅：' + zhangdiefu
        + "\n\n> ![screenshot](" + image_url + ")")
    return image_path, table_item_data


def exec_d(codeItem, zhangdiefu, price):
    # ======================================================60分钟数据
    data_history_60 = ts.get_k_data(codeItem, ktype='60')

    closeArray_60 = num.array(data_history_60['close'])
    doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')

    # 均线
    ma10_60 = ta.SMA(doubleCloseArray_60, timeperiod=10)
    sma10_60 = ta.EMA(ma10_60, timeperiod=10)

    ma60_60 = ta.SMA(doubleCloseArray_60, timeperiod=60)
    sma60_60 = ta.EMA(ma60_60, timeperiod=60)

    ma144_60 = ta.SMA(doubleCloseArray_60, timeperiod=144)
    sma144_60 = ta.EMA(ma144_60, timeperiod=144)

    # ======================================================日线数据
    data_history = ts.get_k_data(codeItem, ktype='D')

    closeArray = num.array(data_history['close'])
    doubleCloseArray = num.asarray(closeArray, dtype='double')

    # 均线
    ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
    sma10 = ta.EMA(ma10, timeperiod=10)

    ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
    sma60 = ta.EMA(ma60, timeperiod=60)

    ma144 = ta.SMA(doubleCloseArray, timeperiod=144)
    sma144 = ta.EMA(ma144, timeperiod=144)

    table_item_data = [zhangdiefu, price, ma10_60[-3], ma10_60[-2], ma10_60[-1], ma10[-3], ma10[-2], ma10[-1]]

    return table_item_data


def main(choice):
    data = []
    headers = ["ZDF", "JG", "ma10_60[-3]", "ma10_60[-2]", "ma10_60[-1]", "ma10[-3]", "ma10[-2]", "ma10[-1]"]
    if choice == '1':
        my_list = ['399006', '300482', '300835']
        index = 0
        while index < len(my_list):
            image_url_path, table_item_data1 = exec(my_list[index])
            data.append(table_item_data1)
            index += 1
    elif choice == '2':
        image_url_path, table_item_data = exec("300482")
        data.append(table_item_data)

    table = tabulate(data, headers, tablefmt="grid")
    print(table)


#######################################################################################################################
##############################################################################################################主执行程序
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            main('1')
        else:
            exec(sys.argv[1])
    else:
        print("==============操作系统面板命令行==================")
        print("(1) 当前持仓")
        print("(2) WanFuShengWu")
        print("===============================================")

        choice = input("请输入命令编号: ").strip().lower()
        main(choice)