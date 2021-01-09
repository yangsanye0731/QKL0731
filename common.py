import time

import numpy as num
import tushare as ts
from dingtalkchatbot.chatbot import DingtalkChatbot
import configparser

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

#######################################################################################################################
############################################################################################################读取配置文件
systemconfig_file_path = rootPath + '//resource//config//systemconfig.ini'
cf = configparser.ConfigParser()
cf.read(systemconfig_file_path, encoding='utf-8')


# 涨跌幅
def zhangdiefu(code):
    data_history_D = ts.get_k_data(code, ktype="D")
    closeArray_D = num.array(data_history_D['close'])
    return "%.2f" % (((closeArray_D[-1] - closeArray_D[-2]) / closeArray_D[-2]) * 100) + '%'


def zhangdiefu_and_price(code):
    data_history_D = ts.get_k_data(code, ktype="D")
    closeArray_D = num.array(data_history_D['close'])
    return "%.2f" % (((closeArray_D[-1] - closeArray_D[-2]) / closeArray_D[-2]) * 100) + '%', "%.2f" % closeArray_D[-1]


# 股票名称（可能为空，不推荐使用）
def gupiaomingcheng(code):
    if (code == '000001'):
        return '上证指数'
    data_realTime = ts.get_realtime_quotes(code)
    nameArray = data_realTime['name']
    return nameArray[0]


# 市净率
def shijinglv(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.daily_basic(ts_code=code, trade_date='20190419',
                         fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
    nameArray = num.array(df['pb'])
    return nameArray[0]


# EPS
def codeEPS(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.fina_indicator(ts_code=code)
    return df['eps'][0], df['basic_eps_yoy'][0], df['or_yoy'][0], df['eps'][1], df['basic_eps_yoy'][1], df['or_yoy'][1]


# 融资比
def codeRongZiBi(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6') or code.startswith('5'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.daily_basic(ts_code=code, trade_date='20191010',
                         fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,total_mv')
    nameArray = num.array(df['total_mv'])

    df = pro.query('margin_detail', trade_date='20191010')
    df = df[df.ts_code.isin([code])]
    rzye = num.array(df['rzye'])

    rongZiBi = rzye[0] / (nameArray[0] * 10000)
    return "%.4f" % rongZiBi


# 总市值
def zongshizhi(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.daily_basic(ts_code=code, trade_date='20190419',
                         fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,total_mv')
    nameArray = num.array(df['total_mv'])
    return nameArray[0]


# 基本数据
def daily_basic(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    if code.startswith('6'):
        code = code + '.SH'
    if code.startswith('0'):
        code = code + '.SZ'
    if code.startswith('3'):
        code = code + '.SZ'
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.daily_basic(ts_code=code, trade_date=timez,
                         fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

    if len(df) == 0:
        timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400))
        print(timez)
        df = pro.daily_basic(ts_code=code, trade_date=timez,
                             fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

        if len(df) == 0:
            timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 2))
            print(timez)
            df = pro.daily_basic(ts_code=code, trade_date=timez,
                                 fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

            if len(df) == 0:
                timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 3))
                print(timez)
                df = pro.daily_basic(ts_code=code, trade_date=timez,
                                     fields='ts_code,trade_date,'
                                            'turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

                if len(df) == 0:
                    timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 4))
                    print(timez)
                    df = pro.daily_basic(ts_code=code, trade_date=timez,
                                         fields='ts_code,trade_date,'
                                                'turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

                    if len(df) == 0:
                        timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 5))
                        print(timez)
                        df = pro.daily_basic(ts_code=code, trade_date=timez,
                                             fields='ts_code,trade_date,'
                                                    'turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

                        if len(df) == 0:
                            timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 6))
                            print(timez)
                            df = pro.daily_basic(ts_code=code, trade_date=timez,
                                                 fields='ts_code,trade_date,'
                                                        'turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

                            if len(df) == 0:
                                timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 7))
                                print(timez)
                                df = pro.daily_basic(ts_code=code, trade_date=timez,
                                                     fields='ts_code,trade_date,'
                                                            'turnover_rate,turnover_rate_f,volume_ratio,pe,pb,total_mv')

                                if len(df) == 0:
                                    timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 8))
                                    print(timez)
                                    df = pro.daily_basic(ts_code=code, trade_date=timez,
                                                         fields='ts_code,trade_date,turnover_rate,turnover_rate_f,'
                                                                'volume_ratio,pe,pb,total_mv')

                                    if len(df) == 0:
                                        timez = time.strftime('%Y%m%d', time.localtime(time.time() - 86400 * 9))
                                        print(timez)
                                        df = pro.daily_basic(ts_code=code, trade_date=timez,
                                                             fields='ts_code,trade_date,turnover_rate,turnover_rate_f,'
                                                                    'volume_ratio,pe,pb,total_mv')
    return df


# 股票名称
def codeName(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    df2 = df.loc[df['symbol'] == code]
    nameArray = num.array(df2['name'])
    return nameArray[0]


def codeName_and_industry(code):
    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    timez = time.strftime('%Y%m%d', time.localtime(time.time()))
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    df2 = df.loc[df['symbol'] == code]
    nameArray = num.array(df2['name'])
    industryArray = num.array(df2['industry'])
    return nameArray[0], industryArray[0]


def dingding_msg(content):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=991bba5d439fb424f4ab1645a86aa353ac89e92352d11e1f44846a0bca812862'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_text(msg=content, is_at_all=False, at_mobiles=at_mobiles)


def dingding_markdown_msg(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=991bba5d439fb424f4ab1645a86aa353ac89e92352d11e1f44846a0bca812862'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


########################################################################################################################
######################################################################################################【01】每日趋势钉钉群
def dingding_markdown_msg_2(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=d62051ad4dd53ae281ef9cb2e7258041a9a0d086bc5bb14612b508930ebd1666'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


########################################################################################################################
######################################################################################################【02】雪球指数钉钉群
def dingding_markdown_msg_02(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=44aed8fcbb24037e166ac9848c55bbe5a955ceea2a62efc5eb743040f70c07c1'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


########################################################################################################################
##################################################################################################### 【03】指数ETF钉钉群
def dingding_markdown_msg_03(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=e6e0ace0004798b428470dda7a0d5760e0043f1bd087eec9d74848378bec043e'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


########################################################################################################################
################################################################################################## 【04】Report报告钉钉群
def dingding_markdown_msg_04(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=fe46cb39d4ce1046cede9896390938f3b33744806feccb249230251f6ba3f49a'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


########################################################################################################################
######################################################################################################### 统一钉钉消息发布
def dingding_markdown_msg_final(groupname, title, text):
    # WebHook地址
    dingding_url = cf.get("DingDing", groupname)
    webhook = dingding_url
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


def dingding_markdown_msg_link(title, text, url):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=7073587d80b34d698a2656dfa1d4aaffb18510c658b1ef12bf2b8cfebb3976cc'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_link(title=title, text=text, message_url=url)


def dingding_markdown_msg_ene(title, text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/' \
              'send?access_token=7073587d80b34d698a2656dfa1d4aaffb18510c658b1ef12bf2b8cfebb3976cc'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息@所有人
    at_mobiles = ['17706417762']
    xiaoding.send_markdown(title=title, text=text, is_at_all=False, at_mobiles=at_mobiles)


# print(zhangdiefu('399006'))
# dingding_markdown_msg_final("dingding01", "触发test", "触发test")
