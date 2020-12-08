import asyncio
from pyppeteer import launch
import datetime
import json
import time

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os


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


project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

js1 = '''() =>{
           Object.defineProperties(navigator,{
           webdriver:{
               get: () => false
               }
           })
       }'''


async def goto_page(page, href):
    await page.goto(href)
    await page.evaluate(js1)
    content_level1 = await page.xpath('//div[@class="style-scope ytd-watch-flexy"]')
    print(content_level1.__len__())
    print("======================================================================================")


#######################################################################################################################
##############################################################################################################主执行程序
async def main(url, title):
    # js2 = '''() => {
    #        alert (
    #            window.navigator.webdriver
    #        )
    #    }'''

    browser = await launch(headless=True, args=['--no-sandbox'])
    # browser = await launch()

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    # 大搜车 非凡电视
    await page.goto(url)
    await page.evaluate(js1)
    # await page.evaluate(js2)

    cookies2 = await page.cookies()
    await save_cookie(cookies2)
    cookie = await load_cookie()

    elements_level1 = await page.xpath('//div[@class="text-wrapper style-scope ytd-video-renderer"]')
    # 新闻总数
    # print(elements_level1.__len__())

    print("============================================================================")
    print("                              " + title + "                                      ")
    print("                              " + title + "                                      ")
    print("============================================================================")
    for item_level1 in elements_level1:
        elements_level2 = await item_level1.xpath('./div[@id="meta"]')
        for item_level2 in elements_level2:
            elements_time = await item_level2.xpath('./ytd-video-meta-block'
                                                    '[@class="style-scope ytd-video-renderer byline-separated"]'
                                                    '/div[@id="metadata"]/div[@id="metadata-line"]'
                                                    '/span[@class="style-scope ytd-video-meta-block"]')
            print(elements_time.__len__())
            if elements_time.__len__() == 0:
                elements_time = await item_level2.xpath(
                    './ytd-video-meta-block[@class="style-scope ytd-video-renderer"]'
                    '/div[@id="metadata"]/div[@id="metadata-line"]'
                    '/span[@class="style-scope ytd-video-meta-block"]')
            time_str = await (await elements_time[1].getProperty("textContent")).jsonValue()
            print(time_str)
            if "1 day ago" in time_str or "days ago" in time_str or "日前" in time_str \
                    or 'hours' in time_str or '小时' in time_str:
                # 打印新闻标题
                elements_level3 = await item_level2 \
                    .xpath('./div[@id="title-wrapper"]'
                           '/h3[@class="title-and-badge style-scope ytd-video-renderer"]'
                           '/a[@class="yt-simple-endpoint style-scope ytd-video-renderer"]')
                print(await (await elements_level3[0].getProperty("title")).jsonValue())

                # 打印新闻标题
                elements_xiangqing = await item_level1 \
                    .xpath('./yt-formatted-string[@id="description-text"]')
                print(await (await elements_xiangqing[0].getProperty("textContent")).jsonValue())
    await browser.close()


url = "https://www.youtube.com/results?" \
      "search_query=%E9%9D%9E%E5%87%A1%E7%94%B5%E8%A7%86+%E5%A4%A7%E7%89%B9%E6%90%9C&sp=CAI%253D"
title = "大特搜"
asyncio.get_event_loop().run_until_complete(main(url, title))
#
# time.sleep(10)

url = "https://www.youtube.com/results?" \
      "search_query=%E6%9D%A8%E4%B8%96%E5%85%89%E5%9C%A8%E9%87%91%E9%92%B1%E7%88%86&sp=CAI%253D"
title = "杨世光在金钱爆"
asyncio.get_event_loop().run_until_complete(main(url, title))
