#encoding=utf-8

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import talib
import tushare as ts
# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
from mpl_finance import candlestick_ohlc
from matplotlib.pylab import date2num
import numpy as num
import time
import os

# 使用ggplot样式，好看些
mpl.style.use("ggplot")
# 获取上证指数数据
data = ts.get_k_data("300203",ktype="W")
# 将date值转换为datetime类型，并且设置成index
data.date = pd.to_datetime(data.date)
data.index = data.date

# 计算MACD指标数据
# data["macd"], data["sigal"], data["hist"] = talib.MACD(data.close)
closeArray = num.array(data['close'])
doubleCloseArray = num.asarray(closeArray, dtype='double')
data["macd"], data["sigal"], data["hist"] = talib.MACD(doubleCloseArray, fastperiod=12, slowperiod=26, signalperiod=9)

# 计算移动平均线
data["ma10"] = talib.MA(data.close, timeperiod=10)
data["ma30"] = talib.MA(data.close, timeperiod=30)

# 计算RSI
data["rsi"] = talib.RSI(data.close)

# 计算移动平均线
data["ma10"] = talib.MA(data.close, timeperiod=10)
data["ma30"] = talib.MA(data.close, timeperiod=30)

# 计算RSI
data["rsi"] = talib.RSI(data.close)

# 绘制第一个图
fig = plt.figure()
fig.set_size_inches((16, 20))

# 左下宽高
ax_canddle = fig.add_axes((0, 0.4, 1, 0.6))
ax_macd = fig.add_axes((0, 0, 1, 0.4))

data_list = []
for date, row in data[["open", "high", "low", "close"]].iterrows():
    t = date2num(date)
    open, high, low, close = row[:]
    datas = (t, open, high, low, close)
    data_list.append(datas)

# 绘制蜡烛图
candlestick_ohlc(ax_canddle, data_list, colorup='r', colordown='green', alpha=0.7, width=0.8)
# 将x轴设置为时间类型
ax_canddle.xaxis_date()
ax_canddle.plot(data.index, data.ma10, label="MA10")
ax_canddle.plot(data.index, data.ma30, label="MA30")
ax_canddle.legend()

# 绘制MACD
print(len(data.index))

ax_macd.plot(data.index, data["macd"], label="macd")
ax_macd.plot(data.index, data["sigal"], label="sigal")
ax_macd.bar(data.index, data["hist"] * 2, label="hist")
ax_macd.legend()

print(data["hist"] * 2)

timeStr1 = time.strftime("%Y%m%d", time.localtime())
path = "./images/" + timeStr1 + "/line"
if not os.path.exists(path):
     os.makedirs(path)

plt.savefig(path + "/" +  timeStr1 + "_5D.png")
plt.close()

