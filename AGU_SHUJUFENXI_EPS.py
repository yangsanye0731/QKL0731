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

def strategy(zhouqi):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    strResult_2 = ""
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
            # if (doubleHighArray[-1] > ma5[-1] and doubleOpenArray[-1] < ma5[-1] and epsup > 0 and yingyeup > 0):
            #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
            #     common_image.plt_image_kuaYueWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)
            #     strResult += common.codeName(codeItem) + "跨越五周线" + "<br>"

            if (ma5[-1] < ma5[-2] and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4] and epsup > 0 and yingyeup > 0 ):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                common_image.plt_image_lianXuXiaJiangWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)
                strResult_2 += common.codeName(codeItem) + "5周线连续下降" + "<br>"

            time.sleep(2)

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult, strResult_2

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

strMailResult_W, strResult_2 = strategy('W')
sendMail(template1(strMailResult_W), "跨域5周线")
time.sleep(10)
sendMail(template1(strResult_2), "5周线连续下降")

re1, re2 = code_eps()
sendMail(template1(re1), "EPS分析结果已输出")
time.sleep(10)
sendMail(template1(re2), "上期EPS分析结果已输出")
