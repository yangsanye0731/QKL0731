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
     titile = name + str15QuShi

     content = name + str15QuShi
     return title, content

str0,content0 = strategy("399006", "※均线形态创业")

titleTmp = ""
str1, content1 = strategy("002281", " 光迅")
if (str1.endswith("买 ")):
     titleTmp = str1 + titleTmp
else:
     titleTmp = titleTmp + str1

str2, content2 = strategy("000625", " 长安")
if (str2.endswith("买 ")):
     titleTmp = str2 + titleTmp
else:
     titleTmp = titleTmp + str2

str3, content3 = strategy("300136", " @信维")
if (str3.endswith("买 ")):
     titleTmp = str3 + titleTmp
else:
     titleTmp = titleTmp + str3

str4, content4 = strategy("002008", " 大族")
if (str4.endswith("买 ")):
     titleTmp = str4 + titleTmp
else:
     titleTmp = titleTmp + str4

str5, content5 = strategy("600498", " 烽火")
if (str5.endswith("买 ")):
     titleTmp = str5 + titleTmp
else:
     titleTmp = titleTmp + str5

str6, content6 = strategy("000739", " 普洛")
if (str6.endswith("买 ")):
     titleTmp = str6 + titleTmp
else:
     titleTmp = titleTmp + str6

str7, content7 = strategy("300328", " 宜安")
if (str7.endswith("买 ")):
     titleTmp = str7 + titleTmp
else:
     titleTmp = titleTmp + str7

str8, content8 = strategy("300251", " 光线")
if (str8.endswith("买 ")):
     titleTmp = str8 + titleTmp
else:
     titleTmp = titleTmp + str8

str9, content9 = strategy("300059", " 东方")
if (str9.endswith("买 ")):
     titleTmp = str9 + titleTmp
else:
     titleTmp = titleTmp + str9

str10, content10 = strategy("300584", " @海辰")
if (str10.endswith("买 ")):
     titleTmp = str10 + titleTmp
else:
     titleTmp = titleTmp + str10

str11, content11 = strategy("300664", " @鹏鹞")
if (str11.endswith("买 ")):
     titleTmp = str11 + titleTmp
else:
     titleTmp = titleTmp + str11

title = str0 + titleTmp

mulu1 = "=================================<br>"
mulu2 = "=圈=子=日=报=：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "<br>"
mulu3 = "=================================<br>"
content = mulu1 + mulu2 + mulu3 + content0 + "<br><hr>" + content1  + "<br><hr>" + content2 + "<br><hr>" + content3 + "<br><hr>" \
          + content4 + "<br><hr>" + content5 + "<br><hr>" + content6 + "<br><hr>" + content7 + "<br><hr>" \
          + content8 + "<br><hr>" + content9 + "<br><hr>" + content10 + "<br><hr>" + content11

sendMail (content, title)
