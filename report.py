
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docxtpl import RichText
import time
import common_mysqlUtil
import common
from bypy import ByPy

asset_url = 'reportTemplate.docx'
tpl = DocxTemplate(asset_url)

context = {'title': '我的每日报告'}
# 当天日期
timeStr = time.strftime("%Y/%m/%d", time.localtime())
context['time'] = timeStr

# 资产概述
context['text'] = timeStr

# myimage=InlineImage(tpl, './images/111222333.png')
# context['myimage'] = myimage

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
celve_dict4 = {'suoshu': '【02国内ETF】', 'mingcheng':'跨越5周线', 'zhuyi':'每天16:00-17:00', 'qita':'已核对'}
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
jiaoxun_dict1 = {'mingcheng': '聚光科技', 'yuanyin':'及时止损，持仓时间过长，均线、上轨及时撤出，不预测', 'zhuyi':'-', 'qita':'-'}
jiaoxun_dict2 = {'mingcheng': '传化智联', 'yuanyin':'横久必跌；进入时机不对；有多次机会出手；持仓时间过长', 'zhuyi':'-', 'qita':'-'}
jiaoxun_dict3 = {'mingcheng': '容大感光', 'yuanyin':'大盘趋势错失，光刻胶概念趋势错失，ENE月线、日线布林下穿，跨越5周线；模糊的确定性明显', 'zhuyi':'-', 'qita':'-'}
jiaoxun_list = []
jiaoxun_list.append(jiaoxun_dict1)
jiaoxun_list.append(jiaoxun_dict2)
jiaoxun_list.append(jiaoxun_dict3)
context['jiaoxun_list'] = jiaoxun_list

tpl.render(context)
timeTitle = time.strftime("%Y%m%d", time.localtime())
tpl.save('./report/每日报告_' + timeTitle + '.docx')

bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath='0000_Report')
bp.upload(localpath="./report", remotepath='0000_Report')
common.dingding_markdown_msg_2('触发【Report】每日投资报告执行完成', '触发【Report】每日投资报告执行完成')