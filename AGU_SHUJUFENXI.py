#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
import common
import common_image
import datetime

xinGaoGeShu = []
zhiShuShuJu = []
riQi = []

def zhou_chuang_xin_gao_count(curDate):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    count2 = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        print(count)
        data_history = ts.get_k_data(codeItem, ktype="W", start="2018-06-01", end=curDate)
        data_history_M = ts.get_k_data(codeItem, ktype="M", start="2018-06-01", end=curDate)

        try:
            closeArray = num.array(data_history['close'])
            highArray = num.array(data_history['high'])
            lowArray = num.array(data_history['low'])

            highArray_M = num.array(data_history_M['high'])

            doubleCloseArray = num.asarray(closeArray, dtype='double')
            doubleHighArray = num.asarray(highArray, dtype='double')
            doubleLowArray = num.asarray(lowArray, dtype='double')

            doubleHighArray_M = num.asarray(highArray_M, dtype='double')

            if (highArray[-1] > doubleHighArray_M[-1] and highArray[-1] > doubleHighArray_M[-2] and highArray[-1] > doubleHighArray_M[-3]):
                count2 = count2 + 1

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    global xinGaoGeShu
    global zhiShuShuJu
    xinGaoGeShu.append(count2)

    data_history_chuangyeban = ts.get_k_data("399006", ktype="D", start="2018-06-01", end=curDate)
    closeArray_chuangyeban = num.array(data_history_chuangyeban['close'])
    doubleCloseArray_chuagnyeban = num.asarray(closeArray_chuangyeban, dtype='double')
    zhiShuShuJu.append(doubleCloseArray_chuagnyeban[-1])

    riQi.append(curDate)
    print(count2)
    print(doubleCloseArray_chuagnyeban[-1])

    return count2,doubleCloseArray_chuagnyeban[-1]

zhou_chuang_xin_gao_count("2019-01-04")
zhou_chuang_xin_gao_count("2019-01-11")
zhou_chuang_xin_gao_count("2019-01-18")
zhou_chuang_xin_gao_count("2019-01-25")
zhou_chuang_xin_gao_count("2019-02-01")
zhou_chuang_xin_gao_count("2019-02-08")
zhou_chuang_xin_gao_count("2019-02-15")
zhou_chuang_xin_gao_count("2019-02-22")
zhou_chuang_xin_gao_count("2019-03-01")
zhou_chuang_xin_gao_count("2019-03-08")
zhou_chuang_xin_gao_count("2019-03-15")
zhou_chuang_xin_gao_count("2019-03-22")
zhou_chuang_xin_gao_count("2019-03-29")
zhou_chuang_xin_gao_count("2019-04-05")
zhou_chuang_xin_gao_count("2019-04-12")
zhou_chuang_xin_gao_count("2019-04-19")
zhou_chuang_xin_gao_count("2019-04-26")
zhou_chuang_xin_gao_count("2019-05-03")
zhou_chuang_xin_gao_count("2019-05-10")
zhou_chuang_xin_gao_count("2019-05-17")
zhou_chuang_xin_gao_count("2019-05-24")
zhou_chuang_xin_gao_count("2019-05-31")
zhou_chuang_xin_gao_count("2019-06-07")
zhou_chuang_xin_gao_count("2019-06-14")
zhou_chuang_xin_gao_count("2019-06-21")
zhou_chuang_xin_gao_count("2019-06-28")
zhou_chuang_xin_gao_count("2019-07-05")
zhou_chuang_xin_gao_count("2019-07-12")
zhou_chuang_xin_gao_count("2019-07-19")
zhou_chuang_xin_gao_count("2019-07-26")
zhou_chuang_xin_gao_count("2019-08-02")
zhou_chuang_xin_gao_count("2019-08-09")
zhou_chuang_xin_gao_count("2019-08-16")
zhou_chuang_xin_gao_count("2019-08-23")

common_image.plt_image_2(xinGaoGeShu, zhiShuShuJu, riQi)
# print(xinGaoGeShu)
# print(zhiShuShuJu)
# print(riQi)
common.dingding_markdown_msg_2("新高执行完成", "新高执行完成")
