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
        print("==============================成功")
        data_content = await page.xpath('//pre')
        # print(await (await data_content[0].getProperty("textContent")).jsonValue())
        json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
        data_history = pd.DataFrame(json_list.get('data').get('item'), columns=['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'volume_post', 'amount_post'])
        print(data_history)

        closeArray = num.array(data_history['close'])
        doubleCloseArray = num.asarray(closeArray, dtype='double')

        highArray = num.array(data_history['high'])
        doubleHighArray = num.asarray(highArray, dtype='double')

        openArray = num.array(data_history['open'])
        doubleOpenArray = num.asarray(openArray, dtype='double')

        # 均线
        ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
        print(ma5)

        n = 0
        # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
        if doubleHighArray[n-1] > ma5[n-1] > doubleOpenArray[n-1] and ma5[n-2] < ma5[n-3] and \
                ma5[n-3] < ma5[n-4] and doubleCloseArray[n-1] > doubleOpenArray[n-1]:
            common.dingding_markdown_msg_2('触发跨越5周线' + codeName, '触发跨越5周线' + codeName)
            common_image.plt_image_tongyichutu_zhishu_xueqiu(doubleCloseArray, codeItem, codeName, "W", "雪球指数跨越5周线", "雪球指数跨越5周线")
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        print(e)

async def main(url, codeName):
    print(datetime.datetime.now())
    await asyncio.sleep(60 + random.randint(1, 120))
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
jsonDicCode = {}
jsonDicCode1 = [('BK0688', '光刻胶'), ('BK0539', '集成电路'), ('BK0636', '大豆'), ('BK0629', '高送转预期'),
                ('BK0647', '网络切片'), ('BK0606', '啤酒'), ('BK0669', '华为海思'), ('BK0602', '语音技术'),
                ('BK0638', '农业种植'), ('BK0656', '透明工厂'), ('BK0637', '玉米'), ('BK0699', 'MINILED'),
                ('BK0586', '芯片概念'), ('BK0686', '氢氟酸'), ('BK0709', '氮化镓'), ('BK0701', '转基因'),
                ('BK0554', '农机'), ('BK0655', '丙烯酸'), ('BK0410', '稀土永磁'), ('BK0417', '苹果概念'),
                ('BK0568', 'OLED'), ('BK0631', '芬太尼'), ('BK0626', '消费电子'), ('BK0692', '无线耳机'),
                ('BK0642', '超清视频'),
                ('BK0670', '国产操作系统'),
                ('BK0711', '数据中心'),
                ('BK0448', '网络安全'),
                ('BK0536', '医药电商'),
                ('BK0529', '互联网彩票'),
                ('BK0489', '5G'),
                ('BK0512', '新股与次新股'),
                ('BK0611', '小米概念'),
                ('BK0623', '百度概念'),
                ('BK0559', '人工智能'),
                ('BK0436', '特高压'),
                ('BK0445', '智能穿戴'),
                ('BK0465', '蓝宝石'),
                ('BK0485', '氟化工'),
                ('BK0632', '华为概念'),
                ('BK0689', '钴'),
                ('BK0713', '富媒体通信'),
                ('BK0414', '云计算'),
                ('BK0435', '安防'),
                ('BK0407', '物联网'),
                ('BK0566', '无人驾驶'),
                ('BK0668', '数字乡村'),
                ('BK0616', '边缘计算'),
                ('BK0561', '量子通信'),
                ('BK0487', '金融IC'),
                ('BK0444', '大数据'),
                ('BK0694', '非科创次新股'),
                ('BK0484', '汽车电子'),
                ('BK0553', '乡村振兴'),
                ('BK0662', '台湾概念'),
                ('BK0589', '人脸识别'),
                ('BK0635', '柔性屏'),
                ('BK0406', '智能电网'),
                ('BK0617', '知识产权'),
                ('BK0450', '乳业'),
                ('BK0504', '卫星导航'),
                ('BK0603', '无线充电'),
                ('BK0612', '富士康'),
                ('BK0609', '工业互联网'),
                ('BK0541', '车联网'),
                ('BK0486', '小金属')
              ]

for key, value in jsonDicCode1:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin=1588755908183&period=week&type=before&count=-142', value))

common.dingding_markdown_msg_2('触发执行完成', '触发执行完成')
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)