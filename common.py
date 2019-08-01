#encoding=utf-8

import tushare as ts
import numpy as num
import time

# 涨跌幅
def zhangdiefu(code):

     if (code == '000001'):
         code = 'sh'
     data_realTime = ts.get_realtime_quotes(code)

     realTimeArray = num.array(data_realTime['price'])
     realTimeArray = realTimeArray.astype(num.float)

     pre_close = num.array(data_realTime['pre_close'])
     pre_close = pre_close.astype(num.float)

     return "%.2f" % (((realTimeArray[0] - pre_close[0]) / pre_close[0]) * 100) + '%'

#股票名称
def gupiaomingcheng(code):

     if (code == '000001'):
          return '上证指数'
     data_realTime = ts.get_realtime_quotes(code)
     nameArray = data_realTime['name']
     return nameArray[0]


def shijinglv(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     if code.startswith('6'):
          code = code + '.SH'
     if code.startswith('0'):
          code = code + '.SZ'
     if code.startswith('3'):
          code = code + '.SZ'
     timez = time.strftime('%Y%m%d',time.localtime(time.time()))
     df = pro.daily_basic(ts_code=code, trade_date='20190419',
                          fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
     nameArray = num.array(df['pb'])
     return nameArray[0]


def zongshizhi(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     if code.startswith('6'):
          code = code + '.SH'
     if code.startswith('0'):
          code = code + '.SZ'
     if code.startswith('3'):
          code = code + '.SZ'
     timez = time.strftime('%Y%m%d', time.localtime(time.time()))
     df = pro.daily_basic(ts_code=code, trade_date='20190419',
                          fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,total_mv')
     nameArray = num.array(df['total_mv'])
     return nameArray[0]

#是否持有
def shifouchiyou(code) :
     chiyou_code_index = num.array(['300349'])
     if (chiyou_code_index.__contains__(code)):
          return 'yes'

#当前价格
def dangqianjiage(code) :
     if (code == '000001'):
         code = 'sh'
     data_realTime = ts.get_realtime_quotes(code)
     # print data_realTime
     realTimeArray = num.array(data_realTime['price'])
     realTimeArray = realTimeArray.astype(num.float)
     return realTimeArray[0]

#最低价格
def zuidijiage(codeCon, type) :
     if (codeCon == '000001'):
          data_history = ts.get_k_data(codeCon, ktype=type, index='true')
     else:
          data_history = ts.get_k_data(codeCon, ktype=type)

     zuijdijiage = num.array(data_history['low'])
     zuijdijiage = zuijdijiage.astype(num.float)
     return zuijdijiage[-1]

#小魔王扩展
def xiaomowangkuozhan(codeItem) :
     # MACD
     macd_60,macdsignal_60,macdhist_60,jsonResult_60,result_60,mairuresult_60,maichuresult_60  = MACD(codeItem,  '60')
     macd_D,macdsignal_D,macdhist_D,jsonResult_D,result_D,mairuresult_D,maichuresult_D  = MACD(codeItem,  'D')
     macd_W,macdsignal_W,macdhist_W,jsonResult_W,result_W,mairuresult_W,maichuresult_W  = MACD(codeItem,  'W')

     # 布林线
     upperband_60, middleband_60, lowerband_60, jsonResult_b_60, result_bl_60,mairuresult_bl_60,maichuresult_bl_60 = BBANDS(codeItem, '60')
     upperband_D, middleband_D, lowerband_D, jsonResult_b_D, result_bl_D,mairuresult_bl_D,maichuresult_bl_D = BBANDS(codeItem, 'D')

     xiaomowang = '<br>==============================' + gupiaomingcheng(codeItem)
     xiaomowang = xiaomowang + '<br>卖出信号：<br>' +  maichuresult_W + '<br>' + maichuresult_D + '<br>' + maichuresult_60 + '<br>' + maichuresult_bl_60 + '<br>' + maichuresult_bl_D
     xiaomowang = xiaomowang + '<br>买入信号：<br>' +  mairuresult_W + '<br>' + mairuresult_D + '<br> ' + mairuresult_60 + '<br>' + mairuresult_bl_60 + '<br>' + mairuresult_bl_D

     return xiaomowang


#print zhangdiefu('150212')
#print gupiaomingcheng('150212')
#print shifouchiyou('150212')
#print dangqianjiage('600547')
#print zuidijiage('600547', 'W')
#print shijinglv('603068')
#print zongshizhi('603068')
