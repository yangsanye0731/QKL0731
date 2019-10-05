#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import mysql_util

def strategy(code, name, fullName, mark):
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
          xingtai = "上好1"
          if (SMA30_15_5[-2] > SMA30_15_10[-2] > SMA30_15_20[-2] > SMA30_15_30[-2]):
               xingtai = "上好2"
               if (SMA30_15_5[-3] > SMA30_15_10[-3] > SMA30_15_20[-3] > SMA30_15_30[-3]):
                    xingtai = "上好3"


     if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
          xingtai = "下好1"
          if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
               xingtai = "下好2"
               if (SMA30_15_5[-1] < SMA30_15_10[-1] < SMA30_15_20[-1] < SMA30_15_30[-1]):
                    xingtai = "下好3"

     if (SMA30_15_5[-1] > SMA30_15_5[-2] and SMA30_15_10[-1] > SMA30_15_10[-2] and SMA30_15_20[-1] > SMA30_15_20[-2] and SMA30_15_30[-1] > SMA30_15_30[-2]):

          str15QuShi = "15买1 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>1" + xingtai + "**\n\n"
          if (SMA30_15_5[-2] > SMA30_15_5[-3] and SMA30_15_10[-2] > SMA30_15_10[-3] and SMA30_15_20[-2] > SMA30_15_20[-3] and SMA30_15_30[-2] > SMA30_15_30[-3]):
               str15QuShi = "15买2 "
               str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>2" + xingtai + "**\n\n"
               if (SMA30_15_5[-3] > SMA30_15_5[-4] and SMA30_15_10[-3] > SMA30_15_10[-4] and SMA30_15_20[-3] > SMA30_15_20[-4] and SMA30_15_30[-3] > SMA30_15_30[-4]):
                    str15QuShi = "15买3 "
                    str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟买入</font>3" + xingtai + "**\n\n"

     elif (SMA30_15_5[-1] < SMA30_15_5[-2] and SMA30_15_10[-1] < SMA30_15_10[-2] and SMA30_15_20[-1] < SMA30_15_20[-2]):
          str15QuShi = "15卖 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟卖出</font>" + xingtai + "**\n\n"
     else:
          str15QuShi = "15空 "
          str15QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">15分钟空仓</font>" + xingtai + "**\n\n"

     ############################################ 30分钟布林线###############################################
     data_history_30 = ts.get_k_data(code, ktype="30")

     closeArray_30 = num.array(data_history_30['close'])
     highArray_30 = num.array(data_history_30['high'])
     lowArray_30 = num.array(data_history_30['low'])

     doubleCloseArray_30 = num.asarray(closeArray_30, dtype='double')
     doubleHighArray_30 = num.asarray(highArray_30, dtype='double')
     doubleLowArray_30 = num.asarray(lowArray_30, dtype='double')

     SMA30_30_5 = ta.SMA(doubleCloseArray_30, timeperiod=5)
     SMA30_30_10 = ta.SMA(doubleCloseArray_30, timeperiod=10)
     SMA30_30_20 = ta.SMA(doubleCloseArray_30, timeperiod=20)
     SMA30_30_30 = ta.SMA(doubleCloseArray_30, timeperiod=30)
     SMA30_30_60 = ta.SMA(doubleCloseArray_30, timeperiod=60)

     MIN30_60MA = ""
     MIN30_60MA_content = ""
     if (SMA30_30_60[-1] > SMA30_30_60[-2]):
          MIN30_60MA = "趋势1"
          MIN30_60MA_content = "30分钟60均线趋势走多1\n\n"
          if (SMA30_30_60[-2] > SMA30_30_60[-3]):
               MIN30_60MA = "趋势2"
               MIN30_60MA_content = "30分钟60均线趋势走多2\n\n"
               if (SMA30_30_60[-3] > SMA30_30_60[-4]):
                    MIN30_60MA = "趋势3"
                    MIN30_60MA_content = "30分钟60均线趋势走多3\n\n"
                    if (SMA30_30_60[-4] > SMA30_30_60[-5]):
                         MIN30_60MA = "趋势4"
                         MIN30_60MA_content = "30分钟60均线趋势走多4\n\n"
                         if (SMA30_30_60[-5] > SMA30_30_60[-6]):
                              MIN30_60MA = "趋势5"
                              MIN30_60MA_content = "30分钟60均线趋势走多5\n\n"
                              if (SMA30_30_60[-6] > SMA30_30_60[-7]):
                                   MIN30_60MA = "趋势6"
                                   MIN30_60MA_content = "30分钟60均线趋势走多6\n\n"
                                   if (SMA30_30_60[-6] > SMA30_30_60[-7]):
                                        MIN30_60MA = "错过"
                                        MIN30_60MA_content = "30分钟60均线趋势错过\n\n"

     xingtai1 = ""
     if (SMA30_30_5[-1] > SMA30_30_10[-1] > SMA30_30_20[-1] > SMA30_30_30[-1]):
          xingtai1 = "上好1"
          if (SMA30_30_5[-2] > SMA30_30_10[-2] > SMA30_30_20[-2] > SMA30_30_30[-2]):
               xingtai1 = "上好2"
               if (SMA30_30_5[-3] > SMA30_30_10[-3] > SMA30_30_20[-3] > SMA30_30_30[-3]):
                    xingtai1 = "上好3"

     if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
          xingtai1 = "下好1"
          if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
               xingtai1 = "下好2"
               if (SMA30_30_5[-1] < SMA30_30_10[-1] < SMA30_30_20[-1] < SMA30_30_30[-1]):
                    xingtai1 = "下好3"

     if (SMA30_30_5[-1] > SMA30_30_5[-2] and SMA30_30_10[-1] > SMA30_30_10[-2] and SMA30_30_20[-1] > SMA30_30_20[-2] and SMA30_30_30[-1] > SMA30_30_30[-2]):

          str30QuShi = "30买1 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>1" + xingtai1 + "**\n\n"
          if (SMA30_30_5[-2] > SMA30_30_5[-3] and SMA30_30_10[-2] > SMA30_30_10[-3] and SMA30_30_20[-2] >
                  SMA30_30_20[-3] and SMA30_30_30[-2] > SMA30_30_30[-3]):
               str30QuShi = "30买2 "
               str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>2" + xingtai1 + "**\n\n"
               if (SMA30_30_5[-3] > SMA30_30_5[-4] and SMA30_30_10[-3] > SMA30_30_10[-4] and SMA30_30_20[-3] >
                       SMA30_30_20[-4] and SMA30_30_30[-3] > SMA30_30_30[-4]):
                    str30QuShi = "30买3 "
                    str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟买入</font>3" + xingtai1 + "**\n\n"

     elif (SMA30_30_5[-1] < SMA30_30_5[-2] and SMA30_30_10[-1] < SMA30_30_10[-2] and SMA30_30_20[-1] < SMA30_30_20[-2]):
          str30QuShi = "30卖 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟卖出</font>" + xingtai1 + "**\n\n"
     else:
          str30QuShi = "30空 "
          str30QuShi_content = "【均线】**<font color=#FF0000 size=6 face=\"微软雅黑\">30分钟空仓</font>" + xingtai1 + "**\n\n"

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

     strBULL60 = "BULL60：" + "%.2f" % upperband_60[-1] + "\_" + "%.2f" % middleband_60[-1] + "\_" + \
             "%.2f" % lowerband_60[-1] + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
             strBULL60_title + "</font>\n\n"
     if (closeArray[-1] > 1000):
         strBULL60 = "BULL60：" + str(int(round(upperband_60[-1]))) + "\_" + str(int(round(middleband_60[-1]))) + \
                 "\_" + str(int(round(lowerband_60[-1]))) + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
                  strBULL60_title + "</font>\n\n"

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

     strBULL1 = "BULL1D：" + "%.2f" % upperband_D[-1] + "\_" + "%.2f" % middleband_D[-1] + "\_" + \
                "%.2f" % lowerband_D[-1] + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
                strBULLD_title + "</font>\n\n"
     if (closeArray[-1] > 1000):
          strBULL1 = "BULL1D：" + str(int(round(upperband_D[-1]))) + "\_" + str(int(round(middleband_D[-1]))) + \
                     "\_" + str(int(round(lowerband_D[-1]))) + " " + "<font color=#FF0000 size=6 face=\"微软雅黑\">" + \
                     strBULLD_title + "</font>\n\n"


     ##################################################################################################################
     # macd 为快线 macdsignal为慢线，macdhist为柱体
     macd, macdsignal, macdhist = ta.MACD(doubleCloseArray_D, fastperiod=12, slowperiod=26, signalperiod=9)
     if (macdhist[-1] > macdhist[-2] and macdhist[-3] > macdhist[-2]):
          macd_title = "MA_转 "
     else:
          macd_title = "MA_平 "

     stock_data = {}
     # 计算KDJ指标
     low_list = data_history_D.low.rolling(9).min()
     low_list.fillna(value=data_history_D.low.expanding().min(), inplace=True)
     high_list = data_history_D.high.rolling(9).max()
     high_list.fillna(value=data_history_D.high.expanding().max(), inplace=True)
     rsv = (doubleCloseArray_D - low_list) / (high_list - low_list) * 100
     # stock_data['KDJ_K'] = pd.ewma(rsv, com=2)
     stock_data['KDJ_K'] = pd.DataFrame.ewm(rsv, com=2).mean()
     # stock_data['KDJ_D'] = pd.ewma(stock_data['KDJ_K'], com=2)
     stock_data['KDJ_D'] = pd.DataFrame.ewm(stock_data['KDJ_K'], com=2).mean()
     stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
     dddd = pd.DataFrame(stock_data)

     KDJ_J_title = "KD_" + "%.1f" % dddd.KDJ_J[len(dddd) - 1] + " "
     # print("%.2f" % dddd.KDJ_J[len(dddd) - 1])

     MA_20 = ta.SMA(doubleCloseArray_D, timeperiod=20)

     MA20_titile = ""
     if(doubleCloseArray_D[-1] > MA_20[-1] and doubleLowArray_D[-1] < MA_20[-1]):
          MA20_titile = "20天均线上穿 "
     ##################################################################################################################

     zhangdiefu = "%.2f" % (((closeArray_D[-1] - closeArray_D[-2]) / closeArray_D[-2]) * 100)  + "%"
     print(name + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
     # title = name + zhangdiefu + xingtai1 + str15QuShi + str30QuShi
     title = name + zhangdiefu + macd_title + KDJ_J_title + MA20_titile + " "

     content = "#### **<font color=#FF0000 size=6 face=\"微软雅黑\">" + fullName + " " + "%.3f" % closeArray[-1] + " " + zhangdiefu + "</font>**\n" + \
               MIN30_60MA_content + str15QuShi_content + str30QuShi_content + strBULL60 + strBULL1
     # print(time.localtime().tm_hour)
     # if (time.localtime().tm_hour > 14):
     #    common_image.plt_image_geGuZhiBiao(code, fullName)
     mingcheng = fullName
     sql = "INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `code`, `zhangdiefu`, `30zhi`, `60zhi`, `beizhu`, `insert_time`) VALUES (" \
           "'" + mingcheng + "', " \
           "'" + code + "', " \
           "'" + zhangdiefu + "', " \
           "'2', '2', " \
           "'" + mark + "', " \
           "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
     print(sql)
     mysql_util.insertRecord(sql)
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
# 趋势 标识：30分钟60均线处于向上态势
# 上好 表示：30分钟 5、10、20、30均线 处于依次叠加良好形态
# 买 表示：30分钟 5、10、20、30均线 均处于向上态势
def pinjie(title, titleTmp, content, contentTmp):
     # if (("趋势" in title or "上好" in title) and "买" in title):
     if ("转" in title or "上穿" in title):
          titleTmp = title + "<br>" + titleTmp
          contentTmp = content + "***\n\n" + contentTmp
     # else:
     #      titleTmp = titleTmp + title
     #      contentTmp = contentTmp + "***\n\n" + content

     return titleTmp, contentTmp

# str0,content0 = strategy("399006", "※创业", "※创业板指")
# str00,content00 = strategy("399975", "※证券", "※证券公司（晴雨表）")
#清空数据库
mysql_util.deleteRecord()

titleTmp = ""
contentTmp = ""

str1, content1 = strategy("399006", " 创业板指", "创业板指", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str1, content1 = strategy("399001", " 深证成指", "深证成指", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str1, content1 = strategy("399975", " 证券公司", "证券公司", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)
#################################################################################################################BBBBBB
str17, content17 = strategy("002594", " 比亚迪", "比亚迪", " ")
titleTmp, contentTmp = pinjie(str17, titleTmp, content17, contentTmp)

str20, content20 = strategy("300294", "博雅生物", "博雅生物", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################CCCCCC
str2, content2 = strategy("000625", " 长安汽车", "长安汽车", " ")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

str2, content2 = strategy("002010", " 传化智联", "传化智联", "传化智联备注信息")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

#################################################################################################################DDDDDD
str4, content4 = strategy("002008", " 大族激光", "大族激光", " ")
titleTmp, contentTmp = pinjie(str4, titleTmp, content4, contentTmp)

str9, content9 = strategy("300059", " 东方财富", "东方财富", " ")
titleTmp, contentTmp = pinjie(str9, titleTmp, content9, contentTmp)

str20, content20 = strategy("002236", "大华股份", "大华股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################EEEEEE
str20, content20 = strategy("002812", "恩捷股份", "恩捷股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################FFFFFF
str5, content5 = strategy("600498", " 烽火通信", "烽火通信", " ")
titleTmp, contentTmp = pinjie(str5, titleTmp, content5, contentTmp)

#################################################################################################################GGGGGG
str1, content1 = strategy("002281", " 光迅科技", "光迅科技", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str12, content12 = strategy("300537", " 广信材料", "广信材料", " ")
titleTmp, contentTmp = pinjie(str12, titleTmp, content12, contentTmp)

str13, content13 = strategy("300480", " 光力科技", "光力科技", " ")
titleTmp, contentTmp = pinjie(str13, titleTmp, content13, contentTmp)

str8, content8 = strategy("300251", " 光线传媒", "光线传媒", " ")
titleTmp, contentTmp = pinjie(str8, titleTmp, content8, contentTmp)

str20, content20 = strategy("002074", "国轩高科", "国轩高科", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300699", "光威复材", "光威复材", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600589", "广东榕泰", "广东榕泰", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300499", "高澜股份", "高澜股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################HHHHHH
str10, content10 = strategy("300584", " 海辰药业", "海辰药业", " ")
titleTmp, contentTmp = pinjie(str10, titleTmp, content10, contentTmp)

str14, content14 = strategy("300462", " 华铭智能", "华铭智能", " ")
titleTmp, contentTmp = pinjie(str14, titleTmp, content14, contentTmp)

str20, content20 = strategy("600271", "航天信息", "航天信息", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("000988", "华工科技", "华工科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600570", "恒生电子", "恒生电子", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################JJJJJJ
str15, content15 = strategy("002020", " 京新药业", "京新药业", " ")
titleTmp, contentTmp = pinjie(str15, titleTmp, content15, contentTmp)

#################################################################################################################KKKKKK
str20, content20 = strategy("002230", "科大讯飞", "科大讯飞", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################LLLLLL
str18, content18 = strategy("300691", "联合光电", "联合光电", " ")
titleTmp, contentTmp = pinjie(str18, titleTmp, content18, contentTmp)

#################################################################################################################NNNNNN
str20, content20 = strategy("300068", "南都电源", "南都电源", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################PPPPPP
str6, content6 = strategy("000739", " 普洛药业", "普洛药业", " ")
titleTmp, contentTmp = pinjie(str6, titleTmp, content6, contentTmp)

str11, content11 = strategy("300664", " 鹏鹞环保", "鹏鹞环保", " ")
titleTmp, contentTmp = pinjie(str11, titleTmp, content11, contentTmp)

#################################################################################################################RRRRRR
str16, content16 = strategy("300576", " 容大感光", "容大感光", " ")
titleTmp, contentTmp = pinjie(str16, titleTmp, content16, contentTmp)

#################################################################################################################SSSSSS
str20, content20 = strategy("000603", "盛达矿业", "盛达矿业", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600703", "三安光电", "三安光电", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################TTTTTT
str20, content20 = strategy("000877", "天山股份", "天山股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################WWWWWW
str20, content20 = strategy("300017", "网宿科技", "网宿科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300253", "卫宁健康", "卫宁健康", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################XXXXXX
str20, content20 = strategy("000997", "新大陆", "新大陆", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str3, content3 = strategy("300136", " 信维通信", "信维通信", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

str3, content3 = strategy("600587", " 新华医疗", "新华医疗", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

#################################################################################################################YYYYYY
str20, content20 = strategy("002182", "云海金属", "云海金属", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str7, content7 = strategy("300328", " 宜安科技", "宜安科技", " ")
titleTmp, contentTmp = pinjie(str7, titleTmp, content7, contentTmp)

#################################################################################################################ZZZZZZ
str19, content19 = strategy("600489", "中金黄金", "中金黄金", " ")
titleTmp, contentTmp = pinjie(str19, titleTmp, content19, contentTmp)

str20, content20 = strategy("600036", "招商银行", "招商银行", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################ETFETF
str20, content20 = strategy("512480", "半导体", "半导体ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("515000", "科技ETF", "科技ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("512930", "AIETF", "AIETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("159934", "黄金ETF", "黄金ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300203", "聚光科技", "聚光科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

title = titleTmp
mulu = "# **<font color=#FF0000 size=6 face=\"微软雅黑\">每日简报 " + time.strftime("%m-%d %H:%M", time.localtime()) + "</font>**\n\n"
content = contentTmp

# 发送信息
# common.dingding_markdown_msg_2(title,content)
# 发送邮件
sendMail(title + "<br><br><br><br>" + content, title)


