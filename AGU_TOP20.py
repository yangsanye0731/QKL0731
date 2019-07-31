#encoding=utf-8

import sys
import tushare as ts
import time
import numpy as num
from datetime import datetime, date
from datetime import timedelta
from email_util import *

'''
#################################
执行函数 execute
说明：
#################################
'''


def execute_shenzhen_1(days):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()

    jsonDic = {}
    for i in range(days) :
        date_n = (date.today() - timedelta(days=i)).strftime("%Y%m%d")
        df = pro.hsgt_top10(trade_date=date_n, market_type='3')
        ts_code = num.array(df['ts_code'])
        name = num.array(df['name'])
        net_amount = num.array(df['net_amount'])
        net_amount = net_amount.astype(num.float)
        if (len(ts_code) > 0):
            for i in range(ts_code.size):
                if (jsonDic.get(name[i]) == None):
                    jsonDic[name[i]] = 0
                jsonDic[name[i]] = jsonDic.get(name[i]) + net_amount[i]

    jsonDic1 = sorted(jsonDic.items(),key=lambda x:x[1])
    return jsonDic1

def execute_shanghai_1(days):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()

    jsonDic = {}
    for i in range(days) :
        date_n = (date.today() - timedelta(days=i)).strftime("%Y%m%d")
        df = pro.hsgt_top10(trade_date=date_n, market_type='1')
        ts_code = num.array(df['ts_code'])
        name = num.array(df['name'])
        net_amount = num.array(df['net_amount'])
        net_amount = net_amount.astype(num.float)
        if (len(ts_code) > 0):
            for i in range(ts_code.size):
                if (jsonDic.get(name[i]) == None):
                    jsonDic[name[i]] = 0
                jsonDic[name[i]] = jsonDic.get(name[i]) + net_amount[i]

    jsonDic1 = sorted(jsonDic.items(),key=lambda x:x[1])
    return jsonDic1

# print("===========================05天：")
# print (execute_shenzhen_1(5))
# print("===========================10天：")
# print(execute_shenzhen_1(10))
# print("===========================30天：")
# print(execute_shenzhen_1(30))
# print("===========================60天：")
# time.sleep(60)
# print(execute_shenzhen_1(60))

print("===========================05天：")
content1 = "===========================深圳05天：<br></br>" + str(execute_shenzhen_1(5)) + "<br></br>"
print("===========================10天：")
content2 = "===========================深圳10天：<br></br>" + str(execute_shenzhen_1(10))+ "<br></br>"
time.sleep(30)
print("===========================20天：")
content3 = "===========================深圳20天：<br></br>" + str(execute_shenzhen_1(20))+ "<br></br>"
time.sleep(60)
print("===========================60天：")
content5 = "===========================深圳60天：<br></br>" + str(execute_shenzhen_1(60))+ "<br></br>"
# time.sleep(60)
# content600 = "===========================上海01天：<br></br>" + str(execute_shanghai_1(1))+ "<br></br>"
# content60 = "===========================上海02天：<br></br>" + str(execute_shanghai_1(2))+ "<br></br>"
# content6 = "===========================上海05天：<br></br>" + str(execute_shanghai_1(5))+ "<br></br>"
# time.sleep(60)
# content7 = "===========================上海10天：<br></br>" + str(execute_shanghai_1(10))+ "<br></br>"
# time.sleep(60)
# content8 = "===========================上海20天：<br></br>" + str(execute_shanghai_1(20))+ "<br></br>"
# time.sleep(60)
# content9 = "===========================上海30天：<br></br>" + str(execute_shanghai_1(30))+ "<br></br>"
# time.sleep(60)
# content10 = "===========================上海60天：<br></br>" + str(execute_shanghai_1(60))+ "<br></br>"

content = content1 + content2 + content3 + content5
sendMail(template1(content), "A股TOP")
