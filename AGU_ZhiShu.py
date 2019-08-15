#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common

def strategy(code, name, fullName):
     ############################################ 15分钟布林线###############################################
     data_history = ts.get_k_data(code, ktype = "15")

     closeArray = num.array(data_history['close'])
     highArray = num.array(data_history['high'])
     lowArray = num.array(data_history['low'])

     doubleCloseArray = num.asarray(closeArray,dtype='double')
     doubleHighArray = num.asarray(highArray,dtype='double')
     doubleLowArray = num.asarray(lowArray,dtype='double')

     SMA30_15_5 = ta.SMA(doubleCloseArray, timeperiod=5)
     SMA30_15_10 = ta.SMA(doubleCloseArray, timeperiod=10)
     SMA30_15_20 = ta.SMA(doubleCloseArray, timeperiod=20)
     SMA30_15_30 = ta.SMA(doubleCloseArray, timeperiod=30)
     xingtai = ""
     if (SMA30_15_5[-1] > SMA30_15_10[-1] > SMA30_15_20[-1] > SMA30_15_30[-1]):
          xingtai = "上好"

     if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
          xingtai = "下好"

     if (SMA30_15_5[-1] > SMA30_15_5[-2] and SMA30_15_10[-1] > SMA30_15_10[-2] and SMA30_15_20[-1] > SMA30_15_20[-2] and SMA30_15_30[-1] > SMA30_15_30[-2]):

          str15QuShi = "买 "
          str15QuShi_content = "【MACD慢线同步与形态】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入1</span>"
          if (SMA30_15_5[-2] > SMA30_15_5[-3] and SMA30_15_10[-2] > SMA30_15_10[-3] and SMA30_15_20[-2] > SMA30_15_20[-3] and SMA30_15_30[-2] > SMA30_15_30[-3]):
               str15QuShi_content = "【MACD慢线同步与形态】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入2</span>"
               if (SMA30_15_5[-3] > SMA30_15_5[-4] and SMA30_15_10[-3] > SMA30_15_10[-4] and SMA30_15_20[-3] > SMA30_15_20[-4] and SMA30_15_30[-3] > SMA30_15_30[-4]):
                    str15QuShi_content = "【MACD慢线同步与形态】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟买入3</span>"

     elif (SMA30_15_5[-1] < SMA30_15_5[-2] and SMA30_15_10[-1] < SMA30_15_10[-2] and SMA30_15_20[-1] < SMA30_15_20[-2]):
          str15QuShi = "卖 "
          str15QuShi_content = "【MACD慢线同步与形态】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟卖出</span>"
     else:
          str15QuShi = "空 "
          str15QuShi_content = "【MACD慢线同步与形态】均线<span style=\"color:#FF0000;font-weight:bold\">15分钟空仓</span>"

     ############################################ 60分钟布林线###############################################
     data_history_60 = ts.get_k_data(code, ktype="60")

     closeArray_60 = num.array(data_history_60['close'])
     highArray_60 = num.array(data_history_60['high'])
     lowArray_60 = num.array(data_history_60['low'])

     doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')
     doubleHighArray_60 = num.asarray(highArray_60, dtype='double')
     doubleLowArray_60 = num.asarray(lowArray_60, dtype='double')

     upperband_60, middleband_60, lowerband_60 = ta.BBANDS(doubleCloseArray_60, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                     matype=0)

     strBULL60_title = "中间"
     if (highArray_60[-1] > upperband_60[-1]):
         strBULL60_title = "上穿"

     if (lowArray_60[-1] < lowerband_60[-1]):
         strBULL60_title = "下穿"

     strBULL60 = "BULL60：" + "%.2f" % upperband_60[-1] + "_" + "%.2f" % middleband_60[-1] + "_" + \
             "%.2f" % lowerband_60[-1] + " " + "<span style=\"color:#FF0000;font-weight:bold\">" + \
             strBULL60_title + "</span>"
     if (closeArray[-1] > 1000):
         strBULL60 = "BULL60：" + str(int(round(upperband_60[-1]))) + "_" + str(int(round(middleband_60[-1]))) + \
                 "_" + str(int(round(lowerband_60[-1]))) + " " + "<span style=\"color:#FF0000;font-weight:bold\">" + \
                  strBULL60_title + "</span>"

     ############################################ 1天布林线    ###############################################
     data_history_D = ts.get_k_data(code, ktype="D")

     closeArray_D = num.array(data_history_D['close'])
     highArray_D = num.array(data_history_D['high'])
     lowArray_D = num.array(data_history_D['low'])

     doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')
     doubleHighArray_D = num.asarray(highArray_D, dtype='double')
     doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

     upperband_D, middleband_D, lowerband_D = ta.BBANDS(doubleCloseArray_D, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

     strBULLD_title = "中间"
     if (highArray_D[-1] > upperband_D[-1]):
          strBULLD_title = "上穿"

     if (lowArray_D[-1] < lowerband_D[-1]):
          strBULLD_title = "下穿"

     strBULL1 = "BULL1D：" + "%.2f" % upperband_D[-1] + "_" + "%.2f" % middleband_D[-1] + "_" + \
                "%.2f" % lowerband_D[-1] + " " + "<span style=\"color:#FF0000;font-weight:bold\">" + \
                strBULLD_title + "</span>"
     if (closeArray[-1] > 1000):
          strBULL1 = "BULL1D：" + str(int(round(upperband_D[-1]))) + "_" + str(int(round(middleband_D[-1]))) + \
                     "_" + str(int(round(lowerband_D[-1]))) + " " + "<span style=\"color:#FF0000;font-weight:bold\">" + \
                     strBULLD_title + "</span>"


     print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     title = name + xingtai + str15QuShi
     zhangdiefu = "%.2f" % (((closeArray_D[-1] - closeArray_D[-2])/closeArray_D[-2])*100)
     content = "<span style=\"color:#FF0000;font-weight:bold\">" + fullName + " "+ "%.3f" % closeArray[-1] + " " + zhangdiefu +  "%</span>" + \
               "<br>" + strBULL60 + "<br>" + strBULL1 + "<br>" + str15QuShi_content + xingtai

     return title, content


#######################################################################################################
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
############################################ 邮件发送###################################################
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#######################################################################################################
def pinjie(title, titleTmp, content, contentTmp):
     if (title.endswith("买 ")):
          titleTmp = title + titleTmp
          contentTmp = content + "<br><hr>" + contentTmp
     else:
          titleTmp = titleTmp + title
          contentTmp = contentTmp + "<br><hr>" + content

     return titleTmp, contentTmp

str0,content0 = strategy("399006", "※创业", "※创业板指")
str00,content00 = strategy("399975", "※证券", "※证券公司（晴雨表）")

titleTmp = ""
contentTmp = ""
str1, content1 = strategy("002281", " 光迅", "光迅科技")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str2, content2 = strategy("000625", " 长安(稳)", "长安汽车")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

str3, content3 = strategy("300136", " @信维", "@信维通信")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

str4, content4 = strategy("002008", " 大族", "大族激光")
titleTmp, contentTmp = pinjie(str4, titleTmp, content4, contentTmp)

str5, content5 = strategy("600498", " 烽火", "烽火通信")
titleTmp, contentTmp = pinjie(str5, titleTmp, content5, contentTmp)

str6, content6 = strategy("000739", " 普洛", "普洛药业")
titleTmp, contentTmp = pinjie(str6, titleTmp, content6, contentTmp)

str7, content7 = strategy("300328", " 宜安", "宜安科技")
titleTmp, contentTmp = pinjie(str7, titleTmp, content7, contentTmp)

str8, content8 = strategy("300251", " 光线", "光线传媒")
titleTmp, contentTmp = pinjie(str8, titleTmp, content8, contentTmp)

str9, content9 = strategy("300059", " 东方", "东方财富")
titleTmp, contentTmp = pinjie(str9, titleTmp, content9, contentTmp)

str10, content10 = strategy("300584", " @海辰", "@海辰药业")
titleTmp, contentTmp = pinjie(str10, titleTmp, content10, contentTmp)

str11, content11 = strategy("300664", " @鹏鹞", "@鹏鹞环保")
titleTmp, contentTmp = pinjie(str11, titleTmp, content11, contentTmp)

title = str0 + str00 + titleTmp

mulu1 = "=================================<br>"
mulu2 = "注意均线形态：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "<br>"
mulu3 = "=================================<br>"
content = mulu1 + mulu2 + mulu3 + content0 + "<br><hr>" + content00 + "<br><hr>" + contentTmp

# 发送邮件
sendMail (content, title)



