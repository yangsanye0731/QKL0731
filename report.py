from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docxtpl import RichText
import time, datetime
import common_mysqlUtil
import common
from bypy import ByPy
import configparser
import tushare as ts
import numpy as num
import talib as ta
import common_image
from docx.shared import Mm

# 个股数
gegu_count = 13
gengong_count = 57


asset_url = 'reportTemplate.docx'
tpl = DocxTemplate(asset_url)

# 图片
def code_strategy(codeItem, field_name, width):
    count = 0
    all_code_index_x = [codeItem]
    myimage = None
    image_path = None
    sign_result = "信号："
    strResult = ""
    for codeItem in all_code_index_x:
        time.sleep(1)
        count = count + 1
        data_history = ts.get_k_data(codeItem, ktype='W')

        data_history_M = ts.get_k_data(codeItem, ktype='M')
        data_history_D = ts.get_k_data(codeItem, ktype='D')

        try:
            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            highArray = num.array(data_history['high'])
            doubleHighArray = num.asarray(highArray, dtype='double')

            openArray = num.array(data_history['open'])
            doubleOpenArray = num.asarray(openArray, dtype='double')

            lowArray = num.array(data_history['low'])
            doubleLowArray = num.asarray(lowArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)


            data = common_mysqlUtil.select_all_code_one(codeItem)
            if len(data) > 0:
                mingcheng = data[0][1]
            image_path = common_image.plt_image_tongyichutu_3(codeItem, "W", "【04每日报告】全部",
                                                              "【04每日报告】全部")
            myimage = InlineImage(tpl, image_path, width=Mm(width))
            context[field_name] = myimage


            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] and \
                    ma5[-3] < ma5[-4] and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
                data = common_mysqlUtil.select_all_code_one(codeItem)
                if len(data) > 0:
                    mingcheng = data[0][1]
                image_path = common_image.plt_image_tongyichutu_3(codeItem, "W", "【04每日报告】跨越5周线容大感光,主力持仓突增", "【04每日报告】跨越5周线容大感光,主力持仓突增")
                myimage=InlineImage(tpl, image_path, width=Mm(width))
                sign_result = sign_result + "触发跨越5周线容大感光,主力持仓突增;  "
                context[field_name] = myimage

            closeArray_M = num.array(data_history_M['close'])
            doubleCloseArray_M = num.asarray(closeArray_M, dtype='double')
            lowArray_M = num.array(data_history_M['low'])
            doubleLowArray_M = num.asarray(lowArray_M, dtype='double')
            closeArray_D = num.array(data_history_D['close'])
            doubleCloseArray_D = num.asarray(closeArray_D, dtype='double')
            lowArray_D = num.array(data_history_D['low'])
            doubleLowArray_D = num.asarray(lowArray_D, dtype='double')

            param_m1 = 11
            param_m2 = 9
            param_n = 10
            sma_n = ta.SMA(closeArray_M, param_n)
            upper = (1 + param_m1 / 100) * sma_n
            lower = (1 - param_m2 / 100) * sma_n
            ene = (upper + lower) / 2
            upper = upper.round(2)
            ene = ene.round(2)
            lower = lower.round(2)

            if (ene[-1] > ene[-2]):
                upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_D, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                             matype=0)
                if doubleLowArray_D[-1] < lowerband[-1] * 1.008:
                    image_path = common_image.plt_image_tongyichutu_3(codeItem, "W", "【04每日报告】ENE月线升势，布林日线下穿", "【04每日报告】ENE月线升势，布林日线下穿")
                    myimage = InlineImage(tpl, image_path, width=Mm(width))
                    context[field_name] = myimage

            sma_n_w = ta.SMA(doubleCloseArray, param_n)
            upper_w = (1 + param_m1 / 100) * sma_n_w
            lower_w = (1 - param_m2 / 100) * sma_n_w
            ene_w = (upper_w + lower_w) / 2
            upper_w = upper_w.round(2)
            ene_w = ene_w.round(2)
            lower_w = lower_w.round(2)

            print("=====================================================" + codeItem)
            print(closeArray[-1])
            print(ene_w[-1])
            if closeArray[-1] < ene_w[-1] :
                sign_result = sign_result + "触发当前价格在ENE周线中线下方；"

        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return myimage, sign_result, image_path

# 返回时间所对应的星期值
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

context = {'title': '我的每日报告'}
# 当天日期
timeStr = time.strftime("%Y/%m/%d", time.localtime())
context['time'] = timeStr
context['week'] = get_week_day(datetime.datetime.now())

# 资产概述
context['text'] = timeStr

filepath = "./config/"
time_path = time.strftime("%Y%m%d", time.localtime())
time_path = '20200705'
script_file_path = filepath + time_path + ".conf"
cf = configparser.RawConfigParser()
cf.read(script_file_path, encoding="utf-8-sig")
gainian1 = cf.get("script", "gainian1")
context['gainian1'] = gainian1
gainian2 = cf.get("script", "gainian2")
context['gainian2'] = gainian2
gainian3 = cf.get("script", "gainian3")
context['gainian3'] = gainian3
gainian4 = cf.get("script", "gainian4")
context['gainian4'] = gainian4

gegu_list = []
for i in range(gegu_count):
    gegu = cf.get("script", "gegu" + str(i))
    image_path, sign_result, image_lujing = code_strategy(gegu.split('|')[1], "codeItemXXX", 135)
    image_url = "http://47.240.11.144/" + image_lujing[9:]
    if "触发" in sign_result:
        common.dingding_markdown_msg_2('触发每日投资报告有鱼[火]，有鱼[火]！' + gegu.split('|')[2] + "【涨跌幅[钉子]：" + common.zhangdiefu(gegu.split('|')[1]) + "】" + sign_result,
                                       '触发每日投资报告有鱼[火]，有鱼[火]！' + gegu.split('|')[2] + "【涨跌幅[钉子]：" + common.zhangdiefu(gegu.split('|')[1]) + "】" + sign_result + "\n\n> ![screenshot](" + image_url + ")")
    rt1 = RichText('')
    rt1.add(sign_result, color='#ff0000', bold=True)
    gegu_dict = {'date': gegu.split('|')[0], 'title': gegu.split('|')[2], 'mark': gegu.split('|')[3], 'qita': rt1, 'image_path':image_path}
    gegu_list.append(gegu_dict)
context['gegu_list'] = gegu_list



# 未来趋势
jiaoyi_labels = ['资讯来源', '数据内容']
context['jiaoyi_labels'] = jiaoyi_labels

# 数据遍历
jiaoyi_dict1 = {'date': '2020-05-27', 'title':'游族网络：20.50卖出', 'mark':'交易原因：涨幅超过7%，收益14000+', 'qita':''}
##################################################################################################################################################################
##################################################################################################################################################################
jiaoyi_dict2 = {'date': '2020-06-18', 'title':'科林电气：11.50买入', 'mark':'价格在大单介入附近，且30,60下降个数较大', 'qita':''}
jiaoyi_dict3 = {'date': '2020-06-19', 'title':'科林电气：11.58卖出', 'mark':'30,60上升个数均超过30，有一定风险，抛出，收益100+', 'qita':''}
##################################################################################################################################################################
##################################################################################################################################################################
jiaoyi_dict4 = {'date': '2020-07-16', 'title':'恒为科技：22.80买入5500股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入', 'qita':''}
jiaoyi_dict5 = {'date': '2020-07-17', 'title':'万通智控：14.30买入11700股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入', 'qita':''}
jiaoyi_dict6 = {'date': '2020-07-21', 'title':'金太阳：21.95买入1600股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入', 'qita':''}
jiaoyi_dict7 = {'date': '2020-07-22', 'title':'万通智控：14.81卖出5500', 'mark':'30分钟上升数达到50+，结合外部环境：美国撤大使馆，科创板解禁，收益4000+', 'qita':''}
jiaoyi_dict8 = {'date': '2020-07-22', 'title':'恒为科技：22.70卖出', 'mark':'30分钟上升数达到50+，结合外部环境：美国撤大使馆，科创板解禁，收益4000+', 'qita':''}
jiaoyi_dict9 = {'date': '2020-07-22', 'title':'万通智控：14.74卖出6000', 'mark':'30分钟上升数达到50+，结合外部环境：美国撤大使馆，科创板解禁，收益4000+', 'qita':''}
##################################################################################################################################################################
##################################################################################################################################################################
jiaoyi_dict10 = {'date': '2020-07-24', 'title':'万通智控：13.90买入5000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict11 = {'date': '2020-07-24', 'title':'恒为科技：22.00买入4000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict12 = {'date': '2020-07-27', 'title':'万通智控：13.48买入5000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict13 = {'date': '2020-07-27', 'title':'恒为科技：21.68买入2000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict14 = {'date': '2020-07-27', 'title':'金太阳：20.70买入8000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict15 = {'date': '2020-07-30', 'title':'金太阳：卖出8000股', 'mark':'30分钟上升数达到40,60分钟数据也达到26，果断抛出，获利：17600+', 'qita':''}
jiaoyi_dict16 = {'date': '2020-07-30', 'title':'恒为科技：卖出6000股', 'mark':'30分钟上升数达到40,60分钟数据也达到26，果断抛出，获利：17600+', 'qita':''}
jiaoyi_dict17 = {'date': '2020-07-30', 'title':'万通智控：卖出10000股', 'mark':'30分钟上升数达到40,60分钟数据也达到26，果断抛出，获利：17600+', 'qita':''}
##################################################################################################################################################################
##################################################################################################################################################################
jiaoyi_dict18 = {'date': '2020-08-07', 'title':'电连技术：31.40买入1300股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict19 = {'date': '2020-08-07', 'title':'金太阳：21.70买入2500股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict20 = {'date': '2020-08-07', 'title':'万通智控：13.53买入1000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict21 = {'date': '2020-08-10', 'title':'万通智控：14.77卖出1000股', 'mark':'30,60上升个数均接近30，获利1000+，卖出有点早了', 'qita':''}
jiaoyi_dict22 = {'date': '2020-08-12', 'title':'金太阳：20.50买入8000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict23 = {'date': '2020-08-12', 'title':'电连技术：30.45买入3000股', 'mark':'30,60下降个数均超过30，ENE下方，大资金接入点位明确，确定性比较强', 'qita':''}
jiaoyi_dict24 = {'date': '2020-08-12', 'title':'游族网络：20.19买入7000股', 'mark':'30,60下降个数均超过30，ENE下方，达到ENE下线，确定性比较强', 'qita':''}
jiaoyi_dict25 = {'date': '2020-08-14', 'title':'游族网络：20.93卖出5000股，减4分之三仓位', 'mark':'30,60上升个数均接近30，获利10000+，周五，担心周末有利空消息', 'qita':''}
jiaoyi_dict26 = {'date': '2020-08-14', 'title':'金太阳：21.11卖出5500股，减2分之一仓位', 'mark':'30,60上升个数均接近30，获利10000+，周五，担心周末有利空消息', 'qita':''}
jiaoyi_dict27 = {'date': '2020-08-14', 'title':'电连技术：32.14卖出4300股，清仓', 'mark':'30,60上升个数大于30，获利3200+', 'qita':''}
jiaoyi_dict28 = {'date': '2020-08-14', 'title':'金太阳：21.22卖出5500股，清仓', 'mark':'30,60上升个数大于30，获利3200+', 'qita':''}
jiaoyi_dict29 = {'date': '2020-08-14', 'title':'游族网络：20.95卖出2000股，清仓', 'mark':'30,60上升个数大于30，获利3200+', 'qita':''}
##################################################################################################################################################################
##################################################################################################################################################################
jiaoyi_list = []
jiaoyi_list.append(jiaoyi_dict1)
jiaoyi_list.append(jiaoyi_dict2)
jiaoyi_list.append(jiaoyi_dict3)
jiaoyi_list.append(jiaoyi_dict4)
jiaoyi_list.append(jiaoyi_dict5)
jiaoyi_list.append(jiaoyi_dict6)
jiaoyi_list.append(jiaoyi_dict7)
jiaoyi_list.append(jiaoyi_dict8)
jiaoyi_list.append(jiaoyi_dict9)
jiaoyi_list.append(jiaoyi_dict10)
jiaoyi_list.append(jiaoyi_dict11)
jiaoyi_list.append(jiaoyi_dict12)
jiaoyi_list.append(jiaoyi_dict13)
jiaoyi_list.append(jiaoyi_dict14)
jiaoyi_list.append(jiaoyi_dict15)
jiaoyi_list.append(jiaoyi_dict16)
jiaoyi_list.append(jiaoyi_dict17)
jiaoyi_list.append(jiaoyi_dict18)
jiaoyi_list.append(jiaoyi_dict19)
jiaoyi_list.append(jiaoyi_dict20)
jiaoyi_list.append(jiaoyi_dict21)
jiaoyi_list.append(jiaoyi_dict22)
jiaoyi_list.append(jiaoyi_dict23)
jiaoyi_list.append(jiaoyi_dict24)
jiaoyi_list.append(jiaoyi_dict25)
jiaoyi_list.append(jiaoyi_dict26)
jiaoyi_list.append(jiaoyi_dict27)
jiaoyi_list.append(jiaoyi_dict28)
jiaoyi_list.append(jiaoyi_dict29)
context['jiaoyi_list'] = jiaoyi_list

# 未来趋势
qushi_labels = ['资讯来源', '数据内容']
context['qushi_labels'] = qushi_labels

# 数据遍历
qushi_dict1 = {'type': '国内趋势（30分钟）', 'title':'上升数、下降数进入30以上', 'mark':'主力趋势指标', 'qita':''}
qushi_dict2 = {'type': '国内趋势（60分钟）', 'title':'上升数、下降数进入30以上', 'mark':'主力趋势指标', 'qita':''}
qushi_dict3 = {'type': '国内趋势（日线）', 'title':'上升数、下降数进入30以上，大趋势', 'mark':'主力趋势指标', 'qita':''}
qushi_list = []
qushi_list.append(qushi_dict1)
qushi_list.append(qushi_dict2)
qushi_list.append(qushi_dict3)
context['qushi_list'] = qushi_list


# 数据资源
zixun_labels = ['资讯来源', '数据内容']
context['zixun_labels'] = zixun_labels

# 获取实时数据
data = common_mysqlUtil.select_report_news()
# 数据遍历
zixun_list = []
for i in range(len(data)):
    title = data[i][1]
    type = data[i][2]
    mark = data[i][3]
    zixun_dict1 = {'type': type, 'title':title, 'mark':mark, 'qita':'需优化'}
    zixun_list.append(zixun_dict1)
context['zixun_list'] = zixun_list

# 数据资源
shuju_labels = ['数据来源', '数据内容']
context['shuju_labels'] = shuju_labels
shuju_dict1 = {'shujulaiyuan': '选股宝', 'shujuneirong':'股票所属概念、概念简述', 'zhuyi':'每周六手动执行', 'qita':'已核对'}

rt1 = RichText('持续盈利:')
rt1.add('临渊履薄', url_id=tpl.build_url_id('https://xueqiu.com/u/5377325546'))

rt2 = RichText('价值择时:')
rt2.add('亚克斯', url_id=tpl.build_url_id('https://xueqiu.com/u/4469239431'))

rt3 = RichText('价值择股:')
rt3.add('广州强', url_id=tpl.build_url_id('https://i.eastmoney.com/7289074629097176'))


shuju_dict2 = {'shujulaiyuan': '东方财富网', 'shujuneirong':rt3, 'zhuyi':'有应用监控提醒', 'qita':'已核对'}
shuju_dict3 = {'shujulaiyuan': '雪球财经', 'shujuneirong': rt1, 'zhuyi':'每交易日更新', 'qita':'已核对'}
shuju_dict4 = {'shujulaiyuan': '雪球财经', 'shujuneirong': rt2, 'zhuyi':'更新频繁', 'qita':'已核对'}
shuju_list = []
shuju_list.append(shuju_dict1)
shuju_list.append(shuju_dict2)
shuju_list.append(shuju_dict3)
shuju_list.append(shuju_dict4)
context['shuju_list'] = shuju_list

# 策略概览
celve_labels = ['策略所属', '策略名称', '注意事项', '其他']
context['celve_labels'] = celve_labels
celve_dict1 = {'suoshu': '【01雪球概念】', 'mingcheng':'ENE月线升势，布林日线下穿', 'zhuyi':'每天10:30, 13:30', 'qita':'已核对'}
celve_dict2 = {'suoshu': '【01雪球概念】', 'mingcheng':'跨越5周线', 'zhuyi':'每天15:10-16:00', 'qita':'已核对'}
celve_dict3 = {'suoshu': '【02指数ETF】', 'mingcheng':'ENE月线升势，布林日线下穿', 'zhuyi':'每天16:00-17:00', 'qita':'已核对'}
celve_dict4 = {'suoshu': '【02指数ETF】', 'mingcheng':'跨越5周线', 'zhuyi':'每天16:00-17:00', 'qita':'已核对'}
celve_dict5 = {'suoshu': '【03全部代码】', 'mingcheng':'ENE月线升势，布林日线下穿', 'zhuyi':'每天15:10-16:00', 'qita':'已核对'}
celve_dict6 = {'suoshu': '【03全部代码】', 'mingcheng':'跨越5周线', 'zhuyi':'每天15:10-16:00', 'qita':'已核对'}
celve_dict7 = {'suoshu': '【03全部代码】', 'mingcheng':'日周双孕线', 'zhuyi':'-', 'qita':'暂不启用'}
celve_list = []
celve_list.append(celve_dict1)
celve_list.append(celve_dict2)
celve_list.append(celve_dict3)
celve_list.append(celve_dict4)
celve_list.append(celve_dict5)
celve_list.append(celve_dict6)
celve_list.append(celve_dict7)
context['celve_list'] = celve_list


# 血的教训
jiaoxun_labels = ['名称', '原因']
context['jiaoxun_labels'] = jiaoxun_labels
jiaoxun_dict1 = {'mingcheng': '聚光科技', 'yuanyin':'没有及时止损，持仓时间过长，均线、上轨及时撤出，不预测', 'zhuyi':'时间：2019-10-15', 'qita':'-'}
jiaoxun_dict2 = {'mingcheng': '传化智联', 'yuanyin':'横久必跌；进入时机不对；有多次机会出手；持仓时间过长，将已有利润全部回吐', 'zhuyi':'时间：2020-05-22', 'qita':'-'}
jiaoxun_dict3 = {'mingcheng': '容大感光（光刻胶行业、换手）', 'yuanyin':'1、大盘趋势错失，光刻胶概念趋势错失，ENE月线、日线布林下穿，跨越5周线；    2、模糊的确定性明显；    3、买入策略没有规划，分批买入', 'zhuyi':'-', 'qita':'-'}
jiaoxun_dict4 = {'mingcheng': '游族网络（游戏行业、换手）', 'yuanyin':'1、在30、60分钟线都符合条件情况下，没有介入，错失良机，个人主观性的预测未来；    2、卖出策略没有规划，分批卖出；   3、当多数概念出现跨越5周线时，预示着一波行情的出现，错过一次20%左右的较大行情', 'zhuyi':'时间：2020-05-28', 'qita':'-'}
jiaoxun_dict5 = {'mingcheng': '科林电气', 'yuanyin':'2020年度6月份交易次数为1，且很快进出，技术是要持续磨练出来的，交易次数少，对成长不利', 'zhuyi':'时间：2019-06-18', 'qita':'-'}
jiaoxun_dict6 = {'mingcheng': '华脉科技', 'yuanyin':'在大盘行情较好，价格在ENE中线下方时，没有及时入手；对盘面没有深入的分析，太懒惰，对自己的技术不自信', 'zhuyi':'时间：2019-07-01', 'qita':'-'}
jiaoxun_dict7 = {'mingcheng': '万通智控', 'yuanyin':'在大盘行情较好，价格在ENE中线下方时，没有及时入手；对盘面没有深入的分析，太懒惰，对自己的技术不自信', 'zhuyi':'时间：2019-07-01', 'qita':'-'}
jiaoxun_dict8 = {'mingcheng': '电连技术', 'yuanyin':'大盘股在拉升，但是30、60数量已经达到了卖出的标准，执行卖出动作，这个时候最好能够看下主力资金的接入情况，如果大资金在卖出，坚决卖出，如果大资金还在持续买入，可以进行观察', 'zhuyi':'时间：2019-08-17', 'qita':'-'}
jiaoxun_dict9 = {'mingcheng': '游族网络', 'yuanyin':'在30、60分钟线都符合条件情况下，没有介入，错失良机，个人主观性的预测未来；买入25%仓位也是可以的，不然又要等比较长的时间，才能出现机会', 'zhuyi':'时间：2019-08-20', 'qita':'-'}
jiaoxun_dict10 = {'mingcheng': '电连技术', 'yuanyin':'在30、60分钟线都符合条件情况下，没有介入，错失良机，个人主观性的预测未来；买入25%仓位也是可以的，不然又要等比较长的时间，才能出现机会', 'zhuyi':'时间：2019-08-20', 'qita':'-'}
jiaoxun_dict11 = {'mingcheng': '游族网络', 'yuanyin':'在30、60分钟线都符合条件情况下，选择对了介入时机，但是选择了换手率比较低的，涨幅较小', 'zhuyi':'时间：2019-08-26', 'qita':'-'}
jiaoxun_dict12 = {'mingcheng': '恒为科技', 'yuanyin':'在30、60分钟线都符合条件情况下，选择对了介入时机，但是选择了换手率比较低的，涨幅较小', 'zhuyi':'时间：2019-08-26', 'qita':'-'}
jiaoxun_list = []
jiaoxun_list.append(jiaoxun_dict1)
jiaoxun_list.append(jiaoxun_dict2)
jiaoxun_list.append(jiaoxun_dict3)
jiaoxun_list.append(jiaoxun_dict4)
jiaoxun_list.append(jiaoxun_dict6)
jiaoxun_list.append(jiaoxun_dict7)
jiaoxun_list.append(jiaoxun_dict8)
jiaoxun_list.append(jiaoxun_dict9)
jiaoxun_list.append(jiaoxun_dict10)
jiaoxun_list.append(jiaoxun_dict11)
jiaoxun_list.append(jiaoxun_dict12)
context['jiaoxun_list'] = jiaoxun_list


genzong_list = []
for i in range(gengong_count):
    try:
        genzong = cf.get("script", "genzong" + str(i))
        image_path, sign_result, image_lujing = code_strategy(genzong.split('|')[1], "codeItemXXX", 120)
        image_url = "http://47.240.11.144/" + image_lujing[9:]
        print(image_url)
        if "触发" in sign_result:
            common.dingding_markdown_msg_2('触发每日投资报告有鱼[火]，有鱼[火]！' + "【涨跌幅[钉子]：" + common.zhangdiefu(genzong.split('|')[1]) + "】" + genzong.split('|')[2] + sign_result,
                                           '触发每日投资报告有鱼[火]，有鱼[火]！' + "【涨跌幅[钉子]：" + common.zhangdiefu(genzong.split('|')[1]) + "】" + genzong.split('|')[2] + sign_result + "\n\n> ![screenshot](" + image_url + ")")
        rt1 = RichText('')
        rt1.add(sign_result, color='#ff0000', bold=True)
        gezong_dict = {'date': genzong.split('|')[0], 'title': genzong.split('|')[2], 'mark': '', 'qita': rt1, 'image_path':image_path}
        genzong_list.append(gezong_dict)
        time.sleep(10)
    except (IOError, TypeError, NameError, IndexError, Exception) as e:
        print(e)
context['genzong_list'] = genzong_list

image_path = common_image.plt_image_geGuZhiBiao("399006","创业板指")
time.sleep(10)
myimage = InlineImage(tpl, image_path, width=Mm(182))
context['image1'] = myimage

image_path = common_image.plt_image_geGuZhiBiao("399300","沪深300")
time.sleep(10)
myimage = InlineImage(tpl, image_path, width=Mm(182))
context['image2'] = myimage


tpl.render(context)
timeTitle = time.strftime("%Y%m%d", time.localtime())
tpl.save('./report/每日报告_2020.docx')
tpl.save('./report/每日报告_' + timeTitle + '.docx')

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath='0000_Report')
bp.upload(localpath="./report", remotepath='0000_Report')
common.dingding_markdown_msg_2('触发【Report】每日投资报告执行完成', '触发【Report】每日投资报告执行完成')