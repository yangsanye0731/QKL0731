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

def strategy():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    all_code_index_x = num.array(all_code_index)

    count = 0
    strResult = ""
    strResult_2 = ""

    for codeItem in all_code_index_x:
        count = count + 1
        print("正在执行：" + str(count))
        data_history = ts.get_k_data(codeItem, ktype='W')
        data_history_D = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            closeArray_D = num.array(data_history_D['close'])
            doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            lowArray = num.array(data_history['low'])
            doubleLowArray = num.asarray(lowArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma30_D = ta.SMA(doubleCloseArray_D, timeperiod=30)
            eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(codeItem)
            codeName = common.codeName(codeItem)

            # 30周线向上，且在20日线以上
            if (ma30_D[-1] > ma30_D[-2] and epsup > 0 and yingyeup > 0 and ma30_D[-2] < ma30_D[-3] and ma30_D[-3] < ma30_D[-4]):
                print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "======================================" + codeItem)
                common_image.plt_image_30DayLineUp(codeItem, codeName, "D", "%.1f" % epsup, "%.1f" % yingyeup)
                strResult += common.codeName(codeItem) + "30周线向上，且在20日线以上" + "<br>"

            # 最高点大于5周线，开点小于5周线，前两周五周线处于下降阶段
            if (doubleHighArray[-1] > ma5[-1] and doubleOpenArray[-1] < ma5[-1] and  epsup > 0 and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4]):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                df = common.daily_basic(codeItem)
                # 判断DataFrame是否为空
                turnover_rate = 0.0
                if df.empty:
                    print("empty")
                else:
                    turnover_rate = num.array(df['turnover_rate'])

                common_image.plt_image_kuaYueWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate)
                strResult += common.codeName(codeItem) + "跨越五周线" + "<br>"

            # 五周线连续下降
            if (ma5[-1] < ma5[-2] and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4] and ma5[-4] < ma5[-5] and epsup > 0 and yingyeup > 0 ):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                common_image.plt_image_lianXuXiaJiangWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)
                strResult_2 += common.codeName(codeItem) + "5周线连续下降" + "<br>"
            time.sleep(4)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult, strResult_2

strMailResult_W, strResult_2 = strategy()
sendMail(template1(strMailResult_W), "跨域5周线")
time.sleep(10)
sendMail(template1(strResult_2), "5周线连续下降")
