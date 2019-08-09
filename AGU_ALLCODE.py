#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common

def strategy(zhouqi):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)

        try:
            closeArray = num.array(data_history['close'])
            # highArray = num.array(data_history['high'])
            # lowArray = num.array(data_history['low'])

            doubleCloseArray = num.asarray(closeArray, dtype='double')
            # doubleHighArray = num.asarray(highArray, dtype='double')
            # doubleLowArray = num.asarray(lowArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
            ma20 = ta.SMA(doubleCloseArray, timeperiod=20)
            ma30 = ta.SMA(doubleCloseArray, timeperiod=30)

            strMa = ""
            if (ma5[-1] > ma10[-1] > ma20[-1] > ma30[-1]):
                strMa = "形态好"

            if (ma5[-1] > ma5[-2] and ma10[-1] > ma10[-2] and ma20[-1] > ma20[-2] and ma30[-1] > ma30[-2]):
                if (ma5[-2] > ma5[-3] and ma10[-2] > ma10[-3] and ma20[-2] > ma20[-3] and ma30[-2] > ma30[-3]):
                    if (ma5[-3] > ma5[-4] and ma10[-3] > ma10[-4] and ma20[-3] > ma20[-4] and ma30[-3] > ma30[-4]):
                        continue

                # macd 为快线 macdsignal为慢线，macdhist为柱体
                macd, macdsignal, macdhist = ta.MACD(doubleCloseArray, fastperiod=12, slowperiod=26, signalperiod=9)
                strMacd = ""
                if (macdsignal[-1] > macdsignal[-2]):
                    strMacd = "_MACD升势"
                strResult += codeItem + "_" + common.gupiaomingcheng(codeItem) + "_" + common.zhangdiefu(codeItem) + strMacd + "_" + strMa + "<br>"
                print(count)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult_D = strategy('D')
sendMail(template1(strMailResult_D), "日线四线俱升")
strMailResult_W = strategy('W')
sendMail(template1(strMailResult_W), "周线四线俱升")
strMailResult_M = strategy('M')
sendMail(template1(strMailResult_M), "月线四线俱升")
