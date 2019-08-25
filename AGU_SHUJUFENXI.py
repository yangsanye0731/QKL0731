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


def zongshuju(code,endDate):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.weekly(ts_code=code, start_date='20180101', end_date=endDate, fields='ts_code,trade_date,open,high,low,close,vol,amount')
    # print(code + "===================================================")
    # print(df)
    return df

def yueshuju(code,endDate):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.monthly(ts_code=code, start_date='20180101', end_date=endDate, fields='ts_code,trade_date,open,high,low,close,vol,amount')
    return df

def zhishu_rishuju(code,endDate):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('0'):
        code = code + '.SH'
    # if code.startswith('01'):
    #     code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.index_daily(ts_code=code, start_date='20180101', end_date=endDate, fields='ts_code,trade_date,open,high,low,close,vol,amount')
    return df


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
        data_history = zongshuju(codeItem,curDate)
        data_history_M = yueshuju(codeItem,curDate)

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
                count2 = count2 + 2

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    global array1
    global array2
    array1.append(count2)

    data_history_chuangyeban = zhishu_rishuju("399006", curDate)
    closeArray_chuangyeban = num.array(data_history_chuangyeban['close'])
    doubleCloseArray_chuagnyeban = num.asarray(closeArray_chuangyeban, dtype='double')
    array2.append(doubleCloseArray_chuagnyeban[0])

    array3.append(curDate)
    print(count2)
    print(doubleCloseArray_chuagnyeban[0])

    return count2,doubleCloseArray_chuagnyeban[0]


countx8 = zhou_chuang_xin_gao_count("20190705")
countx7 = zhou_chuang_xin_gao_count("20190712")
countx6 = zhou_chuang_xin_gao_count("20190719")
countx5 = zhou_chuang_xin_gao_count("20190726")
countx4 = zhou_chuang_xin_gao_count("20190802")
countx3 = zhou_chuang_xin_gao_count("20190809")
countx2 = zhou_chuang_xin_gao_count("20190816")
countx1 = zhou_chuang_xin_gao_count("20190823")






# countx9 = zhou_chuang_xin_gao_count("2019-06-28")
# countx10 = zhou_chuang_xin_gao_count("2019-06-21")
# countx11 = zhou_chuang_xin_gao_count("2019-06-14")
# countx12 = zhou_chuang_xin_gao_count("2019-06-07")
# countx13 = zhou_chuang_xin_gao_count("2019-05-31")
# countx14 = zhou_chuang_xin_gao_count("2019-05-24")
# countx15 = zhou_chuang_xin_gao_count("2019-05-17")
# countx16 = zhou_chuang_xin_gao_count("2019-05-10")
# countx17 = zhou_chuang_xin_gao_count("2019-05-03")
# countx18 = zhou_chuang_xin_gao_count("2019-04-26")
# countx19 = zhou_chuang_xin_gao_count("2019-04-19")
# countx20 = zhou_chuang_xin_gao_count("2019-04-12")
# countx21 = zhou_chuang_xin_gao_count("2019-04-05")
# countx22 = zhou_chuang_xin_gao_count("2019-03-29")
# countx23 = zhou_chuang_xin_gao_count("2019-03-22")
# countx24 = zhou_chuang_xin_gao_count("2019-03-15")
# countx25 = zhou_chuang_xin_gao_count("2019-03-08")
# countx26 = zhou_chuang_xin_gao_count("2019-03-01")
# countx27 = zhou_chuang_xin_gao_count("2019-02-22")
# countx28 = zhou_chuang_xin_gao_count("2019-02-15")
# countx29 = zhou_chuang_xin_gao_count("2019-02-08")
# countx30 = zhou_chuang_xin_gao_count("2019-02-01")
# countx31 = zhou_chuang_xin_gao_count("2019-01-25")
# countx32 = zhou_chuang_xin_gao_count("2019-01-18")
# countx33 = zhou_chuang_xin_gao_count("2019-01-11")
# countx34 = zhou_chuang_xin_gao_count("2019-01-04")


# common_image.plt_image_2(array1, array2, array3)

print(array1)
print(array2)
print(array3)

common.dingding_markdown_msg_2("aaa", array1)
