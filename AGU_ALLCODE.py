#encoding=utf-8

import time
import numpy as num
import tushare as ts
import common
import common_mysqlUtil
import common_image
from bypy import ByPy

dict = {}
def strategy(zhouqi, n):
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    all_code_index_x = num.array(all_code_index)
    str_result = 0
    for codeItem in all_code_index_x:
        count = count + 1
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
                        if len(data) > 0:
                            mingcheng = data[0][1]
                        global dict
                        if codeItem not in dict:
                            dict[codeItem] = 1
                        else:
                            dict[codeItem] = dict[codeItem] + 1
                            # zhangdiefu = common.zhangdiefu(codeItem)
                            common_mysqlUtil.insert_ZhiShuLog_record(codeItem, mingcheng, "ACD", "", "", "", "",
                                                                     "触发孕线日线周线双策略")
                            common.dingding_markdown_msg_2("触发孕线日线周线双策略(" + mingcheng + codeItem + ")",
                                                           "触发孕线日线周线双策略(" + mingcheng + codeItem + ")")
                            common_image.plt_image_tongyichutu(codeItem, "W", "日周双孕线", "双孕线")
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return str(str_result)

common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "ACD", "====", "========", "============", "======", "")
m = 0
str_result = strategy('D', m)
str_result = strategy('D', m-1)
str_result = strategy('D', m-2)
str_result = strategy('D', m-3)
str_result = strategy('D', m-4)

str_result = strategy('W', 0)
str_result = strategy('W', -1)

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
