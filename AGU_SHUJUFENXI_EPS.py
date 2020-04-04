#encoding=utf-8

import numpy as num
import tushare as ts
import talib as ta
import common
import common_image
import common_image_xuangubao
import common_zhibiao
from email_util import *
from bypy import ByPy
import common_mysqlUtil

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

            highArray_D = num.array(data_history_D['high'])
            doubleHighArray_D = num.asarray(highArray_D, dtype='double')

            lowArray = num.array(data_history['low'])
            doubleLowArray = num.asarray(lowArray, dtype='double')

            lowArray_D = num.array(data_history_D['low'])
            doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            openArray_D = num.array(data_history_D['open'])
            doubleOpenArray_D = num.asarray(openArray_D, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma30_D = ta.SMA(doubleCloseArray_D, timeperiod=30)
            eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(codeItem)
            codeName, industry = common.codeName_and_industry(codeItem)
            ene_qushi_D = common_zhibiao.ENE_zhibiao(doubleCloseArray_D)
            ene_qushi_W = common_zhibiao.ENE_zhibiao(doubleCloseArray)

            # # 30周线向上，且在20日线以上
            # if (ma30_D[-1] > ma30_D[-2] and epsup > 0 and yingyeup > 0 and ma30_D[-2] < ma30_D[-3] and ma30_D[-3] < ma30_D[-4]):
            #     print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "======================================" + codeItem)
            #     common_image.plt_image_30DayLineUp(codeItem, codeName, "D", "%.1f" % epsup, "%.1f" % yingyeup)
            #     strResult += common.codeName(codeItem) + "30周线向上，且在20日线以上" + "<br>"

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if (doubleHighArray[-1] > ma5[-1] and doubleOpenArray[-1] < ma5[-1] and  epsup > 0 and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4]):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                df = common.daily_basic(codeItem)
                # 判断DataFrame是否为空
                turnover_rate = 0.0
                if df.empty:
                    print("empty")
                else:
                    turnover_rate = num.array(df['turnover_rate'])

                common_image.plt_image_kuaYueWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                strResult += common.codeName(codeItem) + "跨越五周线" + "<br>"

            # 周ENE中线趋势向上
            if ("ENE" in ene_qushi_W and  epsup > 0):
                print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "======================================" + codeItem)
                df = common.daily_basic(codeItem)
                # 判断DataFrame是否为空
                turnover_rate = 0.0
                if df.empty:
                    print("empty")
                else:
                    turnover_rate = num.array(df['turnover_rate'])

                common_image.plt_image_ENEWEEK(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                strResult += common.codeName(codeItem) + "ENE 周线趋势向上" + "<br>"

            # 周孕线
            n = 0
            if (doubleCloseArray[n-3] > doubleCloseArray[n-2] and doubleCloseArray[n-1] >= doubleCloseArray[n-2]):
                if (doubleHighArray[n-2] > doubleHighArray[n-1] and doubleLowArray[n-2] < doubleLowArray[n-1]):
                    if(doubleOpenArray[n-2] > doubleCloseArray[n-1] and doubleCloseArray[n-2] < doubleOpenArray[n-1]):
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                        df = common.daily_basic(codeItem)
                        # 判断DataFrame是否为空
                        turnover_rate = 0.0
                        if df.empty:
                            print("empty")
                        else:
                            turnover_rate = num.array(df['turnover_rate'])

                        common_image.plt_image_YUNXIANWEEK(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                        strResult += common.codeName(codeItem) + "周孕线" + "<br>"

            # 日孕线
            n = 0
            if (doubleCloseArray_D[n - 3] > doubleCloseArray_D[n - 2] and doubleCloseArray_D[n - 1] >= doubleCloseArray_D[n - 2]):
                if (doubleHighArray_D[n - 2] > doubleHighArray_D[n - 1] and doubleLowArray_D[n - 2] < doubleLowArray_D[n - 1]):
                    if (doubleOpenArray_D[n - 2] > doubleCloseArray_D[n - 1] and doubleCloseArray_D[n - 2] < doubleOpenArray_D[n - 1]):
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                        df = common.daily_basic(codeItem)
                        # 判断DataFrame是否为空
                        turnover_rate = 0.0
                        if df.empty:
                            print("empty")
                        else:
                            turnover_rate = num.array(df['turnover_rate'])

                        common_image.plt_image_YUNXIANDAY(codeItem, codeName, "D", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                        strResult += common.codeName(codeItem) + "日孕线" + "<br>"

            # # 五周线连续下降
            # if (ma5[-1] < ma5[-2] and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4] and ma5[-4] < ma5[-5] and epsup > 0 and yingyeup > 0 ):
            #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
            #     common_image.plt_image_lianXuXiaJiangWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup)
            #     strResult_2 += common.codeName(codeItem) + "5周线连续下降" + "<br>"
            time.sleep(3)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult, strResult_2


def strategy2():
    # 获取实时数据
    data = common_mysqlUtil.select_xuangubao()

    count = 0
    strResult = ""
    strResult_2 = ""

    for i in range(len(data)):
        count = count + 1
        print("正在执行：" + str(count))
        codeItem = str(data[i][0])
        data_history = ts.get_k_data(codeItem, ktype='W')
        data_history_D = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            closeArray_D = num.array(data_history_D['close'])
            doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            highArray_D = num.array(data_history_D['high'])
            doubleHighArray_D = num.asarray(highArray_D, dtype='double')

            lowArray = num.array(data_history['low'])
            doubleLowArray = num.asarray(lowArray, dtype='double')

            lowArray_D = num.array(data_history_D['low'])
            doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            openArray_D = num.array(data_history_D['open'])
            doubleOpenArray_D = num.asarray(openArray_D, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma30_D = ta.SMA(doubleCloseArray_D, timeperiod=30)
            eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(codeItem)
            codeName, industry = common.codeName_and_industry(codeItem)
            ene_qushi_D = common_zhibiao.ENE_zhibiao(doubleCloseArray_D)
            ene_qushi_W = common_zhibiao.ENE_zhibiao(doubleCloseArray)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if (doubleHighArray[-1] > ma5[-1] and doubleOpenArray[-1] < ma5[-1] and ma5[-2] < ma5[-3] and ma5[-3] < ma5[-4]):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                df = common.daily_basic(codeItem)
                # 判断DataFrame是否为空
                turnover_rate = 0.0
                if df.empty:
                    print("empty")
                else:
                    turnover_rate = num.array(df['turnover_rate'])

                common_image_xuangubao.plt_image_kuaYueWeek5Line(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                strResult += common.codeName(codeItem) + "跨越五周线" + "<br>"

            # 周ENE中线趋势向上
            if ("ENE" in ene_qushi_W):
                print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "======================================" + codeItem)
                df = common.daily_basic(codeItem)
                # 判断DataFrame是否为空
                turnover_rate = 0.0
                if df.empty:
                    print("empty")
                else:
                    turnover_rate = num.array(df['turnover_rate'])

                common_image_xuangubao.plt_image_ENEWEEK(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                strResult += common.codeName(codeItem) + "ENE 周线趋势向上" + "<br>"

            # 周孕线
            n = 0
            if (doubleCloseArray[n-3] > doubleCloseArray[n-2] and doubleCloseArray[n-1] >= doubleCloseArray[n-2]):
                if (doubleHighArray[n-2] > doubleHighArray[n-1] and doubleLowArray[n-2] < doubleLowArray[n-1]):
                    if(doubleOpenArray[n-2] > doubleCloseArray[n-1] and doubleCloseArray[n-2] < doubleOpenArray[n-1]):
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                        df = common.daily_basic(codeItem)
                        # 判断DataFrame是否为空
                        turnover_rate = 0.0
                        if df.empty:
                            print("empty")
                        else:
                            turnover_rate = num.array(df['turnover_rate'])

                        common_image_xuangubao.plt_image_YUNXIANWEEK(codeItem, codeName, "W", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                        strResult += common.codeName(codeItem) + "周孕线" + "<br>"

            # 日孕线
            n = 0
            if (doubleCloseArray_D[n - 3] > doubleCloseArray_D[n - 2] and doubleCloseArray_D[n - 1] >= doubleCloseArray_D[n - 2]):
                if (doubleHighArray_D[n - 2] > doubleHighArray_D[n - 1] and doubleLowArray_D[n - 2] < doubleLowArray_D[n - 1]):
                    if (doubleOpenArray_D[n - 2] > doubleCloseArray_D[n - 1] and doubleCloseArray_D[n - 2] < doubleOpenArray_D[n - 1]):
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "======================================" + codeItem)
                        df = common.daily_basic(codeItem)
                        # 判断DataFrame是否为空
                        turnover_rate = 0.0
                        if df.empty:
                            print("empty")
                        else:
                            turnover_rate = num.array(df['turnover_rate'])

                        common_image_xuangubao.plt_image_YUNXIANDAY(codeItem, codeName, "D", "%.1f" % epsup, "%.1f" % yingyeup, "%.2f" % turnover_rate, industry)
                        strResult += common.codeName(codeItem) + "日孕线" + "<br>"
            time.sleep(3)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult, strResult_2

strMailResult_W, strResult_2 = strategy()
#strMailResult, strResult = strategy2()
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
sendMail(template1(strMailResult), "跨域5周线")
time.sleep(10)
sendMail(template1(strResult), "5周线连续下降")
