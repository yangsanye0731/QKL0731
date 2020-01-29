#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
import common
import common_mysqlUtil

def strategy(zhouqi, n):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        count = count + 1
        # print(count)
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)

        try:
            closeArray = num.array(data_history['close'])
            highArray = num.array(data_history['high'])
            lowArray = num.array(data_history['low'])
            openArray = num.array(data_history['open'])

            doubleCloseArray = num.asarray(closeArray, dtype='double')
            doubleHighArray = num.asarray(highArray, dtype='double')
            doubleLowArray = num.asarray(lowArray, dtype='double')
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 倒数第二天是下降，倒数第一天是上升
            if (doubleCloseArray[n-3] > doubleCloseArray[n-2]  and doubleCloseArray[n-1] >= doubleCloseArray[n-2]):
                if (doubleHighArray[n-2] > doubleHighArray[n-1] and doubleLowArray[n-2] < doubleLowArray[n-1]):
                    if(doubleOpenArray[n-2] > doubleCloseArray[n-1] and doubleCloseArray[n-2] < doubleOpenArray[n-1]):

                        data = common_mysqlUtil.select_all_code_one(codeItem)
                        huanshoulv = ""
                        mingcheng = ""
                        print(data)
                        if len(data) > 0:
                            huanshoulv = "@换手：" + data[0][4] + "%"
                            mingcheng = data[0][1]
                        zhangdiefu = common.zhangdiefu(codeItem) + huanshoulv
                        common_mysqlUtil.insert_ZhiShuLog_record(codeItem, mingcheng, "ACD", "", "", "", zhangdiefu,
                                                "触发孕线策略")
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return strResult

common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "ACD", "====", "========", "============", "======", "")
strMailResult_D = strategy('D', 0)
print(strMailResult_D)
