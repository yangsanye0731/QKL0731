#encoding=utf-8
from mark.email_util import *
import common_mysqlUtil

def strategy(code, name, fullName, mark):
    title, content = common_mysqlUtil.insert_zhishu_record(code, name, fullName, " ", mark,"ZXG")
    return title, content

#######################################################################################################
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
############################################ 邮件发送###################################################
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#####                                                                                             #####
#######################################################################################################
# 趋势 标识：30分钟60均线处于向上态势
# 上好 表示：30分钟 5、10、20、30均线 处于依次叠加良好形态
# 买 表示：30分钟 5、10、20、30均线 均处于向上态势
def pinjie(title, titleTmp, content, contentTmp):
     # if (("趋势" in title or "上好" in title) and "买" in title):
     if ("上升" in content):
          titleTmp = title + " " + titleTmp
          contentTmp = content + contentTmp
     # else:
     #      titleTmp = titleTmp + title
     #      contentTmp = contentTmp + "***\n\n" + content

     return titleTmp, contentTmp

#清空数据库
common_mysqlUtil.deleteRecord()
titleTmp = ""
contentTmp = ""
str_cy, content_cy = strategy("399006", "创业板指", "创业板指", " ")
# titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str_sz, content_sz = strategy("399001", "深证成指", "深证成指", " ")
# titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str1, content1 = strategy("399975", "证券公司", "证券公司", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)
#################################################################################################################BBBBBB
str17, content17 = strategy("002594", "比亚迪", "比亚迪", " ")
titleTmp, contentTmp = pinjie(str17, titleTmp, content17, contentTmp)

str20, content20 = strategy("300294", "博雅生物", "博雅生物", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("002649", "博彦科技", "博彦科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################CCCCCC
str2, content2 = strategy("000625", " 长安汽车", "长安汽车", " ")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

str2, content2 = strategy("002010", "传化智联", "传化智联", "传化智联备注信息")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

str2, content2 = strategy("300036", "超图软件", "超图软件", "传化智联备注信息")
titleTmp, contentTmp = pinjie(str2, titleTmp, content2, contentTmp)

#################################################################################################################DDDDDD
str4, content4 = strategy("002008", "大族激光", "大族激光", " ")
titleTmp, contentTmp = pinjie(str4, titleTmp, content4, contentTmp)

str9, content9 = strategy("300059", "东方财富", "东方财富", " ")
titleTmp, contentTmp = pinjie(str9, titleTmp, content9, contentTmp)

str20, content20 = strategy("002236", "大华股份", "大华股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################EEEEEE
str20, content20 = strategy("002812", "恩捷股份", "恩捷股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################FFFFFF
str5, content5 = strategy("600498", "烽火通信", "烽火通信", " ")
titleTmp, contentTmp = pinjie(str5, titleTmp, content5, contentTmp)

#################################################################################################################GGGGGG
str1, content1 = strategy("002281", "光迅科技", "光迅科技", " ")
titleTmp, contentTmp = pinjie(str1, titleTmp, content1, contentTmp)

str12, content12 = strategy("300537", "广信材料", "广信材料", " ")
titleTmp, contentTmp = pinjie(str12, titleTmp, content12, contentTmp)

str13, content13 = strategy("300480", "光力科技", "光力科技", " ")
titleTmp, contentTmp = pinjie(str13, titleTmp, content13, contentTmp)

str8, content8 = strategy("300251", "光线传媒", "光线传媒", " ")
titleTmp, contentTmp = pinjie(str8, titleTmp, content8, contentTmp)

str20, content20 = strategy("002074", "国轩高科", "国轩高科", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300699", "光威复材", "光威复材", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600589", "广东榕泰", "广东榕泰", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300499", "高澜股份", "高澜股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("002741", "光华科技", "光华科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################HHHHHH
str10, content10 = strategy("300584", "海辰药业", "海辰药业", " ")
titleTmp, contentTmp = pinjie(str10, titleTmp, content10, contentTmp)

str14, content14 = strategy("300462", "华铭智能", "华铭智能", " ")
titleTmp, contentTmp = pinjie(str14, titleTmp, content14, contentTmp)

str20, content20 = strategy("600271", "航天信息", "航天信息", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("000988", "华工科技", "华工科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600570", "恒生电子", "恒生电子", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("002415", "海康威视", "海康威视", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################JJJJJJ
str15, content15 = strategy("002020", "京新药业", "京新药业", " ")
titleTmp, contentTmp = pinjie(str15, titleTmp, content15, contentTmp)

str20, content20 = strategy("300203", "聚光科技", "聚光科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("000656", "金科股份", "金科股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################KKKKKK
str20, content20 = strategy("002230", "科大讯飞", "科大讯飞", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("002022", "科华生物", "科华生物", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600422", "昆药集团", "昆药集团", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600260", "凯乐科技", "凯乐科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300662", "科锐国际", "科锐国际", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300234", "开尔新材", "开尔新材", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################LLLLLL
str18, content18 = strategy("300691", "联合光电", "联合光电", " ")
titleTmp, contentTmp = pinjie(str18, titleTmp, content18, contentTmp)

#################################################################################################################MMMMMM
str20, content20 = strategy("300586", "美联新材", "美联新材", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################NNNNNN
str20, content20 = strategy("300068", "南都电源", "南都电源", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################PPPPPP
str6, content6 = strategy("000739", " 普洛药业", "普洛药业", " ")
titleTmp, contentTmp = pinjie(str6, titleTmp, content6, contentTmp)

str11, content11 = strategy("300664", "鹏鹞环保", "鹏鹞环保", " ")
titleTmp, contentTmp = pinjie(str11, titleTmp, content11, contentTmp)

str11, content11 = strategy("300438", "鹏辉能源", "鹏辉能源", " ")
titleTmp, contentTmp = pinjie(str11, titleTmp, content11, contentTmp)

#################################################################################################################RRRRRR
str16, content16 = strategy("300576", "容大感光", "容大感光", " ")
titleTmp, contentTmp = pinjie(str16, titleTmp, content16, contentTmp)

#################################################################################################################SSSSSS
str20, content20 = strategy("000603", "盛达矿业", "盛达矿业", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("600703", "三安光电", "三安光电", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("000034", "神州数码", "神州数码", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("603881", "数据港", "数据港", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("002796", "世嘉科技", "世嘉科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################TTTTTT
str20, content20 = strategy("000877", "天山股份", "天山股份", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################WWWWWW
str20, content20 = strategy("300017", "网宿科技", "网宿科技", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("300253", "卫宁健康", "卫宁健康", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("000338", "潍柴动力", "潍柴动力", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################XXXXXX
str20, content20 = strategy("000997", "新大陆", "新大陆", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str3, content3 = strategy("300136", " 信维通信", "信维通信", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

str3, content3 = strategy("600587", " 新华医疗", "新华医疗", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

str3, content3 = strategy("300450", " 先导智能", "先导智能", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

str3, content3 = strategy("300207", " 欣旺达", "欣旺达", " ")
titleTmp, contentTmp = pinjie(str3, titleTmp, content3, contentTmp)

#################################################################################################################YYYYYY
str20, content20 = strategy("002182", "云海金属", "云海金属", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str7, content7 = strategy("300328", " 宜安科技", "宜安科技", " ")
titleTmp, contentTmp = pinjie(str7, titleTmp, content7, contentTmp)

str7, content7 = strategy("600066", " 宇通客车", "宇通客车", " ")
titleTmp, contentTmp = pinjie(str7, titleTmp, content7, contentTmp)

#################################################################################################################ZZZZZZ
str19, content19 = strategy("600489", "中金黄金", "中金黄金", " ")
titleTmp, contentTmp = pinjie(str19, titleTmp, content19, contentTmp)

str20, content20 = strategy("600036", "招商银行", "招商银行", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("603127", "昭衍新药", "昭衍新药", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("603338", "浙江鼎力", "浙江鼎力", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("603986", "兆易创新", "兆易创新", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

#################################################################################################################ETFETF
str20, content20 = strategy("512480", "半导体", "半导体ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("515000", "科技ETF", "科技ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("512930", "AIETF", "AIETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("159934", "黄金ETF", "黄金ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

str20, content20 = strategy("512690", "酒ETF", "酒ETF", " ")
titleTmp, contentTmp = pinjie(str20, titleTmp, content20, contentTmp)

title = str_cy + str_sz + titleTmp
mulu = "# **<font color=#FF0000 size=6 face=\"微软雅黑\">每日简报 " + time.strftime("%m-%d %H:%M", time.localtime()) + "</font>**\n\n"
content = content_cy + content_sz + contentTmp

# 发送信息
# common.dingding_markdown_msg_2(title,content)
# 发送邮件
# sendMail(title + "<br><br><br><br>" + content, title)


