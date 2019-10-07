#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import common_xiangguanxing

def strategy():
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        print(count)

        try:
            result = common_xiangguanxing.xiangguanxing('399006',codeItem)
            if (result < 0.5):
                print(codeItem + ":" + "%.2f" % result)
                strResult = strResult + codeItem + ":" + "%.2f" % result + "<br>"
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print("")
    return strResult

strMailResult = strategy()
sendMail(strMailResult, "相似度执行完了")