#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import common_zhibiao
import common_mysqlUtil

def strategy():
    # 获取实时数据
    data = common_mysqlUtil.select_xuangubao()
    # 数据遍历
    for i in range(len(data)):

        code = str(data[i][0])
        name = str(data[i][1])
        plate = str(data[i][2])
        mark = str(data[i][3])
        print(code)
        print(name)
        print(plate)
        print(mark)
        common_mysqlUtil.insert_zhishu_record(code, name, name,  plate, mark, "XGB")


strategy()


