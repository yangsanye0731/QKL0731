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

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            # ma20 = ta.SMA(doubleCloseArray, timeperiod=20)
            ma30 = ta.SMA(doubleCloseArray, timeperiod=30)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] and \
                    ma5[-3] < ma5[-4] and doubleCloseArray[-1] > doubleOpenArray[-1] and ma30[-1] > ma30[-2] and ma60[-1] > ma60[-2]:
                print(codeItem + "=======================================================================================")
                common.dingding_markdown_msg_2("触发20跨越5周线策略(" + codeItem + ")",
                                               "触发20跨越5周线策略(" + codeItem + ")")
                common_image.plt_image_tongyichutu(codeItem, "W", "20跨越5周线容大感光", "20跨越5周线容大感光")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

strMailResult_W = strategy('W')
sendMail(template1(strMailResult_W), "跨域5周线")

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发20跨越5周线执行完成', '触发20跨越5周线执行完成')