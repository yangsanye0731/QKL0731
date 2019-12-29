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
def execute():
    jsonDicCode = {}
    jsonDicCode1 = [('399001', '深证成指'), ('399006', '创业板指'),('399231', '农林指数'), ('399232', '采矿指数'),
                    ('399234', '水电指数'), ('399235', '建筑指数'), ('399239', 'IT指数'),
                    ('399241', '地产指数'), ('399248', '文化指数'), ('399363', '计算机指数'), ('399365', '国证农业'),
                    ('399368', '国证军工'), ('399382', '1000材料'), ('399394', '国证医药'), ('399395', '国证有色'),
                    ('399396', '国证食品'),
                    ('399412', '国证新能'), ('399432', '国证汽车与汽车零配件行业'), ('399434', '国证传媒'),
                    ('399437', '国证证券'), ('399431', '国证银行'),
                    ('399434', '国证传媒'), ('399435', '国证农林牧渔'), ('399441', '国证生物医药'), ('399693', '安防产业'),
                    ('399804', '中证体育产业'), ('399807', '中证高铁产业'), ('399812', '中证养老产业'),
                    ('399936', '中证电信指数'), ('399936', '中证信息技术'), ('399970', '中证移动互联网'),
                    ('399976', '中证新能源汽车'),
                    ('399989', '中证医疗'), ('399993', '中证生物科技'), ('399996', '中证智能家居'), ('399997', '中证白酒'),
                    ('399998', '中证煤炭')]

    for key,value in jsonDicCode1:
        codeStr = key
        codeName = value
        common_mysqlUtil.insert_zhishu_record(codeStr, codeName, codeName, " ", " ", "ZHISHU")

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
common_mysqlUtil.deleteTopRecord("ZHISHU")
common_mysqlUtil.insert_ZhiShuLog_record("======", "========", "ZHISHU", "============", "====", "====", "======", "")
execute()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
