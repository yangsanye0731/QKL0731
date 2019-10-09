#encoding=utf-8

import tushare as ts
import numpy as num
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import matplotlib
import matplotlib.pyplot as plt
import os
import tushare as ts
import talib as ta
import pandas as pd

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

     price =  "%.2f" % doubleCloseArray[-1] + "_" + "%.2f" % doubleCloseArray[-2] + "_" + "%.2f" % doubleCloseArray[-3]

     MA_5 = ta.SMA(doubleCloseArray, timeperiod=5)
     MA_10 = ta.SMA(doubleCloseArray, timeperiod=10)
     MA_20 = ta.SMA(doubleCloseArray, timeperiod=20)
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
                   if (MA_5[-4] > MA_5[-5] and MA_10[-4] > MA_10[-5] and MA_20[-4] > MA_20[-5] and MA_30[-4] > MA_30[-5]):
                        qushi_5_10_20_30 = "均线5、10、20、30齐升4"
                        if (MA_5[-5] > MA_5[-6] and MA_10[-5] > MA_10[-6] and MA_20[-5] > MA_20[-6] and MA_30[-5] > MA_30[-6]):
                             qushi_5_10_20_30 = "均线5、10、20、30齐升5"
                             if (MA_5[-6] > MA_5[-7] and MA_10[-6] > MA_10[-7] and MA_20[-6] > MA_20[-7] and MA_30[-6] > MA_30[-7]):
                                  qushi_5_10_20_30 = "均线5、10、20、30齐升6"
                                  if (MA_5[-7] > MA_5[-8] and MA_10[-7] > MA_10[-8] and MA_20[-7] > MA_20[-8] and MA_30[-7] > MA_30[-8]):
                                       qushi_5_10_20_30 = "均线5、10、20、30齐升7"
                                       if (MA_5[-8] > MA_5[-9] and MA_10[-8] > MA_10[-9] and MA_20[-8] > MA_20[-9] and MA_30[-8] > MA_30[-9]):
                                            qushi_5_10_20_30 = "均线5、10、20、30齐升8"
                                            if (MA_5[-9] > MA_5[-10] and MA_10[-9] > MA_10[-10] and MA_20[-9] > MA_20[-10] and MA_30[-9] > MA_30[-10]):
                                                 qushi_5_10_20_30 = "均线5、10、20、30齐升9"

     if (MA_5[-1] < MA_5[-2] and MA_10[-1] < MA_10[-2] and MA_20[-1] < MA_20[-2] and MA_30[-1] < MA_30[-2]):
         qushi_5_10_20_30 = "均线5、10、20、30齐降1"
         if (MA_5[-2] < MA_5[-3] and MA_10[-2] < MA_10[-3] and MA_20[-2] < MA_20[-3] and MA_30[-2] < MA_30[-3]):
              qushi_5_10_20_30 = "均线5、10、20、30齐降2"
              if (MA_5[-3] < MA_5[-4] and MA_10[-3] < MA_10[-4] and MA_20[-3] < MA_20[-4] and MA_30[-3] < MA_30[-4]):
                   qushi_5_10_20_30 = "均线5、10、20、30齐降3"
                   if (MA_5[-4] < MA_5[-5] and MA_10[-4] < MA_10[-5] and MA_20[-4] < MA_20[-5] and MA_30[-4] < MA_30[-5]):
                        qushi_5_10_20_30 = "均线5、10、20、30齐降4"
                        if (MA_5[-5] < MA_5[-6] and MA_10[-5] < MA_10[-6] and MA_20[-5] < MA_20[-6] and MA_30[-5] < MA_30[-6]):
                             qushi_5_10_20_30 = "均线5、10、20、30齐降5"
                             if (MA_5[-6] < MA_5[-7] and MA_10[-6] < MA_10[-7] and MA_20[-6] < MA_20[-7] and MA_30[-6] < MA_30[-7]):
                                  qushi_5_10_20_30 = "均线5、10、20、30齐降6"
                                  if (MA_5[-7] < MA_5[-8] and MA_10[-7] < MA_10[-8] and MA_20[-7] < MA_20[-8] and MA_30[-7] < MA_30[-8]):
                                       qushi_5_10_20_30 = "均线5、10、20、30齐降7"
                                       if (MA_5[-8] < MA_5[-9] and MA_10[-8] < MA_10[-9] and MA_20[-8] < MA_20[-9] and MA_30[-8] < MA_30[-9]):
                                            qushi_5_10_20_30 = "均线5、10、20、30齐降8"
                                            if (MA_5[-9] < MA_5[-10] and MA_10[-9] < MA_10[-10] and MA_20[-9] < MA_20[-10] and MA_30[-9] < MA_30[-10]):
                                                 qushi_5_10_20_30 = "均线5、10、20、30齐降9"

     stock_data = {}
     low_list = data_history.low.rolling(9).min()
     low_list.fillna(value=data_history.low.expanding().min(), inplace=True)
     high_list = data_history.high.rolling(9).max()
     high_list.fillna(value=data_history.high.expanding().max(), inplace=True)
     rsv = (doubleCloseArray - low_list) / (high_list - low_list) * 100
     stock_data['KDJ_K'] = pd.DataFrame.ewm(rsv, com=2).mean()
     stock_data['KDJ_D'] = pd.DataFrame.ewm(stock_data['KDJ_K'], com=2).mean()
     stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
     dddd = pd.DataFrame(stock_data)
     KDJ_J_title = "KDJ_" + "%.2f" % dddd.KDJ_J[len(dddd) - 1] + " "

     # macd 为快线 macdsignal为慢线，macdhist为柱体
     macd, macdsignal, macdhist = ta.MACD(doubleCloseArray, fastperiod=12, slowperiod=26, signalperiod=9)
     if (macdhist[-1] > macdhist[-2] and macdhist[-3] > macdhist[-2]):
          MACD_title = "MA_转 "
     else:
          MACD_title = "MA_平 "

     upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                        matype=0)

     BULL_middleband = ""
     if (middleband[-1] >= middleband[-2]):
          BULL_middleband = "布林中线趋势上升"
     else:
          BULL_middleband = "布林中线趋势下降"

     BULL_title = ""
     if (highArray[-1] > upperband[-1]):
          BULL_title = "上穿布林线上沿"

     if (lowArray[-1] < lowerband[-1]):
          BULL_title = "下穿布林线下沿"

     # 返回20均线是否上传，30均线趋势, KDJ J 是否处于低位， MACD是否转折
     # MA30_titile = MA30_titile + "%.2f" % MA_30[-1] + "_" + "%.2f" % MA_30[-2] + "_" + "%.2f" % MA_30[-3]
     # BULL_title = BULL_title + "%.2f" % lowerband[-1] + "_" + "%.2f" % lowerband[-2] + "_" + "%.2f" % lowerband[-3]
     return price, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, KDJ_J_title, MACD_title, BULL_title, BULL_middleband

# 返回20均线是否上传，30均线趋势
# MA20_titile, MA30_titile, KDJ_J_title, MACD_title, BULL_title = zhibiao('002010','D')
# print(MA20_titile)
# print(MA30_titile)
# print(KDJ_J_title)
# print(MACD_title)
# print(BULL_title)