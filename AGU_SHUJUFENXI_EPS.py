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

# EPS分析结果
def code_eps():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = "EPS分析结果：<br>"
    strResult_2 = "上期EPS分析结果：<br>"
    for codeItem in all_code_index_x:
        count = count + 1
        print(count)
        try:
            eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2  = common.codeEPS(codeItem)
            codeName = common.codeName(codeItem)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "本期EPS:" + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup + " LYL:" + "%.1f" % yingyeup)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "上期EPS:" + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup_2 + " LYL:" + "%.1f" % yingyeup_2)
            if (epsup > 20 and yingyeup > 20):
                print(common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup +  " LYL:" + "%.1f" % yingyeup)
                strResult = strResult  + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup +  " LYL:" + "%.1f" % yingyeup + "<br>"

                data_history_W = ts.get_k_data(codeItem, ktype="W")
                closeArray_W = num.array(data_history_W['close'])
                doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')

                SMA_W_5 = ta.SMA(doubleCloseArray_W, timeperiod=5)
                if (doubleCloseArray_W[-1] < SMA_W_5[-1]):
                    strResult = strResult + codeName + "本期EPS增长50%以上，但当前价格在5周线以下=================================<br>"
                    common_image.plt_image_week5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)

            if (epsup_2 > 20 and yingyeup_2 > 20):
                print(common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup_2 + " LYL:" + "%.1f" % yingyeup_2)
                strResult_2 = strResult_2 + common.codeName(codeItem) + ",EPS:" + "%.1f" % epsup_2 + " LYL:" + "%.1f" % yingyeup_2 + "<br>"

                data_history_W = ts.get_k_data(codeItem, ktype="W")
                closeArray_W = num.array(data_history_W['close'])
                doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')

                SMA_W_5 = ta.SMA(doubleCloseArray_W, timeperiod=5)
                if (doubleCloseArray_W[-1] < SMA_W_5[-1]):
                    strResult_2 = strResult_2 + codeName + "上期EPS增长50%以上，但当前价格在5周线以下=================================<br>"
                    common_image.plt_image_week5Line(codeItem, codeName, "W", "%.1f" % epsup_2, "%.1f" % yingyeup_2)
            time.sleep(2)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    return strResult, strResult_2

re1, re2 = code_eps()
sendMail(template1(re1), "EPS分析结果已输出")
time.sleep(10)
sendMail(template1(re2), "上期EPS分析结果已输出")
