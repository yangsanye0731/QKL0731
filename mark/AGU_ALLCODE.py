import time
import numpy as num
import tushare as ts
import common_mysqlUtil
from bypy import ByPy

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os
project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_image

#######################################################################################################################
###########################################################################################################跨域5周线策略
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
            if doubleCloseArray[n-3] > doubleCloseArray[n-2]  and doubleCloseArray[n-1] >= doubleCloseArray[n-2]:
                if doubleHighArray[n-2] > doubleHighArray[n-1] and doubleLowArray[n-2] < doubleLowArray[n-1]:
                    if doubleOpenArray[n-2] > doubleCloseArray[n-1] and doubleCloseArray[n-2] < doubleOpenArray[n-1]:
                        data = common_mysqlUtil.select_all_code_one(codeItem)
                        if len(data) > 0:
                            mingcheng = data[0][1]
                        global dict
                        if codeItem not in dict:
                            dict[codeItem] = 1
                        else:
                            dict[codeItem] = dict[codeItem] + 1
                            zhangdiefu = common.zhangdiefu(codeItem)
                            common_mysqlUtil.insert_ZhiShuLog_record(codeItem, mingcheng, "ACD", "", "", "", zhangdiefu,
                                                                     "触发孕线日线周线双策略")
                            common.dingding_markdown_msg_2("触发【03全部代码】日周双孕线(" + mingcheng + codeItem + ")",
                                                           "触发【03全部代码】日周双孕线(" + mingcheng + codeItem + ")")
                            common_image.plt_image_tongyichutu(codeItem, "W", "【03全部代码】日周双孕线", "【03全部代码】日周双孕线")
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return str(str_result)

#######################################################################################################################
##############################################################################################################主程序执行
common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "ACD", "====", "========", "============", "======", "")
m = 0
strategy('D', m)
strategy('D', m-1)
strategy('D', m-2)
strategy('D', m-3)
strategy('D', m-4)

strategy('W', 0)
strategy('W', -1)

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1 + os.sep
                    + '【03全部代码】日周双孕线', remotepath=timeStr1)
