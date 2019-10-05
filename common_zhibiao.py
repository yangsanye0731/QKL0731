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

     BULL_title = ""
     if (highArray[-1] > upperband[-1]):
          BULL_title = "上穿布林线上沿"

     if (lowArray[-1] < lowerband[-1]):
          BULL_title = "下穿布林线下沿"

     # 返回20均线是否上传，30均线趋势, KDJ J 是否处于低位， MACD是否转折
     MA30_titile = MA30_titile + "%.2f" % MA_30[-1] + "_" + "%.2f" % MA_30[-2] + "_" + "%.2f" % MA_30[-3]
     BULL_title = BULL_title + "%.2f" % lowerband[-1] + "_" + "%.2f" % lowerband[-2] + "_" + "%.2f" % lowerband[-3]
     return price, MA20_titile, MA30_titile, KDJ_J_title, MACD_title, BULL_title


def strategy(code, name, fullName, mark):
     ############################################ 15分钟布林线###############################################
     data_history = ts.get_k_data(code, ktype="15")

     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])

     doubleCloseArray = num.asarray(closeArray, dtype='double')
     doubleHighArray = num.asarray(highArray, dtype='double')
     doubleLowArray = num.asarray(lowArray, dtype='double')

     SMA30_15_5 = ta.SMA(doubleCloseArray, timeperiod=5)
     SMA30_15_10 = ta.SMA(doubleCloseArray, timeperiod=10)
     SMA30_15_20 = ta.SMA(doubleCloseArray, timeperiod=20)
     SMA30_15_30 = ta.SMA(doubleCloseArray, timeperiod=30)

     xingtai = ""
     if (SMA30_15_5[-1] > SMA30_15_10[-1] > SMA30_15_20[-1] > SMA30_15_30[-1]):
          xingtai = "上好1"
          if (SMA30_15_5[-2] > SMA30_15_10[-2] > SMA30_15_20[-2] > SMA30_15_30[-2]):
               xingtai = "上好2"
               if (SMA30_15_5[-3] > SMA30_15_10[-3] > SMA30_15_20[-3] > SMA30_15_30[-3]):
                    xingtai = "上好3"

     if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
          xingtai = "下好1"
          if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
               xingtai = "下好2"
               if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
                    xingtai = "下好3"

     if (SMA30_15_5[-1] > SMA30_15_5[-2] and SMA30_15_10[-1] > SMA30_15_10[-2] and SMA30_15_20[-1] > SMA30_15_20[-2] and
             SMA30_15_30[-1] > SMA30_15_30[-2]):

          str15QuShi = "15买1 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>1" + xingtai + "**\n\n"
          if (SMA30_15_5[-2] > SMA30_15_5[-3] and SMA30_15_10[-2] > SMA30_15_10[-3] and SMA30_15_20[-2] > SMA30_15_20[
               -3] and SMA30_15_30[-2] > SMA30_15_30[-3]):
               str15QuShi = "15买2 "
               str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>2" + xingtai + "**\n\n"
               if (SMA30_15_5[-3] > SMA30_15_5[-4] and SMA30_15_10[-3] > SMA30_15_10[-4] and SMA30_15_20[-3] >
                       SMA30_15_20[-4] and SMA30_15_30[-3] > SMA30_15_30[-4]):
                    str15QuShi = "15买3 "
                    str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>3" + xingtai + "**\n\n"

     elif (SMA30_15_5[-1] < SMA30_15_5[-2] and SMA30_15_10[-1] < SMA30_15_10[-2] and SMA30_15_20[-1] < SMA30_15_20[-2]):
          str15QuShi = "15卖 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟卖出</font>" + xingtai + "**\n\n"
     else:
          str15QuShi = "15空 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟空仓</font>" + xingtai + "**\n\n"

     ############################################ 30分钟布林线###############################################
     data_history_30 = ts.get_k_data(code, ktype="30")

     closeArray_30 = num.array(data_history_30['close'])
     highArray_30 = num.array(data_history_30['high'])
     lowArray_30 = num.array(data_history_30['low'])

     doubleCloseArray_30 = num.asarray(closeArray_30, dtype='double')
     doubleHighArray_30 = num.asarray(highArray_30, dtype='double')
     doubleLowArray_30 = num.asarray(lowArray_30, dtype='double')

     SMA30_30_5 = ta.SMA(doubleCloseArray_30, timeperiod=5)
     SMA30_30_10 = ta.SMA(doubleCloseArray_30, timeperiod=10)
     SMA30_30_20 = ta.SMA(doubleCloseArray_30, timeperiod=20)
     SMA30_30_30 = ta.SMA(doubleCloseArray_30, timeperiod=30)
     SMA30_30_60 = ta.SMA(doubleCloseArray_30, timeperiod=60)

     MIN30_60MA = ""
     MIN30_60MA_content = ""
     if (SMA30_30_60[-1] > SMA30_30_60[-2]):
          MIN30_60MA = "趋势1"
          MIN30_60MA_content = "30分钟60均线趋势走多1\n\n"
          if (SMA30_30_60[-2] > SMA30_30_60[-3]):
               MIN30_60MA = "趋势2"
               MIN30_60MA_content = "30分钟60均线趋势走多2\n\n"
               if (SMA30_30_60[-3] > SMA30_30_60[-4]):
                    MIN30_60MA = "趋势3"
                    MIN30_60MA_content = "30分钟60均线趋势走多3\n\n"
                    if (SMA30_30_60[-4] > SMA30_30_60[-5]):
                         MIN30_60MA = "趋势4"
                         MIN30_60MA_content = "30分钟60均线趋势走多4\n\n"
                         if (SMA30_30_60[-5] > SMA30_30_60[-6]):
                              MIN30_60MA = "趋势5"
                              MIN30_60MA_content = "30分钟60均线趋势走多5\n\n"
                              if (SMA30_30_60[-6] > SMA30_30_60[-7]):
                                   MIN30_60MA = "趋势6"
                                   MIN30_60MA_content = "30分钟60均线趋势走多6\n\n"
                                   if (SMA30_30_60[-6] > SMA30_30_60[-7]):
                                        MIN30_60MA = "错过"
                                        MIN30_60MA_content = "30分钟60均线趋势错过\n\n"

     xingtai1 = ""
     if (SMA30_30_5[-1] > SMA30_30_10[-1] > SMA30_30_20[-1] > SMA30_30_30[-1]):
          xingtai1 = "上好1"
          if (SMA30_30_5[-2] > SMA30_30_10[-2] > SMA30_30_20[-2] > SMA30_30_30[-2]):
               xingtai1 = "上好2"
               if (SMA30_30_5[-3] > SMA30_30_10[-3] > SMA30_30_20[-3] > SMA30_30_30[-3]):
                    xingtai1 = "上好3"

     if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
          xingtai1 = "下好1"
          if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
               xingtai1 = "下好2"
               if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
                    xingtai1 = "下好3"

     if (SMA30_30_5[-1] > SMA30_30_5[-2] and SMA30_30_10[-1] > SMA30_30_10[-2] and SMA30_30_20[-1] > SMA30_30_20[-2] and
             SMA30_30_30[-1] > SMA30_30_30[-2]):

          str30QuShi = "30买1 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>1" + xingtai1 + "**\n\n"
          if (SMA30_30_5[-2] > SMA30_30_5[-3] and SMA30_30_10[-2] > SMA30_30_10[-3] and SMA30_30_20[-2] >
                  SMA30_30_20[-3] and SMA30_30_30[-2] > SMA30_30_30[-3]):
               str30QuShi = "30买2 "
               str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>2" + xingtai1 + "**\n\n"
               if (SMA30_30_5[-3] > SMA30_30_5[-4] and SMA30_30_10[-3] > SMA30_30_10[-4] and SMA30_30_20[-3] >
                       SMA30_30_20[-4] and SMA30_30_30[-3] > SMA30_30_30[-4]):
                    str30QuShi = "30买3 "
                    str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>3" + xingtai1 + "**\n\n"

     elif (SMA30_30_5[-1] < SMA30_30_5[-2] and SMA30_30_10[-1] < SMA30_30_10[-2] and SMA30_30_20[-1] < SMA30_30_20[-2]):
          str30QuShi = "30卖 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟卖出</font>" + xingtai1 + "**\n\n"
     else:
          str30QuShi = "30空 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟空仓</font>" + xingtai1 + "**\n\n"

     ############################################ 60分钟布林线###############################################
     data_history_60 = ts.get_k_data(code, ktype="60")

     closeArray_60 = num.array(data_history_60['close'])
     highArray_60 = num.array(data_history_60['high'])
     lowArray_60 = num.array(data_history_60['low'])

     doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')
     doubleHighArray_60 = num.asarray(highArray_60, dtype='double')
     doubleLowArray_60 = num.asarray(lowArray_60, dtype='double')

     upperband_60, middleband_60, lowerband_60 = ta.BBANDS(doubleCloseArray_60, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                           matype=0)

     strBULL60_title = "中间"
     if (highArray_60[-1] > upperband_60[-1]):
          strBULL60_title = "上穿"

     if (lowArray_60[-1] < lowerband_60[-1]):
          strBULL60_title = "下穿"

     strBULL60 = "BULL60：" + "%.2f" % upperband_60[-1] + "\_" + "%.2f" % middleband_60[-1] + "\_" + \
                 "%.2f" % lowerband_60[-1] + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
                 strBULL60_title + "</font>\n\n"
     if (closeArray[-1] > 1000):
          strBULL60 = "BULL60：" + str(int(round(upperband_60[-1]))) + "\_" + str(int(round(middleband_60[-1]))) + \
                      "\_" + str(int(round(lowerband_60[-1]))) + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
                      strBULL60_title + "</font>\n\n"
# 返回20均线是否上传，30均线趋势
# MA20_titile, MA30_titile, KDJ_J_title, MACD_title, BULL_title = zhibiao('002010','D')
# print(MA20_titile)
# print(MA30_titile)
# print(KDJ_J_title)
# print(MACD_title)
# print(BULL_title)