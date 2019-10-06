#encoding=utf-8

import tushare as ts
import numpy as num
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import matplotlib
import matplotlib.pyplot as plt
import os
import tushare as ts
import talib as ta
import pandas as pd

def xiangguanxing(code, code2):
     data_history = ts.get_k_data(code, ktype='D')
     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])
     openArray = num.array(data_history['open'])

     doubleCloseArray = num.asarray(closeArray, dtype='double')
     doubleHighArray = num.asarray(highArray, dtype='double')
     doubleLowArray = num.asarray(lowArray, dtype='double')
     doubleOpenArray = num.asarray(openArray, dtype='double')

     data_history2 = ts.get_k_data(code2, ktype='D')
     # print(data_history2)

     closeArray2 = num.array(data_history2['close'])
     highArray2 = num.array(data_history2['high'])
     lowArray2 = num.array(data_history2['low'])
     openArray2 = num.array(data_history2['open'])

     doubleCloseArray2 = num.asarray(closeArray2, dtype='double')
     doubleHighArray2 = num.asarray(highArray2, dtype='double')
     doubleLowArray2 = num.asarray(lowArray2, dtype='double')
     doubleOpenArray2 = num.asarray(openArray2, dtype='double')

     length1 = len(doubleCloseArray)
     length2 = len(doubleCloseArray)
     min_length = 0
     if (length1 >= length2):
          min_length = length2
     if (length1 < length2):
          min_length = length1

     tongxiang = 0
     i = 0
     while i < min_length:
          if ((doubleCloseArray[i] - doubleOpenArray[i])> 0 and (doubleCloseArray2[i] - doubleOpenArray2[i])> 0):
               tongxiang = tongxiang + 1
          if ((doubleCloseArray[i] - doubleOpenArray[i]) < 0 and (doubleCloseArray2[i] - doubleOpenArray2[i])< 0):
               tongxiang = tongxiang + 1
          i = i + 1
     xiangsixing = tongxiang / min_length
     return xiangsixing

# xiangguanxing('399006', '399006')