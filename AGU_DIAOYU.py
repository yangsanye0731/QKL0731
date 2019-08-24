#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import datetime

def diaoyu(code, startTime):
    count = 0
    # 1、起始时间的字符串转时间
    detester = startTime
    n_days = datetime.datetime.strptime(detester, "%Y-%m-%d")

    while(True):

        # 2、判断是否为交易日
        OpenList = ts.trade_cal()
        OpentimeList = OpenList.isOpen[OpenList.calendarDate == n_days.strftime("%Y-%m-%d")]

        # 3、如果是交易日 加1
        if (OpentimeList.values[0] == 1):
            print(n_days.strftime("%Y-%m-%d") + "是交易日，交易次数加1" )
            count = count + 1

        # 4、判断是否到当前时间，到了之后停止，如果没到，继续执行
        now = datetime.datetime.now()
        if (n_days.date() == now.date()):
            break

        delta = datetime.timedelta(days=1)
        n_days = n_days + delta

    return "今天是" + datetime.datetime.now().strftime("%Y-%m-%d") + ","+ code + "已下跌" + str(count) + "天，注意均线趋势"

str1 = diaoyu("比亚迪","2019-07-29")
common.dingding_markdown_msg_2(str1, str1)
str1 = diaoyu("恒顺酱油","2019-07-02")
common.dingding_markdown_msg_2(str1, str1)
str1 = diaoyu("联合光电","2019-08-23")
common.dingding_markdown_msg_2(str1, str1)
str1 = diaoyu("鹏鹞环保","2019-08-15")
common.dingding_markdown_msg_2(str1, str1)
