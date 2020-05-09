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
            common_image.plt_image_tongyichutu_zhishu_xueqiu(data_history['close'], codeItem, codeName, "W", "雪球指数跨越5周线", "雪球指数跨越5周线")
    except (IOError, TypeError, NameError, IndexError, TimeoutError, Exception) as e:
        print(e)

async def main(url, codeName):
    print(datetime.datetime.now())
    await asyncio.sleep(60 + random.randint(1, 100))
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
                ('BK0486', '小金属'),
                ('BK0696', '云游戏'),
                ('BK0622', '送转填权'),
                ('BK0426', '智能医疗'),
                ('BK0506', '足球'),
                ('BK0702', 'HIT电池'),
                ('BK0565', '二维码识别'),
                ('BK0483', '新材料概念'),
                ('BK0685', 'ETC'),
                ('BK0595', '互联网医疗'),
                ('BK0490', '超导'),
                ('BK0498', '国产软件'),
                ('BK0549', '军工'),
                ('BK0695', '胎压监测'),
                ('BK0619', '数字中国'),
                ('BK0418', '智慧城市'),
                ('BK0653', '横琴新区'),
                ('BK0468', '尾气治理'),
                ('BK0601', '智能音箱'),
                ('BK0408', '移动支付'),
                ('BK0664', '眼科医疗'),
                ('BK0573', '军民融合'),
                ('BK0442', '节能照明'),
                ('BK0451', '特斯拉'),
                ('BK0604', '燃料电池'),
                ('BK0488', 'PM2.5'),
                ('BK0680', '仿制药'),
                ('BK0525', '高送转'),
                ('BK0679', '创业板重组松绑'),
                ('BK0556', '虚拟现实'),
                ('BK0413', '石墨烯'),
                ('BK0467', '禽流感'),
                ('BK0596', '智能交通'),
                ('BK0678', '垃圾分类'),
                ('BK0557', '锂电池'),
                ('BK0433', '脱硫脱硝'),
                ('BK0519', '工业4.0'),
                ('BK0625', '北汽新能源'),
                ('BK0672', '动物疫苗'),
                ('BK0480', '医疗器械'),
                ('BK0698', '分拆上市'),
                ('BK0441', '新能源汽车'),
                ('BK0587', '区块链'),
                ('BK0687', '磷化工'),
                ('BK0700', '网红经济'),
                ('BK0705', '云办公'),
                ('BK0505', '基因测序'),
                ('BK0547', '深股通'),
                ('BK0530', '物流电商平台'),
                ('BK0515', '阿里巴巴概念'),
                ('BK0615', '宁德时代概念'),
                ('BK0471', '机器人概念'),
                ('BK0665', '人造肉'),
                ('BK0574', '雄安新区'),
                ('BK0621', '国产航母'),
                ('BK0600', '智能物流'),
                ('BK0690', '数字货币'),
                ('BK0482', '家用电器'),
                ('BK0493', '高铁'),
                ('BK0560', '参股新三板'),
                ('BK0534', '供应链金融'),
                ('BK0646', '电力物联网'),
                ('BK0411', '新疆振兴'),
                ('BK0463', '通用航空'),
                ('BK0714', '今日头条概念'),
                ('BK0453', '智能家居'),
                ('BK0474', '养老概念'),
                ('BK0627', '国资驰援'),
                ('BK0697', '澳交所'),
                ('BK0430', '污水治理'),
                ('BK0639', '商誉减值'),
                ('BK0466', '生态农业'),
                ('BK0495', '无人机'),
                ('BK0455', '电子发票'),
                ('BK0510', '中韩自贸区'),
                ('BK0613', '独角兽'),
                ('BK0558', '互联网+'),
                ('BK0497', '大飞机'),
                ('BK0624', '燃料乙醇'),
                ('BK0478', '光伏概念'),
                ('BK0584', '微信小程序'),
                ('BK0608', '水泥'),
                ('BK0431', '创投'),
                ('BK0644', '工业大麻'),
                ('BK0693', '年报预增'),
                ('BK0703', '流感'),
                ('BK0432', '文化传媒'),
                ('BK0649', '氢能源'),
                ('BK0710', '超级电容'),
                ('BK0550', '杭州亚运会'),
                ('BK0544', 'PPP概念'),
                ('BK0598', '无人零售'),
                ('BK0479', '3D打印'),
                ('BK0583', '网约车'),
                ('BK0671', '生物疫苗'),
                ('BK0477', '黄金概念'),
                ('BK0508', '举牌'),
                ('BK0518', '福建自贸区'),
                ('BK0409', '融资融券'),
                ('BK0438', '高端装备'),
                ('BK0567', '电子竞技'),
                ('BK0597', '互联网保险'),
                ('BK0417', '美丽中国'),
                ('BK0456', '参股民营银行'),
                ('BK0620', '空铁WIFI'),
                ('BK0712', 'C2M概念'),
                ('BK0449', '充电桩'),
                ('BK0513', '网络游戏'),
                ('BK0551', '健康中国'),
                ('BK0708', '航空发动机'),
                ('BK0599', '细胞免疫治疗'),
                ('BK0605', '腾讯概念'),
                ('BK0427', '生物医药'),
                ('BK0454', '在线教育'),
                ('BK0503', '猪肉'),
                ('BK0704', '口罩'),
                ('BK0706', '消毒液'),
                ('BK0675', '烟草'),
                ('BK0446', '互联网金融'),
                ('BK0437', '海工装备'),
                ('BK0659', '黑洞概念'),
                ('BK0402', '稀缺资源'),
                ('BK0676', '青蒿素'),
                ('BK0641', 'MSCI概念'),
                ('BK0464', '冷链物流'),
                ('BK0673', '富时罗素概念股'),
                ('BK0481', '二胎概念'),
                ('BK0628', '壳资源'),
                ('BK0663', '郭台铭概念'),
                ('BK0494', '节能环保'),
                ('BK0715', '新三板精选层'),
                ('BK0570', '债转股'),
                ('BK0707', '医疗垃圾处理'),
                ('BK0447', '手机游戏'),
                ('BK0527', '风电'),
                ('BK0569', '股权转让'),
                ('BK0674', '黑龙江自贸区'),
                ('BK0429', '固废处理'),
                ('BK0491', '金改'),
                ('BK0511', '央企国资改革'),
                ('BK0658', '长三角一体化'),
                ('BK0684', '中船系'),
                ('BK0469', '京津冀一体化'),
                ('BK0443', '土地流转'),
                ('BK0502', '水利'),
                ('BK0428', '食品安全'),
                ('BK0540', '能源互联网'),
                ('BK0614', '网络直播'),
                ('BK0691', '标普道琼斯A股'),
                ('BK0579', '蚂蚁金融'),
                ('BK0578', '可燃冰'),
                ('BK0460', '一带一路'),
                ('BK0501', '核电'),
                ('BK0531', '碳纤维'),
                ('BK0523', '农村电商'),
                ('BK0591', '超级品牌'),
                ('BK0521', '参股保险'),
                ('BK0405', '生物质能'),
                ('BK0458', '民营医院'),
                ('BK0666', '人民币贬值'),
                ('BK0543', '高校'),
                ('BK0548', '深圳国资改革'),
                ('BK0472', '沪股通'),
                ('BK0654', '融媒体'),
                ('BK0507', '职业教育'),
                ('BK0575', 'MSCI概念'),
                ('BK0517', '迪士尼'),
                ('BK0657', '超级真菌'),
                ('BK0416', '页岩气'),
                ('BK0607', '石墨电极'),
                ('BK0652', '外资券商'),
                ('BK0520', '参股券商'),
                ('BK0537', '证金持股'),
                ('BK0594', '自由贸易港'),
                ('BK0452', '上海自贸区'),
                ('BK0500', '期货概念'),
                ('BK0434', '电子商务'),
                ('BK0545', '地下管网'),
                ('BK0661', '参股银行'),
                ('BK0425', '煤化工'),
                ('BK0634', '养鸡'),
                ('BK0516', '体育产业'),
                ('BK0528', '跨境电商'),
                ('BK0533', '钛白粉'),
                ('BK0588', '租售同权'),
                ('BK0457', '天津自贸区'),
                ('BK0577', '共享单车'),
                ('BK0524', '分散染料'),
                ('BK0645', '数字孪生'),
                ('BK0440', '天然气'),
                ('BK0581', '参股万达商业'),
                ('BK0580', '特色小镇'),
                ('BK0459', '上海国资改革'),
                ('BK0473', '粤港澳大湾区'),
                ('BK0460', '信托概念'),
                ('BK0509', '电力改革'),
                ('BK0571', '中字头股票'),
                ('BK0651', '冰雪产业'),
                ('BK0461', '油品改革'),
                ('BK0564', '广东自贸区'),
                ('BK0590', '装配式建筑'),
                ('BK0610', '新零售'),
                ('BK0572', '摘帽'),
                ('BK0526', '草甘膦'),
                ('BK0576', '消费金融'),
                ('BK0475', '白酒'),
                ('BK0532', '两桶油改革'),
                ('BK0563', '航运概念'),
                ('BK0618', '赛马概念'),
                ('BK0439', '特钢概念'),
                ('BK0667', '草地贪夜蛾防治'),
                ('BK0552', '东盟自贸区'),
                ('BK0400', 'ST板块'),
                ('BK0462', '在线旅游'),
                ('BK0522', '西安自贸区')
              ]

for key, value in jsonDicCode1:
    codeItem = key
    count = count + 1
    print(codeItem)
    print(value)
    asyncio.get_event_loop().run_until_complete(main(
        'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=' + key + '&begin=1588755908183&period=week&type=before&count=-142', value))

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath=timeStr1)
bp.upload(localpath="./images/" + timeStr1, remotepath=timeStr1)
common.dingding_markdown_msg_2('触发执行完成', '触发执行完成')