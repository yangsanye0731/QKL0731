#encoding=utf-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import datetime
import talib
import tushare
import time
import os
import common
import numpy as num
import common_mysqlUtil
import json

def plt_image(code, codeName, type):
    matplotlib.rcParams['font.family'] = 'SimHei'
    ts = tushare.get_k_data(code, ktype = type)
    # ts=ts.get_hist_data("002941",start="2018-08-27",end="2019-08-17")
    ts=ts[["open","close","high","low","volume"]]
    #print(ts)

    # 画5日均线图
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(8,4))
    plt.plot(avg_5,color="r")
    plt.plot(avg_10,color="y")
    plt.plot(avg_20,color="g")
    plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    if (type == "W"):
        plt.title(codeName + '周线均线')
    plt.xlabel('Date')
    plt.ylabel('Price')
    #设置坐标轴范围

    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "_" + type
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" +  code + "_" + codeName + "_" + timeStr2 + "qushi.png")
    plt.show()

# 跨越5周线图
def plt_image_kuaYueWeek5Line(code, codeName, type, eps, yoy, turnover_rate, industry):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "W"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：跨越5周线，5周线前2期下降', fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code)  + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)
    if (changdu > 200):
        plt.xlim(100, changdu)
    if (changdu > 300):
        plt.xlim(200, changdu)
    if (changdu > 400):
        plt.xlim(300, changdu)
    if (changdu > 500):
        plt.xlim(400, changdu)
    if (changdu > 600):
        plt.xlim(500, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/kuaYueWeek5Line"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

# 周ENE中线趋势
def plt_image_ENEWEEK(code, codeName, type, eps, yoy, turnover_rate, industry):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "W"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：ENE周线向上', fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code)  + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)
    if (changdu > 200):
        plt.xlim(100, changdu)
    if (changdu > 300):
        plt.xlim(200, changdu)
    if (changdu > 400):
        plt.xlim(300, changdu)
    if (changdu > 500):
        plt.xlim(400, changdu)
    if (changdu > 600):
        plt.xlim(500, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/ENEWEEK"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

# 周孕线
def plt_image_YUNXIANWEEK(code, codeName, type, eps, yoy, turnover_rate, industry):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "W"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：周孕线', fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code)  + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)
    if (changdu > 200):
        plt.xlim(100, changdu)
    if (changdu > 300):
        plt.xlim(200, changdu)
    if (changdu > 400):
        plt.xlim(300, changdu)
    if (changdu > 500):
        plt.xlim(400, changdu)
    if (changdu > 600):
        plt.xlim(500, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/YUNXIANWEEK"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

# 日孕线
def plt_image_YUNXIANDAY(code, codeName, type, eps, yoy, turnover_rate, industry):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "D"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：日孕线', fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code) + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)
    # if (changdu > 300):
    #     plt.xlim(200, changdu)
    # if (changdu > 400):
    #     plt.xlim(300, changdu)
    # if (changdu > 500):
    #     plt.xlim(400, changdu)
    # if (changdu > 600):
    #     plt.xlim(500, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/YUNXIANDAY"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()







# 统一出图
def plt_image_tongyichutu(code, type, pathType, guizeMingcheng):
    eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(code)
    if epsup < 0 or yingyeup < 0:
        return

    codeName, industry = common.codeName_and_industry(code)
    eps = "%.1f" % epsup
    yoy = "%.1f" % yingyeup

    df = common.daily_basic(code)
    # 判断DataFrame是否为空
    turnover_rate = 0.0
    if df.empty:
        print("empty")
    else:
        turnover_rate = num.array(df['turnover_rate'])
    turnover_rate = "%.2f" % turnover_rate

    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code) + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

# 统一出图
def plt_image_tongyichutu_2(code, type, pathType, guizeMingcheng):
    # eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(code)
    eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = 0,0,0,0,0,0
    re = ""
    codeName = ''
    data = common_mysqlUtil.select_all_code_one(code)
    if len(data) > 0:
        plate = data[0][2]
        codeName = data[0][1]
        print(plate)
        if (len(plate) > 0):
            json_list = json.loads(plate)
            items = json_list.items()
            count = 1
            re = "\n"
            for key, value in items:
                if count % 5 == 0:
                    re = re + "   " + str(value.get('plate_name')) + "\n"
                else:
                    re = re + "   " + str(value.get('plate_name'))
                count = count + 1

    eps = "%.1f" % epsup
    yoy = "%.1f" % yingyeup

    # df = common.daily_basic(code)
    # # 判断DataFrame是否为空
    # turnover_rate = 0.0
    # if df.empty:
    #     print("empty")
    # else:
    #     turnover_rate = num.array(df['turnover_rate'])
    # turnover_rate = "%.2f" % turnover_rate

    turnover_rate = "0"

    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,13))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%" + re,
                  fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code), fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

    image_path = path + "/" + timeStr1 + "_" + codeName + ".png"
    return image_path



# 统一出图
def plt_image_tongyichutu_3(code, type, pathType, guizeMingcheng):
    eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(code)

    eps = "%.1f" % epsup
    yoy = "%.1f" % yingyeup

    df = common.daily_basic(code)
    # 判断DataFrame是否为空
    turnover_rate = 0.0
    if df.empty:
        print("empty")
    else:
        turnover_rate = num.array(df['turnover_rate'])
    turnover_rate = "%.2f" % turnover_rate

    re = ""
    codeName = ''
    data = common_mysqlUtil.select_all_code_one(code)
    if len(data) > 0:
        plate = data[0][2]
        codeName = data[0][1]
        print(plate)
        if (len(plate) > 0):
            json_list = json.loads(plate)
            items = json_list.items()
            count = 1
            re = "\n"
            for key, value in items:
                if count % 5 == 0:
                    re = re + "   " + str(value.get('plate_name')) + "\n"
                else:
                    re = re + "   " + str(value.get('plate_name'))
                count = count + 1


    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,13))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%" + re,
                  fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code), fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

    image_path = path + "/" + timeStr1 + "_" + codeName + ".png"
    return image_path




# 统一出图
def plt_image_tongyichutu_wueps(code, type, pathType, guizeMingcheng):
    eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = 0,0,0,0,0,0


    codeName, industry = "", ""
    eps = "%.1f" % epsup
    yoy = "%.1f" % yingyeup

    turnover_rate = ""

    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%,换手率：" + turnover_rate + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code) + ", " + industry, fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + code + ".png")
    plt.close()


def plt_image_tongyichutu_zhishu(code, codeName, type, pathType, guizeMingcheng):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype=type)
    ts = ts[["open", "close", "high", "low", "volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig = plt.subplots(figsize=(15, 12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10, color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    # 设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(
        timeStr1 + "_" + codeName + '(' + code + ')EPS:' + "" + "%,营业额：" + "" + "%,换手率：" + "" + "%",
        fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)
    plt.ylabel('价格 ' + common.zhangdiefu(code) + ", " + "", fontproperties=myfont)

    # 设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(changdu - 100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()

def plt_image_tongyichutu_zhishu_xueqiu(doubleCloseArray, code, codeName, type, pathType, guizeMingcheng, zhangdiefu, huanshoulv):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    # 画5日均线图
    avg_1 = talib.MA(doubleCloseArray, timeperiod=1)
    avg_5 = talib.MA(doubleCloseArray, timeperiod=5)
    avg_10 = talib.MA(doubleCloseArray, timeperiod=10)
    avg_20 = talib.MA(doubleCloseArray, timeperiod=20)
    avg_30 = talib.MA(doubleCloseArray, timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig = plt.subplots(figsize=(15, 12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10, color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    # 设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    plt.title(
        timeStr1 + "_" + codeName + '(' + code + ')' + ",换手率：" + huanshoulv + "%",
        fontproperties=myfont)
    plt.xlabel('日期，规则：' + guizeMingcheng, fontproperties=myfont)

    # zhangdiefu = "%.2f" % (((doubleCloseArray[-1] - doubleCloseArray[-2]) / doubleCloseArray[-2]) * 100) + '%'
    plt.ylabel('价格:' + zhangdiefu, fontproperties=myfont)

    # 设置坐标轴范围
    changdu = len(doubleCloseArray)
    if (changdu > 200):
        plt.xlim(changdu - 100, changdu)

    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/" + pathType
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + ".png")
    plt.close()
    image_path = path + "/" + timeStr1 + "_" + codeName + ".png"
    return image_path









# 30日线上升
def plt_image_30DayLineUp(code, codeName, type, eps, yoy):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    # avg_5 = talib.MA(ts["close"], timeperiod=5)
    # avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_20, "k.-")
    plt.plot(avg_30,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "D"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%",
                  fontproperties=myfont)
    plt.xlabel('日期，规则：30日线上升，30日线线前2期下降', fontproperties=myfont)
    plt.ylabel('价格 '+ common.zhangdiefu(code), fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)
    if (changdu > 200):
        plt.xlim(changdu-100, changdu)

    path = "./images/" + timeStr1 + "/30DayLineUp"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + "30D.png")
    plt.close()

# 5周线图
def plt_image_week5Line(code, codeName, type, eps, yoy):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]
    #print(ts)

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "W"):
        plt.title(timeStr1 + "_" + codeName + '(' + code + ')EPS:' + eps + "%,营业额：" + yoy + "%", fontproperties=myfont)
    plt.xlabel('日期，规则：EPS大于20，价格在5周线以下', fontproperties=myfont)
    plt.ylabel('价格 ' + common.zhangdiefu(code), fontproperties=myfont)
    #设置坐标轴范围
    changdu = len(ts)
    if (changdu > 200):
        plt.xlim(100, changdu)
    if (changdu > 300):
        plt.xlim(200, changdu)
    if (changdu > 400):
        plt.xlim(300, changdu)
    if (changdu > 500):
        plt.xlim(400, changdu)
    if (changdu > 600):
        plt.xlim(500, changdu)

    path = "./images/" + timeStr1 + "/week5Line"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" + timeStr1 + "_" + codeName + "5W.png")
    plt.close()

# 百日新高绘图
def plt_image_baiRiXinGao(xinGaoGeShu, zhiShuShuJu, riQi):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc")

    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(111)
    ax.plot(riQi, zhiShuShuJu, 'rs-', )
    ax2 = ax.twinx()
    ax2.plot(riQi, xinGaoGeShu, 'b.-')

    ax.legend(loc=0)
    ax.grid()
    ax.set_xlabel("日期（周）", fontproperties=myfont)
    ax.set_ylabel("创业板指", fontproperties=myfont)
    ax2.set_ylabel("个数", fontproperties=myfont)
    ax2.set_ylim(-10, 3500)
    ax.set_ylim(1000, 2000)
    ax2.legend(loc=0)

    for xtick in ax.get_xticklabels():
        xtick.set_rotation(90)

    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/baiRiXinGao"
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(path + "/" + timeStr2 + "qushi.png")

# 5周线连续下降
def plt_image_lianXuXiaJiangWeek5Line(code, codeName, type, eps, yoy):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")
    ts = tushare.get_k_data(code, ktype = type)
    ts=ts[["open","close","high","low","volume"]]

    # 画5日均线图
    avg_1 = talib.MA(ts["close"], timeperiod=1)
    avg_5 = talib.MA(ts["close"], timeperiod=5)
    avg_10 = talib.MA(ts["close"], timeperiod=10)
    avg_20 = talib.MA(ts["close"], timeperiod=20)
    avg_30 = talib.MA(ts["close"], timeperiod=30)
    # print(avg_5)
    # print(avg_10)
    # print(avg_20)
    # print(avg_30)

    fig=plt.subplots(figsize=(15,12))
    plt.plot(avg_1, "b.-")
    plt.plot(avg_5, "k.-")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    if (type == "W"):
        plt.title(timeStr1 + "_" + codeName + '(' + code  + ')EPS:' + eps + "%,营业额：" + yoy + "%", fontproperties=myfont)
    plt.xlabel('日期，规则：5周线连续下降', fontproperties=myfont)
    plt.ylabel('价格 ' + common.zhangdiefu(code), fontproperties=myfont)

    #设置坐标轴范围
    changdu = len(ts)
    print(changdu)

    if (changdu > 200):
        plt.xlim(100, changdu)
    if (changdu > 300):
        plt.xlim(200, changdu)
    if (changdu > 400):
        plt.xlim(300, changdu)
    if (changdu > 500):
        plt.xlim(400, changdu)
    if (changdu > 600):
        plt.xlim(500, changdu)

    path = "./images/" + timeStr1 + "/lianXuXiaJiangWeek5Line"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" +  timeStr1 + "_" + codeName + "5D.png")
    plt.close()

import pandas as pd
def KDJ_zhibiao(data_history, doubleCloseArray):
    stock_data = {}
    low_list = data_history.low.rolling(9).min()
    low_list.fillna(value=data_history.low.expanding().min(), inplace=True)
    high_list = data_history.high.rolling(9).max()
    high_list.fillna(value=data_history.high.expanding().max(), inplace=True)
    rsv = (doubleCloseArray - low_list) / (high_list - low_list) * 100
    stock_data['KDJ_K'] = pd.DataFrame.ewm(rsv, com=2).mean()
    stock_data['KDJ_D'] = pd.DataFrame.ewm(stock_data['KDJ_K'], com=2).mean()
    stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
    dddd = pd.DataFrame(stock_data)
    return dddd


# 个股指标
def plt_image_geGuZhiBiao(code, fullName):
    codeName = fullName + "(" + code + ")"
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc", size="25")

    fig = plt.figure(figsize=(15,10))
    # fig.suptitle(codeName, fontproperties=myfont_title)
    # 1*1 的第一个图表
    ax_macd_60 = fig.add_subplot(331)
    ax_macd_d = fig.add_subplot(332)
    ax_macd = fig.add_subplot(333)
    ax_bull_60 = fig.add_subplot(334)
    ax_bull_d = fig.add_subplot(335)
    ax_bull = fig.add_subplot(336)
    ax_kdj_60 = fig.add_subplot(337)
    ax_kdj_d = fig.add_subplot(338)
    ax_kdj = fig.add_subplot(339)

    data_60 = tushare.get_k_data(code, ktype="60")
    ts_60 = data_60[["open", "close", "high", "low", "volume"]]
    closeArray_60 = num.array(data_60['close'])
    doubleCloseArray_60 = num.asarray(closeArray_60, dtype='double')

    data_d = tushare.get_k_data(code, ktype="D")
    ts_d = data_d[["open", "close", "high", "low", "volume"]]
    closeArray_d = num.array(data_d['close'])
    doubleCloseArray_d = num.asarray(closeArray_d, dtype='double')

    data = tushare.get_k_data(code, ktype="W")
    ts = data[["open", "close", "high", "low", "volume"]]
    closeArray = num.array(data['close'])
    doubleCloseArray = num.asarray(closeArray, dtype='double')

    kdj_60 = KDJ_zhibiao(data_60, closeArray_60)
    kdj_d = KDJ_zhibiao(data_d, closeArray_d)
    kdj = KDJ_zhibiao(data, closeArray)

    # 计算MACD指标数据
    data_60["macd"], data_60["sigal"], data_60["hist"] = talib.MACD(ts_60['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    ax_macd_60.plot(data_60.index, data_60["macd"], label="macd")
    ax_macd_60.plot(data_60.index, data_60["sigal"], label="sigal")
    ax_macd_60.bar(data_60.index, data_60["hist"] * 2, label="hist")
    ax_macd_60.set_xlabel( "60MACD买入卖出量与力道", fontproperties=myfont)
    ax_macd_60.set_ylabel(codeName + "涨跌幅：" + common.zhangdiefu(code), fontproperties=myfont)

    changdu = len(ts_60)
    if (changdu > 200):
        ax_macd_60.set_xlim(100, changdu)
    if (changdu > 300):
        ax_macd_60.set_xlim(200, changdu)
    if (changdu > 400):
        ax_macd_60.set_xlim(300, changdu)
    if (changdu > 500):
        ax_macd_60.set_xlim(400, changdu)
    if (changdu > 600):
        ax_macd_60.set_xlim(500, changdu)



    # 计算MACD指标数据
    data_d["macd"], data_d["sigal"], data_d["hist"] = talib.MACD(ts_d['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    ax_macd_d.plot(data_d.index, data_d["macd"], label="macd")
    ax_macd_d.plot(data_d.index, data_d["sigal"], label="sigal")
    ax_macd_d.bar(data_d.index, data_d["hist"] * 2, label="hist")
    ax_macd_d.set_xlabel("MACD（日线）", fontproperties=myfont)

    changdu = len(ts_d)
    if (changdu > 200):
        ax_macd_d.set_xlim(100, changdu)
    if (changdu > 300):
        ax_macd_d.set_xlim(200, changdu)
    if (changdu > 400):
        ax_macd_d.set_xlim(300, changdu)
    if (changdu > 500):
        ax_macd_d.set_xlim(400, changdu)
    if (changdu > 600):
        ax_macd_d.set_xlim(500, changdu)




    # 计算MACD指标数据
    data["macd"], data["sigal"], data["hist"] = talib.MACD(ts['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.plot(data.index, data["sigal"], label="sigal")
    ax_macd.bar(data.index, data["hist"] * 2, label="hist")
    ax_macd.set_xlabel("MACD（周线）", fontproperties=myfont)

    changdu = len(ts)
    if (changdu > 200):
        ax_macd.set_xlim(100, changdu)
    if (changdu > 300):
        ax_macd.set_xlim(200, changdu)
    if (changdu > 400):
        ax_macd.set_xlim(300, changdu)
    if (changdu > 500):
        ax_macd.set_xlim(400, changdu)
    if (changdu > 600):
        ax_macd.set_xlim(500, changdu)






    data_60['upperband'], data_60['middleband'], data_60['lowerband'] = talib.BBANDS(ts_60['close'], timeperiod=20, nbdevup=2,
                                                                            nbdevdn=2,
                                                                            matype=0)
    ax_bull_60.plot(data_60.index, data_60["upperband"], label="UP")
    ax_bull_60.plot(data_60.index, data_60["middleband"], label="MID")
    ax_bull_60.plot(data_60.index, data_60["lowerband"], label="LOW")
    ax_bull_60.plot(data_60.index, data_60["low"], "b.-", label="Line")

    ax_bull_60.set_xlabel("布林（60）", fontproperties=myfont)
    ax_bull_60.set_ylabel("BULL", fontproperties=myfont)

    changdu = len(ts_60)
    if (changdu > 200):
        ax_bull_60.set_xlim(100, changdu)
    if (changdu > 300):
        ax_bull_60.set_xlim(200, changdu)
    if (changdu > 400):
        ax_bull_60.set_xlim(300, changdu)
    if (changdu > 500):
        ax_bull_60.set_xlim(400, changdu)
    if (changdu > 600):
        ax_bull_60.set_xlim(500, changdu)


    data_d['upperband'], data_d['middleband'], data_d['lowerband'] = talib.BBANDS(ts_d['close'], timeperiod=20, nbdevup=2,
                                                                            nbdevdn=2,
                                                                            matype=0)
    ax_bull_d.plot(data_d.index, data_d["upperband"], label="UP")
    ax_bull_d.plot(data_d.index, data_d["middleband"], label="MID")
    ax_bull_d.plot(data_d.index, data_d["lowerband"], label="LOW")
    ax_bull_d.plot(data_d.index, data_d["low"], "b.-", label="Line")
    ax_bull_d.set_xlabel("布林（日）", fontproperties=myfont)

    changdu = len(ts_d)
    if (changdu > 200):
        ax_bull_d.set_xlim(100, changdu)
    if (changdu > 300):
        ax_bull_d.set_xlim(200, changdu)
    if (changdu > 400):
        ax_bull_d.set_xlim(300, changdu)
    if (changdu > 500):
        ax_bull_d.set_xlim(400, changdu)
    if (changdu > 600):
        ax_bull_d.set_xlim(500, changdu)



    data['upperband'], data['middleband'],data['lowerband']  = talib.BBANDS(ts['close'], timeperiod=20, nbdevup=2, nbdevdn=2,
                                                          matype=0)
    ax_bull.plot(data.index, data["upperband"], label="UP")
    ax_bull.plot(data.index, data["middleband"], label="MID")
    ax_bull.plot(data.index, data["lowerband"], label="LOW")
    ax_bull.plot(data.index, data["low"], "b.-" , label="Line")
    ax_bull.set_xlabel("布林（周）", fontproperties=myfont)

    changdu = len(ts)
    if (changdu > 200):
        ax_bull.set_xlim(100, changdu)
    if (changdu > 300):
        ax_bull.set_xlim(200, changdu)
    if (changdu > 400):
        ax_bull.set_xlim(300, changdu)
    if (changdu > 500):
        ax_bull.set_xlim(400, changdu)
    if (changdu > 600):
        ax_bull.set_xlim(500, changdu)



    # ax_kdj_60.plot(kdj_60.index, kdj_60["KDJ_K"], label="K")
    ax_kdj_60.plot(kdj_60.index, kdj_60["KDJ_D"], label="D")
    ax_kdj_60.plot(kdj_60.index, kdj_60["KDJ_J"], label="J")

    ax_kdj_60.set_xlabel("KDJ（60）", fontproperties=myfont)
    ax_kdj_60.set_ylabel("KDJ", fontproperties=myfont)

    changdu = len(ts_60)
    if (changdu > 200):
        ax_kdj_60.set_xlim(100, changdu)
    if (changdu > 300):
        ax_kdj_60.set_xlim(200, changdu)
    if (changdu > 400):
        ax_kdj_60.set_xlim(300, changdu)
    if (changdu > 500):
        ax_kdj_60.set_xlim(400, changdu)
    if (changdu > 600):
        ax_kdj_60.set_xlim(500, changdu)

    ax_kdj_d.plot(kdj_d.index, kdj_d["KDJ_D"], label="D")
    ax_kdj_d.plot(kdj_d.index, kdj_d["KDJ_J"], label="J")

    ax_kdj_d.set_xlabel("KDJ（日）", fontproperties=myfont)

    changdu = len(ts_d)
    if (changdu > 200):
        ax_kdj_d.set_xlim(100, changdu)
    if (changdu > 300):
        ax_kdj_d.set_xlim(200, changdu)
    if (changdu > 400):
        ax_kdj_d.set_xlim(300, changdu)
    if (changdu > 500):
        ax_kdj_d.set_xlim(400, changdu)
    if (changdu > 600):
        ax_kdj_d.set_xlim(500, changdu)

    ax_kdj.plot(kdj.index, kdj["KDJ_D"], label="D")
    ax_kdj.plot(kdj.index, kdj["KDJ_J"], label="J")

    ax_kdj.set_xlabel("KDJ（周）", fontproperties=myfont)

    changdu = len(ts)
    if (changdu > 200):
        ax_kdj.set_xlim(100, changdu)
    if (changdu > 300):
        ax_kdj.set_xlim(200, changdu)
    if (changdu > 400):
        ax_kdj.set_xlim(300, changdu)
    if (changdu > 500):
        ax_kdj.set_xlim(400, changdu)
    if (changdu > 600):
        ax_kdj.set_xlim(500, changdu)


    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/geGuZhiBiao"
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(path + "/" + timeStr1 + "_" + code + ".png")
    plt.close()
    image_path = path + "/" + timeStr1 + "_" + code + ".png"
    return image_path

# plt_image_geGuZhiBiao("399006","创业板指")