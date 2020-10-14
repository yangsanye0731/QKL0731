import numpy as num
import talib as ta
import tushare as ts
from bypy import ByPy
import time

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os
project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_image

#######################################################################################################################
################################################################################################################指数策略
def strategy(zhouqi, n):
    count = 0
    jsonDicCode1 = [('399001', '深证成指'), ('399006', '创业板指'), ('399231', '农林指数'), ('399232', '采矿指数'),
                    ('399234', '水电指数'), ('399235', '建筑指数'), ('399239', 'IT指数'), ('399365', '国证农业'),
                    ('399241', '地产指数'), ('399248', '文化指数'), ('399353', '国证物流'), ('399363', '计算机指数'),
                    ('399368', '国证军工'), ('399382', '1000材料'), ('399394', '国证医药'), ('399395', '国证有色'),
                    ('399396', '国证食品'), ('399412', '国证新能'), ('399432', '国证汽车与零配件'), ('399434', '国证传媒'),
                    ('399437', '国证证券'), ('399431', '国证银行'), ('399997', '中证白酒'), ('600519', '白酒_茅台'),
                    ('399434', '国证传媒'), ('399435', '国证农林牧渔'), ('399441', '国证生物医药'), ('399693', '安防产业'),
                    ('399804', '中证体育'), ('399807', '中证高铁'), ('399812', '中证养老'), ('399976', '中证新能源汽车'),
                    ('399936', '中证电信'), ('399936', '中证信息技术'), ('399970', '中证移动互联网'), ('399989', '中证医疗'),
                    ('399993', '中证生物科技'), ('399996', '中证智能家居'), ('399998', '中证煤炭'), ('601088', '煤炭_神华'),
                    ('512480', '半导体ETF'), ('512760', '半导体50ETF'), ('512930', 'AIETF'),  ('515050', '5GETF'),
                    ('512690', '酒ETF'),  ('518880', '黄金ETF'), ('515110', '一带一路国企ETF'), ('159995', '芯片ETF'),
                    ('515000', '科技ETF'), ('515030', '新能源车ETF'), ('512170', '医疗ETF'), ('512660', '军工ETF'),
                    ('515880', '通信ETF'), ('515980', '人工智能ETF')]

    for key, value in jsonDicCode1:
        codeItem = key
        count = count + 1
        print(count)
        data_history_W = ts.get_k_data(codeItem, ktype='W')
        data_history_M = ts.get_k_data(codeItem, ktype='M')
        data_history_D = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray_W = num.array(data_history_W['close'])
            doubleCloseArray_W = num.asarray(closeArray_W, dtype='double')
            highArray_W = num.array(data_history_W['high'])
            doubleHighArray_W = num.asarray(highArray_W, dtype='double')
            openArray_W = num.array(data_history_W['open'])
            doubleOpenArray_W = num.asarray(openArray_W, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray_W, timeperiod=5)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray_W[n-1] > ma5[n-1] > doubleOpenArray_W[n-1] and ma5[n - 2] < ma5[n - 3] < ma5[n - 4] \
                    and doubleCloseArray_W[n - 1] > doubleOpenArray_W[n - 1]:
                print(value)
                image_path = common_image.plt_image_tongyichutu_zhishu(codeItem, value,
                                                          "W",
                                                          "【02国内指数】跨越5周线",
                                                          "【02国内指数】跨越5周线")

                image_url = "http://47.240.11.144/" + image_path[6:]
                print(image_url)
                common.dingding_markdown_msg_03('触发【02国内指数】跨越5周线' + value + '(' + codeItem + ')',
                                                '触发【02国内指数】跨越5周线' + value + '(' + codeItem + ')'
                                                + "\n\n> ![screenshot](" + image_url + ")")

            closeArray_M = num.array(data_history_M['close'])
            doubleCloseArray_M = num.asarray(closeArray_M, dtype='double')
            lowArray_M = num.array(data_history_M['low'])
            doubleLowArray_M = num.asarray(lowArray_M, dtype='double')
            closeArray_D = num.array(data_history_D['close'])
            doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')
            lowArray_D = num.array(data_history_D['low'])
            doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

            param_m1 = 11
            param_m2 = 9
            param_n = 10
            sma_n = ta.SMA(closeArray_M, param_n)
            upper = (1 + param_m1 / 100) * sma_n
            lower = (1 - param_m2 / 100) * sma_n
            ene = (upper + lower) / 2
            upper = upper.round(2)
            ene = ene.round(2)
            lower = lower.round(2)

            if ene[-1] > ene[-2]:
                upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_D, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                             matype=0)
                if doubleLowArray_D[-1] < lowerband[-1] * 1.008:
                    common_image.plt_image_tongyichutu_zhishu(codeItem, value,
                                                              "W",
                                                              "【02国内指数】ENE月线升势，布林日线下穿",
                                                              "【02国内指数】ENE月线升势，布林日线下穿")
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)

#######################################################################################################################
##############################################################################################################主执行程序
strategy('W', 0)
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_03('触发【02国内指数】执行完成', '触发【02国内指数】执行完成')