# encoding=utf-8
import os
import time
import pprint

from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties

#######################################################################################################################
# ############################################################################################### 配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
import common
import common_notion
import common_mysqlSSHUtil

import logging

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

integrations_token = "secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc"


def create_content(database_id, title, operate, is_operate, create_time):
    database = Database(
        integrations_token=integrations_token
    )
    database.retrieve_database(
        database_id=database_id, get_properties=True
    )

    PROPERTY = Properties()
    PROPERTY.set_title("title", title)
    PROPERTY.set_rich_text("操作", operate)
    PROPERTY.set_rich_text("是否操作", is_operate)
    PROPERTY.set_rich_text("时间", create_time)
    P = Page(integrations_token=integrations_token)
    P.create_page(database_id=database_id, properties=PROPERTY)


def exe(type_input, code):
    string_input = "python "
    if type_input == 'd':
        string_input = string_input + "autoDischarge.py"
    else:
        code_input = code
        price_input = "25.00"
        # 获取配置项
        dic = common_notion.find_config_item_from_database("18fcc6b54f574e97b1d6fe907260d37a")
        my_list = dic.get('chicang_list').split(",")
        count_input = "3000"

        if type_input == 's':
            string_input = string_input + "autosell.py " + code_input + " " + price_input + " " + count_input
        elif type_input == 'b':
            string_input = string_input + "autobuy.py " + code_input + " " + price_input + " " + count_input
        else:
            return "参数错误"
    print(string_input)

    # 生成命令
    # create_content(database_id="c7d5a0173e1948e3a8a52a2af6411260", title=code, operate=string_input, is_operate='否', create_time=time.strftime("%Y-%m-%d", time.localtime()))
    common_mysqlSSHUtil.insert_record(
        "INSERT INTO operate (`code`, `operate`, `is_operate`, `gmt_create`) VALUES ('" + code + "', '" + string_input + "', '" + "否" + "', '" + time.strftime("%Y-%m-%d", time.localtime()) + "');")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        type = sys.argv[1]
        code = sys.argv[2]
        exe(type, code)
    else:
        print("======================")
