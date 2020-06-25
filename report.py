
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docxtpl import RichText
import time, datetime
import common_mysqlUtil
import common
from bypy import ByPy
import configparser

asset_url = 'reportTemplate.docx'
tpl = DocxTemplate(asset_url)

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

# myimage=InlineImage(tpl, './images/111222333.png')
# context['myimage'] = myimage

filepath = "./report_list/"
time_path = time.strftime("%Y%m%d", time.localtime())
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

gegu1 = cf.get("script", "gegu1")
context['gegu1'] = gegu1
gegu2 = cf.get("script", "gegu2")
context['gegu2'] = gegu2
gegu3 = cf.get("script", "gegu3")
context['gegu3'] = gegu3
gegu4 = cf.get("script", "gegu4")
context['gegu4'] = gegu4
gegu5 = cf.get("script", "gegu5")
context['gegu5'] = gegu5
gegu6 = cf.get("script", "gegu6")
context['gegu6'] = gegu6



# 未来趋势
jiaoyi_labels = ['资讯来源', '数据内容']
context['jiaoyi_labels'] = jiaoyi_labels

# 数据遍历
jiaoyi_dict1 = {'date': '2020-05-27', 'title':'游族网络：20.50卖出', 'mark':'交易原因：涨幅超过7%', 'qita':''}
jiaoyi_dict2 = {'date': '2020-06-18', 'title':'科林电器：11.50买入', 'mark':'价格在大单介入附近，且30,60下降个数较大', 'qita':''}
jiaoyi_dict3 = {'date': '2020-06-19', 'title':'科林电器：11.58卖出', 'mark':'30,60上升个数均超过30，有一定风险，抛出', 'qita':''}
jiaoyi_list = []
jiaoyi_list.append(jiaoyi_dict1)
jiaoyi_list.append(jiaoyi_dict2)
jiaoyi_list.append(jiaoyi_dict3)
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
jiaoxun_dict3 = {'mingcheng': '容大感光（光刻胶行业、换手）', 'yuanyin':'1、大盘趋势错失，光刻胶概念趋势错失，ENE月线、日线布林下穿，跨越5周线；    2、模糊的确定性明显；    3、买入策略没有规划', 'zhuyi':'-', 'qita':'-'}
jiaoxun_dict4 = {'mingcheng': '游族网络（游戏行业、换手）', 'yuanyin':'1、在30、60分钟线都符合条件情况下，没有介入，错失良机，个人主观性的预测未来；    2、卖出策略没有规划', 'zhuyi':'时间：2020-05-28', 'qita':'-'}
jiaoxun_list = []
jiaoxun_list.append(jiaoxun_dict1)
jiaoxun_list.append(jiaoxun_dict2)
jiaoxun_list.append(jiaoxun_dict3)
jiaoxun_list.append(jiaoxun_dict4)
context['jiaoxun_list'] = jiaoxun_list

tpl.render(context)
timeTitle = time.strftime("%Y%m%d", time.localtime())
tpl.save('./report/每日报告_' + timeTitle + '.docx')

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath='0000_Report')
bp.upload(localpath="./report", remotepath='0000_Report')
common.dingding_markdown_msg_2('触发【Report】每日投资报告执行完成', '触发【Report】每日投资报告执行完成')