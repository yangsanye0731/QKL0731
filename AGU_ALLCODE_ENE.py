#encoding=utf-8

import time
import numpy as num
import tushare as ts
import common
import common_mysqlUtil
import talib as ta
import common_image
from bypy import ByPy

def strategy(zhouqi, zhouqi2):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    str_result = 0
    for codeItem in all_code_index_x:
        count = count + 1
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)
        data_history_2 = ts.get_k_data(codeItem, ktype=zhouqi2)

        try:
            closeArray = num.array(data_history['close'])
            highArray = num.array(data_history['high'])
            lowArray = num.array(data_history['low'])
            openArray = num.array(data_history['open'])

            closeArray_2 = num.array(data_history_2['close'])
            highArray_2 = num.array(data_history_2['high'])
            lowArray_2 = num.array(data_history_2['low'])
            openArray_2 = num.array(data_history_2['open'])

            doubleCloseArray = num.asarray(closeArray, dtype='double')
            doubleHighArray = num.asarray(highArray, dtype='double')
            doubleLowArray = num.asarray(lowArray, dtype='double')
            doubleOpenArray = num.asarray(openArray, dtype='double')

            doubleCloseArray_2 = num.asarray(closeArray_2, dtype='double')
            doubleHighArray_2 = num.asarray(highArray_2, dtype='double')
            doubleLowArray_2 = num.asarray(lowArray_2, dtype='double')
            doubleOpenArray_2 = num.asarray(openArray_2, dtype='double')

            param_m1 = 11
            param_m2 = 9
            param_n = 10
            sma_n = ta.SMA(doubleCloseArray, param_n)
            upper = (1 + param_m1 / 100) * sma_n
            lower = (1 - param_m2 / 100) * sma_n
            ene = (upper + lower) / 2
            upper = upper.round(2)
            ene = ene.round(2)
            lower = lower.round(2)

            upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_2, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                         matype=0)
            data = common_mysqlUtil.select_all_code_one(codeItem)
            mingcheng = ""
            if len(data) > 0:
                mingcheng = data[0][1]

            if (ene[-1] > ene[-2]):
                if (lowArray_2[-1] < lowerband[-1]):
                    common_image.plt_image_tongyichutu_wueps(codeItem, "W", "04月线ENE上升，日线触布林下轨", "04月线ENE上升，日线触布林下轨")
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return str(str_result)

str_result = strategy('M', 'D')
print(str_result)
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发04月线ENE上升，日线触布林下轨', '触发04月线ENE上升，日线触布林下轨')
