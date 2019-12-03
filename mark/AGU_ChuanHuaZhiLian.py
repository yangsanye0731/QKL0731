#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *

a = 0

def strategy(code, name, zhouqi):
     global a
     if (a == 1):
          return

     if (zhouqi == '30'):
          zhouqi_ch = "30分钟"
     if (zhouqi == '60'):
          zhouqi_ch = "60分钟"
     if (zhouqi == 'D'):
          zhouqi_ch = "1天"
     if (zhouqi == 'W'):
          zhouqi_ch = "1周"

     data_history = ts.get_k_data(code, ktype = zhouqi)

     # 02、 数据格式处理、并计算布林线值
     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])

     doubleCloseArray = num.asarray(closeArray,dtype='double')
     doubleHighArray = num.asarray(highArray,dtype='double')
     doubleLowArray = num.asarray(lowArray,dtype='double')

     upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     print(zhouqi_ch + "LOWER===============" + str(lowArray[-1]))
     print(zhouqi_ch + "HIGHER==============" + str(highArray[-1]))
     print(zhouqi_ch + "CLOSE===============" + str(closeArray[-1]))
     print(zhouqi_ch + "BULL upperband======" +  str(upperband[-1]))
     print(zhouqi_ch + "BULL middleband=====" +  str(middleband[-1]))
     print(zhouqi_ch + "BULL lowerband======" +  str(lowerband[-1]))

     if ((lowArray[-1] - lowerband[-1])/lowArray[-1] <= 0.01 ):
          a = 1
          sendMail(name + "触发" + zhouqi_ch + "布林线下沿,当前价格：" + str(closeArray[-1]), name + "触发" + zhouqi_ch + "布林线下沿,当前价格：" + str(closeArray[-1]))
     if (highArray[-1] >= upperband[-1]):
          a = 1
          sendMail(name + "触发" + zhouqi_ch + "布林线上沿,当前价格：" + str(closeArray[-1]), name + "触发" + zhouqi_ch + "布林线上沿,当前价格：" + str(closeArray[-1]))


strategy("002010", "传化智联", "30")
strategy("002010", "传化智联", "60")
strategy("002010", "传化智联", "D")
