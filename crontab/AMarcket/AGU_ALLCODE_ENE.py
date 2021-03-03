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


#######################################################################################################################
###########################################################################################################跨域5月线策略
def strategy(zhouqi, beishu):
    # 局部变量初始化
    count = 0
    count_b = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)

    time_str = time.strftime("%Y%m%d", time.localtime())
    fo = open("换手率_" + zhouqi + "_大于" + str(beishu) + "_" + time_str + ".txt", "w")
    fo2 = open("换手率_" + zhouqi + "_大于" + str(beishu) + "_" + "ENE趋势_" + time_str + ".txt", "w")

    # 遍历
    for codeItem in all_code_index_x:
        codeItem = codeItem[0:6]
        time.sleep(0.01)
        count = count + 1
        print(count)
        data_history = ts.get_hist_data(codeItem, ktype=zhouqi)

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            turnoverArray = num.array(data_history['turnover'])
            doubleTurnoverArray = num.asarray(turnoverArray, dtype='double')

            print(codeItem + "======================================================================")
            # print(doubleTurnoverArray[0])
            # print(doubleTurnoverArray[1])
            # print(doubleTurnoverArray[2])
            # print(doubleTurnoverArray[0] / doubleTurnoverArray[1])
            if doubleTurnoverArray[0] / doubleTurnoverArray[1] > beishu:
                print(doubleTurnoverArray[0] / doubleTurnoverArray[1])
                fo.write(codeItem + "\n")

                param_m1 = 11
                param_m2 = 9
                param_n = 10
                sma_n = ta.SMA(doubleCloseArray, param_n)
                upper = (1 + param_m1 / 100) * sma_n
                lower = (1 - param_m2 / 100) * sma_n
                ene = (upper + lower) / 2
                # upper = upper.round(2)
                ene = ene.round(2)
                # lower = lower.round(2)

                if ene[-1] > ene[-2]:
                    fo2.write(codeItem + "\n")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

    # 关闭打开的文件
    fo.close()
    fo2.close()


#######################################################################################################################
##############################################################################################################主执行程序
# count_result_b = strategy('W', 1.5)
# strategy('D', 3)
# strategy('W', 3.75)
strategy('M', 2)
# strategy('D', 5)

# bp = ByPy()
# timeStr1 = time.strftime("%Y%m%d", time.localtime())
# bp.mkdir(remotepath=timeStr1)
# bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
# common.dingding_markdown_msg_2('触发【03全部代码】跨越5月线,主力持仓、换手率突增执行完成',
#                                '触发【03全部代码】跨越5月线,主力持仓、换手率突增执行完成')
