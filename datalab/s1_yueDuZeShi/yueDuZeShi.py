import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts
# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


########################################################################################################################
############################################################################################################ 计算日收益率
def get_daily_ret(code='sh', start='2000-01-01', end='2020-10-26'):
    df = ts.get_k_data(code, start=start, end=end)
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
def plot_mean_ret(code, title):
    daily_ret = get_daily_ret(code)
    # 月度收益率
    mnthly_ret = daily_ret.resample('M').apply(lambda x: ((1 + x).prod() - 1))
    mrets = (mnthly_ret.groupby(mnthly_ret.index.month).mean() * 100).round(2)
    attr = [str(i) + '月' for i in range(1, 13)]
    v = list(mrets)

    plt.bar(attr, v, fc='r')
    plt.show()


# plot_mean_ret('sh', '上证综指')
# plot_mean_ret('cyb', '创业板指')
# plot_mean_ret('300322', '硕贝德')
