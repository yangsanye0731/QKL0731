import matplotlib.patches as mpatches
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts
# 正常显示画图时出现的中文和负号
from pylab import mpl
import time
import numpy as num
import common_image
import common
from bypy import ByPy

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)


########################################################################################################################
############################################################################################################ 计算日收益率
def get_daily_ret(code='sh', start='2000-01-01'):
    df = ts.get_k_data(code, start=start)
    df.index = pd.to_datetime(df.date)
    # 计算日收益率
    daily_ret = df['close'].pct_change()
    # 删除缺失值
    daily_ret.dropna(inplace=True)
    # print(daily_ret)
    return daily_ret


########################################################################################################################
########################################################################################################## 计算月度收益率
def plot_mnthly_ret(code, title):
    daily_ret = get_daily_ret(code)
    # 月度收益率
    mnthly_ret = daily_ret.resample('M').apply(lambda x: ((1 + x).prod() - 1))
    # print(mnthly_ret)
    # 可视化
    plt.rcParams['figure.figsize'] = [20, 5]
    mnthly_ret.plot()
    start_date = mnthly_ret.index[0]
    end_date = mnthly_ret.index[-1]
    plt.xticks(pd.date_range(start_date, end_date, freq='Y'),
               [str(y) for y in range(start_date.year + 1, end_date.year + 1)])
    # 显示月收益率大于3/4分位数的点
    dates = mnthly_ret[mnthly_ret > mnthly_ret.quantile(0.75)].index
    for i in range(0, len(dates)):
        plt.scatter(dates[i], mnthly_ret[dates[i]], color='r')
    labs = mpatches.Patch(color='red', alpha=.5, label="月收益率高于3/4分位")
    plt.title(title + '月度收益率', size=15)
    plt.legend(handles=[labs])
    plt.show()


def plot_votil(code, title):
    # 月度收益率的年化标准差（波动率）
    daily_ret = get_daily_ret(code)
    mnthly_annu = daily_ret.resample('M').std() * np.sqrt(12)
    plt.rcParams['figure.figsize'] = [20, 5]
    mnthly_annu.plot()
    start_date = mnthly_annu.index[0]
    end_date = mnthly_annu.index[-1]
    plt.xticks(pd.date_range(start_date, end_date, freq='Y'),
               [str(y) for y in range(start_date.year + 1, end_date.year + 1)])
    dates = mnthly_annu[mnthly_annu > 0.07].index
    for i in range(0, len(dates) - 1, 3):
        plt.axvspan(dates[i], dates[i + 1], color='r', alpha=.5)
    plt.title(title + '月度收益率标准差', size=15)
    labs = mpatches.Patch(color='red', alpha=.5, label="波动集聚")
    plt.legend(handles=[labs])
    plt.show()


########################################################################################################################
##################################################################################################### 计算月度收益率平均值
# pyecharts是0.5.11版本
def plot_mean_ret(code):
    daily_ret = get_daily_ret(code)
    # 月度收益率
    mnthly_ret = daily_ret.resample('M').apply(lambda x: ((1 + x).prod() - 1))
    mrets = (mnthly_ret.groupby(mnthly_ret.index.month).mean() * 100).round(2)
    attr = [str(i) + 'M' for i in range(1, 13)]
    v = list(mrets)

    jsonDic[code] = v[0]
    print(code)
    print(v)
    print(v[0])


    # plt.bar(attr, v, fc='r')

    # timeStr1 = time.strftime("%Y%m%d", time.localtime())
    # path = rootPath + os.sep + "images" + os.sep + timeStr1 + os.sep + '月度择时策略'
    # if not os.path.exists(path):
    #     os.makedirs(path)
    #
    # suiji_str = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 5))
    # plt.savefig(path + os.sep + timeStr1 + "_" + code + suiji_str + ".png")
    # plt.close()
    # image_path = path + os.sep + timeStr1 + "_" + code + suiji_str + ".png"
    # return image_path

jsonDic = {}
def strategy():
    # 局部变量初始化
    count = 0
    count_b = 0
    count_e = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # all_code = ts.get_stock_basics()
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)

    # 遍历
    for codeItem in all_code_index_x:
        codeItem = codeItem[0:6]
        print(codeItem)
        plot_mean_ret(codeItem)

strategy()
jsonDic1 = sorted(jsonDic.items(), key=lambda item: item[1], reverse=True)
print(jsonDic1)

count = 1
for key, value in jsonDic1:
    if count <= 100:
        print(key)
        print(value)
        common_image.plt_image_tongyichutu_2(key,
                                             "W",
                                             "【03全部代码】1月前20增长",
                                             "【03全部代码】1月前20增长，排名为：第" + str(count) + "位")

    count = count + 1

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)