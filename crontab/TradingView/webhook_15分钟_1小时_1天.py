# encoding=utf-8
import numpy as num
import talib as ta
import tushare as ts
import time

#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
import common_image
import common
import common_mysqlUtil


#######################################################################################################################
###########################################################################################################跨域5周线策略
def exec(argv):
    codeItem = argv[1]
    print(codeItem)
    data = common_mysqlUtil.select_all_code_one(codeItem)
    if len(data) > 0:
        codeName = data[0][1]
    print(codeName)
    image_path = common_image.plt_image_geGuZhiBiao_tradingview(codeItem, codeName)
    image_url = "http://" + "8.218.97.91:8080" + "/" + image_path[6:]

    print(image_path)
    print(image_url)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    zhangdiefu,price = common.zhangdiefu_and_price(codeItem)
    common.dingding_markdown_msg_03(time_str + '触发TradingView策略' + codeName + '(' + codeItem + ')' + '当前价格：' + price + '涨跌幅：' + zhangdiefu,
                                    time_str + '触发TradingView策略' + codeName + '(' + codeItem + ')' + '当前价格：' + price + '涨跌幅：' + zhangdiefu
                                    + "\n\n> ![screenshot](" + image_url + ")")
    return image_path


#######################################################################################################################
##############################################################################################################主执行程序
if __name__ == "__main__":
    exec(sys.argv)
