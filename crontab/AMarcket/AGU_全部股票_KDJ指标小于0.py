import os
#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import time

import numpy as num
import tushare as ts

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_zhibiao

def strategy(zhouqi, endstr):
    # 局部变量初始化
    count = 0
    count_b = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)
    time_str = time.strftime("%Y%m%d", time.localtime())
    fo = open("C:\\Users\\yangj\\Desktop\\" +  "KDJ_" + zhouqi + "_" + endstr + ".txt", "w")
    # 遍历
    for codeItem in all_code_index_x:
        codeItem = codeItem[0:6]
        time.sleep(0.1)
        count = count + 1
        print(count)

        try:
            data_history = ts.get_hist_data(codeItem, ktype=zhouqi, end=endstr)
            data_history = data_history.iloc[::-1]
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # print(data_history)
            KDJ_K, KDJ_D, KDJ_J, KDJ_J_title= common_zhibiao.KDJ_zhibiao(data_history, doubleCloseArray)

            print(KDJ_J)
            if float(KDJ_J) < 0 :
                print(codeItem + "========================================")
                print(KDJ_K)
                print(KDJ_D)
                print(KDJ_J)
                fo.write(codeItem + "\n")


            # # 均线
            # ma5 = ta.SMA(doubleCloseArray, timeperiod=5)[图片]
            # ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
            #
            # # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            # if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] < ma5[-4] \
            #         and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
            #     common_image.plt_image_tongyichutu_2(codeItem,
            #                                          "M",
            #                                          "【03全部代码】跨越5月线",
            #                                          "【03全部代码】跨越5月线")
            #     count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b

#######################################################################################################################
##############################################################################################################主执行程序
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
# count_result_b = strategy('D', time_str1)
# count_result_b = strategy('W', time_str1)
count_result_b = strategy('M', "2021-10-29")
# bp = ByPy()
# timeStr1 = time.strftime("%Y%m%d", time.localtime())
# bp.mkdir(remotepath=timeStr1)
# bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【03全部代码】SKDJ金叉', '触发【03全部代码】SKDJ金叉')
