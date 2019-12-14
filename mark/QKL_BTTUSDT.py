#encoding=utf-8
import pandas as pd
import time
import numpy as num
import ccxt
import talib as ta
from email_util import *

a = 0

def strategy(name,zhouqi):
    global a
    if (a == 1):
        return
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
        zhouqi_ch = "1小时"
    if (zhouqi == '2h'):
        since_time = current_time - limit * 2 * 60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='2h', limit=500, since=since_time)
        zhouqi_ch = "2小时"
    if (zhouqi == '4h'):
        since_time = current_time - limit * 4*  60 * 60 * 1000
        data = gateio.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time)
        zhouqi_ch = "4小时"

    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)

    # 02、 数据格式处理、并计算布林线值
    closeArray = num.array(df['close'])
    highArray = num.array(df['high'])
    lowArray = num.array(df['low'])

    doubleCloseArray = num.asarray(closeArray, dtype='double')
    doubleHighArray = num.asarray(highArray, dtype='double')
    doubleLowArray = num.asarray(lowArray, dtype='double')

    upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray*10000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    upperband = upperband/10000
    middleband = middleband/10000
    lowerband = lowerband/10000
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(zhouqi_ch + "CLOSE===============" + str(closeArray[-1]))
    print(zhouqi_ch + "LOWER===============" + str(lowArray[-1]))
    print(zhouqi_ch + "HIGHER==============" + str(highArray[-1]))
    print(zhouqi_ch + "BULL upperband======" + str(upperband[-1]))
    print(zhouqi_ch + "BULL middleband=====" + str(middleband[-1]))
    print(zhouqi_ch + "BULL lowerband======" + str(lowerband[-1]))

    if (lowArray[-1] <= lowerband[-1]):
        a = 1
        sendMail(name + "触"+ zhouqi_ch +"BL下沿：" + str(closeArray[-1]), name + "触"+ zhouqi_ch +"BL下沿：" + str(closeArray[-1]))
    if (highArray[-1] >= upperband[-1]):
        a = 1
        sendMail(name + "触"+ zhouqi_ch +"BL上沿：" + str(closeArray[-1]), name + "触"+ zhouqi_ch +"BL上沿：" + str(closeArray[-1]))

strategy("BTT/USDT","15m")
strategy("BTT/USDT","1h")
strategy("BTT/USDT","2h")
strategy("BTT/USDT","4h")





