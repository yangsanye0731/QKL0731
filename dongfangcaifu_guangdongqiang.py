import asyncio
from pyppeteer import launch
import datetime
import common

async def main():

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
    # browser = await launch()

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    await page.goto('https://i.eastmoney.com/7289074629097176')
    await page.evaluate(js1)
    # await page.evaluate(js2)

    elements_level1 = await page.xpath('//div[@class="detailright"]')

    itemArray = {}
    for item_level1 in elements_level1:
        item = dict()
        elements_level2_title = await item_level1.xpath('./a[@class="detailtitle"]')
        # print(await (await elements_level2_title[0].getProperty("textContent")).jsonValue())
        item['title'] = await (await elements_level2_title[0].getProperty("textContent")).jsonValue()

        elements_level2_content = await item_level1.xpath('./div[@class="detailcontent"]')
        # print(await (await elements_level2_content[0].getProperty("textContent")).jsonValue())
        item['content'] = await (await elements_level2_content[0].getProperty("textContent")).jsonValue()

        elements_level2_date = await item_level1.xpath('./div[@class="date"]')
        # print(await (await elements_level2_date[0].getProperty("textContent")).jsonValue())
        item['date'] = await (await elements_level2_date[0].getProperty("textContent")).jsonValue()

        dateTime_p = datetime.datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')

        if dateTime_p > datetime.datetime.now() + datetime.timedelta(days=-2):
            print(item)
            print("======================================================================")
            common.dingding_markdown_msg_2("触发东方财富网广州强有更新：" + item['title'], "触发东方财富网广州强有更新：" + item['title'])

    await browser.close()
asyncio.get_event_loop().run_until_complete(main())