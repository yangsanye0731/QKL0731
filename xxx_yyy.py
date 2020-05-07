import asyncio
from pyppeteer import launch
import datetime
import common
import time
from asyncio import sleep
import json
import pandas as pd
import random
import common

async def save_cookie(cookie):
    with open("cookie.json", 'w+', encoding="utf-8") as file:
        json.dump(cookie, file, ensure_ascii=False)

# 读取cookie
async def load_cookie():
    with open("cookie.json", 'r', encoding="utf-8") as file:
        cookie = json.load(file)
    return cookie

# 加载首页
async def index(page, cookie1,url):
    try:
        for cookie in cookie1:
            await page.setCookie(cookie)
        await page.goto(url)
        print("==============================成功")
        data_content = await page.xpath('//pre')
        # print(await (await data_content[0].getProperty("textContent")).jsonValue())
        json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
        res = pd.DataFrame(json_list.get('data').get('item'), columns=['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'volume_post', 'amount_post'])
        print(res)
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        print(e)

async def main(url):
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
    await index(page, cookie, url)
    await browser.close()


count = 0
jsonDicCode = {}
jsonDicCode1 = [('BK0688', '光刻胶'), ('BK0539', '集成电路'), ('BK0636', '大豆'), ('BK0629', '高送转预期'),
                ('BK0647', '网络切片'), ('BK0606', '啤酒'), ('BK0669', '华为海思'), ('BK0602', '语音技术'),
                ('BK0638', '农业种植'), ('BK0656', '透明工厂'), ('BK0637', '玉米'), ('BK0699', 'MINILED'),
                ('BK0586', '芯片概念'), ('BK0686', '氢氟酸'), ('BK0709', '氮化镓'), ('BK0701', '转基因'),
                ('BK0554', '农机'), ('BK0655', '丙烯酸'), ('BK0410', '稀土永磁'), ('BK0417', '苹果概念'),
                ('BK0568', 'OLED'), ('BK0631', '芬太尼'), ('BK0626', '消费电子'), ('BK0692', '无线耳机')
              ]

for key, value in jsonDicCode1:
    codeItem = key
    count = count + 1
    print(count)
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin=1588755908183&period=week&type=before&count=-142'))

common.dingding_markdown_msg_2('触发执行完成', '触发执行完成')