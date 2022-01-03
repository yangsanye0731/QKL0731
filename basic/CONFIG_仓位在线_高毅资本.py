import asyncio
import os
#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import time

import numpy as num
import tushare as ts
from pyppeteer import launch

import common_image
import common_zhibiao

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


#######################################################################################################################
#############################################################################请求选股宝股票页面，获取其对应的概念并更新数据库
async def main(url, keyword):
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

    fo = open("仓位在线Base_" + keyword + "_" + time_str + ".txt", "w", encoding='UTF-8')
    fo2 = open("仓位在线_" + keyword + "_" + time_str + ".txt", "w", encoding='UTF-8')
    print(list.__len__())
    for itemXunHuan in list:
        codeItem = itemXunHuan.get('guPiaoDaiMa')
        try:
            data_history = ts.get_hist_data(codeItem, ktype='M')
            data_history = data_history.iloc[::-1]
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            # print(data_history)
            KDJ_K, KDJ_D, KDJ_J, KDJ_J_title = common_zhibiao.KDJ_zhibiao(data_history, doubleCloseArray)

            print(KDJ_J)
            if float(KDJ_J) < 0:
                fo2.write(codeItem + "\n")
                print(codeItem + "========================================")
                print(KDJ_K)
                print(KDJ_D)
                print(KDJ_J)
                fo.write(codeItem + "__" + itemXunHuan.get('gengXinRiQi') + "__"
                         + itemXunHuan.get('guDongMingCheng') + "__" + itemXunHuan.get('guPiaoMingCheng') + "\n")
                fo2.write(codeItem + "\n")

                common_image.plt_image_tongyichutu_2(codeItem,
                                                     "M",
                                                     "【" + keyword + "】月KDJ小于0",
                                                     "【" + keyword + "】月KDJ小于0")
        except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
            print(e)

#######################################################################################################################
##########################################################################################################遍历A股所有股票
asyncio.get_event_loop().run_until_complete(main("http://cwzx.shdjt.com/cwcx.asp?gdmc=%B8%DF%D2%E3%D7%CA%B2%FA", "高毅"))
