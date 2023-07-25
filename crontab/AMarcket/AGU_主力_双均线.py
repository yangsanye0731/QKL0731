# encoding=utf-8
import numpy as num
import talib as ta
import tushare as ts
import time
import requests
import common_mysqlUtil

#######################################################################################################################
# ############################################################################################### 配置程序应用所需要环境PATH
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
import common


#######################################################################################################################
# ########################################################################################################## 跨域5周线策略
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

    time_str = endstr
    fo_10 = open("主力_双均线10_" + zhouqi + "_" + time_str + ".txt", "w")
    fo_60 = open("主力_双均线60_" + zhouqi + "_" + time_str + ".txt", "w")
    fo_144 = open("主力_双均线144_" + zhouqi + "_" + time_str + ".txt", "w")

    url = 'https://hook.us1.make.com/r7gj5cb1go2l7x23i44tnyivdj7sy7ei'

    # 遍历
    for codeItem in open('zhuli.txt'):
        try:
            codeItem = codeItem.strip('\n')
            # time.sleep(0.5)
            count = count + 1
            print(count)
            codeName = ''
            data = common_mysqlUtil.select_all_code_one(codeItem)
            if len(data) > 0:
                codeName = data[0][1]

            data_history = ts.get_hist_data(codeItem, ktype=zhouqi, end=endstr)
            data_history = data_history.iloc[::-1]

            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            # 均线
            ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
            sma10 = ta.EMA(ma10, timeperiod=10)

            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
            sma60 = ta.EMA(ma60, timeperiod=60)

            ma144 = ta.SMA(doubleCloseArray, timeperiod=144)
            sma144 = ta.EMA(ma144, timeperiod=144)

            if ma10[-1] > sma10[-1] and ma10[-2] < sma10[-2]:
                print("双均线10：" + codeItem)
                fo_10.write(codeItem + "\n")
                common_image.plt_image_tongyichutu_2(codeItem,
                                                     "D",
                                                     "【全部代码】双均线10",
                                                     "【全部代码】双均线10", time_str)

                data = {
                    's_code': codeItem,
                    's_name': codeName,
                    's_type': '10Day'
                }
                requests.post(url, data=data)

            if ma60[-1] > sma60[-1] and ma60[-2] < sma60[-2]:
                print("双均线60：" + codeItem)
                fo_60.write(codeItem + "\n")
                common_image.plt_image_tongyichutu_2(codeItem,
                                                     "D",
                                                     "【全部代码】双均线60",
                                                     "【全部代码】双均线60", time_str)

                data = {
                    's_code': codeItem,
                    's_name': codeName,
                    's_type': '60Day'
                }
                requests.post(url, data=data)

            if ma144[-1] > sma144[-1] and ma144[-2] < sma144[-2]:
                print("双均线144：" + codeItem)
                fo_144.write(codeItem + "\n")
                common_image.plt_image_tongyichutu_2(codeItem,
                                                     "D",
                                                     "【全部代码】双均线144",
                                                     "【全部代码】双均线144", time_str)

                data = {
                    's_code': codeItem,
                    's_name': codeName,
                    's_type': '144Day'
                }
                requests.post(url, data=data)

                count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
            common.dingding_markdown_msg_03("AGU_主力_双均线执行异常", "AGU_主力_双均线执行异常")
    return count_b, count_e


#######################################################################################################################
# ############################################################################################################# 主执行程序
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
count_result_b, count_result_e = strategy('D', time_str1)
common.dingding_markdown_msg_03("AGU_主力_双均线执行完成", "AGU_主力_双均线执行完成")
