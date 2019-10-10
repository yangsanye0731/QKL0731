#encoding=utf-8

import sys
import tushare as ts
import time
import numpy as num
from datetime import datetime, date
from datetime import timedelta
from email_util import *
import common
import common_mysqlUtil

'''
#################################
执行函数 execute
说明：
#################################
'''

def execute_shenzhen_1():
    jsonDicCode = {}
    jsonDicCode1 = [('000100.SZ', 'TCL集团'), ('000002.SZ', '万科A'), ('300059.SZ', '东方财富'), ('000063.SZ', '中兴通讯'),
                    ('002129.SZ', '中环股份'), ('000538.SZ', '云南白药'), ('000858.SZ', '五粮液'), ('000725.SZ', '京东方A'),
                    ('300014.SZ', '亿纬锂能'), ('300136.SZ', '信维通信'), ('300450.SZ', '先导智能'), ('300012.SZ', '华测检测'),
                    ('002402.SZ', '和而泰'), ('002236.SZ', '大华股份'), ('002008.SZ', '大族激光'), ('300750.SZ', '宁德时代'),
                    ('000001.SZ', '平安银行'), ('001979.SZ', '招商蛇口'), ('000651.SZ', '格力电器'), ('002456.SZ', '欧菲光'),
                    ('002241.SZ', '歌尔股份'), ('002157.SZ', '正邦科技'), ('002463.SZ', '沪电股份'), ('300347.SZ', '泰格医药'),
                    ('000568.SZ', '泸州老窖'), ('002304.SZ', '洋河股份'), ('000977.SZ', '浪潮信息'), ('002415.SZ', '海康威视'),
                    ('000089.SZ', '深圳机场'), ('300498.SZ', '温氏股份'), ('002714.SZ', '牧原股份'), ('002422.SZ', '科伦药业'),
                    ('002475.SZ', '立讯精密'), ('000333.SZ', '美的集团')]

    for key,value in jsonDicCode1:
        codeStr = key[0:6]
        codeName = value
        common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", "TOP")

def execute_shanghai_1():
    jsonDicCode = {}
    jsonDicCode1 = [('600309.SH', '万华化学'), ('600031.SH', '三一重工'), ('600703.SH', '三安光电'), ('600104.SH', '上汽集团'),
                    ('600009.SH', '上海机场'), ('600030.SH', '中信证券'), ('601390.SH', '中国中铁'), ('601888.SH', '中国国旅'),
                    ('601601.SH', '中国太保'), ('601318.SH', '中国平安'), ('600028.SH', '中国石化'), ('600050.SH', '中国联通'),
                    ('600536.SH', '中国软件'), ('600887.SH', '伊利股份'), ('600048.SH', '保利地产'), ('603986.SH', '兆易创新'),
                    ('601166.SH', '兴业银行'), ('601288.SH', '农业银行'), ('600547.SH', '山东黄金'), ('601138.SH', '工业富联'),
                    ('601398.SH', '工商银行'), ('600276.SH', '恒瑞医药'), ('600570.SH', '恒生电子'), ('600036.SH', '招商银行'),
                    ('603160.SH', '汇顶科技'), ('603338.SH', '浙江鼎力'), ('600000.SH', '浦发银行'), ('603288.SH', '海天味业'),
                    ('600690.SH', '海尔智家'), ('600585.SH', '海螺水泥'), ('600837.SH', '海通证券'), ('600183.SH', '生益科技'),
                    ('603259.SH', '药明康德'), ('600519.SH', '贵州茅台'), ('600900.SH', '长江电力'), ('601012.SH', '隆基股份'),
                    ('600600.SH', '青岛啤酒')]


    for key, value in jsonDicCode1:
        codeStr = key[0:6]
        codeName = value
        common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", "TOP")

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
common_mysqlUtil.deleteTopRecord("TOP")
content1 = "===========================深圳60天：<br></br>" + str(execute_shenzhen_1())+ "<br></br>"
content2 = "===========================上海60天：<br></br>" + str(execute_shanghai_1())+ "<br></br>"
# sendMail(content1, "TOP执行完成")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
