# encoding=utf-8
import numpy as num
import talib as ta
import tushare as ts
import time

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
print(rootPath1)
import common_image
import common_mysqlUtil
import common


#######################################################################################################################
###########################################################################################################跨域5周线策略
def strategy(zhouqi, endstr):
    # 局部变量初始化
    count = 0
    count_b = 0
    count_e = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # all_code = ts.get_stock_basics()
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)

    time_str = time.strftime("%Y%m%d", time.localtime())
    fo = open("跨越5周_" + zhouqi + "_" + time_str + ".txt", "w")

    # 遍历
    for codeItem in all_code_index_x:
        try:
            codeItem = codeItem[0:6]
            print(codeItem)
            # time.sleep(0.5)
            count = count + 1
            print(count)
            # data_history = ts.get_k_data(codeItem, ktype=zhouqi)
            # data_history_M = ts.get_k_data(codeItem, ktype='M')
            # data_history_D = ts.get_k_data(codeItem, ktype='D')

            data_history = ts.get_hist_data(codeItem, ktype=zhouqi, end=endstr)
            data_history = data_history.iloc[::-1]

            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] < ma5[-4] \
                    and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
                fo.write(codeItem + "\n")
                common_mysqlUtil.insert_codeitem(codeItem, zhouqi, "跨越5周线", endstr)
                if zhouqi == 'W':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "W",
                                                         "【全部代码】跨越5周线",
                                                         "【全部代码】跨越5周线", time_str)
                if zhouqi == 'M':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "M",
                                                         "【全部代码】跨越5月线",
                                                         "【全部代码】跨越5月线", time_str)
                count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b, count_e


#######################################################################################################################
##############################################################################################################主执行程序
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
count_result_b, count_result_e = strategy('W', time_str1)
# count_result_b, count_result_e = strategy('M', time_str1)
# bp = ByPy()
# timeStr1 = time.strftime("%Y%m%d", time.localtime())
# bp.mkdir(remotepath=timeStr1)
# bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_02("AGU_全部股票_跨越5周线执行完成", "AGU_全部股票_跨越5周线执行完成")
