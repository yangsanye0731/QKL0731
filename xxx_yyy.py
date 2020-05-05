import asyncio
from pyppeteer import launch
import datetime
import common
import time
from asyncio import sleep
import json

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
    for cookie in cookie1:
        await page.setCookie(cookie)
    await page.goto(url)
    print("==============================成功")
    data_content = await page.xpath('//pre')
    # print(await (await data_content[0].getProperty("textContent")).jsonValue())
    json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
    print(json_list.get('data').get('item'))

    for item in json_list.get('data').get('item'):
        print(item)

async def main(url):
    print(datetime.datetime.now())
    await asyncio.sleep(10)
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


asyncio.get_event_loop().run_until_complete(main('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=BK0669&begin=1588755908183&period=week&type=before&count=-142'))
asyncio.get_event_loop().run_until_complete(main('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=BK0602&begin=1588755908183&period=week&type=before&count=-142'))
asyncio.get_event_loop().run_until_complete(main('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=BK0539&begin=1588755908183&period=week&type=before&count=-142'))