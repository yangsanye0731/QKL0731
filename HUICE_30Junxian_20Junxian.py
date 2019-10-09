from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import tushare as ts
import datetime
import numpy as num
from email_util import *

class QushiStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 每日收盘线
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        # self.sma5 = bt.indicators.SimpleMovingAverage(self.datas[0], period=5)
        # self.sma10 = bt.indicators.SimpleMovingAverage(self.datas[0], period=10)
        self.sma20 = bt.indicators.SimpleMovingAverage(self.datas[0], period=20)
        self.sma30 = bt.indicators.SimpleMovingAverage(self.datas[0], period=30)
        self.bull = bt.indicators.BollingerBands(self.datas[0])
        self.MACD = bt.indicators.MACDHisto(self.datas[0])

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])
        # self.log('SMA5, %.2f' % self.sma5[0])
        # self.log('SMA10, %.2f' % self.sma10[0])
        # self.log('SMA20, %.2f' % self.sma20[0])
        # self.log('SMA30, %.2f' % self.sma30[0])
        # self.log('BULL TOP, %.2f' % self.bull.top[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            if (self.sma30[0] > self.sma30[-1] and self.datas[0].low < self.bull.bot[0]):
            # if (self.MACD.macd[0] > self.MACD.macd[-1]):
            #     if(self.dataclose[0] > self.sma20[0] and self.datas[0].open < self.sma20[0] and self.dataclose[-1] < self.sma20[-1]):
            #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy(size=10000)
        else:
            if (self.datas[0].close > self.bull.top[0]):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=10000)

if __name__ == '__main__':
    all_code = ts.get_stock_basics()
    all_code_index = all_code[1:-1].index
    count = 0
    success_count = 0
    all_code_index_x = num.array(all_code_index)

    strResult = ""
    for codeItem in all_code_index_x:
        try:
            # 创建回测
            cerebro = bt.Cerebro()
            # 设置交易费用
            cerebro.broker.setcommission(commission=0.001)
            #  添加策略
            cerebro.addstrategy(QushiStrategy)

            # 日线数据
            data_D = ts.get_k_data(codeItem, ktype='30', start="2019-01-01")
            data_D['datetime'] = data_D['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))
            data_D['openInterest'] = 0
            data_D = data_D[["open", "close", "high", "low", "volume", "datetime", "openInterest"]]
            data_D.set_index("datetime", inplace=True)
            add_data_D = bt.feeds.PandasData(dataname=data_D)
            print(add_data_D)

            # 添加数据
            cerebro.adddata(add_data_D)

            # 设置初始账户
            cerebro.broker.setcash(300000.0)

            print(codeItem + '===============================Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
            cerebro.run()
            # cerebro.plot()
            cerebro.runstop()
            count = count + 1
            if (cerebro.broker.getvalue() - 300000 >= 0):
                success_count = success_count + 1
            print(codeItem + '===============================Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        except IndexError as e:
            print(e)

    shenglv = "%.2f" % (success_count/count)
    print(success_count/count)
    sendMail("策略胜率执行完成", "策略胜率执行完成" + shenglv)