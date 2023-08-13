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

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
print(rootPath1)
import common_image
import common_mysqlUtil
import common
import common_notion
import logging
from datetime import datetime, timedelta

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
import traceback


#######################################################################################################################
###########################################################################################################跨域5周线策略
def strategy(zhouqi, endstr, database_id):
    # 局部变量初始化
    count = 0
    count_b = 0
    count_e = 0

    ts.set_token('a0a3a3ee133d6623bf9072236a5a8423c1c021d00aba3eb0c7bdfa5e')
    pro = ts.pro_api()
    all_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # all_code = ts.get_stock_basics()
    all_code = all_code[1:-1].ts_code
    all_code_index_x = num.array(all_code)

    time_str = endstr
    fo = open("跨越5周_" + zhouqi + "_" + time_str + ".txt", "w")
    fo_10 = open("双均线10_" + zhouqi + "_" + time_str + ".txt", "w")
    fo_60 = open("双均线60_" + zhouqi + "_" + time_str + ".txt", "w")
    fo_144 = open("双均线144_" + zhouqi + "_" + time_str + ".txt", "w")

    # 遍历
    for codeItem in all_code_index_x:
        try:
            codeItem = codeItem[0:6]
            print(codeItem)
            # time.sleep(0.5)
            count = count + 1
            print(count)

            data_history = ts.get_hist_data(codeItem, ktype=zhouqi, end=endstr)
            data_history = data_history.iloc[::-1]

            closeArray = num.array(data_history['close'])
            doubleCloseArray = num.asarray(closeArray, dtype='double')

            codeName = ''
            data = common_mysqlUtil.select_all_code_one(codeItem)
            if len(data) > 0:
                codeName = data[0][1]

            # highArray = num.array(data_history['high'])
            # doubleHighArray = num.asarray(highArray, dtype='double')

            # openArray = num.array(data_history['open'])
            # doubleOpenArray = num.asarray(openArray, dtype='double')

            # 均线
            ma10 = ta.SMA(doubleCloseArray, timeperiod=10)
            sma10 = ta.EMA(ma10, timeperiod=10)

            ma60 = ta.SMA(doubleCloseArray, timeperiod=60)
            sma60 = ta.EMA(ma60, timeperiod=60)

            ma144 = ta.SMA(doubleCloseArray, timeperiod=144)
            sma144 = ta.EMA(ma144, timeperiod=144)

            mark = ""
            if ma10[-1] > sma10[-1] and ma10[-2] < sma10[-2]:
                print("双均线10：" + codeItem)
                fo_10.write(codeItem + "\n")
                image_path, gai_nian = common_image.plt_image_tongyichutu_2(codeItem,
                                                                            "D",
                                                                            "【全部代码】双均线10",
                                                                            "【全部代码】双均线10", time_str, mark, 'multi')
                image_url = "http://" + "8.218.97.91:8080" + "/" + image_path[6:]
                logging.debug("图片URL：%s", image_path)
                common_notion.create_content(database_id=database_id, title=codeName,
                                             ce_lve_lei_xing='10天双均线金叉', tu_pian=image_url,
                                             mark=mark, gai_nian=gai_nian, code=codeItem, create_time=time_str)

            if ma60[-1] > sma60[-1] and ma60[-2] < sma60[-2]:
                print("双均线60：" + codeItem)
                fo_60.write(codeItem + "\n")
                image_path, gai_nian = common_image.plt_image_tongyichutu_2(codeItem,
                                                                            "D",
                                                                            "【全部代码】双均线60",
                                                                            "【全部代码】双均线60", time_str, mark, 'multi')

                image_url = "http://" + "8.218.97.91:8080" + "/" + image_path[6:]
                logging.debug("图片URL：%s", image_path)
                common_notion.create_content(database_id=database_id, title=codeName,
                                             ce_lve_lei_xing='60天双均线金叉', tu_pian=image_url,
                                             mark=mark, gai_nian=gai_nian, code=codeItem, create_time=time_str)

            if ma144[-1] > sma144[-1] and ma144[-2] < sma144[-2]:
                print("双均线144：" + codeItem)
                fo_144.write(codeItem + "\n")
                image_path, gai_nian = common_image.plt_image_tongyichutu_2(codeItem,
                                                                            "D",
                                                                            "【全部代码】双均线144",
                                                                            "【全部代码】双均线144", time_str, mark, 'multi')

                image_url = "http://" + "8.218.97.91:8080" + "/" + image_path[6:]
                logging.debug("图片URL：%s", image_path)
                common_notion.create_content(database_id=database_id, title=codeName,
                                             ce_lve_lei_xing='144天双均线金叉', tu_pian=image_url,
                                             mark=mark, gai_nian=gai_nian, code=codeItem, create_time=time_str)

                count_b = count_b + 1
        except (IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)
            traceback.print_exc()
            # common.dingding_markdown_msg_03("触发AGU_全部股票_双均线执行异常", "触发AGU_全部股票_双均线执行异常")
    return count_b, count_e


#######################################################################################################################
##############################################################################################################主执行程序
if __name__ == "__main__":
    # 获取命令行参数数量（不包括脚本文件名）
    num_args = len(sys.argv) - 1
    if num_args < 1:
        time_str1 = time.strftime("%Y-%m-%d", time.localtime())
        database_id = "32967c2c42a84cec94d65e8c7cf163f2"
        count_result_b, count_result_e = strategy('D', time_str1, database_id)
        # image_url = "http://" + "8.218.97.91:8080" + "software/QKL0731/crontab/AMarcket/双均线10" + image_path[6:]
        # common_notion.create_content(database_id=database_id, title=time_str1 + "文件",
        #                              ce_lve_lei_xing='10天双均线金叉', tu_pian=image_url,
        #                              mark=mark, gai_nian=gai_nian, code=codeItem, create_time=time_str)

        common.dingding_markdown_msg_02("触发AGU_全部股票_双均线执行完成", "触发AGU_全部股票_双均线执行完成")
    else:
        logging.info("开始策略回测逻辑")
        # Notion数据库ID：任务跟踪（Auto）（回测）
        database_id = "472afd1c0f3541fea9f4e132ae1a430e"

        # 按月进行回测,回测1月份数据
        # 设置起始日期为2023年1月1日
        start_date = datetime(2023, 7, 1)

        # 计算结束日期为2023年2月1日（不包含2月1日）
        end_date = datetime(2023, 7, 10)

        # 循环遍历日期
        current_date = start_date
        while current_date < end_date:
            time_str1 = current_date.strftime('%Y-%m-%d')
            time_str2 = current_date.strftime('%Y%m')
            strategy(zhouqi='D', endstr=time_str1, database_id=database_id)
            current_date += timedelta(days=1)
