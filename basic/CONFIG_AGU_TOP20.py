import tushare as ts
import numpy as num
from datetime import date
from datetime import timedelta
import common_mysqlUtil
import time

#######################################################################################################################
#######################################################################################################深圳市场60天top10
def execute_shenzhen_1(days):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()

    jsonDic = {}
    jsonDicCode = {}
    for i in range(days) :
        date_n = (date.today() - timedelta(days=i)).strftime("%Y%m%d")
        df = pro.hsgt_top10(trade_date=date_n, market_type='3')
        time.sleep(1)
        ts_code = num.array(df['ts_code'])
        name = num.array(df['name'])
        net_amount = num.array(df['net_amount'])
        net_amount = net_amount.astype(num.float)
        if len(ts_code) > 0:
            for i in range(ts_code.size):
                if jsonDic.get(name[i]) is None:
                    jsonDic[name[i]] = 0
                    jsonDicCode[ts_code[i]] = name[i]
                jsonDic[name[i]] = jsonDic.get(name[i]) + net_amount[i]
                jsonDicCode[ts_code[i]] = name[i]

    jsonDic1 = sorted(jsonDic.items(),key=lambda x:x[1])
    jsonDicCode1 = sorted(jsonDicCode.items(), key=lambda x: x[1])
    print(jsonDic1)
    print(jsonDicCode1)

    # for key,value in jsonDicCode1:
    #     codeStr = key[0:6]
    #     codeName = value
    #     common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", " ", "TOP_SZ")

    return jsonDic1

#######################################################################################################################
#######################################################################################################上海市场60天top10
def execute_shanghai_1(days):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()

    jsonDic = {}
    jsonDicCode = {}
    for i in range(days):
        date_n = (date.today() - timedelta(days=i)).strftime("%Y%m%d")
        df = pro.hsgt_top10(trade_date=date_n, market_type='1')
        time.sleep(1)
        ts_code = num.array(df['ts_code'])
        name = num.array(df['name'])
        net_amount = num.array(df['net_amount'])
        net_amount = net_amount.astype(num.float)
        if len(ts_code) > 0:
            for i in range(ts_code.size):
                if jsonDic.get(name[i]) is None:
                    jsonDic[name[i]] = 0
                    jsonDicCode[ts_code[i]] = name[i]
                jsonDic[name[i]] = jsonDic.get(name[i]) + net_amount[i]
                jsonDicCode[ts_code[i]] = name[i]

    jsonDic1 = sorted(jsonDic.items(), key=lambda x: x[1])
    jsonDicCode1 = sorted(jsonDicCode.items(), key=lambda x: x[1])
    print(jsonDic1)
    print(jsonDicCode1)

    # for key, value in jsonDicCode1:
    #     codeStr = key[0:6]
    #     codeName = value
    #     common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", " ", "TOP_SH")

    return jsonDic1

#######################################################################################################################
##############################################################################################################主程序运行
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
common_mysqlUtil.deleteTopRecord("TOP_SZ")
content1 = "===========================深圳60天：<br></br>" + str(execute_shenzhen_1(60)) + "<br></br>"
time.sleep(60)
common_mysqlUtil.deleteTopRecord("TOP_SH")
content2 = "===========================上海60天：<br></br>" + str(execute_shanghai_1(60)) + "<br></br>"
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
