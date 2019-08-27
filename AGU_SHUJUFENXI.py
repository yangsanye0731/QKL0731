#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import datetime

array1 = []
array2 = []
array3 = []

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

    global array1
    global array2
    array1.append(count2)

    data_history_chuangyeban = ts.get_k_data("399006", ktype="D", start="2018-06-01", end=curDate)
    closeArray_chuangyeban = num.array(data_history_chuangyeban['close'])
    doubleCloseArray_chuagnyeban = num.asarray(closeArray_chuangyeban, dtype='double')
    array2.append(doubleCloseArray_chuagnyeban[-1])

    array3.append(curDate)
    print(count2)
    print(doubleCloseArray_chuagnyeban[-1])

    return count2,doubleCloseArray_chuagnyeban[-1]



countx34 = zhou_chuang_xin_gao_count("2019-01-04")
countx33 = zhou_chuang_xin_gao_count("2019-01-11")
countx32 = zhou_chuang_xin_gao_count("2019-01-18")
countx31 = zhou_chuang_xin_gao_count("2019-01-25")
countx30 = zhou_chuang_xin_gao_count("2019-02-01")
countx29 = zhou_chuang_xin_gao_count("2019-02-08")
countx28 = zhou_chuang_xin_gao_count("2019-02-15")
countx27 = zhou_chuang_xin_gao_count("2019-02-22")
countx26 = zhou_chuang_xin_gao_count("2019-03-01")
countx25 = zhou_chuang_xin_gao_count("2019-03-08")
countx24 = zhou_chuang_xin_gao_count("2019-03-15")
countx23 = zhou_chuang_xin_gao_count("2019-03-22")
countx22 = zhou_chuang_xin_gao_count("2019-03-29")
countx21 = zhou_chuang_xin_gao_count("2019-04-05")
countx20 = zhou_chuang_xin_gao_count("2019-04-12")
countx19 = zhou_chuang_xin_gao_count("2019-04-19")
countx18 = zhou_chuang_xin_gao_count("2019-04-26")
countx17 = zhou_chuang_xin_gao_count("2019-05-03")
countx16 = zhou_chuang_xin_gao_count("2019-05-10")
countx15 = zhou_chuang_xin_gao_count("2019-05-17")
countx14 = zhou_chuang_xin_gao_count("2019-05-24")
countx13 = zhou_chuang_xin_gao_count("2019-05-31")
countx12 = zhou_chuang_xin_gao_count("2019-06-07")
countx11 = zhou_chuang_xin_gao_count("2019-06-14")
countx10 = zhou_chuang_xin_gao_count("2019-06-21")
countx9 = zhou_chuang_xin_gao_count("2019-06-28")
countx8 = zhou_chuang_xin_gao_count("2019-07-05")
countx7 = zhou_chuang_xin_gao_count("2019-07-12")
countx6 = zhou_chuang_xin_gao_count("2019-07-19")
countx5 = zhou_chuang_xin_gao_count("2019-07-26")
countx4 = zhou_chuang_xin_gao_count("2019-08-02")
countx3 = zhou_chuang_xin_gao_count("2019-08-09")
countx2 = zhou_chuang_xin_gao_count("2019-08-16")
countx1 = zhou_chuang_xin_gao_count("2019-08-23")

common_image.plt_image_2(array1, array2, array3)

print(array1)
print(array2)
print(array3)
common.dingding_markdown_msg_2("新高执行完成", "新高执行完成")
