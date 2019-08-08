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

str0 = strategy("399006", "※均线形态创业")

titleTmp = ""
str1 = strategy("002281", " 光迅")
if (str1.endswith("买 ")):
     titleTmp = str1 + titleTmp
else:
     titleTmp = titleTmp + str1

str2 = strategy("000625", " 长安")
if (str2.endswith("买 ")):
     titleTmp = str2 + titleTmp
else:
     titleTmp = titleTmp + str2

str3 = strategy("300136", " 信维")
if (str3.endswith("买 ")):
     titleTmp = str3 + titleTmp
else:
     titleTmp = titleTmp + str3

str4 = strategy("002008", " 大族")
if (str4.endswith("买 ")):
     titleTmp = str4 + titleTmp
else:
     titleTmp = titleTmp + str4

str5 = strategy("600498", " 烽火")
if (str5.endswith("买 ")):
     titleTmp = str5 + titleTmp
else:
     titleTmp = titleTmp + str5

str6 = strategy("000739", " 普洛")
if (str6.endswith("买 ")):
     titleTmp = str6 + titleTmp
else:
     titleTmp = titleTmp + str6

str7 = strategy("300328", " 宜安")
if (str7.endswith("买 ")):
     titleTmp = str7 + titleTmp
else:
     titleTmp = titleTmp + str7

str8 = strategy("300251", " 光线")
if (str8.endswith("买 ")):
     titleTmp = str8 + titleTmp
else:
     titleTmp = titleTmp + str8

str9 = strategy("300059", " 东方")
if (str9.endswith("买 ")):
     titleTmp = str9 + titleTmp
else:
     titleTmp = titleTmp + str9


content = str0 + titleTmp
title = str0 + titleTmp
sendMail (content, title)
