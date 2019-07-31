#encoding=utf-8
import pandas as pd
import time
import numpy as num
import ccxt
import talib as ta
from email_util import *

a = 0

def strategy(name,zhouqi):
    gateio = ccxt.gateio()
    huobi = ccxt.huobipro()
    binance = ccxt.binance()
    limit = 500
    current_time = int(time.time()//60*60*1000)

    if (zhouqi == '15m'):
        since_time = current_time - limit * 15 * 60 * 1000
        data = binance.fetch_ohlcv(symbol=name,timeframe='15m', limit=500,since=since_time)
        zhouqi_ch = "15分钟"
    if (zhouqi == '1h'):
        #######################################################################################################
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        ############################################ 数据获取###################################################
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #####                                                                                             #####
        #######################################################################################################
        ##############获取1小时数据#############################################################################
        since_time = current_time - limit * 1* 60 * 60 * 1000
        data = huobi.fetch_ohlcv(symbol=name, timeframe='1h', limit=500, since=since_time)
        time.sleep(2)

        # ##############获取6小时数据#############################################################################
        since_time_6h = current_time - limit * 6 * 60 * 60 * 1000
        data_6h = gateio.fetch_ohlcv(symbol=name, timeframe='6h', limit=500, since=since_time_6h)
        time.sleep(2)

        ##############获取12小时数据#############################################################################
        since_time_12h = current_time - limit * 12 * 60 * 60 * 1000
        data_12h = gateio.fetch_ohlcv(symbol=name, timeframe='12h', limit=500, since=since_time_12h)
        # time.sleep(2)

        ##############获取30分钟数据#############################################################################
        # since_time_30 = current_time - limit * 1* 30 * 60 * 1000
        # data_30 = huobi.fetch_ohlcv(symbol=name, timeframe='30m', limit=500, since=since_time_30)
        # time.sleep(2)

        ##############获取15分钟数据#############################################################################
        # since_time_15 = current_time - limit * 1 * 15 * 60 * 1000
        # data_15 = huobi.fetch_ohlcv(symbol=name, timeframe='15m', limit=500, since=since_time_15)
        # time.sleep(2)

        ##############获取05分钟数据#############################################################################
        # since_time_5 = current_time - limit * 1 * 5 * 60 * 1000
        # data_5 = huobi.fetch_ohlcv(symbol=name, timeframe='5m', limit=500, since=since_time_5)
        # time.sleep(2)

        ##############获取04小时数据#############################################################################
        since_time_4h = current_time - limit * 4 * 60 * 60 * 1000
        data_4h = gateio.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time_4h)
        time.sleep(2)

        zhouqi_ch = "1h"

    if (zhouqi == '2h'):
        since_time = current_time - limit * 2 * 60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='2h', limit=500, since=since_time)
        zhouqi_ch = "2h"
    if (zhouqi == '4h'):
        since_time = current_time - limit * 4*  60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time)
        zhouqi_ch = "4h"

    #######################################################################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    ############################################ 数据处理###################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #######################################################################################################
    ############################################ 1小时数据处理##############################################
    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray = num.array(df['close'])
    highArray = num.array(df['high'])
    lowArray = num.array(df['low'])
    openArray = num.array(df['open'])
    doubleCloseArray = num.asarray(closeArray, dtype='double')
    doubleHighArray = num.asarray(highArray, dtype='double')
    doubleLowArray = num.asarray(lowArray, dtype='double')
    doubleOpenArray = num.asarray(openArray, dtype='double')

    ############################################ 15分钟数据处理############################################
    df_6h = pd.DataFrame(data_6h)
    df_6h = df_6h.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df_6h['open_time'] = pd.to_datetime(df_6h['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray_6h = num.array(df_6h['close'])
    doubleCloseArray_6h = num.asarray(closeArray_6h, dtype='double')

    ############################################ 15分钟数据处理############################################
    df_12h = pd.DataFrame(data_12h)
    df_12h = df_12h.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df_12h['open_time'] = pd.to_datetime(df_12h['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray_12h = num.array(df_12h['close'])
    doubleCloseArray_12h = num.asarray(closeArray_12h, dtype='double')

    ############################################ 15分钟数据处理############################################
    # df_15 = pd.DataFrame(data_15)
    # df_15 = df_15.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    # df_15['open_time'] = pd.to_datetime(df_15['open_time'], unit='ms') + pd.Timedelta(hours=8)
    # closeArray_15 = num.array(df_15['close'])
    # doubleCloseArray_15 = num.asarray(closeArray_15, dtype='double')

    ############################################ 05分钟数据处理############################################
    # df_5 = pd.DataFrame(data_5)
    # df_5 = df_5.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    # df_5['open_time'] = pd.to_datetime(df_5['open_time'], unit='ms') + pd.Timedelta(hours=8)
    # closeArray_5 = num.array(df_5['close'])
    # doubleCloseArray_5 = num.asarray(closeArray_5, dtype='double')

    ############################################ 30分钟数据处理############################################
    # df_30 = pd.DataFrame(data_30)
    # df_30 = df_30.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    # df_30['open_time'] = pd.to_datetime(df_30['open_time'], unit='ms') + pd.Timedelta(hours=8)
    # closeArray_30 = num.array(df_30['close'])
    # doubleCloseArray_30 = num.asarray(closeArray_30, dtype='double')

    ############################################ 04小时数据处理############################################
    data_4h = pd.DataFrame(data_4h)
    data_4h = data_4h.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    data_4h['open_time'] = pd.to_datetime(data_4h['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray_4h = num.array(data_4h['close'])
    doubleCloseArray_4h = num.asarray(closeArray_4h, dtype='double')







    #######################################################################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    ############################################ 数据处理###################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #######################################################################################################
    ############################################ 05分钟均线趋势#############################################
    # SMA30_5 = ta.SMA(doubleCloseArray_5, timeperiod=30)
    # # print("#####################################################################################15")
    # print(SMA30_5)
    # str5 = ""
    # if (SMA30_5[-1] > SMA30_5[-2]):
    #     str5 = "升1 "
    #     if ((SMA30_5[-2] > SMA30_5[-3])):
    #         str5 = "升2 "
    #         if ((SMA30_5[-3] > SMA30_5[-4])):
    #             str5 = "升3 "
    #
    # if (SMA30_5[-1] < SMA30_5[-2]):
    #     str5 = "降1 "
    #     if ((SMA30_5[-2] < SMA30_5[-3])):
    #         str5 = "降2 "
    #         if ((SMA30_5[-3] < SMA30_5[-4])):
    #             str5 = "降3 "


    # ############################################ 15分钟均线趋势#############################################
    # SMA30_15 = ta.SMA(doubleCloseArray, timeperiod=30)
    # SMA30_15_6 = ta.SMA(doubleCloseArray, timeperiod=6)
    # SMA30_15_12 = ta.SMA(doubleCloseArray, timeperiod=12)
    # SMA30_15_24 = ta.SMA(doubleCloseArray, timeperiod=24)
    # #print("#####################################################################################15")
    # #print(SMA30_15)
    # str15 = ""
    # if (SMA30_15[-1]>SMA30_15[-2]):
    #     str15 = "升1 "
    #     if((SMA30_15[-2]>SMA30_15[-3])):
    #         str15 = "升2 "
    #         if ((SMA30_15[-3] > SMA30_15[-4])):
    #             str15 = "升3 "
    #
    # if (SMA30_15[-1] < SMA30_15[-2]):
    #     str15 = "降1 "
    #     if ((SMA30_15[-2] < SMA30_15[-3])):
    #         str15 = "降2 "
    #         if ((SMA30_15[-3] < SMA30_15[-4])):
    #             str15 = "降3 "
    #
    # # print(SMA30_15_6)
    # # print(SMA30_15_12)
    # # print(SMA30_15_24)
    # str15QuShi = ""
    # if (SMA30_15_6[-1] > SMA30_15_6[-2] and SMA30_15_12[-1] > SMA30_15_12[-2] and SMA30_15_24[-1] > SMA30_15_24[-2]):
    #     str15QuShi = "均线1小时坚定买入1"
    #     if (SMA30_15_6[-2] > SMA30_15_6[-3] and SMA30_15_12[-2] > SMA30_15_12[-3] and SMA30_15_24[-2] > SMA30_15_24[-3]):
    #         str15QuShi = "均线1小时坚定买入2"
    # elif (SMA30_15_6[-1] < SMA30_15_6[-2] and SMA30_15_12[-1] < SMA30_15_12[-2] and SMA30_15_24[-1] < SMA30_15_24[-2]):
    #     str15QuShi = "均线1小时坚定卖出1"
    #     if (SMA30_15_6[-2] < SMA30_15_6[-3] and SMA30_15_12[-2] < SMA30_15_12[-3] and SMA30_15_24[-2] < SMA30_15_24[-3]):
    #         str15QuShi = "均线1小时坚定卖出2"
    # else:
    #     str15QuShi = "均线1小时坚定空仓"




    ############################################ 30分钟均线趋势#############################################
    # SMA30_30 = ta.SMA(doubleCloseArray_30, timeperiod=30)
    # #print("#####################################################################################30")
    # #print(SMA30_30)
    # str30 = ""
    # if (SMA30_30[-1]>SMA30_30[-2]):
    #     str30 = "升1 "
    #     if((SMA30_30[-2]>SMA30_30[-3])):
    #         str30 = "升2 "
    #         if ((SMA30_30[-3] > SMA30_30[-4])):
    #             str30 = "升3 "
    #
    # if (SMA30_30[-1] < SMA30_30[-2]):
    #     str30 = "降1 "
    #     if ((SMA30_30[-2] < SMA30_30[-3])):
    #         str30 = "降2 "
    #         if ((SMA30_30[-3] < SMA30_30[-4])):
    #             str30 = "降3 "
    #
    # ############################################ 01小时均线趋势#############################################
    # SMA30_1h = ta.SMA(doubleCloseArray, timeperiod=30)
    # # print("#####################################################################################1h")
    # # print(SMA30_1h)
    # str1h = ""
    # if (SMA30_1h[-1] > SMA30_1h[-2]):
    #     str1h = "升1 "
    #     if ((SMA30_1h[-2] > SMA30_1h[-3])):
    #         str1h = "升2 "
    #         if ((SMA30_1h[-3] > SMA30_1h[-4])):
    #             str1h = "升3 "
    #
    # if (SMA30_1h[-1] < SMA30_1h[-2]):
    #     str1h = "降1 "
    #     if ((SMA30_1h[-2] < SMA30_1h[-3])):
    #         str1h = "降2 "
    #         if ((SMA30_1h[-3] < SMA30_1h[-4])):
    #             str1h = "降3 "
    #
    # ############################################ 04小时均线趋势#############################################
    # SMA30_4h = ta.SMA(doubleCloseArray_4h, timeperiod=30)
    # # print("#####################################################################################4h")
    # # print(SMA30_4h)
    # str4h = ""
    # if (SMA30_4h[-1] > SMA30_4h[-2]):
    #     str4h = "升1 "
    #     if ((SMA30_4h[-2] > SMA30_4h[-3])):
    #         str4h = "升2 "
    #         if ((SMA30_4h[-3] > SMA30_4h[-4])):
    #             str4h = "升3 "
    #
    # if (SMA30_4h[-1] < SMA30_4h[-2]):
    #     str4h = "降1 "
    #     if ((SMA30_4h[-2] < SMA30_4h[-3])):
    #         str4h = "降2 "
    #         if ((SMA30_4h[-3] < SMA30_4h[-4])):
    #             str4h = "降3 "
    #
    #
    # strQuShi = "势5" + str5 + "4H" + str4h + "1H" + str1h + "30" + str30 + "15" + str15
    #
    # ############################################ 30小时STOCHRSI#############################################
    # fastk_30, fastd_30 = ta.STOCHRSI(num.asarray(doubleCloseArray_30, dtype='double'), timeperiod=14, fastk_period=14,
    #                                  fastd_period=3, fastd_matype=3)
    #
    ############################################ 01小时STOCHRSI#############################################
    fastk, fastd = ta.STOCHRSI(num.asarray(doubleCloseArray_4h, dtype='double'), timeperiod=14, fastk_period=14,
                               fastd_period=3, fastd_matype=3)
    #print(fastd)
    #
    #
    # # strRSI = " 周期1H:" + "%.1f" % fastd[-3] + "/" + "%.1f" % fastd[-2] + "/" + "%.1f" % fastd[-1] + " 30M:" + "%.1f" % \
    # #          fastd_30[-3] + "/" + "%.1f" % fastd_30[-2] + "/" + "%.1f" % fastd_30[-1] + " "
    # strRSI = " 周30:" + "%.1f" % fastd_30[-3] + "/" + "%.1f" % fastd_30[-2] + "/" + "%.1f" % fastd_30[-1] + " "
    #
    #
    # ############################################ 15分钟MACD    #############################################
    # # macd 为快线 macdsignal为慢线，macdhist为柱体
    # # print(doubleCloseArray_15)
    # macd, macdsignal, macdhist = ta.MACD(num.asarray(doubleCloseArray_15 * 1000, dtype='double'), fastperiod=12,
    #                                      slowperiod=26,
    #                                      signalperiod=9)
    # macd = macd / 1000
    # macdsignal = macdsignal / 1000
    # macdhist = macdhist / 1000
    #
    # strMA = " M15:" + "%.1f" % (macdsignal[-3]*100) + "/" + "%.1f" % (macdsignal[-2]*100) + "/" + "%.1f" % (macdsignal[-1]*100)
    #
    ############################################ 1小时布林线    ###############################################
    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_4h*1000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    upperband = upperband / 1000
    middleband = middleband / 1000
    lowerband = lowerband / 1000

    #print(lowerband)





    #######################################################################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    ############################################ 信息打印###################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #######################################################################################################
    print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(zhouqi_ch + "CLOSE===============" + str(closeArray[-1]))
    print(zhouqi_ch + "LOWER===============" + str(lowArray[-1]))
    print(zhouqi_ch + "HIGHER==============" + str(highArray[-1]))
    # print(zhouqi_ch + "RSI_1h =============" + "%.2f" % fastd[-5] + "_" + "%.2f" % fastd[-4] + "_" + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])



    #######################################################################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    ############################################ 邮件发送###################################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #######################################################################################################
    name_jian = name[0:3]
    # if (zhouqi == '1h'):
    #     if (fastd[-1] < 50):
    #         sendMail(name_jian + "%.3f" % closeArray[-1] + strQuShi + strRSI + strMA,
    #                  name_jian + "%.3f" % closeArray[-1] + strQuShi + strRSI + strMA)
    #     if (fastd[-1] > 50):
    #         sendMail(name_jian + "%.3f" % closeArray[-1] + strQuShi + strRSI + strMA,
    #                  name_jian + "%.3f" % closeArray[-1] + strQuShi + strRSI + strMA)
    if (zhouqi == '1h'):
            sendMail(name_jian + "%.3f" % closeArray[-1] + " RSI4H:" + "%.1f" % fastd[-3] + "_" + "%.1f" % fastd[-2] + "_" + "%.1f" % fastd[-1] + " BULL4H:" + "%.2f" % upperband[-1] + "_" + "%.2f" % middleband[-1] + "_" + "%.2f" % lowerband[-1],
                     name_jian + "%.3f" % closeArray[-1] + " RSI4H:" + "%.1f" % fastd[-3] + "_" + "%.1f" % fastd[-2] + "_" + "%.1f" % fastd[-1] + " BULL4H:" + "%.2f" % upperband[-1] + "_" + "%.2f" % middleband[-1] + "_" + "%.2f" % lowerband[-1])

strategy("EOS/USDT","1h")
