import numpy as num
import talib as ta
import tushare as ts
import time
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
import common_zhibiao

#######################################################################################################################
###########################################################################################################跨域5月线策略
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
    fo = open("C:\\Users\\yangj\\Desktop\\" +  "SKDJ_小于20_" + zhouqi + "_" + endstr + ".txt", "w")
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
            k0,d0 = common_zhibiao.SKDJ_zhibiao(data_history, doubleCloseArray)

            if k0[-1] < 20 and d0[-1] < 20:
                print(codeItem + "========================================")
                print(k0[-1])
                print(d0[-1])
                fo.write(codeItem + "\n")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b

#######################################################################################################################
##############################################################################################################主执行程序
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
count_result_b = strategy('D', time_str1)
count_result_b = strategy('W', time_str1)
count_result_b = strategy('M', time_str1)
# bp = ByPy()
# timeStr1 = time.strftime("%Y%m%d", time.localtime())
# bp.mkdir(remotepath=timeStr1)
# bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【03全部代码】SKDJ金叉', '触发【03全部代码】SKDJ金叉')
