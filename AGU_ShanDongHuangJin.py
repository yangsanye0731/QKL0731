#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *

a = 0

def strategy(code, name, zhouqi):

     if (zhouqi == '30'):
          zhouqi_ch = "30分"
     if (zhouqi == '60'):
          zhouqi_ch = "1h"
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

     fastk, fastd = ta.STOCHRSI(num.asarray(doubleCloseArray, dtype='double'), timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=3)
     #print(fastd)

     print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     print(zhouqi_ch + "LOWER===============" + str(lowArray[-1]))
     print(zhouqi_ch + "HIGHER==============" + str(highArray[-1]))
     print(zhouqi_ch + "CLOSE===============" + str(closeArray[-1]))
     print(zhouqi_ch + "BULL upperband======" +  str(upperband[-1]))
     print(zhouqi_ch + "BULL middleband=====" +  str(middleband[-1]))
     print(zhouqi_ch + "BULL lowerband======" +  str(lowerband[-1]))
     print(zhouqi_ch + "RSI_1h =============" + "%.2f" % fastd[-5] + "_"+ "%.2f" % fastd[-4] + "_"+ "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])

     if (zhouqi == '60'):
          if (fastd[-1] < 10):
               sendMail(name + "触" + zhouqi_ch + "底:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1],
                        name + "触" + zhouqi_ch + "底:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])
          if (fastd[-1] > 80):
               sendMail(name + "触" + zhouqi_ch + "顶:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1],
                        name + "触" + zhouqi_ch + "顶:" + str(closeArray[-1]) + " " + "%.2f" % fastd[-3] + "_" + "%.2f" % fastd[-2] + "_" + "%.2f" % fastd[-1])

strategy("600547", "山东黄金", "60")
strategy("002415", "海康威视", "60")
strategy("600570", "恒生电子", "60")
strategy("000063", "中兴通讯", "60")
strategy("300059", "东方财富", "60")
strategy("002334", "英威腾", "60")
strategy("000725", "京东方A", "60")