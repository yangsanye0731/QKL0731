#encoding=utf-8
import pandas as pd
import time
import numpy as num
import ccxt
import talib as ta
from email_util import *
import common
import common_mysqlUtil

def strategy(type):
    # 获取实时数据
    data1 = common_mysqlUtil.selectCountRecord(type)
    print("实时数据：" + str(data1))

    # 获取已经入库的历史数据
    data2 = common_mysqlUtil.select_zhishu_count_record(type)
    print("已入库的历史数据:" + str(data2))

    # 如果历史数据为空，插入数据
    print(len(data2))
    if (len(data2) == 0):
        common_mysqlUtil.insert_zhishu_count_record(type)
        data2 = common_mysqlUtil.select_zhishu_count_record(type)

    # 插入日志信息
    common_mysqlUtil.insert_zhishu_count_record(type)

    # 30MIN上升数大于下降数，且上升数增加
    print("上升数：" + str(data1[0][5]))
    print("下降数：" + str(data1[0][6]))
    print("总数：" + str(data1[0][0]))
    print("总数618：" + str(int(data1[0][0] * 0.6)))
    if (data1[0][5] == 4 or data1[0][6] == 4 or data1[0][5] == 3 or data1[0][6] == 3 or data1[0][5] == 5 or data1[0][6] == 5):
        # sendMail("30MIN上升数，下降数达到一半", "30MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2(type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势",
                                       type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势")

        time.sleep(0.5)
        common.dingding_markdown_msg_2(type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势",
                                       type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势")

        time.sleep(0.5)
        common.dingding_markdown_msg_2(type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势",
                                       type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "已开始趋势")

    if (data1[0][3] == 4 or data1[0][4] == 4 or data1[0][3] == 3 or data1[0][4] == 3 or data1[0][3] == 5 or data1[0][4] == 5):
        # sendMail("60MIN上升数，下降数达到一半", "60MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2(type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势",
                                       type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势")

        time.sleep(0.5)
        common.dingding_markdown_msg_2(type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势",
                                       type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势")
        time.sleep(0.5)
        common.dingding_markdown_msg_2(type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势",
                                       type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "已开始趋势")


common_mysqlUtil.deleteTopRecord("BTC")
common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "BTC", "====", "========", "============", "======", "")
common_mysqlUtil.insert_zhishu_record("BTC/USDT", "BTC/USDT", "BTC/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("ETH/USDT", "ETH/USDT", "ETH/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("XRP/USDT", "XRP/USDT", "XRP/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("BCH/USDT", "BCH/USDT", "BCH/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("LTC/USDT", "LTC/USDT", "LTC/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("EOS/USDT", "EOS/USDT", "EOS/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("XLM/USDT", "XLM/USDT", "XLM/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("ADA/USDT", "ADA/USDT", "ADA/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("TRX/USDT", "TRX/USDT", "TRX/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("XMR/USDT", "XMR/USDT", "XMR/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("NEO/USDT", "NEO/USDT", "NEO/USDT",  "", "", "BTC")
time.sleep(10)
common_mysqlUtil.insert_zhishu_record("ETC/USDT", "ETC/USDT", "ETC/USDT",  "", "", "BTC")
time.sleep(10)
strategy("BTC")


