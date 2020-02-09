#encoding=utf-8

import time
import numpy as num
import tushare as ts
import common
import common_mysqlUtil

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
                        huanshoulv = ""
                        mingcheng = ""
                        epsup = ""
                        print(data)
                        if len(data) > 0:
                            # huanshoulv = "@换手：" + data[0][4] + "%"
                            # epsup = "@EPS：" + data[0][5] + "%"
                            mingcheng = data[0][1]
                        zhangdiefu = common.zhangdiefu(codeItem) + huanshoulv + epsup
                        common_mysqlUtil.insert_ZhiShuLog_record(codeItem, mingcheng, "ACD", "", "", "", zhangdiefu,
                                                "触发孕线" + zhouqi + "策略")
                        str_result = str_result + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return str(str_result)

common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "ACD", "====", "========", "============", "======", "")
# str_result = strategy('D', 0)
# common.dingding_markdown_msg_2("触发孕线D策略完成(" + str_result + ")", "触发孕线D策略完成(" + str_result + ")")
# time.sleep(0.5)
# common.dingding_markdown_msg_2("触发孕线D策略完成(" + str_result + ")", "触发孕线D策略完成(" + str_result + ")")

str_result = strategy('W', -1)
common.dingding_markdown_msg_2("触发孕线W策略完成(" + str_result + ")", "触发孕线W策略完成(" + str_result + ")")
time.sleep(0.5)
common.dingding_markdown_msg_2("触发孕线W策略完成(" + str_result + ")", "触发孕线W策略完成(" + str_result + ")")
