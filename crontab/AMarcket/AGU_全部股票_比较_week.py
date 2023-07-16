# encoding=utf-8
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

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
print(rootPath1)
import common_image
import common_mysqlUtil

import pandas as pd


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
                common_mysqlUtil.insert_codeitem(codeItem, zhouqi, "跨越5周线",endstr)
                if zhouqi == 'W':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "W",
                                                         "【全部代码】跨越5周线",
                                                         "【全部代码】跨越5周线")
                if zhouqi == 'M':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "M",
                                                         "【全部代码】跨越5月线",
                                                         "【全部代码】跨越5月线")
                count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return count_b, count_e


#######################################################################################################################
##############################################################################################################主执行程序
df_qianyitian = pd.read_csv('./week_excel/china_2023-05-10_84788.csv')
df_houyitian = pd.read_csv('./week_excel/china_2023-05-11_b41ca.csv')
# print(df1)
# print(df2)
for index in df_qianyitian.index:
    try:
        # print(index)
        # print(df1['商品代码'].get(index))
        data = df_houyitian[(df_houyitian["商品代码"] == df_qianyitian['商品代码'].get(index))]
        # print(df1['描述'].get(index))
        # print(df1['移动平均线评级'].get(index))
        # print(data['移动平均评级'].iloc[0])
        # print(df1['移动平均评级'].get(index))
        # print(data)
        str_houyitian = data['移动平均评级'].iloc[0]
        str_shangpindaima = data['商品代码'].iloc[0]
        # print("后一天移动平均评级：" + str_houyitian)
        # print("后一天商品代码：" + str(str_shangpindaima))
        str_qianyitian = df_qianyitian['移动平均评级'].get(index)
        str_shangpindaima_qian = df_qianyitian['商品代码'].get(index)
        # print("前一天移动平均评级：" + str_qianyitian)
        # print("前一天商品代码：" + str(str_shangpindaima_qian))
        str_qianyitian = str_qianyitian.strip()
        str_houyitian = str_houyitian.strip()
        if str_qianyitian != str_houyitian:
            if (str_qianyitian == '卖出' or str_qianyitian == '强烈卖出') and (str_houyitian == '强烈买入'):
                # print(data)
                # print(df_houyitian['描述'].get(index) + "，原状态：" + str_qianyitian + ",目标状态：" + str_houyitian)
                # str_houyitian = data['移动平均评级'].iloc[0]
                # print(str_houyitian)
                if str(str_shangpindaima).__len__() == 6 :
                    print(str(str_shangpindaima))
                if str(str_shangpindaima).__len__() == 5:
                    print('0' + str(str_shangpindaima))
                if str(str_shangpindaima).__len__() == 4:
                    print('00' + str(str_shangpindaima))
                if str(str_shangpindaima).__len__() == 3:
                    print('000' + str(str_shangpindaima))
                if str(str_shangpindaima).__len__() == 2:
                    print('0000' + str(str_shangpindaima))
                if str(str_shangpindaima).__len__() == 1:
                    print('00000' + str(str_shangpindaima))
    except (IOError, TypeError, NameError, IndexError, Exception) as e:
        print(e)

