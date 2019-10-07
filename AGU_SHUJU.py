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

def strategy():
    data1 = common_mysqlUtil.selectCountRecord()
    print(data1)
    data2 = common_mysqlUtil.select_zhishu_count_record()
    print(data2)

    print(len(data2))
    if (len(data2) == 0):
        common_mysqlUtil.insert_zhishu_count_record("ZXG")
        data2 = common_mysqlUtil.select_zhishu_count_record()

    # 30MIN上升数大于下降数，且上升数增加
    if (data1[0][5] > data1[0][6] and data1[0][5] > int(data2[0][5])):
        sendMail("30MIN上升数增加", "30MIN上升数增加，买入")

    # 30MIN上升数小于下降数,且下降数增加
    if (data1[0][5] < data1[0][6] and data1[0][6] > int(data2[0][6])):
        sendMail("30MIN下降数增加", "30MIN下降数增加，强烈卖出")
    common_mysqlUtil.insert_zhishu_count_record("ZXG")

strategy()
# 发送信息
# common.dingding_markdown_msg_2(title,content)
# 发送邮件
# sendMail(title + "<br><br><br><br>" + content, title)


