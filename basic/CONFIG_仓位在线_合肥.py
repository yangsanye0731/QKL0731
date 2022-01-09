import asyncio
import os
#######################################################################################################################
# ###############################################################################################配置程序应用所需要环境PATH
import sys
import time

import numpy as num
import tushare as ts
from pyppeteer import launch

import common_zhibiao

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import common_image
import talib as ta


#######################################################################################################################
# ########################################################################################################请求仓位在线页面
async def main(url, keyword, zhouqi):
    js1 = '''() =>{
              Object.defineProperties(navigator,{
              webdriver:{
                  get: () => false
                  }
              })
          }'''

    browser = await launch(headless=True, args=['--no-sandbox'])
    # browser = await launch()

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    await page.goto(url, options={"timeout": 1000000})
    await page.evaluate(js1)
    # await page.evaluate(js2)

    elements_level1 = await page.xpath('//tr[@height="25"]')

    count = 0
    list = []
    codeList = []
    time_str = time.strftime("%Y%m%d", time.localtime())

    for item_level1 in elements_level1:
        try:
            item = dict()
            elements_level2_title = await item_level1.xpath('./td')
            for item_level2 in elements_level2_title:
                str = await (await item_level2.getProperty("textContent")).jsonValue()
                if str.__len__() == 6 and (str.startswith('000') or str.startswith('002') or str.startswith('300')
                                           or str.startswith('688') or str.startswith('600') or str.startswith('601')
                                           or str.startswith('602') or str.startswith('603')):
                    # print("=====================股票代码：" + str)
                    item['guPiaoDaiMa'] = str
                if str.__contains__("2021-") or str.__contains__("2020-"):
                    # print("=====================更新日期：" + str)
                    item['gengXinRiQi'] = str
                if str.__contains__(keyword):
                    # print("=====================股东名称：" + str)
                    item['guDongMingCheng'] = str
                if str.__contains__("F10"):
                    # print("=====================股东名称：" + str)
                    item['guPiaoMingCheng'] = str[0:4]
            count = count + 1
            print(count)
            # print(item)
            if item['guPiaoDaiMa'] is not None and not codeList.__contains__(item.get('guPiaoDaiMa')):
                list.append(item)
                codeList.append(item.get('guPiaoDaiMa'))
        except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
            print(e)
            continue
    await browser.close()

    fo = open("仓位在线Base_" + keyword + "_" + zhouqi + "_" + time_str + ".txt", "w", encoding='UTF-8')
    fo2 = open("仓位在线_" + keyword + "_" + zhouqi + "_" + time_str + ".txt", "w", encoding='UTF-8')
    print(list.__len__())
    for itemXunHuan in list:
        codeItem = itemXunHuan.get('guPiaoDaiMa')
        try:
            data_history = ts.get_hist_data(codeItem, ktype=zhouqi)
            data_history = data_history.iloc[::-1]
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # print(codeItem + "========================================")
            # print(data_history)
            KDJ_K, KDJ_D, KDJ_J, KDJ_J_title = common_zhibiao.KDJ_zhibiao(data_history, doubleCloseArray)

            if float(KDJ_J) < 0:
                fo2.write(codeItem + "\n")
                print(codeItem + "========================================")
                print(KDJ_K)
                print(KDJ_D)
                print(KDJ_J)
                fo.write(codeItem + "__" + itemXunHuan.get('gengXinRiQi') + "__"
                         + itemXunHuan.get('guDongMingCheng') + "__" + itemXunHuan.get('guPiaoMingCheng') + "\n")

                if zhouqi == 'W':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "W",
                                                         "【" + keyword + "】_" + "周KDJ小于0",
                                                         "【" + keyword + "】_" + "周KDJ小于0")
                if zhouqi == 'M':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "M",
                                                         "【" + keyword + "】_" + "月KDJ小于0",
                                                         "【" + keyword + "】_" + "月KDJ小于0")

            # ###############################################################################################跨越5周/月线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] < ma5[-4] \
                    and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
                if zhouqi == 'W':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "W",
                                                         "【" + keyword + "】_" + "跨越5周线",
                                                         "【" + keyword + "】_" + "跨越5周线")
                if zhouqi == 'M':
                    common_image.plt_image_tongyichutu_2(codeItem,
                                                         "M",
                                                         "【" + keyword + "】_" + "跨越5月线",
                                                         "【" + keyword + "】_" + "跨越5月线")

        except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
            print(e)


#######################################################################################################################
# ###############################################################################################################仓位在线
asyncio.get_event_loop().run_until_complete(
    main("http://cwzx.shdjt.com/cwcx.asp?gdmc=%BA%CF%B7%CA", "合肥", "M"))
asyncio.get_event_loop().run_until_complete(
    main("http://cwzx.shdjt.com/cwcx.asp?gdmc=%BA%CF%B7%CA", "合肥", "W"))
