import asyncio
import datetime
import json
import time

import numpy as num
import pandas as pd
import talib as ta
from bypy import ByPy
from docx.shared import Mm
from docxtpl import DocxTemplate
from docxtpl import InlineImage
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
    myimage = None
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
        huanshoulv  = num.array(data_history['turnoverrate'])
        print("==============================================================")
        print(zhangdiefu[-1])
        print(huanshoulv[-1])
        # 均线
        ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
        print(ma5)

        n = 0
        image_path = common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName,
                                                                      "W", "【01雪球指数】雪球报告",
                                                                      "【01雪球指数】跨越5周线",
                                                                      str(zhangdiefu[-1]), "%.2f" % huanshoulv[-1])
        myimage = InlineImage(tpl, image_path, width=Mm(135))
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        common.dingding_markdown_msg_2('触发【01雪球指数】雪球报告' + codeName + '(' + codeItem + ')报错了 ！！！！！！',
                                       '触发【01雪球指数】雪球报告' + codeName + '(' + codeItem + ')报错了 ！！！！！！')
        print(e)
    return myimage

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
    # 华为海思概念股
    image_path = await index(page, cookie, url, codeName)
    gezong_dict = {'date': timeStr, 'title': codeName, 'mark': '', 'qita': '',
                   'image_path': image_path}
    genzong_list.append(gezong_dict)
    context['genzong_list'] = genzong_list
    await browser.close()

def get_week_day(date):
  week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期天',
  }
  day = date.weekday()
  return week_day_dict[day]

asset_url = rootPath + os.sep + 'resource' + os.sep + 'template' + os.sep + 'reportXueqiuTemplate.docx'
tpl = DocxTemplate(asset_url)
context = {'title': '雪球报告'}
# 当天日期
timeStr = time.strftime("%Y/%m/%d", time.localtime())
context['time'] = timeStr
context['week'] = get_week_day(datetime.datetime.now())
genzong_list = []

count = 0
for key, value in const.XUEQIUGAINIAN:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    curtime = str(int(time.time()*1000))
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol='
        + key + '&begin=' + curtime + '&period=week&type=before&count=-142', value))

#######################################################################################################################
################################################################################################################生成文件
tpl.render(context)
timeTitle = time.strftime("%Y%m%d", time.localtime())
tpl.save(rootPath + os.sep + 'report' + os.sep + '雪球报告_' + timeTitle + '.docx')


#######################################################################################################################
################################################################################################################同步数据
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath='0000_Report')
bp.upload(localpath=rootPath + os.sep + "report", remotepath='0000_Report')
common.dingding_markdown_msg_2('触发【01雪球指数】雪球报告', '触发【01雪球指数】雪球报告')
