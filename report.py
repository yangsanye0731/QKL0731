from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docxtpl import RichText
import time
import datetime
import common_mysqlUtil
from bypy import ByPy
import configparser
import tushare as ts
import numpy as num
import talib as ta
from docx.shared import Mm

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os
project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common
import common_image


asset_url = rootPath + os.sep + 'resource' + os.sep + 'template' + os.sep + 'reportTemplate.docx'
tpl = DocxTemplate(asset_url)

#######################################################################################################################
###########################################################################################################工具方法：策略
def code_strategy(codeItem, field_name, width):
    count = 0
    all_code_index_x = [codeItem]
    myimage = None
    image_path = None
    sign = "信号："
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

            # lowArray = num.array(data_history['low'])
            # doubleLowArray = num.asarray(lowArray, dtype='double')

            # 均线
            ma5 = ta.SMA(doubleCloseArray, timeperiod=5)
            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
            image_path = common_image.plt_image_tongyichutu_3(codeItem,
                                                              "W",
                                                              "【04每日报告】全部",
                                                              "【04每日报告】全部")
            myimage = InlineImage(tpl, image_path, width=Mm(width))
            context[field_name] = myimage

            # 跨越5周线, 最高点大于5周线, 开点小于5周线, 前两周五周线处于下降阶段
            if doubleHighArray[-1] > ma5[-1] > doubleOpenArray[-1] and ma5[-2] < ma5[-3] < ma5[-4] \
                    and doubleCloseArray[-1] > doubleOpenArray[-1] and ma60[-1] > ma60[-2]:
                image_path = common_image.plt_image_tongyichutu_3(codeItem,
                                                                  "W",
                                                                  "【04每日报告】跨越5周线容大感光,主力持仓突增",
                                                                  "【04每日报告】跨越5周线容大感光,主力持仓突增")
                myimage = InlineImage(tpl, image_path, width=Mm(width))
                sign = sign + "触发跨越5周线容大感光,主力持仓突增;  "
                context[field_name] = myimage

            closeArray_M = num.array(data_history_M['close'])
            # doubleCloseArray_M = num.asarray(closeArray_M, dtype='double')
            # lowArray_M = num.array(data_history_M['low'])
            # doubleLowArray_M = num.asarray(lowArray_M, dtype='double')
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
            # upper = upper.round(2)
            ene = ene.round(2)
            # lower = lower.round(2)

            if ene[-1] > ene[-2]:
                upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray_D, timeperiod=20, nbdevup=2, nbdevdn=2,
                                                             matype=0)
                if doubleLowArray_D[-1] < lowerband[-1] * 1.008:
                    image_path = common_image.plt_image_tongyichutu_3(codeItem,
                                                                      "W",
                                                                      "【04每日报告】ENE月线升势，布林日线下穿",
                                                                      "【04每日报告】ENE月线升势，布林日线下穿")
                    myimage = InlineImage(tpl, image_path, width=Mm(width))
                    context[field_name] = myimage

            sma_n_w = ta.SMA(doubleCloseArray, param_n)
            upper_w = (1 + param_m1 / 100) * sma_n_w
            lower_w = (1 - param_m2 / 100) * sma_n_w
            ene_w = (upper_w + lower_w) / 2
            # upper_w = upper_w.round(2)
            ene_w = ene_w.round(2)
            # lower_w = lower_w.round(2)

            print("=====================================================" + codeItem)
            print(closeArray[-1])
            print(ene_w[-1])
            # if closeArray[-1] < ene_w[-1] :
                # sign = sign + "触发当前价格在ENE周线中线下方；"
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
    return myimage, sign, image_path

#######################################################################################################################
###########################################################################################工具方法：返回时间所对应的星期值
def get_week_day(date):
  week_day_dict = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期天',
  }
  day = date.weekday()
  return week_day_dict[day]

#######################################################################################################################
#########################################################################################################投资报告首页信息
context = {'title': '我的每日报告'}
# 当天日期
timeStr = time.strftime("%Y/%m/%d", time.localtime())
context['time'] = timeStr
context['week'] = get_week_day(datetime.datetime.now())

filepath = rootPath + + os.sep + 'resource' + os.sep + 'config'
script_file_path = filepath + + os.sep + "datasource.ini"
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

#######################################################################################################################
########################################################################################################跨越5周线个股筛选
gegu_list = []
gegu_count = cf.get("script", "gegu_count")
for i in range(int(gegu_count) + 1):
    gegu = cf.get("script", "gegu" + str(i))
    image_path_result, sign_result, image_lujing = code_strategy(gegu.split('|')[1], "codeItemXXX", 135)
    image_url = "http://47.240.11.144/" + image_lujing[9:]
    print(image_url)
    if "触发" in sign_result:
        common.dingding_markdown_msg_2('触发每日投资报告有鱼[火]，有鱼[火]！' + gegu.split('|')[2]
                                       + "【涨跌幅[钉子]：" + common.zhangdiefu(gegu.split('|')[1]) + "】" + sign_result,
                                       '触发每日投资报告有鱼[火]，有鱼[火]！' + gegu.split('|')[2]
                                       + "【涨跌幅[钉子]：" + common.zhangdiefu(gegu.split('|')[1]) + "】"
                                       + sign_result + "\n\n> ![screenshot](" + image_url + ")")
    rt1 = RichText('')
    rt1.add(sign_result, color='#ff0000', bold=True)
    gegu_dict = {'date': gegu.split('|')[0], 'title': gegu.split('|')[2], 'mark': gegu.split('|')[3],
                 'qita': rt1, 'image_path': image_path_result}
    gegu_list.append(gegu_dict)
context['gegu_list'] = gegu_list

#######################################################################################################################
################################################################################################################交易记录
jiaoyi_list = []
jiaoyi_count = cf.get("script", "jiaoyi_count")
for i in range(1, int(jiaoyi_count) + 1):
    jiaoyi = cf.get("script", "jiaoyi" + str(i))
    jiaoyi_dict = {'date': jiaoyi.split('|')[0], 'title': jiaoyi.split('|')[1] + '【' + jiaoyi.split('|')[2] + '】',
                   'mark': jiaoyi.split('|')[3] + '， ' + jiaoyi.split('|')[4], 'huoli': jiaoyi.split('|')[5]}
    jiaoyi_list.append(jiaoyi_dict)
context['jiaoyi_list'] = jiaoyi_list

#######################################################################################################################
########################################################################################################未来趋势&介入时机
qushi_dict1 = {'type': '国内趋势（30分钟）', 'title': '上升数、下降数进入30以上', 'mark': '主力趋势指标', 'qita': ''}
qushi_dict2 = {'type': '国内趋势（60分钟）', 'title': '上升数、下降数进入30以上', 'mark': '主力趋势指标', 'qita': ''}
qushi_dict3 = {'type': '国内趋势（日线）', 'title': '上升数、下降数进入30以上，大趋势', 'mark': '主力趋势指标', 'qita': ''}
qushi_list = [qushi_dict1, qushi_dict2, qushi_dict3]
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
    zixun_type = data[i][2]
    mark = data[i][3]
    zixun_dict1 = {'type': zixun_type, 'title': title, 'mark': mark, 'qita': '需优化'}
    zixun_list.append(zixun_dict1)
context['zixun_list'] = zixun_list

#######################################################################################################################
################################################################################################################数据资源
shuju_labels = ['数据来源', '数据内容']
context['shuju_labels'] = shuju_labels
shuju_dict1 = {'shujulaiyuan': '选股宝', 'shujuneirong': '股票所属概念、概念简述',
               'zhuyi': '每周六手动执行', 'qita': '已核对'}

rt1 = RichText('持续盈利:')
rt1.add('临渊履薄', url_id=tpl.build_url_id('https://xueqiu.com/u/5377325546'))
rt2 = RichText('价值择时:')
rt2.add('亚克斯', url_id=tpl.build_url_id('https://xueqiu.com/u/4469239431'))
rt3 = RichText('价值择股:')
rt3.add('广州强', url_id=tpl.build_url_id('https://i.eastmoney.com/7289074629097176'))

shuju_dict2 = {'shujulaiyuan': '东方财富网', 'shujuneirong': rt3, 'zhuyi': '有应用监控提醒', 'qita': '已核对'}
shuju_dict3 = {'shujulaiyuan': '雪球财经', 'shujuneirong': rt1, 'zhuyi': '每交易日更新', 'qita': '已核对'}
shuju_dict4 = {'shujulaiyuan': '雪球财经', 'shujuneirong': rt2, 'zhuyi': '更新频繁', 'qita': '已核对'}
shuju_list = [shuju_dict1, shuju_dict2, shuju_dict3, shuju_dict4]
context['shuju_list'] = shuju_list

#######################################################################################################################
################################################################################################################策略概览
celve_labels = ['策略所属', '策略名称', '注意事项', '其他']
context['celve_labels'] = celve_labels
celve_dict1 = {'suoshu': '【01雪球概念】', 'mingcheng': 'ENE月线升势，布林日线下穿',
               'zhuyi': '每天10:30, 13:30', 'qita': '已核对'}
celve_dict2 = {'suoshu': '【01雪球概念】', 'mingcheng': '跨越5周线',
               'zhuyi': '每天15:10-16:00', 'qita': '已核对'}
celve_dict3 = {'suoshu': '【02指数ETF】', 'mingcheng': 'ENE月线升势，布林日线下穿',
               'zhuyi': '每天16:00-17:00', 'qita': '已核对'}
celve_dict4 = {'suoshu': '【02指数ETF】', 'mingcheng': '跨越5周线',
               'zhuyi': '每天16:00-17:00', 'qita': '已核对'}
celve_dict5 = {'suoshu': '【03全部代码】', 'mingcheng': 'ENE月线升势，布林日线下穿',
               'zhuyi': '每天15:10-16:00', 'qita': '已核对'}
celve_dict6 = {'suoshu': '【03全部代码】', 'mingcheng': '跨越5周线',
               'zhuyi': '每天15:10-16:00', 'qita': '已核对'}
celve_dict7 = {'suoshu': '【03全部代码】', 'mingcheng': '跨越5月线',
               'zhuyi': '每天18:10-19:00', 'qita': '已核对'}
celve_dict8 = {'suoshu': '【03全部代码】', 'mingcheng': '日周双孕线',
               'zhuyi': '-', 'qita': '暂不启用'}
celve_list = [celve_dict1, celve_dict2, celve_dict3, celve_dict4, celve_dict5, celve_dict6, celve_dict7, celve_dict8]
context['celve_list'] = celve_list

#######################################################################################################################
################################################################################################################血的教训
jiaoxun_list = []
jiaoxun_count = cf.get("script", "jiaoxun_count")
for i in range(1, int(jiaoxun_count) + 1):
    jiaoxun = cf.get("script", "jiaoxun" + str(i))
    jiaoxun_dict = {'mingcheng': jiaoxun.split('|')[0], 'yuanyin': jiaoxun.split('|')[1],
                    'zhuyi': jiaoxun.split('|')[2], 'qita': '-'}
    jiaoxun_list.append(jiaoxun_dict)
context['jiaoxun_list'] = jiaoxun_list

#######################################################################################################################
################################################################################################################股票跟踪
genzong_list = []
gengong_count = cf.get("script", "genzong_count")
for i in range(int(gengong_count) + 1):
    try:
        genzong = cf.get("script", "genzong" + str(i))
        image_path_result, sign_result, image_lujing = code_strategy(genzong.split('|')[1], "codeItemXXX", 120)
        image_url = "http://47.240.11.144/" + image_lujing[9:]
        print(image_url)
        if "触发" in sign_result:
            common.dingding_markdown_msg_2('触发每日投资报告有鱼[火]，有鱼[火]！' + "【涨跌幅[钉子]："
                                           + common.zhangdiefu(genzong.split('|')[1]) + "】"
                                           + genzong.split('|')[2] + sign_result,
                                           '触发每日投资报告有鱼[火]，有鱼[火]！' + "【涨跌幅[钉子]："
                                           + common.zhangdiefu(genzong.split('|')[1]) + "】"
                                           + genzong.split('|')[2] + sign_result + "\n\n> ![screenshot]("
                                           + image_url + ")")
        rt1 = RichText('')
        rt1.add(sign_result, color='#ff0000', bold=True)
        gezong_dict = {'date': genzong.split('|')[0], 'title': genzong.split('|')[2] + '【' + sign_result + '】',
                       'mark': '', 'qita': rt1, 'image_path': image_path_result}
        genzong_list.append(gezong_dict)
        time.sleep(10)
    except (IOError, TypeError, NameError, IndexError, Exception) as e:
        print(e)
context['genzong_list'] = genzong_list

#######################################################################################################################
############################################################################################################指数指标图片
image_path_399006 = common_image.plt_image_geGuZhiBiao("399006", "创业板指")
time.sleep(10)
myimage_399006 = InlineImage(tpl, image_path_399006, width=Mm(245))
context['image1'] = myimage_399006

image_path_399300 = common_image.plt_image_geGuZhiBiao("399300", "沪深300")
time.sleep(10)
myimage_399300 = InlineImage(tpl, image_path_399300, width=Mm(245))
context['image2'] = myimage_399300

#######################################################################################################################
################################################################################################################生成文件
tpl.render(context)
timeTitle = time.strftime("%Y%m%d", time.localtime())
tpl.save(rootPath + os.sep + 'report' + os.sep + '每日报告_2020.docx')
tpl.save(rootPath + os.sep + 'report' + os.sep + '每日报告_' + timeTitle + '.docx')

#######################################################################################################################
################################################################################################################同步数据
bp = ByPy()
timeStr1 = time.strftime("%Y%m%d", time.localtime())
bp.mkdir(remotepath='0000_Report')
bp.upload(localpath=rootPath + os.sep + "report", remotepath='0000_Report')
common.dingding_markdown_msg_2('触发【Report】每日投资报告执行完成', '触发【Report】每日投资报告执行完成')
