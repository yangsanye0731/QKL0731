#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import common_zhibiao
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

    # 30MIN上升数大于下降数，且上升数增加
    print("上升数：" + str(data1[0][5]))
    print("上升数：" + str(data1[0][6]))
    print("总数：" + str(data1[0][0]))
    print("总数618：" + str(int(data1[0][0] * 0.6)))
    if (data1[0][5] > int(data1[0][0] * 0.6) or data1[0][6] > int(data1[0][0] * 0.6)):
        sendMail("30MIN上升数，下降数达到618", "30MIN上升数，下降数达到618")

    # # 30MIN上升数小于下降数,且下降数增加
    # if (data1[0][5] < data1[0][6] and data1[0][6] > int(data2[0][6])):
    #     sendMail("30MIN下降数增加", "30MIN下降数增加，强烈卖出")

    # 插入日志信息
    common_mysqlUtil.insert_zhishu_count_record(type)

strategy("ZXG")
strategy("TOP")
# 发送信息
# common.dingding_markdown_msg_2(title,content)
# 发送邮件
# sendMail(title + "<br><br><br><br>" + content, title)


