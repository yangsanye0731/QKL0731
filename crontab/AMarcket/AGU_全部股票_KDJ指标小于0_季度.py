import os
#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import time
import pandas as pd
import talib as ta
import numpy as num
import tushare as ts

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_zhibiao
import common_image


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
    fo = open("C:\\Users\\yangj\\Desktop\\" + "KDJ_" + 'Q' + "_" + endstr + ".txt", "w")
    # 遍历
    for codeItem in all_code_index_x:
        codeItem = codeItem[0:6]
        time.sleep(0.1)
        count = count + 1
        print(count)

        try:
            stock_data = ts.get_hist_data(codeItem, ktype=zhouqi, end=endstr)
            stock_day = stock_data.iloc[::-1]

            period_type = 'Q'
            # 1、必须将时间索引类型编程Pandas默认的类型
            stock_day.index = pd.to_datetime(stock_day.index)

            # 2、进行频率转换日K---周K,首先让所有指标都为最后一天的价格
            period_quarter_data = stock_day.resample(period_type).last()

            # 分别对于开盘、收盘、最高价、最低价进行处理
            period_quarter_data['open'] = stock_day['open'].resample(period_type).first()
            # 处理最高价和最低价
            period_quarter_data['high'] = stock_day['high'].resample(period_type).max()
            # 最低价
            period_quarter_data['low'] = stock_day['low'].resample(period_type).min()
            # 收盘价
            period_quarter_data['close'] = stock_day['close'].resample(period_type).last()

            closeArray = num.array(period_quarter_data['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(period_quarter_data['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(period_quarter_data['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # print(data_history)
            KDJ_K, KDJ_D, KDJ_J, KDJ_J_title = common_zhibiao.KDJ_zhibiao(period_quarter_data, doubleCloseArray)

            if float(KDJ_J) < 0:
                print(codeItem + "========================================")
                print(KDJ_K)
                print(KDJ_D)
                print(KDJ_J)
                fo.write(codeItem + "\n")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b


#######################################################################################################################
##############################################################################################################主执行程序
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
count_result_b = strategy('D', time_str1)

# bp = ByPy()
# timeStr1 = time.strftime("%Y%m%d", time.localtime())
# bp.mkdir(remotepath=timeStr1)
# bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【03全部代码】SKDJ金叉', '触发【03全部代码】SKDJ金叉')
