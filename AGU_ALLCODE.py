#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common

def strategy():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        data_history = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray = num.array(data_history['close'])
            highArray = num.array(data_history['high'])
            lowArray = num.array(data_history['low'])

            doubleCloseArray = num.asarray(closeArray, dtype='double')
            doubleHighArray = num.asarray(highArray, dtype='double')
            doubleLowArray = num.asarray(lowArray, dtype='double')
            ma5 = ta.SMA(num.asarray(doubleCloseArray, dtype='double'), timeperiod=5)
            ma10 = ta.SMA(num.asarray(doubleCloseArray, dtype='double'), timeperiod=10)
            ma20 = ta.SMA(num.asarray(doubleCloseArray, dtype='double'), timeperiod=20)

            if (ma5[-1] > ma5[-2] and ma10[-1] > ma10[-2] and ma20[-1] > ma20[-2]):
                if (ma5[-2] > ma5[-3] and ma10[-2] > ma10[-3] and ma20[-2] > ma20[-3]):
                    continue
                strResult += "编号:" + codeItem + "名称：" + common.gupiaomingcheng(codeItem) + "涨跌幅：" + common.zhangdiefu(codeItem) + "<br>"
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult = strategy()
sendMail(template1(strMailResult), "四线俱升")
