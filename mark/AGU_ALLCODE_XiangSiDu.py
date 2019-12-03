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
import common_mysqlUtil

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
            result = common_xiangguanxing.xiangguanxing('600587',codeItem)
            if (result < 1):
                print(codeItem + ":" + "%.2f" % result)
                strResult = strResult + codeItem + ":" + "%.2f" % result + "<br>"
                time.sleep(1)
                codeName = common.codeName(codeItem)
                zhangdiefu = common.zhangdiefu(codeItem)
                common_mysqlUtil.insert_xiangsidu_record(codeItem, codeName, "%.2f" % result, zhangdiefu)

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print("")
    return strResult

common_mysqlUtil.deleteXiangSiDuRecord()
strMailResult = strategy()
sendMail(strMailResult, "相似度计算执行完成，请查看")