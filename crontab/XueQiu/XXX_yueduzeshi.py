import asyncio
import datetime
import json
import time
import matplotlib

import numpy as num
import pandas as pd
from bypy import ByPy
from pyppeteer import launch
import random
import matplotlib.pyplot as plt

jsonDic = {}

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

matplotlib.use('Agg')


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
################################################################################################################月度择时
def plot_mean_ret(codeName, daily_ret):
    # 月度收益率
    mnthly_ret = daily_ret.resample('M').apply(lambda x: ((1 + x).prod() - 1))
    mrets = (mnthly_ret.groupby(mnthly_ret.index.month).mean() * 100).round(2)
    attr = [str(i) + 'M' for i in range(1, 13)]
    v = list(mrets)
    print(v)

    for i in range(v.__len__()):
        if v[i] > 5 and daily_ret.size > 500:
            if jsonDic.get("M" + str(i + 1)) is None:
                jsonDic["M" + str(i + 1)] = codeName
            else:
                jsonDic["M" + str(i + 1)] = jsonDic.get("M" + str(i + 1)) + "," + codeName

    myfont = matplotlib.font_manager.FontProperties(fname=rootPath + os.sep + "simsun.ttc", size="14")
    plt.bar(attr, v, fc='r')
    plt.title("雪球概念:" + codeName + "月度择时，统计数量：" + str(daily_ret.size), fontproperties=myfont)

    timeStr1 = time.strftime("%Y%m%d", time.localtime())
    path = rootPath + os.sep + "images" + os.sep + timeStr1 + os.sep + '雪球月度择时策略'
    if not os.path.exists(path):
        os.makedirs(path)

    suiji_str = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 5))
    plt.savefig(path + os.sep + timeStr1 + "_" + codeName + suiji_str + ".png")
    plt.close()
    image_path = path + os.sep + timeStr1 + "_" + codeName + suiji_str + ".png"
    return image_path


#######################################################################################################################
################################################################################################################数据解析
async def index(page, cookie1, url, codename):
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
        # print(data_history)
        # data_history['timestamp'] = data_history['timestamp'].apply(pd.to_datetime)
        # print(data_history['timestamp'])
        data_history.index = pd.to_datetime(data_history['timestamp'], unit='ms')
        daily_ret = data_history['close'].pct_change()

        # 删除缺失值
        daily_ret.dropna(inplace=True)
        # print(daily_ret)
        plot_mean_ret(codename, daily_ret)

    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_02('触发【01雪球指数】月度择时' + codename + '(' + codeItem + ')报错了 ！！！！！！',
                                        '触发【01雪球指数】月度择时' + codename + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)


#######################################################################################################################
#############################################################################################################数据爬虫入口
async def main(url, codename):
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
    await index(page, cookie, url, codename)
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
        '&begin=' + curtime + '&period=day&type=before&count=-10000', value))
    time.sleep(5)

jsonDic1 = sorted(jsonDic.items(), key=lambda kv: (kv[1], kv[0]))
print(jsonDic)
print(jsonDic1)

#######################################################################################################################
################################################################################################################数据同步
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
bp.upload(localpath=rootPath + os.sep + "images" + os.sep + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_02('触发【01雪球指数】' + timeStr1 + '月度择时执行完成',
                                '触发【01雪球指数】' + timeStr1 + '月度择时执行完成' + str(jsonDic1))
