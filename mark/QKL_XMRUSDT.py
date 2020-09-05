#encoding=utf-8
import pandas as pd
import numpy as num
import ccxt
import talib as ta
from mark.email_util import *

a = 0

def strategy(name,zhouqi):

    gateio = ccxt.gateio()
    limit = 500
    current_time = int(time.time()//60*60*1000)

    if (zhouqi == '15m'):
        since_time = current_time - limit * 15 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name,timeframe='15m', limit=500,since=since_time)
        zhouqi_ch = "15分钟"
    if (zhouqi == '1h'):
        since_time = current_time - limit * 1* 60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='1h', limit=500, since=since_time)
        zhouqi_ch = "1h"
    if (zhouqi == '2h'):
        since_time = current_time - limit * 2 * 60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='2h', limit=500, since=since_time)
        zhouqi_ch = "2h"
    if (zhouqi == '4h'):
        since_time = current_time - limit * 4*  60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time)
        zhouqi_ch = "4h"

    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)

    # 02、 数据格式处理、并计算布林线值
    closeArray = num.array(df['close'])
    highArray = num.array(df['high'])
    lowArray = num.array(df['low'])
    openArray = num.array(df['open'])

    doubleCloseArray = num.asarray(closeArray, dtype='double')
    doubleHighArray = num.asarray(highArray, dtype='double')
    doubleLowArray = num.asarray(lowArray, dtype='double')
    doubleOpenArray = num.asarray(openArray, dtype='double')

    # 布林线
    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray*1000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    upperband = upperband / 1000
    middleband = middleband / 1000
    lowerband = lowerband / 1000

    # macd 为快线 macdsignal为慢线，macdhist为柱体
    macd, macdsignal, macdhist = ta.MACD(num.asarray(doubleCloseArray*1000, dtype='double'), fastperiod=12, slowperiod=26,
                                         signalperiod=9)
    macd = macd / 1000
    macdsignal = macdsignal / 1000
    macdhist = macdhist / 1000

    fastk, fastd = ta.STOCHRSI(num.asarray(doubleCloseArray, dtype='double'), timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=3)
    print(fastd)
    if (zhouqi == '1h'):
        global fastd_1h
        fastd_1h = fastd

    print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(zhouqi_ch + "CLOSE===============" + str(closeArray[-1]))
    print(zhouqi_ch + "LOWER===============" + str(lowArray[-1]))
    print(zhouqi_ch + "HIGHER==============" + str(highArray[-1]))
    print(zhouqi_ch + "BULL upperband======" + str(upperband[-1]))
    print(zhouqi_ch + "BULL middleband=====" + str(middleband[-1]))
    print(zhouqi_ch + "BULL lowerband======" + str(lowerband[-1]))

    print(zhouqi_ch + "MACD 快线===========" + str(macd[-1]))
    print(zhouqi_ch + "MACD 慢线===========" + str(macdsignal[-1]))
    print(zhouqi_ch + "MACD 柱体===========" + str(macdhist[-1]))
    print(zhouqi_ch + "RSI_1h =============" + "%.2f" % fastd[-5] + "_" + "%.2f" % fastd[-4] + "_" + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])

    name_jian = name[0:3]
    if (zhouqi == '1h'):
        if (fastd[-1] < 50):
            sendMail(name_jian + "触" + zhouqi_ch + "底:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1],
                     name_jian + "触" + zhouqi_ch + "底:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])
        if (fastd[-1] > 50):
            sendMail(name_jian + "触" + zhouqi_ch + "顶:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1],
                     name_jian + "触" + zhouqi_ch + "顶:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])

strategy("XMR/USDT","1h")
