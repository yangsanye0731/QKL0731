# encoding=utf-8
import rpyc
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
import warnings

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties


# 远程调用
def execute_remote_command(command):
    # conn = rpyc.connect("192.168.233.128", 18861)  # 替换为服务器的IP地址
    conn = rpyc.connect("localhost", 18861)  # 替换为服务器的IP地址
    conn._config['sync_request_timeout'] = 1200
    remote_service = conn.root

    result = remote_service.exposed_execute_command(command)
    conn.close()
    return result


class PropertyItem:
    def __init__(self, id, command, property):
        self.id = id
        self.command = command
        self.property = property


# 根据状态查询记录
def query_database_by_op_status(status):
    database = Database(integrations_token="secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc")
    database.run_query_database(database_id="ff1187eb3ca74d18839e1e306cb83387",
                                db_filter={
                                    "and": [
                                        {
                                            "property": "执行状态",
                                            "checkbox": {
                                                "equals": status
                                            }
                                        },
                                        {
                                            "property": "Tags",
                                            "multi_select": {
                                                "contains": "OP"
                                            }
                                        }
                                    ]
                                })
    item = database.result["results"]
    p_array = []
    for item in database.result["results"]:
        id = item["id"]
        command = ""
        for select_item in item["properties"]["命令"]["rich_text"]:
            command = select_item["plain_text"]
        PROPERTY = Properties()
        PROPERTY.set_rich_text("命令", command)
        PROPERTY.set_checkbox("执行状态", status)

        p_array.append(PropertyItem(id, command, PROPERTY))

    return p_array


def op_exe():
    print("执行自动Notion命令")
    # 获取待执行的列表
    p_array = query_database_by_op_status(False)
    for propertyItem in p_array:
        # 执行命令
        print("执行命令：" + propertyItem.command)
        execute_remote_command(propertyItem.command)
        # 更新状态
        PROPERTY = propertyItem.property
        PROPERTY.set_checkbox("执行状态", True)
        P = Page(integrations_token="secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc")
        P.update_page(page_id=propertyItem.id, properties=PROPERTY)

