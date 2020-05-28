# encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
from bypy import ByPy

def strategy(zhouqi, n):
    count = 0
    jsonDicCode = {}
    jsonDicCode1 = [('399001', '深证成指'), ('399006', '创业板指'), ('399231', '农林指数'), ('399232', '采矿指数'),
                    ('399234', '水电指数'), ('399235', '建筑指数'), ('399239', 'IT指数'),
                    ('399241', '地产指数'), ('399248', '文化指数'), ('399353', '国证物流'), ('399363', '计算机指数'), ('399365', '国证农业'),
                    ('399368', '国证军工'), ('399382', '1000材料'), ('399394', '国证医药'), ('399395', '国证有色'),
                    ('399396', '国证食品'),
                    ('399412', '国证新能'), ('399432', '国证汽车与汽车零配件行业'), ('399434', '国证传媒'),
                    ('399437', '国证证券'), ('399431', '国证银行'),
                    ('399434', '国证传媒'), ('399435', '国证农林牧渔'), ('399441', '国证生物医药'), ('399693', '安防产业'),
                    ('399804', '中证体育产业'), ('399807', '中证高铁产业'), ('399812', '中证养老产业'),
                    ('399936', '中证电信指数'), ('399936', '中证信息技术'), ('399970', '中证移动互联网'),
                    ('399976', '中证新能源汽车'),
                    ('399989', '中证医疗'), ('399993', '中证生物科技'), ('399996', '中证智能家居'),
                    ('399997', '中证白酒'), ('600519', '白酒_茅台'),
                    ('399998', '中证煤炭'), ('601088', '煤炭_神华'),
                    ('512480', '半导体ETF'), ('512760', '半导体50ETF'), ('512930', 'AIETF'),  ('515050', '5GETF'), ('512690', '酒ETF')]

    for key, value in jsonDicCode1:
        codeItem = key
        count = count + 1
        print(count)
        data_history = ts.get_k_data(codeItem, ktype=zhouqi)

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[n-1] > ma5[n-1] > doubleOpenArray[n-1] and ma5[n-2] < ma5[n-3] and \
                    ma5[n-3] < ma5[n-4] and doubleCloseArray[n-1] > doubleOpenArray[n-1]:
                print(value)
                common_image.plt_image_tongyichutu_zhishu(codeItem, value, "W", "【02国内指数】跨越5周线", "【02国内指数】跨越5周线")

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

strategy('W', 0)

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【02国内指数】跨越5周线执行完成', '触发【02国内指数】跨越5周线执行完成')