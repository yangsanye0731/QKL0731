#encoding=utf-8

import tushare as ts
import numpy as num
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import matplotlib
import matplotlib.pyplot as plt
import os
import talib as ta
import pandas as pd


'''
公共功能：ENE指标
'''
def ENE_zhibiao(doubleCloseArray):
     param_m1 = 11
     param_m2 = 9
     param_n = 10
     sma_n = ta.SMA(doubleCloseArray, param_n)
     upper = (1 + param_m1 / 100) * sma_n
     lower = (1 - param_m2 / 100) * sma_n
     ene = (upper + lower) / 2
     upper = upper.round(2)
     ene = ene.round(2)
     lower = lower.round(2)
     ene_qushi = ""
     if (ene[-1] > ene[-2] and ene[-3] > ene[-2]):
          ene_qushi = "ENE中线趋势上升"
     else:
         ene_qushi = "%.2f" % ene[-3] +  "_"  + "%.2f" % ene[-2] + "_" + "%.2f" % ene[-1]
     return ene_qushi

'''
公共功能：ENE指标
'''
def ENE_zhibiao_line(doubleCloseArray, lowArray):
     param_m1 = 11
     param_m2 = 9
     param_n = 10
     sma_n = ta.SMA(doubleCloseArray, param_n)
     upper = (1 + param_m1 / 100) * sma_n
     lower = (1 - param_m2 / 100) * sma_n
     ene = (upper + lower) / 2
     upper = upper.round(2)
     ene = ene.round(2)
     print(ene)
     lower = lower.round(2)
     ene_qushi = ""

     percent = (doubleCloseArray[-1] - ene[-1])/ene[-1] * 100
     return percent, "%.2f" % ene[-1]

'''
公共功能：KDJ指标
'''
def KDJ_zhibiao(data_history, doubleCloseArray):
     stock_data = {}
     low_list = data_history.low.rolling(9).min()
     low_list.fillna(value=data_history.low.expanding().min(), inplace=True)
     high_list = data_history.high.rolling(9).max()
     high_list.fillna(value=data_history.high.expanding().max(), inplace=True)
     rsv = (doubleCloseArray - low_list) / (high_list - low_list) * 100
     print(rsv)
     stock_data['KDJ_K'] = pd.DataFrame.ewm(rsv, com=2).mean()
     stock_data['KDJ_D'] = pd.DataFrame.ewm(stock_data['KDJ_K'], com=2).mean()
     stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
     dddd = pd.DataFrame(stock_data)
     KDJ_J_title = "KDJ_" + "%.2f" % dddd.KDJ_J[len(dddd) - 1] + " "
     KDJ_K = "%.2f" % dddd.KDJ_K[len(dddd) - 1]
     KDJ_D = "%.2f" % dddd.KDJ_D[len(dddd) - 1]
     KDJ_J = "%.2f" % dddd.KDJ_J[len(dddd) - 1]
     return KDJ_K, KDJ_D, KDJ_J, KDJ_J_title


def SKDJ_zhibiao(data_history, doubleCloseArray):
     # RSV := (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100;
     # K: SMA(RSV, M1, 1);
     # D: SMA(K, M2, 1);
     # J: 3 * K - 2 * D;

     stock_data = {}
     # SKDJ_LOWV := LLV(LOW, SKDJN);
     low_list = data_history.low.rolling(9).min()
     low_list.fillna(value=data_history.low.expanding().min(), inplace=True)

     # SKDJ_HIGHV := HHV(HIGH, SKDJN);
     high_list = data_history.high.rolling(9).max()
     high_list.fillna(value=data_history.high.expanding().max(), inplace=True)

     # SKDJN := 9;
     # SKDJM := 3;
     # SKDJ_LOWV := LLV(LOW, SKDJN);
     # SKDJ_HIGHV := HHV(HIGH, SKDJN);
     # SKDJ_RSV := EMA((CLOSE - SKDJ_LOWV) / (SKDJ_HIGHV - SKDJ_LOWV) * 100, SKDJM);
     rsv = (doubleCloseArray - low_list) / (high_list - low_list) * 100
     skdj_rsv = ta.EMA(rsv, timeperiod=3)
     # #K0: EMA(SKDJ_RSV, SKDJM), COLORWHITE;
     # #D0: MA(K0, SKDJM), COLORYELLOW;
     k0 = ta.EMA(skdj_rsv, timeperiod=3)
     d0 = ta.EMA(k0, timeperiod=3)

     # print("========================================================K")
     # print(k0)
     # print("========================================================D")
     # print(d0)

     return k0,d0



'''
公共功能：BULL指标
'''
def BULL_zhibiao(doubleCloseArray, closeArray, lowArray):
     upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
     BULL_middleband = ""
     if (middleband[-1] >= middleband[-2]):
          BULL_middleband = "布林中线趋势上升"
     else:
          BULL_middleband = "布林中线趋势下降"

     BULL_title = ""
     if (closeArray[-1] > upperband[-1]):
          BULL_title = "上穿布林线上沿"

     if (lowArray[-1] < lowerband[-1] * 1.008):
          BULL_title = "下穿布林线下沿"

     upperband = "%.2f" % upperband[-1]
     middleband = "%.2f" % middleband[-1]
     lowerband = "%.2f" % lowerband[-1]
     return upperband, middleband, lowerband, BULL_title, BULL_middleband

'''
公共功能：MACD指标
'''
def MACD_zhibiao(doubleCloseArray):
     # macd 为快线 macdsignal为慢线，macdhist为柱体
     macd, macdsignal, macdhist = ta.MACD(doubleCloseArray, fastperiod=12, slowperiod=26, signalperiod=9)
     MACD_title = ""
     if (macdsignal[-1] > macdsignal[-2]):
          MACD_title = "MACD慢线上行1"
          if (macdsignal[-2] > macdsignal[-3]):
               MACD_title = "MACD慢线上行2"
               if (macdsignal[-3] > macdsignal[-4]):
                    MACD_title = "MACD慢线上行3"
                    if (macdsignal[-4] > macdsignal[-5]):
                         MACD_title = "MACD慢线上行4"
                         if (macdsignal[-5] > macdsignal[-6]):
                              MACD_title = "MACD慢线上行5"
                              if (macdsignal[-6] > macdsignal[-7]):
                                   MACD_title = "MACD慢线上行6"
                                   if (macdsignal[-7] > macdsignal[-8]):
                                        MACD_title = "MACD慢线上行7"
                                        if (macdsignal[-8] > macdsignal[-9]):
                                             MACD_title = "MACD慢线上行8"
                                             if (macdsignal[-9] > macdsignal[-10]):
                                                  MACD_title = "MACD慢线上行9"
                                                  if (macdsignal[-11] > macdsignal[-12]):
                                                       MACD_title = "MACD慢线上行10"

     return MACD_title

'''
公共功能：均线指标
'''
def junxian_zhibiao(doubleCloseArray, doubleOpenArray, doubleHighArray):
     MA_5 = ta.SMA(doubleCloseArray, timeperiod=5)
     MA_10 = ta.SMA(doubleCloseArray, timeperiod=10)
     MA_20 = ta.SMA(doubleCloseArray, timeperiod=20)

     MA5_titile = ""
     # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
     if (doubleHighArray[-1] > MA_5[-1] and doubleOpenArray[-1] < MA_5[-1] and MA_5[-2] < MA_5[-3] and MA_5[-3] < MA_5[-4]):
          MA5_titile = "5均线上穿"

     MA20_titile = ""
     if (doubleCloseArray[-1] > MA_20[-1] and doubleOpenArray[-1] < MA_20[-1]):
          MA20_titile = "20均线上穿"

     MA30_titile = ""
     MA_30 = ta.SMA(doubleCloseArray, timeperiod=30)
     if (MA_30[-1] > MA_30[-2]):
          MA30_titile = "30均线上行1"
          if (MA_30[-2] > MA_30[-3]):
               MA30_titile = "30均线上行2"
               if (MA_30[-3] > MA_30[-4]):
                    MA30_titile = "30均线上行3"
                    if (MA_30[-4] > MA_30[-5]):
                         MA30_titile = "30均线上行4"
                         if (MA_30[-5] > MA_30[-6]):
                              MA30_titile = "30均线上行5"
                              if (MA_30[-6] > MA_30[-7]):
                                   MA30_titile = "30均线上行6"
                                   if (MA_30[-7] > MA_30[-8]):
                                        MA30_titile = "30均线上行7"
                                        if (MA_30[-8] > MA_30[-9]):
                                             MA30_titile = "30均线上行8"
                                             if (MA_30[-9] > MA_30[-10]):
                                                  MA30_titile = "30均线上行9"
                                                  if (MA_30[-10] > MA_30[-11]):
                                                       MA30_titile = "30均线上行10"

     MA60_titile = ""
     MA_60 = ta.SMA(doubleCloseArray, timeperiod=60)
     if (MA_60[-1] > MA_60[-2]):
          MA60_titile = "60均线上行1"
          if (MA_60[-2] > MA_60[-3]):
               MA60_titile = "60均线上行2"
               if (MA_60[-3] > MA_60[-4]):
                    MA60_titile = "60均线上行3"
                    if (MA_60[-4] > MA_60[-5]):
                         MA60_titile = "60均线上行4"
                         if (MA_60[-5] > MA_60[-6]):
                              MA60_titile = "60均线上行5"
                              if (MA_60[-6] > MA_60[-7]):
                                   MA60_titile = "60均线上行6"
                                   if (MA_60[-7] > MA_60[-8]):
                                        MA60_titile = "60均线上行7"
                                        if (MA_60[-8] > MA_60[-9]):
                                             MA60_titile = "60均线上行8"
                                             if (MA_60[-9] > MA_60[-10]):
                                                  MA60_titile = "60均线上行9"
                                                  if (MA_60[-10] > MA_60[-11]):
                                                       MA60_titile = "60均线上行10"

     qushi_5_10_20_30 = ""
     if (MA_5[-1] > MA_5[-2] and MA_10[-1] > MA_10[-2] and MA_20[-1] > MA_20[-2] and MA_30[-1] > MA_30[-2]):
          qushi_5_10_20_30 = "均线5、10、20、30齐升1"
          if (MA_5[-2] > MA_5[-3] and MA_10[-2] > MA_10[-3] and MA_20[-2] > MA_20[-3] and MA_30[-2] > MA_30[-3]):
               qushi_5_10_20_30 = "均线5、10、20、30齐升2"
               if (MA_5[-3] > MA_5[-4] and MA_10[-3] > MA_10[-4] and MA_20[-3] > MA_20[-4] and MA_30[-3] > MA_30[-4]):
                    qushi_5_10_20_30 = "均线5、10、20、30齐升3"
                    if (MA_5[-4] > MA_5[-5] and MA_10[-4] > MA_10[-5] and MA_20[-4] > MA_20[-5] and MA_30[-4] > MA_30[
                         -5]):
                         qushi_5_10_20_30 = "均线5、10、20、30齐升4"
                         if (MA_5[-5] > MA_5[-6] and MA_10[-5] > MA_10[-6] and MA_20[-5] > MA_20[-6] and MA_30[-5] >
                                 MA_30[-6]):
                              qushi_5_10_20_30 = "均线5、10、20、30齐升5"
                              if (MA_5[-6] > MA_5[-7] and MA_10[-6] > MA_10[-7] and MA_20[-6] > MA_20[-7] and MA_30[
                                   -6] > MA_30[-7]):
                                   qushi_5_10_20_30 = "均线5、10、20、30齐升6"
                                   if (MA_5[-7] > MA_5[-8] and MA_10[-7] > MA_10[-8] and MA_20[-7] > MA_20[-8] and
                                           MA_30[-7] > MA_30[-8]):
                                        qushi_5_10_20_30 = "均线5、10、20、30齐升7"
                                        if (MA_5[-8] > MA_5[-9] and MA_10[-8] > MA_10[-9] and MA_20[-8] > MA_20[-9] and
                                                MA_30[-8] > MA_30[-9]):
                                             qushi_5_10_20_30 = "均线5、10、20、30齐升8"
                                             if (MA_5[-9] > MA_5[-10] and MA_10[-9] > MA_10[-10] and MA_20[-9] > MA_20[
                                                  -10] and MA_30[-9] > MA_30[-10]):
                                                  qushi_5_10_20_30 = "均线5、10、20、30齐升9"

     if (MA_5[-1] < MA_5[-2] and MA_10[-1] < MA_10[-2] and MA_20[-1] < MA_20[-2] and MA_30[-1] < MA_30[-2]):
          qushi_5_10_20_30 = "均线5、10、20、30齐降1"
          if (MA_5[-2] < MA_5[-3] and MA_10[-2] < MA_10[-3] and MA_20[-2] < MA_20[-3] and MA_30[-2] < MA_30[-3]):
               qushi_5_10_20_30 = "均线5、10、20、30齐降2"
               if (MA_5[-3] < MA_5[-4] and MA_10[-3] < MA_10[-4] and MA_20[-3] < MA_20[-4] and MA_30[-3] < MA_30[-4]):
                    qushi_5_10_20_30 = "均线5、10、20、30齐降3"
                    if (MA_5[-4] < MA_5[-5] and MA_10[-4] < MA_10[-5] and MA_20[-4] < MA_20[-5] and MA_30[-4] < MA_30[
                         -5]):
                         qushi_5_10_20_30 = "均线5、10、20、30齐降4"
                         if (MA_5[-5] < MA_5[-6] and MA_10[-5] < MA_10[-6] and MA_20[-5] < MA_20[-6] and MA_30[-5] <
                                 MA_30[-6]):
                              qushi_5_10_20_30 = "均线5、10、20、30齐降5"
                              if (MA_5[-6] < MA_5[-7] and MA_10[-6] < MA_10[-7] and MA_20[-6] < MA_20[-7] and MA_30[
                                   -6] < MA_30[-7]):
                                   qushi_5_10_20_30 = "均线5、10、20、30齐降6"
                                   if (MA_5[-7] < MA_5[-8] and MA_10[-7] < MA_10[-8] and MA_20[-7] < MA_20[-8] and
                                           MA_30[-7] < MA_30[-8]):
                                        qushi_5_10_20_30 = "均线5、10、20、30齐降7"
                                        if (MA_5[-8] < MA_5[-9] and MA_10[-8] < MA_10[-9] and MA_20[-8] < MA_20[-9] and
                                                MA_30[-8] < MA_30[-9]):
                                             qushi_5_10_20_30 = "均线5、10、20、30齐降8"
                                             if (MA_5[-9] < MA_5[-10] and MA_10[-9] < MA_10[-10] and MA_20[-9] < MA_20[
                                                  -10] and MA_30[-9] < MA_30[-10]):
                                                  qushi_5_10_20_30 = "均线5、10、20、30齐降9"

     return MA5_titile, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30

'''
公共功能：指标
'''
def zhibiao(code, type):
     data_history = ts.get_k_data(code, ktype=type)

     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])
     openArray = num.array(data_history['open'])

     doubleCloseArray = num.asarray(closeArray, dtype='double')
     doubleHighArray = num.asarray(highArray, dtype='double')
     doubleLowArray = num.asarray(lowArray, dtype='double')
     doubleOpenArray = num.asarray(openArray, dtype='double')

     ########################################################################################################## 股票价格
     price =  "%.2f" % doubleCloseArray[-1] + "_" + "%.2f" % doubleCloseArray[-2] + "_" + "%.2f" % doubleCloseArray[-3]
     # print("Price:" + price)
     ########################################################################################################## KDJ 指标
     KDJ_K, KDJ_D, KDJ_J, KDJ_J_title = KDJ_zhibiao(data_history, doubleCloseArray)
     # print("KDJ_K:" + KDJ_K)
     # print("KDJ_D:" + KDJ_D)
     # print("KDJ_J:" + KDJ_J)
     ########################################################################################################## MACD 指标
     MACD_title = MACD_zhibiao(doubleCloseArray)
     ########################################################################################################## BULL 指标
     upperband, middleband, lowerband, BULL_title, BULL_middleband = BULL_zhibiao(doubleCloseArray, closeArray, lowArray)
     # print("上沿：" + upperband)
     # print("中线：" + middleband)
     # print("下沿：" + lowerband)
     ########################################################################################################## 均线指标
     MA5_titile, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30 = junxian_zhibiao(doubleCloseArray, doubleOpenArray, doubleHighArray)

     ########################################################################################################## ENS指标
     ene_qushi = ENE_zhibiao(doubleCloseArray)
     # 指标返回
     return price, MA5_titile, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, KDJ_J, MACD_title, BULL_title, BULL_middleband, ene_qushi

# 返回20均线是否上传，30均线趋势
# price, MA5_titile, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, KDJ_J, MACD_title, BULL_title, BULL_middleband, ene_qushi = zhibiao('002010','W')
# print(price)
# print(MA5_titile)
# print(MACD_title)
# print(BULL_title)
# print(BULL_middleband)
# print(MA20_titile)


# data_history = ts.get_hist_data('300322', ktype='W')
# data_history = data_history.iloc[::-1]
#
# try:
#      closeArray = num.array(data_history['close'])
#      doubleCloseArray = num.asarray(closeArray, dtype='double')
#
#      highArray = num.array(data_history['high'])
#      doubleHighArray = num.asarray(highArray, dtype='double')
#
#      openArray = num.array(data_history['open'])
#      doubleOpenArray = num.asarray(openArray, dtype='double')
#
#      turnoverArray = num.array(data_history['turnover'])
#      doubleTurnoverArray = num.asarray(turnoverArray, dtype='double')
#
#
#
#      k0,d0 = SKDJ_zhibiao(data_history, doubleCloseArray)
#      print('300322' + "======================================================================")
#      print('300322' + "======================================================================")
#      print('300322' + "======================================================================")
#      print(k0[-1])
#      print(k0[-2])
#      print(d0[-1])
#      print(d0[-2])
#
#      # print('300322' + "======================================================================")
#      # KDJ_zhibiao(data_history, doubleCloseArray)
#
# except (IOError, TypeError, NameError, IndexError, Exception) as e:
#   print(e)
