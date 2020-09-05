import asyncio
import datetime
import json
import time

import numpy as num
import pandas as pd
import talib as ta
from bypy import ByPy
from pyppeteer import launch

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os
project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_image
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
async def index(page, cookie1, url, codeName, codeItem):
    result = 0
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

        lowArray = num.array(data_history['low'])
        # doubleLowArray = num.asarray(lowArray, dtype='double')

        param_m1 = 11
        param_m2 = 9
        param_n = 10
        sma_n = ta.SMA(doubleCloseArray, param_n)
        upper = (1 + param_m1 / 100) * sma_n
        lower = (1 - param_m2 / 100) * sma_n
        ene = (upper + lower) / 2
        upper = upper.round(2)
        ene = ene.round(2)
        lower = lower.round(2)

        if ene[-1] > ene[-2]:
            result = 1
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_2('触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！',
                                       '触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)

    return result

#######################################################################################################################
################################################################################################################数据解析
async def index2(page, cookie1, url, codeName, codeItem):
    result = 0
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

        lowArray = num.array(data_history['low'])
        doubleLowArray = num.asarray(lowArray, dtype='double')

        zhangdiefu = num.array(data_history['percent'])
        huanshoulv = num.array(data_history['turnoverrate'])

        upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                     matype=0)

        if lowArray[-1] < lowerband[-1] * 1.008:
            result = 1
            common.dingding_markdown_msg_link('触发【01雪球指数】ENE月线升势，布林日线下穿'
                                              + codeName + '(' + codeItem + ')',
                                              '触发【01雪球指数】ENE月线升势，布林日线下穿'
                                              + codeName + '(' + codeItem + ')',
                                              "https://xueqiu.com/S/" + codeItem)
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_2('触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！',
                                       '触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)

    return result

#######################################################################################################################
################################################################################################################数据解析
async def index3(page, cookie1, url, codeName, codeItem):
    result = 0
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

        lowArray = num.array(data_history['low'])
        doubleLowArray = num.asarray(lowArray, dtype='double')

        zhangdiefu = num.array(data_history['percent'])
        huanshoulv = num.array(data_history['turnoverrate'])

        print(data_history)
        common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                         "W",
                                                         "【01雪球指数】ENE月线升势，布林日线下穿",
                                                         "【01雪球指数】ENE月线升势，布林日线下穿",
                                                         str(zhangdiefu[-1]),
                                                         "%.2f" % huanshoulv[-1])

    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_2('触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！',
                                       '触发【01雪球指数】ENE月线升势，布林日线下穿' + codeName
                                       + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)

#######################################################################################################################
#############################################################################################################数据爬虫入口
async def main(url1, url2, url3, codeName, codeItem):
    print(datetime.datetime.now())
    # await asyncio.sleep(10 + random.randint(1, 10))
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
    ###################################################################################################################
    ############################################################################################################精华逻辑
    result = await index(page, cookie, url1, codeName, codeItem)
    if result == 1:
        result2 = await index2(page, cookie, url2, codeName, codeItem)
        print(result2)
        if result2 == 1:
            await index3(page, cookie, url3, codeName, codeItem)
            print("===========================================================================================")
    await browser.close()
    return result

#######################################################################################################################
#############################################################################################################遍历雪球概念
count = 0
for key, value in const.XUEQIUGAINIAN:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    curtime = str(int(time.time()*1000))
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin='
        + curtime + '&period=month&type=before&count=-142',
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin='
        + curtime + '&period=day&type=before&count=-142',
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin='
        + curtime + '&period=week&type=before&count=-142',
        value, codeItem))

#######################################################################################################################
################################################################################################################数据同步
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【01雪球指数】ENE月线升势，布林日线下穿执行完成',
                               '触发【01雪球指数】ENE月线升势，布林日线下穿执行完成')