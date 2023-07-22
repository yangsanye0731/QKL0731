import asyncio
import datetime
import json
import time

import numpy as num
import pandas as pd
import talib as ta
from bypy import ByPy
from pyppeteer import launch
import random

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_image
import common_zhibiao
from common_constants import const


#######################################################################################################################
##############################################################################################################保存COOKIE
async def save_cookie(cookie):
    with open("cookie.json", 'w+', encoding="utf-8") as file:
        json.dump(cookie, file, ensure_ascii=False)


#######################################################################################################################
##############################################################################################################读取COOKIE
async def load_cookie():
    with open("cookie.json", 'r', encoding="utf-8") as file:
        cookie = json.load(file)
    return cookie


#######################################################################################################################
################################################################################################################数据解析
async def index(page, cookie1, url, codeName):
    try:
        for cookie in cookie1:
            await page.setCookie(cookie)
        await page.goto(url)
        data_content = await page.xpath('//pre')
        # print(await (await data_content[0].getProperty("textContent")).jsonValue())
        json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
        data_history = pd.DataFrame(json_list.get('data').get('item'),
                                    columns=['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent',
                                             'turnoverrate', 'amount', 'volume_post', 'amount_post'])

        closeArray = num.array(data_history['close'])
        doubleCloseArray = num.asarray(closeArray, dtype='double')

        highArray = num.array(data_history['high'])
        doubleHighArray = num.asarray(highArray, dtype='double')

        openArray = num.array(data_history['open'])
        doubleOpenArray = num.asarray(openArray, dtype='double')

        zhangdiefu = num.array(data_history['percent'])
        huanshoulv = num.array(data_history['turnoverrate'])
        print("==============================================================")
        print(zhangdiefu[-1])
        print(huanshoulv[-1])

        # 均线
        ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
        sma10 = ta.EMA(ma10, timeperiod=10)

        ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
        sma60 = ta.EMA(ma60, timeperiod=60)

        ma144 = ta.SMA(doubleCloseArray, timeperiod=144)
        sma144 = ta.EMA(ma144, timeperiod=144)

        time_str = time.strftime("%Y%m%d", time.localtime())
        if ma10[-1] > sma10[-1] and ma10[-2] < sma10[-2]:
            image_path = common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                                          "D",
                                                                          "【01雪球指数】双均线10交叉",
                                                                          "【01雪球指数】双均线10交叉" + time_str,
                                                                          str(zhangdiefu[-1]),
                                                                          "%.2f" % huanshoulv[-1])

        if ma60[-1] > sma60[-1] and ma60[-2] < sma60[-2]:
            image_path = common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                                          "D",
                                                                          "【01雪球指数】双均线60交叉",
                                                                          "【01雪球指数】双均线60交叉" + time_str,
                                                                          str(zhangdiefu[-1]),
                                                                          "%.2f" % huanshoulv[-1])

        if ma144[-1] > sma144[-1] and ma144[-2] < sma144[-2]:
            image_path = common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                                          "D",
                                                                          "【01雪球指数】双均线60交叉",
                                                                          "【01雪球指数】双均线60交叉" + time_str,
                                                                          str(zhangdiefu[-1]),
                                                                          "%.2f" % huanshoulv[-1])

    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_02("AGU_雪球概念_双均线执行异常", "AGU_雪球概念_双均线执行异常")
        print(e)


#######################################################################################################################
#############################################################################################################数据爬虫入口
async def main(url, codeName):
    print(datetime.datetime.now())
    await asyncio.sleep(30 + random.randint(60, 200))
    print(datetime.datetime.now())
    js1 = '''() =>{
           Object.defineProperties(navigator,{
           webdriver:{
               get: () => false
               }
           })
       }'''

    js2 = '''() => {
           alert (
               window.navigator.webdriver
           )
       }'''

    browser = await launch(headless=True, args=['--no-sandbox'])

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    await page.goto("https://www.xueqiu.com/")
    await page.evaluate(js1)
    # await page.evaluate(js2)
    # print(await page.content())
    cookies2 = await page.cookies()
    await save_cookie(cookies2)
    cookie = await load_cookie()
    await index(page, cookie, url, codeName)
    await browser.close()


#######################################################################################################################
#############################################################################################################遍历雪球概念
count = 0
for key, value in const.XUEQIUGAINIAN:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    print(count)
    curtime = str(int(time.time() * 1000))
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key +
        '&begin=' + curtime + '&period=day&type=before&count=-10000', value))

#######################################################################################################################
################################################################################################################数据同步
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
common.dingding_markdown_msg_02("AGU_雪球概念_双均线执行完成", "AGU_雪球概念_双均线执行完成")
