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
    # 获取实时数据
    data = common_mysqlUtil.select_xuangubao()
    # 数据遍历
    for i in range(len(data)):
        code = str(data[i][0])
        name = str(data[i][1])
        df = common.daily_basic(code)
        # 判断DataFrame是否为空
        if df.empty:
            continue
        # 总市值
        total_mv = num.array(df['total_mv'])
        # 市盈率
        pe = num.array(df['pe'])

        if pe[0] is None:
            pe[0] = 0.0
        # 换手率
        turnover_rate = num.array(df['turnover_rate'])
        # 名称
        time.sleep(5)
        name = common.codeName(code)
        common_mysqlUtil.update_xuangubao(name, "%.2f" % (total_mv / 10000), "%.2f" % pe, "%.2f" % turnover_rate, code)
        time.sleep(5)
strategy()