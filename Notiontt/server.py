# encoding=utf-8
import rpyc
import subprocess
import time
import datetime

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

import logging

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

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


class RemoteCommandsService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")

    def on_disconnect(self, conn):
        print("Client disconnected.")

    def exposed_execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            # print(result)

            if "autobuy.py" in command or "autosell.py" in command:
                # 同步Notion
                word_list = command.split()
                create_content(database_id="c7d5a0173e1948e3a8a52a2af6411260", title=word_list[2], operate=command,
                               is_operate='是', create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # # 记录操作日志
            # common_mysqlSSHUtil.insert_record(
            #     "INSERT INTO operate (`code`, `operate`, `is_operate`, `gmt_create`) VALUES ('" + "code" + "', '" +
            #     command + "', '" + "是" + "', '" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "');")
            # # 返回信息
            return result
        except subprocess.CalledProcessError as e:
            print(e.output)
            # return f"Error executing command: {e.output}"
        except UnicodeDecodeError as e:
            print(e.output)


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(RemoteCommandsService, port=18861)
    server.start()
