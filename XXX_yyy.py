import asyncio
from pyppeteer import launch
import datetime
import time
from asyncio import sleep
import json
import pandas as pd
import random
import common
import common_image
from bypy import ByPy
import talib as ta
import numpy as num
from common_constants import const

async def save_cookie(cookie):
    with open("cookie.json", 'w+', encoding="utf-8") as file:
        json.dump(cookie, file, ensure_ascii=False)

# 读取cookie
async def load_cookie():
    with open("cookie.json", 'r', encoding="utf-8") as file:
        cookie = json.load(file)
    return cookie

# 加载首页
async def index(page, cookie1, url, codeName):
    try:
        for cookie in cookie1:
            await page.setCookie(cookie)
        await page.goto(url)
        data_content = await page.xpath('//pre')
        # print(await (await data_content[0].getProperty("textContent")).jsonValue())
        json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
        data_history = pd.DataFrame(json_list.get('data').get('item'), columns=['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'volume_post', 'amount_post'])

        closeArray = num.array(data_history['close'])
        doubleCloseArray = num.asarray(closeArray, dtype='double')

        highArray = num.array(data_history['high'])
        doubleHighArray = num.asarray(highArray, dtype='double')

        openArray = num.array(data_history['open'])
        doubleOpenArray = num.asarray(openArray, dtype='double')

        zhangdiefu = num.array(data_history['percent'])
        huanshoulv  = num.array(data_history['turnoverrate'])
        print("==============================================================")
        print(zhangdiefu[-1])
        print(huanshoulv[-1])
        # 均线
        ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
        print(ma5)

        n = 0
        # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
        if doubleHighArray[n-1] > ma5[n-1] > doubleOpenArray[n-1] and ma5[n-2] < ma5[n-3] and \
                ma5[n-3] < ma5[n-4] and doubleCloseArray[n-1] > doubleOpenArray[n-1]:
            common.dingding_markdown_msg_2('触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')', '触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')')
            common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName, "W", "【01雪球指数】跨越5周线", "【01雪球指数】跨越5周线", str(zhangdiefu[-1]), "%.2f" % huanshoulv[-1])
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_2('触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')报错了 ！！！！！！',
                                       '触发【01雪球指数】跨越5周线' + codeName + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)

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
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    await page.goto("https://www.xueqiu.com/")
    await page.evaluate(js1)
    # await page.evaluate(js2)
    # print(await page.content())
    cookies2 = await page.cookies()
    await save_cookie(cookies2)
    cookie = await load_cookie()
    # 华为海思概念股
    await index(page, cookie, url, codeName)
    await browser.close()

count = 0
for key, value in const.XUEQIUGAINIAN:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    curtime = str(int(time.time()*1000))
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin=' + curtime + '&period=week&type=before&count=-142', value))

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发【01雪球指数】跨越5周线执行完成', '触发【01雪球指数】跨越5周线执行完成')