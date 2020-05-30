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
import tushare as ts
import common_mysqlUtil

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
    result = 0
    try:
        for cookie in cookie1:
            await page.setCookie(cookie)
        await page.goto(url, options={"timeout":10000})
        data_content = await page.xpath('//pre')
        # print(await (await data_content[0].getProperty("textContent")).jsonValue())
        json_list = json.loads(await (await data_content[0].getProperty("textContent")).jsonValue())
        print("==================================================================================")
        common_mysqlUtil.update_all_code_plate(codeName, str(json.dumps(json_list.get('data'), ensure_ascii=False)))
        # items = json_list.get('data').items()
        # for key, value in items:
        #     print(str(key) + '=' + str(value.get('plate_name')))
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        print(e)
    return result

async def main(url1, codeName):
    print(datetime.datetime.now())
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
    await page.goto("https://www.xuangubao.cn/")
    await page.evaluate(js1)
    # await page.evaluate(js2)

    cookies2 = await page.cookies()
    await save_cookie(cookies2)
    cookie = await load_cookie()
    result = await index(page, cookie, url1, codeName)
    await browser.close()
    return result

all_code = ts.get_stock_basics()
all_code_index = all_code[1:-1].index
count = 0
all_code_index_x = num.array(all_code_index)
for codeItem in all_code_index_x:
    try:
        count = count + 1
        print(count)
        print(codeItem)
        code = codeItem
        data = common_mysqlUtil.select_all_code_one(code)
        if len(data) > 0:
            plate = data[0][2]
            if(plate is not None and len(plate)>0):
                continue

            if codeItem.startswith('6'):
                codeItem = codeItem + '.SS'
            if codeItem.startswith('0'):
                codeItem = codeItem + '.SZ'
            if codeItem.startswith('3'):
                codeItem = codeItem + '.SZ'
            asyncio.get_event_loop().run_until_complete(main('https://flash-api.xuangubao.cn/api/stage2/plates_by_any_stock?symbol=' + codeItem + '&fields=core_avg_pcp,plate_name',
                code))
        else:
            code_name = common.codeName(code)
            common_mysqlUtil.insert_all_code(code, code_name)

            if codeItem.startswith('6'):
                codeItem = codeItem + '.SS'
            if codeItem.startswith('0'):
                codeItem = codeItem + '.SZ'
            if codeItem.startswith('3'):
                codeItem = codeItem + '.SZ'
            asyncio.get_event_loop().run_until_complete(main('https://flash-api.xuangubao.cn/api/stage2/plates_by_any_stock?symbol=' + codeItem + '&fields=core_avg_pcp,plate_name',
                code))

    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        print(e)