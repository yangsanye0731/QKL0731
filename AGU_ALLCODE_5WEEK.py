#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image

def strategy(zhouqi):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        print(count)
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            # print(codeItem)
            # print(doubleCloseArray[-1])
            # print(ma5[-1])
            if (doubleCloseArray[-1] < ma5[-1]):
                print("======================================" + codeItem)
                strResult += common.codeName(codeItem) + "五周线以下" + "<br>"
                time.sleep(1)

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult_W = strategy('W')
sendMail(template1(strMailResult_W), "周线5周线以下")
