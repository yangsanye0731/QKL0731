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
        ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
        print(ma5)

        n = 0
        # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
        time_str = time.strftime("%Y%m%d", time.localtime())
        if doubleHighArray[n - 1] > ma5[n - 1] > doubleOpenArray[n - 1] and ma5[n - 2] < ma5[n - 3] < ma5[n - 4] \
                and doubleCloseArray[n - 1] > doubleOpenArray[n - 1]:
            image_path = common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                                          "W",
                                                                          "【01雪球指数】跨越5周线",
                                                                          "【01雪球指数】跨越5周线" + time_str,
                                                                          str(zhangdiefu[-1]),
                                                                          "%.2f" % huanshoulv[-1])
            image_url = "http://47.240.11.144/" + image_path[6:]
            common.dingding_markdown_msg_02('触发【01雪球指数】跨越5周线' + time_str + codeName + '(' + codeItem + ')',
                                            '触发【01雪球指数】跨越5周线' + time_str + codeName + '(' + codeItem + ')'
                                            + "\n\n> ![screenshot](" + image_url + ")")

        param_m1 = 11
        param_m2 = 9
        param_n = 10
        sma_n = ta.SMA(doubleCloseArray, param_n)
        upper = (1 + param_m1 / 100) * sma_n
        lower = (1 - param_m2 / 100) * sma_n
        ene = (upper + lower) / 2
        # upper = upper.round(2)
        ene = ene.round(2)
        # lower = lower.round(2)

        if doubleCloseArray[-1] < ene[-1]:
            # common.dingding_markdown_msg_2('触发【01雪球指数】当前价格在ENE周线中线下方' + codeName + '(' + codeItem + ')',
            #                                '触发【01雪球指数】当前价格在ENE周线中线下方' + codeName + '(' + codeItem + ')')
            common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                             "W",
                                                             "【01雪球指数】ENE周中线下方",
                                                             "【01雪球指数】ENE周中线下方", str(zhangdiefu[-1]),
                                                             "%.2f" % huanshoulv[-1])
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_02('触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')报错了 ！！！！！！',
                                        '触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)


#######################################################################################################################
#############################################################################################################数据爬虫入口
async def main(url, codeName):
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
    curtime = str(int(time.time() * 1000))
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key +
        '&begin=' + curtime + '&period=week&type=before&count=-142', value))

#######################################################################################################################
################################################################################################################数据同步
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_02('触发【01雪球指数】' + timeStr1 + '跨越5周线执行完成',
                                '触发【01雪球指数】' + timeStr1 + '跨越5周线执行完成')
