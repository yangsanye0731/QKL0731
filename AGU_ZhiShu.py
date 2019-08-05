#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *

def strategy(code, name):
     data_history = ts.get_k_data(code, ktype = "15")

     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])

     doubleCloseArray = num.asarray(closeArray,dtype='double')
     doubleHighArray = num.asarray(highArray,dtype='double')
     doubleLowArray = num.asarray(lowArray,dtype='double')

     SMA30_15_4 = ta.SMA(doubleCloseArray, timeperiod=5)
     SMA30_15_8 = ta.SMA(doubleCloseArray, timeperiod=10)
     SMA30_15_20 = ta.SMA(doubleCloseArray, timeperiod=20)

     if (SMA30_15_4[-1] > SMA30_15_4[-2] and SMA30_15_8[-1] > SMA30_15_8[-2] and SMA30_15_20[-1] > SMA30_15_20[-2]):
          str15QuShi = "买 "
     elif (SMA30_15_4[-1] < SMA30_15_4[-2] and SMA30_15_8[-1] < SMA30_15_8[-2] and SMA30_15_20[-1] < SMA30_15_20[-2]):
          str15QuShi = "卖 "
     else:
          str15QuShi = "空 "

     print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     return name + str15QuShi

str0 = strategy("399006", "创业")
str1 = strategy("002281", " 光迅")
str2 = strategy("000625", " 长安")
str3 = strategy("300136", " 信维")
str4 = strategy("002008", " 大族")
str5 = strategy("600498", " 烽火")
str6 = strategy("000739", " 普洛")
str7 = strategy("300328", " 宜安")
str8 = strategy("300251", " 光线")

content = str0 + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8
title = str0 + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8
sendMail (content, title)
