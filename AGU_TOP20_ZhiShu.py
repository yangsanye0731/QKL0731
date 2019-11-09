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
    jsonDicCode1 = [('399231', '农林指数'),('399235', '建筑指数'),('399239', 'IT指数'),('399241', '地产指数'),
                    ('399363', '计算机指数'),('399368', '国证军工'),('399394', '国证医药'),('399395', '国证有色'),
                    ('399412', '国证新能'), ('399417', '国证新能源汽车'), ('399437', '国证证券'), ('399431', '国证银行'),
                    ('399435', '国证农林牧渔'), ('399441', '国证生物医药'), ('399936', '中证电信指数'), ('399936', '中证信息技术'),
                    ('399970', '中证移动互联网'), ('399997', '中证白酒'), ('399989', '中证医疗')]

    for key,value in jsonDicCode1:
        codeStr = key
        codeName = value
        common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", "ZHISHU")

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
common_mysqlUtil.deleteTopRecord("ZHISHU")
content1 = "===========================深圳60天：<br></br>" + str(execute_shenzhen_1())+ "<br></br>"
# sendMail(content1, "TOP执行完成")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
