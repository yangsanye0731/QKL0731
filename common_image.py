#encoding=utf-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib.pylab import date2num
import datetime
import talib
import tushare
import time
import os


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
    print(avg_5)
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

# 5周线图
def plt_image_week5Line(code, codeName, type, eps, yoy):
    myfont = matplotlib.font_manager.FontProperties(fname="/root/software/QKL/simsun.ttc")
    ts = tushare.get_k_data(code, ktype = type)
    # ts=ts.get_hist_data("002941",start="2018-08-27",end="2019-08-17")
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
    plt.plot(avg_5,color="r")
    plt.plot(avg_10,color="y")
    # plt.plot(avg_20,color="g")
    # plt.plot(avg_30,color="b")
    plt.xticks(rotation=75)
    #设置坐标轴名称
    if (type == "W"):
        plt.title(codeName + '(' + code  + ')周线均线,EPS:' + eps + ",营业额：" + yoy, fontproperties=myfont)
    plt.xlabel('日期', fontproperties=myfont)
    plt.ylabel('价格', fontproperties=myfont)
    #设置坐标轴范围

    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    timeStr2 = time.strftime("%m%d%H%M", time.localtime())
    path = "./images/" + timeStr1 + "/week5Line"
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + "/" +  code + "_" + codeName + "_" + timeStr2 + "qushi.png")

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

# plt_image("399006", "创业板指", "30")