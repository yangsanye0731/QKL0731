# encoding=utf-8
import os
import time
import pprint

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name

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

import logging

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

integrations_token = "secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc"


def create_content(database_id, title, ce_lve_lei_xing, tu_pian, mark, gai_nian, code, create_time):
    database = Database(
        integrations_token=integrations_token
    )
    database.retrieve_database(
        database_id=database_id, get_properties=True
    )

    PROPERTY = Properties()
    if code is not None:
        PROPERTY.set_title("title", title + "(" + common.zhangdiefu(code) + ")")
    else:
        PROPERTY.set_title("title", title)
    PROPERTY.set_rich_text("策略类型", ce_lve_lei_xing)
    PROPERTY.set_rich_text("备注", mark)
    gai_nian = gai_nian.strip()
    PROPERTY.set_rich_text("概念", gai_nian)
    PROPERTY.set_rich_text("插入时间", create_time)
    if tu_pian is not None:
        PROPERTY.set_files("图片", files_list=[tu_pian])
    P = Page(integrations_token=integrations_token)
    P.create_page(database_id=database_id, properties=PROPERTY)


def clear_database(database_id):
    database = Database(
        integrations_token=integrations_token
    )
    database.find_all_page(database_id=database_id)
    for item in database.result["results"]:
        P = Page(integrations_token=integrations_token)
        P.archive_page(page_id=item["id"], archived=True)


def find_config_item_from_database(database_id):
    database = Database(
        integrations_token=integrations_token
    )
    database.find_all_page(database_id=database_id)
    # pprint.pprint(database.result)
    dic = {}
    for item in database.result["results"]:
        name = item["properties"]["Name"]["title"][0]["plain_text"]
        value = item["properties"]["value"]["rich_text"][0]["plain_text"]
        dic[name] = value

    logging.info("配置项集合：%s", dic)
    return dic


# find_config_item_from_database('18fcc6b54f574e97b1d6fe907260d37a')
# create_content("163fe8f3baa744c2922f78657a7e7066","title", "ce_lve_lei_xing", "tu_pian", "mark")
# clear_database("163fe8f3baa744c2922f78657a7e7066")
# create_content(database_id="355a99d2c49a49749fc329cc2606fcda", title="codeName",
#                ce_lve_lei_xing='60天双均线金叉', tu_pian=None,
#                mark="", gai_nian="雪球概念", code=None, create_time="2023-08-01")
