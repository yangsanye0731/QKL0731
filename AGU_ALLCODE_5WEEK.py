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

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(codeItem)
            codeName = common.codeName(codeItem)
            # print(codeItem)
            # print(doubleCloseArray[-1])
            # print(ma5[-1])
            if (doubleHighArray[-1] > ma5[-1] and doubleOpenArray[-1] < ma5[-1] and epsup > 0 and yingyeup > 0):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                common_image.plt_image_kuaYueWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)
                strResult += common.codeName(codeItem) + "跨越五周线" + "<br>"
            time.sleep(2)

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult_W = strategy('W')
sendMail(template1(strMailResult_W), "跨域5周线")
