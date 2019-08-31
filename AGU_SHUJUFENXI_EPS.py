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

def code_eps():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    count2 = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        # print(count)

        try:
            eps, epsup = common.codeEPS(codeItem)
            if (epsup > 300):
                strResult = strResult  + codeItem + ",EPS增长率：" + "%.1f" % epsup + "\n\n"
            time.sleep(2)
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    return strResult

re = code_eps()
print(re)
common.dingding_markdown_msg_2("EPS执行完成", re)