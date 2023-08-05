# encoding=utf-8
import os
import time

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name

from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties

integrations_token = "secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc"


def create_content(database_id, title, ce_lve_lei_xing, tu_pian, mark):
    database = Database(
        integrations_token=integrations_token
    )
    database.retrieve_database(
        database_id=database_id, get_properties=True
    )
    print(database.properties_list)

    PROPERTY = Properties()
    PROPERTY.set_title("title", title)
    PROPERTY.set_rich_text("策略类型", ce_lve_lei_xing)
    PROPERTY.set_rich_text("备注", mark)
    PROPERTY.set_rich_text("插入时间", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    PROPERTY.set_files("图片", files_list=[tu_pian])
    P = Page(integrations_token=integrations_token)
    P.create_page(database_id=database_id, properties=PROPERTY)


def clear_database(database_id):
    database = Database(
        integrations_token=integrations_token
    )
    database.find_all_page(database_id=database_id)
    for item in database.result["results"]:
        print(item["id"])
        P = Page(integrations_token=integrations_token)
        P.archive_page(page_id=item["id"], archived=True)


# create_content("163fe8f3baa744c2922f78657a7e7066","title", "ce_lve_lei_xing", "tu_pian", "mark")
# clear_database("163fe8f3baa744c2922f78657a7e7066")
