#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
import common
import common_image
import datetime
from email_util import *

def code_eps():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    count2 = 0
    all_code_index_x = num.array(all_code_index)

    strResult = "EPS分析结果：\n\n"
    strResult_2 = "上期EPS分析结果：\n\n"
    for codeItem in all_code_index_x:
        count = count + 1
        # print(count)

        try:
            eps, epsup,yingyeup = common.codeEPS(codeItem)
            eps_2, epsup_2, yingyeup_2 = common.codeEPS(codeItem)
            if (epsup > 50 and yingyeup > 20):
                print(common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup +  " LYL:" + "%.1f" % yingyeup)
                strResult = strResult  + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup +  " LYL:" + "%.1f" % yingyeup + "\n\n"

                data_history_W = ts.get_k_data(codeItem, ktype="W")
                closeArray_W = num.array(data_history_W['close'])
                doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')

                SMA_W_5 = ta.SMA(data_history_W, timeperiod=5)
                if (doubleCloseArray_W[-1] < SMA_W_5[-1]):
                    strResult = strResult + common.codeName(codeItem) + "本期EPS增长50%以上，但当前价格在5周线以下\n\n"
                time.sleep(3)
            if (eps_2 > 50 and yingyeup_2 > 20):
                print(common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup_2 + " LYL:" + "%.1f" % yingyeup_2)
                strResult_2 = strResult_2 + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup_2 + " LYL:" + "%.1f" % yingyeup_2 + "\n\n"

                data_history_W = ts.get_k_data(codeItem, ktype="W")
                closeArray_W = num.array(data_history_W['close'])
                doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')

                SMA_W_5 = ta.SMA(data_history_W, timeperiod=5)
                if (doubleCloseArray_W[-1] < SMA_W_5[-1]):
                    strResult_2 = strResult_2 + common.codeName(codeItem) + "上期EPS增长50%以上，但当前价格在5周线以下\n\n"
                time.sleep(3)

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    return strResult, strResult_2

re1, re2 = code_eps()
sendMail(template1(re1), "EPS分析结果已输出")
time.sleep(10)
sendMail(template1(re2), "上期EPS分析结果已输出")
