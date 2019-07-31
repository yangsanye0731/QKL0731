#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *

def strategy(code, name):
     data_history = ts.get_k_data(code, ktype = "15")

     # 02、 数据格式处理、并计算布林线值
     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])

     doubleCloseArray = num.asarray(closeArray,dtype='double')
     doubleHighArray = num.asarray(highArray,dtype='double')
     doubleLowArray = num.asarray(lowArray,dtype='double')

     SMA30_15_4 = ta.SMA(doubleCloseArray, timeperiod=4)
     SMA30_15_8 = ta.SMA(doubleCloseArray, timeperiod=8)
     SMA30_15_20 = ta.SMA(doubleCloseArray, timeperiod=20)
     SMA30_15_28 = ta.SMA(doubleCloseArray, timeperiod=28)

     if (SMA30_15_4[-1] > SMA30_15_4[-2] and SMA30_15_8[-1] > SMA30_15_8[-2] and SMA30_15_20[-1] > SMA30_15_20[-2] and SMA30_15_28[-1] > SMA30_15_28[-2]):
          str15QuShi = "买 "
     elif (SMA30_15_4[-1] < SMA30_15_4[-2] and SMA30_15_8[-1] < SMA30_15_8[-2] and SMA30_15_20[-1] < SMA30_15_20[-2] and SMA30_15_28[-1] < SMA30_15_28[-2]):
          str15QuShi = "卖 "
     else:
          str15QuShi = "空 "

     print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     #sendMail(name + "%.1f" % closeArray[-1]  + "_" + str15QuShi, name + "%.1f" % closeArray[-1]  + "_" + str15QuShi)
     return name + str15QuShi

str0 = strategy("399006", " 创业")
str1 = strategy("002281", " 光迅")
str2 = strategy("000625", " 长安")
str3 = strategy("300136", " 信维")

content = str0 + str1 + str2 + str3
title = str0 + str1 + str2 + str3
sendMail (content, title)
