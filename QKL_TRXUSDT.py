#encoding=utf-8
import pandas as pd
import time
import numpy as num
import ccxt
import talib as ta
from email_util import *
import common

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
        ##############获取15分钟数据############################################################################
        since_time_15 = current_time - limit * 1 * 15 * 60 * 1000
        data_15 = huobi.fetch_ohlcv(symbol=name, timeframe='15m', limit=500, since=since_time_15)
        time.sleep(1)

        ##############获取01小时数据############################################################################
        since_time = current_time - limit * 1* 60 * 60 * 1000
        data = huobi.fetch_ohlcv(symbol=name, timeframe='1h', limit=500, since=since_time)
        time.sleep(1)

        ##############获取04小时数据############################################################################
        since_time_4h = current_time - limit * 4 * 60 * 60 * 1000
        data_4h = gateio.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time_4h)
        time.sleep(1)

        ###############获取06小时数据###########################################################################
        since_time_6h = current_time - limit * 6 * 60 * 60 * 1000
        data_6h = gateio.fetch_ohlcv(symbol=name, timeframe='6h', limit=500, since=since_time_6h)
        time.sleep(1)

        ##############获取12小时数据############################################################################
        since_time_12h = current_time - limit * 12 * 60 * 60 * 1000
        data_12h = gateio.fetch_ohlcv(symbol=name, timeframe='12h', limit=500, since=since_time_12h)
        time.sleep(1)

        ##############获取30分钟数据#############################################################################
        # since_time_30 = current_time - limit * 1* 30 * 60 * 1000
        # data_30 = huobi.fetch_ohlcv(symbol=name, timeframe='30m', limit=500, since=since_time_30)
        # time.sleep(2)

        ##############获取05分钟数据#############################################################################
        # since_time_5 = current_time - limit * 1 * 5 * 60 * 1000
        # data_5 = huobi.fetch_ohlcv(symbol=name, timeframe='5m', limit=500, since=since_time_5)
        # time.sleep(2)

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
    print(closeArray)

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
    df_15 = pd.DataFrame(data_15)
    df_15 = df_15.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df_15['open_time'] = pd.to_datetime(df_15['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray_15 = num.array(df_15['close'])
    doubleCloseArray_15 = num.asarray(closeArray_15, dtype='double')

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
    lowArray_4h = num.array(data_4h['low'])
    highArray_4h = num.array(data_4h['high'])
    doubleCloseArray_4h = num.asarray(closeArray_4h, dtype='double')

    ############################################ 06小时数据处理############################################
    data_6h = pd.DataFrame(data_6h)
    data_6h = data_6h.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    data_6h['open_time'] = pd.to_datetime(data_6h['open_time'], unit='ms') + pd.Timedelta(hours=8)
    closeArray_6h = num.array(data_6h['close'])
    lowArray_6h = num.array(data_6h['low'])
    highArray_6h = num.array(data_6h['high'])
    doubleCloseArray_6h = num.asarray(closeArray_6h, dtype='double')

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
    ############################################ 15分钟均线趋势#############################################
    SMA30_15M_5 = ta.SMA(doubleCloseArray_15, timeperiod=5)
    SMA30_15M_10 = ta.SMA(doubleCloseArray_15, timeperiod=10)
    SMA30_15M_20 = ta.SMA(doubleCloseArray_15, timeperiod=20)
    SMA30_15M_30 = ta.SMA(doubleCloseArray_15, timeperiod=30)

    str15MQuShi = ""
    xingtai = ""

    if (SMA30_15M_5[-1] > SMA30_15M_10[-1] > SMA30_15M_20[-1] > SMA30_15M_30[-1]):
        xingtai = "上好"

    if (SMA30_15M_5[-1] < SMA30_15M_10[-1] < SMA30_15M_20[-1] < SMA30_15M_30[-1]):
        xingtai = "下好"

    if (SMA30_15M_5[-1] > SMA30_15M_5[-2] and SMA30_15M_10[-1] > SMA30_15M_10[-2] and SMA30_15M_20[-1] > SMA30_15M_20[-2] and SMA30_15M_30[-1] > SMA30_15M_30[-2]):

        str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入</span>1\n\n"
        if (SMA30_15M_5[-2] > SMA30_15M_5[-3] and SMA30_15M_10[-2] > SMA30_15M_10[-3] and SMA30_15M_20[-2] > SMA30_15M_20[-3] and SMA30_15M_30[-2] > SMA30_15M_30[-3]):
            str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入</span>2\n\n"
            if (SMA30_15M_5[-3] > SMA30_15M_5[-4] and SMA30_15M_10[-3] > SMA30_15M_10[-4] and SMA30_15M_20[-3] > SMA30_15M_20[-4] and SMA30_15M_30[-2] > SMA30_15M_30[-3]):
                str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入</span>3\n\n"

    elif (SMA30_15M_5[-1] < SMA30_15M_5[-2] and SMA30_15M_10[-1] < SMA30_15M_10[-2] and SMA30_15M_20[-1] < SMA30_15M_20[-2] and SMA30_15M_30[-1] > SMA30_15M_30[-2]):

        str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟卖出</span>1\n\n"
        if (SMA30_15M_5[-2] < SMA30_15M_5[-3] and SMA30_15M_10[-2] < SMA30_15M_10[-3] and SMA30_15M_20[-2] < SMA30_15M_20[-3] and SMA30_15M_30[-2] < SMA30_15M_30[-3]):
            str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟卖出</span>2\n\n"
            if (SMA30_15M_5[-3] < SMA30_15M_5[-4] and SMA30_15M_10[-3] < SMA30_15M_10[-4] and SMA30_15M_20[-3] < SMA30_15M_20[-4] and SMA30_15M_30[-3] < SMA30_15M_30[-4]):
                str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟卖出</span>3\n\n"

    else:
        str15MQuShi = "【MACD慢线同步】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟空仓</span>\n\n"


    ##################################    ########### 1小时均线趋势#############################################
    SMA30_1h_5 = ta.SMA(doubleCloseArray, timeperiod=5)
    SMA30_1h_10 = ta.SMA(doubleCloseArray, timeperiod=10)
    SMA30_1h_20 = ta.SMA(doubleCloseArray, timeperiod=20)
    SMA30_1h_30 = ta.SMA(doubleCloseArray, timeperiod=30)

    # print(SMA30_1h_5)
    str1HQuShi = ""
    str1HQuShi_title = ""
    if (SMA30_1h_5[-1] > SMA30_1h_5[-2] and SMA30_1h_10[-1] > SMA30_1h_10[-2] and SMA30_1h_20[-1] > SMA30_1h_20[-2] and SMA30_1h_30[-1] > SMA30_1h_30[-2]):
        str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时买入</font>1\n\n"
        str1HQuShi_title = "买1"
        if (SMA30_1h_5[-2] > SMA30_1h_5[-3] and SMA30_1h_10[-2] > SMA30_1h_10[-3] and SMA30_1h_20[-2] > SMA30_1h_20[-3] and SMA30_1h_30[-2] > SMA30_1h_30[-3]):
            str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时买入</font>2\n\n"
            str1HQuShi_title = "买2"
            if (SMA30_1h_5[-3] > SMA30_1h_5[-4] and SMA30_1h_10[-3] > SMA30_1h_10[-4] and SMA30_1h_20[-3] > SMA30_1h_20[-4] and SMA30_1h_30[-3] > SMA30_1h_30[-4]):
                str1HQuShi = "【关注MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时买入</font>3\n\n"
                str1HQuShi_title = "买3"
    elif (SMA30_1h_5[-1] < SMA30_1h_5[-2] and SMA30_1h_10[-1] < SMA30_1h_10[-2] and SMA30_1h_20[-1] < SMA30_1h_20[-2] and SMA30_1h_30[-1] < SMA30_1h_30[-2]):
        str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时卖出</font>1\n\n"
        str1HQuShi_title = "卖1"
        if (SMA30_1h_5[-2] < SMA30_1h_5[-3] and SMA30_1h_10[-2] < SMA30_1h_10[-3] and SMA30_1h_20[-2] < SMA30_1h_20[-3] and SMA30_1h_30[-2] < SMA30_1h_30[-3]):
            str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时卖出</font>2\n\n"
            str1HQuShi_title = "卖2"
            if (SMA30_1h_5[-3] < SMA30_1h_5[-4] and SMA30_1h_10[-3] < SMA30_1h_10[-4] and SMA30_1h_20[-3] < SMA30_1h_20[-4] and SMA30_1h_30[-3] < SMA30_1h_30[-4]):
                str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时卖出</font>3\n\n"
                str1HQuShi_title = "卖3"
    else:
        str1HQuShi = "【MACD慢线同步】均线<font color=#FF0000 size=6 face=\"黑体\">01小时空仓</font>\n\n"
        str1HQuShi_title = "空"

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
    ############################################ 01小时STOCHRSI##############################################
    fastk_1H, fastd_1H = ta.STOCHRSI(num.asarray(doubleCloseArray, dtype='double'), timeperiod=14, fastk_period=14,
                                     fastd_period=3, fastd_matype=3)

    ############################################ 04小时STOCHRSI#############################################
    fastk_4H, fastd_4H = ta.STOCHRSI(num.asarray(doubleCloseArray_4h, dtype='double'), timeperiod=14, fastk_period=14,
                               fastd_period=3, fastd_matype=3)
    strRSI_1H_title = " R:" + "%.1f" % fastd_1H[-1]
    strRSI_1H = "RSI1小时【关注0,100】：" + "%.1f" % fastd_1H[-3] + "\_" + "%.1f" % fastd_1H[-2] + "\_" +  "%.1f" % fastd_1H[-1] + "\n\n"
    strRSI_4H = "RSI4小时【关注0,100】：" + "%.1f" % fastd_4H[-3] + "\_" + "%.1f" % fastd_4H[-2] + "\_" +  "%.1f" % fastd_4H[-1] + "\n\n"

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

    ############################################ 01小时布林线    ###############################################
    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray * 1000, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                 matype=0)
    upperband = upperband / 1000
    middleband = middleband / 1000
    lowerband = lowerband / 1000

    strBULL1_title = "中间"
    if (highArray[-1] > upperband[-1]):
        strBULL1_title = "上穿"

    if (lowArray[-1] < lowerband[-1]):
        strBULL1_title = "下穿"

    strBULL1 = "BULL1H：" + "%.2f" % upperband[-1] + "\_" + "%.2f" % middleband[-1] + "\_" + \
               "%.2f" % lowerband[-1] + " " + "<font color=#FF0000 size=6 face=\"黑体\">" + \
               strBULL1_title + "</font>\n\n"
    if (closeArray[-1] > 100):
        strBULL1 = "BULL1H：" + str(int(round(upperband[-1]))) + "\_" + str(int(round(middleband[-1]))) + \
                   "\_" + str(int(round(lowerband[-1]))) + " " + "<font color=#FF0000 size=6 face=\"黑体\">" + \
                   strBULL1_title + "</font>\n\n"

    ############################################ 04小时布林线    ###############################################
    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_4h*1000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    upperband = upperband / 1000
    middleband = middleband / 1000
    lowerband = lowerband / 1000

    strBULL4_title = "中间"
    if (highArray_4h[-1] > upperband[-1]):
        strBULL4_title = "上穿"

    if  (lowArray_4h[-1] < lowerband[-1]):
        strBULL4_title = "下穿"

    strBULL4 = "BULL4H：" + "%.2f" % upperband[-1] + "\_" + "%.2f" % middleband[-1] + "\_" + \
               "%.2f" % lowerband[-1] + " " +  "<font color=red>" + \
               strBULL4_title + "</font>\n\n"
    if (closeArray[-1] > 100):
        strBULL4 = "BULL4H：" + str(int(round(upperband[-1]))) + "\_" + str(int(round(middleband[-1]))) + \
                   "\_" + str(int(round(lowerband[-1]))) + " " + "<font color=red>" + \
                   strBULL4_title + "</font>\n\n"

    ############################################ 06小时布林线    ###############################################
    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_6h * 1000, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                 matype=0)
    upperband = upperband / 1000
    middleband = middleband / 1000
    lowerband = lowerband / 1000

    strBULL6_title = "中间"
    if (highArray_6h[-1] > upperband[-1]):
        strBULL6_title = "上穿"

    if (lowArray_6h[-1] < lowerband[-1]):
        strBULL6_title = "下穿"

    strBULL6 = "BULL6H：" + "%.2f" % upperband[-1] + "\_" + "%.2f" % middleband[-1] + "\_" + \
               "%.2f" % lowerband[-1] + " " + "<font color=#FF0000 size=6 face=\"黑体\">" + \
               strBULL6_title + "</font>\n\n"
    if (closeArray[-1] > 100):
        strBULL6 = "BULL6H：" + str(int(round(upperband[-1]))) + "\_" + \
                   str(int(round(middleband[-1]))) + "\_" + str(int(round(lowerband[-1]))) + \
                   " " + "<font color=#FF0000 size=6 face=\"黑体\">" + strBULL6_title + "</font>\n\n"

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
    ############################################ 邮件发送内容###############################################
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #####                                                                                             #####
    #######################################################################################################
    name_jian = name[0:3]
    title = " " + name_jian + "%.2f" % closeArray[-1] + strRSI_1H_title + str1HQuShi_title + strBULL4_title + xingtai
    if (closeArray[-1] > 100):
        title = " " + name_jian + str(int(round(closeArray[-1]))) + strRSI_1H_title + str1HQuShi_title + strBULL4_title + xingtai
    zhangdiefu = "%.2f" % (((closeArray[-1] - openArray[-1]) / openArray[-1]) * 100)
    content = "#### **<font color=#FF0000 size=6 face=\"黑体\">" + name_jian + " "+ "%.3f" % closeArray[-1] + " 1H涨跌：" +  zhangdiefu + "%"+ "</font>**\n" + strRSI_1H + strRSI_4H + \
                     strBULL1 + strBULL4 + strBULL6 + str15MQuShi + xingtai + str1HQuShi
    return title, content

title0, content0 = strategy("BTC/USDT","1h")
title1, content1 = strategy("ETH/USDT","1h")
title2, content2 = strategy("EOS/USDT","1h")
title3, content3 = strategy("LTC/USDT","1h")
title30, content30 = strategy("BCH/USDT","1h")
title4, content4 = strategy("HT/USDT","1h")
title5, content5 = strategy("XRP/USDT","1h")
title6, content6 = strategy("TRX/USDT","1h")

mulu = "# **<font color=#FF0000 size=6 face=\"黑体\">每日简报</font>**\n\n"
content = mulu + \
          content0 + "***\n\n" + content1 \
          + "***\n\n" + content2 \
          + "***\n\n" + content3 \
          + "***\n\n" + content30 \
          + "***\n\n" + content4 \
          + "***\n\n" + content5 \
          + "***\n\n" + content6

title = title0 + title1 + title2

# 邮件发送
#sendMail(content, title)
# common.dingding_msg(title)
# common.dingding_msg(content)
common.dingding_markdown_msg(title, content)