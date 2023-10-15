import numpy as num
import tushare as ts
import talib as ta

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

import logging

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


#######################################################################################################################
############################################################################################################读取配置文件
def code_matrix_table(codeItem, zhangdiefu, price, codeName):
    # ======================================================60分钟数据
    data_history_60 = ts.get_k_data(codeItem, ktype='60')

    closeArray_60 = num.array(data_history_60['close'])
    doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')

    highArray_60 = num.array(data_history_60['high'])
    doubleHighArray_60 = num.asarray(highArray_60, dtype='double')

    lowArray_60 = num.array(data_history_60['low'])
    doubleLowArray_60 = num.asarray(lowArray_60, dtype='double')

    # 均线
    ma10_60 = ta.SMA(doubleCloseArray_60, timeperiod=10)
    sma10_60 = ta.EMA(ma10_60, timeperiod=10)

    # ma60_60 = ta.SMA(doubleCloseArray_60, timeperiod=60)
    # sma60_60 = ta.EMA(ma60_60, timeperiod=60)
    # ma144_60 = ta.SMA(doubleCloseArray_60, timeperiod=144)
    # sma144_60 = ta.EMA(ma144_60, timeperiod=144)
    state_60 = state(ma10_60, sma10_60)

    # 60分钟操作机会1：触碰到唐奇安底线
    state_dc_h = ""
    dc_high_60 = ta.MAX(doubleHighArray_60, timeperiod=20)
    dc_low_60 = ta.MIN(doubleLowArray_60, timeperiod=20)
    if doubleLowArray_60[-1] == dc_low_60[-1]:
        logging.info("【交易机会】" + codeItem + codeName + "将触碰到唐奇安小时线底线")
        state_dc_h = "小时底线"
    if doubleHighArray_60[-1] == dc_high_60[-1]:
        logging.info("【交易机会】" + codeItem + codeName + "将触碰到唐奇安小时线高线")
        state_dc_h = "小时高线"

    # ======================================================日线数据
    data_history = ts.get_k_data(codeItem, ktype='D')

    closeArray = num.array(data_history['close'])
    doubleCloseArray = num.asarray(closeArray, dtype='double')

    highArray = num.array(data_history['high'])
    doubleHighArray = num.asarray(highArray, dtype='double')

    lowArray = num.array(data_history['low'])
    doubleLowArray = num.asarray(lowArray, dtype='double')

    # 均线
    ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
    sma10 = ta.EMA(ma10, timeperiod=10)

    # ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
    # sma60 = ta.EMA(ma60, timeperiod=60)
    # ma144 = ta.SMA(doubleCloseArray, timeperiod=144)
    # sma144 = ta.EMA(ma144, timeperiod=144)
    state_D = state(ma10, sma10)

    # 日线操作机会1：触碰到唐奇安底线
    dc_high = ta.MAX(doubleHighArray, timeperiod=20)
    dc_low = ta.MIN(doubleLowArray, timeperiod=20)
    state_dc_d = ""
    if doubleLowArray[-1] == dc_low[-1] or (doubleLowArray[-1] - dc_low[-1]) / dc_low[-1] < 0.01:
        logging.info("【交易机会】" + codeItem + codeName + "将触碰到唐奇安日线底线")
        state_dc_d = "日线底线"
    if doubleHighArray[-1] == dc_high[-1] or (dc_high[-1] - doubleHighArray[-1]) / dc_high[-1] < 0.01:
        logging.info("【交易机会】" + codeItem + codeName + "将触碰到唐奇安日线高线")
        state_dc_d = "日线高线"

    table_item_data = [codeName, zhangdiefu, price, ma10_60[-3], ma10_60[-2], ma10_60[-1], state_60, ma10[-3], ma10[-2],
                       ma10[-1],
                       state_D, state_dc_h, state_dc_d]

    return table_item_data


def state(ma10, sma10):
    item_state = ""
    if ma10[-3] < ma10[-2] < ma10[-1]:
        item_state = "上升"
    if ma10[-3] < ma10[-2] > ma10[-1]:
        item_state = "顶部"
    if ma10[-3] > ma10[-2] > ma10[-1]:
        item_state = "下降"
    if ma10[-3] > ma10[-2] < ma10[-1]:
        item_state = "底部"
    if ma10[-1] > sma10[-1] and ma10[-2] < sma10[-2]:
        item_state = "上穿"
    if ma10[-1] < sma10[-1] and ma10[-2] > sma10[-2]:
        item_state = "下穿"
    return item_state

# print(zhangdiefu('399006'))
# dingding_markdown_msg_final("dingding01", "触发test", "触发test")
