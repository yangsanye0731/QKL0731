# encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
from bypy import ByPy
import common_mysqlUtil

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

        data_history_M = ts.get_k_data(codeItem, ktype='M')
        data_history_D = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] and \
                    ma5[-3] < ma5[-4] and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
                data = common_mysqlUtil.select_all_code_one(codeItem)
                if len(data) > 0:
                    mingcheng = data[0][1]
                common_image.plt_image_tongyichutu_2(codeItem, "W", "【03全部代码】跨越5周线容大感光,主力持仓突增", "【03全部代码】跨越5周线容大感光,主力持仓突增")

                # common.dingding_markdown_msg_link("触发【03全部代码】跨越5周线容大感光,主力持仓突增(" + mingcheng + codeItem + ")",
                #                                "触发【03全部代码】跨越5周线容大感光,主力持仓突增(" + mingcheng + codeItem + ")",
                #                                    "http://stockpage.10jqka.com.cn/" + codeItem)

            closeArray_M = num.array(data_history_M['close'])
            doubleCloseArray_M = num.asarray(closeArray_M, dtype='double')
            lowArray_M = num.array(data_history_M['low'])
            doubleLowArray_M = num.asarray(lowArray_M, dtype='double')
            closeArray_D = num.array(data_history_D['close'])
            doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')
            lowArray_D = num.array(data_history_D['low'])
            doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

            param_m1 = 11
            param_m2 = 9
            param_n = 10
            sma_n = ta.SMA(closeArray_M, param_n)
            upper = (1 + param_m1 / 100) * sma_n
            lower = (1 - param_m2 / 100) * sma_n
            ene = (upper + lower) / 2
            upper = upper.round(2)
            ene = ene.round(2)
            lower = lower.round(2)

            if (ene[-1] > ene[-2]):
                upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_D, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                             matype=0)
                if doubleLowArray_D[-1] < lowerband[-1]:
                    common_image.plt_image_tongyichutu_2(codeItem, "W", "【03全部代码】ENE月线升势，布林日线下穿", "【03全部代码】ENE月线升势，布林日线下穿")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult_W = strategy('W')
sendMail(template1(strMailResult_W), "【03全部代码】跨越5周线容大感光,主力持仓突增执行完成")

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【03全部代码】跨越5周线容大感光,主力持仓突增', '触发【03全部代码】跨越5周线容大感光,主力持仓突增')