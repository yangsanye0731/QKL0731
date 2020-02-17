#encoding=utf-8

import tushare as ts
import numpy as num
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import matplotlib
import matplotlib.pyplot as plt
import os

# 涨跌幅
def zhangdiefu(code):
     data_history_D = ts.get_k_data(code, ktype="D")
     closeArray_D = num.array(data_history_D['close'])
     return "%.2f" % (((closeArray_D[-1] - closeArray_D[-2]) / closeArray_D[-2]) * 100) + '%'

# 股票名称（可能为空，不推荐使用）
def gupiaomingcheng(code):
     if (code == '000001'):
          return '上证指数'
     data_realTime = ts.get_realtime_quotes(code)
     nameArray = data_realTime['name']
     return nameArray[0]

# 市净率
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

# EPS
def codeEPS(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     if code.startswith('6'):
          code = code + '.SH'
     if code.startswith('0'):
          code = code + '.SZ'
     if code.startswith('3'):
          code = code + '.SZ'
     timez = time.strftime('%Y%m%d', time.localtime(time.time()))
     df = pro.fina_indicator(ts_code=code)
     return df['eps'][0],df['basic_eps_yoy'][0],df['or_yoy'][0],df['eps'][1], df['basic_eps_yoy'][1], df['or_yoy'][1]

# 融资比
def codeRongZiBi(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     if code.startswith('6') or code.startswith('5'):
          code = code + '.SH'
     if code.startswith('0'):
          code = code + '.SZ'
     if code.startswith('3'):
          code = code + '.SZ'
     timez = time.strftime('%Y%m%d', time.localtime(time.time()))
     df = pro.daily_basic(ts_code=code, trade_date='20191010',
                          fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,total_mv')
     nameArray = num.array(df['total_mv'])

     df = pro.query('margin_detail', trade_date='20191010')
     df = df[df.ts_code.isin([code])]
     rzye = num.array(df['rzye'])

     rongZiBi = rzye[0]/(nameArray[0]*10000)
     return "%.4f" % rongZiBi

# 总市值
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

# 基本数据
def daily_basic(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     if code.startswith('6'):
          code = code + '.SH'
     if code.startswith('0'):
          code = code + '.SZ'
     if code.startswith('3'):
          code = code + '.SZ'
     timez = time.strftime('%Y%m%d', time.localtime(time.time()))
     df = pro.daily_basic(ts_code=code, trade_date="20200217",
                          fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')
     #print(df)
     return df

# 股票名称
def codeName(code):
     ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
     pro = ts.pro_api()
     timez = time.strftime('%Y%m%d', time.localtime(time.time()))
     df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
     df2 = df.loc[df['symbol'] == code]
     nameArray = num.array(df2['name'])
     return nameArray[0]

def dingding_msg(content):
     # WebHook地址
     webhook = 'https://oapi.dingtalk.com/robot/send?access_token=991bba5d439fb424f4ab1645a86aa353ac89e92352d11e1f44846a0bca812862'
     # 初始化机器人小丁
     xiaoding = DingtalkChatbot(webhook)
     # Text消息@所有人
     at_mobiles = ['17706417762']
     xiaoding.send_text(msg=content, is_at_all=False, at_mobiles=at_mobiles)

def dingding_markdown_msg(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=991bba5d439fb424f4ab1645a86aa353ac89e92352d11e1f44846a0bca812862'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)

def dingding_markdown_msg_2(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=d62051ad4dd53ae281ef9cb2e7258041a9a0d086bc5bb14612b508930ebd1666'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)

def dingding_markdown_msg_ene(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=7073587d80b34d698a2656dfa1d4aaffb18510c658b1ef12bf2b8cfebb3976cc'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)

# daily_basic("002655")