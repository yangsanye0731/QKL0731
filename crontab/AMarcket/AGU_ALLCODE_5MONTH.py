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
def strategy(zhouqi):
    # 局部变量初始化
    count = 0
    count_b = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)

    # 遍历
    for codeItem in all_code_index_x:
        codeItem = codeItem[0:6]
        time.sleep(0.1)
        count = count + 1
        print(count)
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)

        try:
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
                common_image.plt_image_tongyichutu_2(codeItem,
                                                     "M",
                                                     "【03全部代码】跨越5月线,主力持仓,换手率突增",
                                                     "【03全部代码】跨越5月线,主力持仓,换手率突增")
                count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b

#######################################################################################################################
##############################################################################################################主执行程序
count_result_b = strategy('M')
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【03全部代码】跨越5月线,主力持仓、换手率突增执行完成',
                               '触发【03全部代码】跨越5月线,主力持仓、换手率突增执行完成')
