# encoding=utf-8
import time

import pymysql
from sshtunnel import SSHTunnelForwarder
#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

#######################################################################################################################
############################################################################################################读取配置文件



def get_tunnel():
    # 创建SSH隧道
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(mysql_host, mysql_port)
    ) as tunnel:
        return tunnel


def insert_record(sql):
    # 创建SSH隧道
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(mysql_host, mysql_port)
    ) as tunnel:
        # 连接到MySQL数据库
        db_connection = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=mysql_username,
            passwd=mysql_password,
            db=mysql_db
        )
        cursor = db_connection.cursor()

        # 执行查询等操作
        cursor.execute(sql)
        db_connection.commit()

        # 关闭连接
        cursor.close()
        db_connection.close()


def select_record(sql):
    # 创建SSH隧道
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(mysql_host, mysql_port)
    ) as tunnel:
        # 连接到MySQL数据库
        db_connection = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=mysql_username,
            passwd=mysql_password,
            db=mysql_db
        )
        cursor = db_connection.cursor()

        # 执行查询等操作
        cursor.execute(sql)
        data = cursor.fetchall()

        # 关闭连接
        cursor.close()
        db_connection.close()

        return data


def insert_record_with_tunnel(tunnel, sql):
    # 连接到MySQL数据库
    db_connection = pymysql.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=mysql_username,
        passwd=mysql_password,
        db=mysql_db
    )
    cursor = db_connection.cursor()

    # 执行查询等操作
    cursor.execute(sql)
    db_connection.commit()

    # 关闭连接
    cursor.close()
    db_connection.close()


def select_record_with_tunnel(tunnel, sql):
    # 连接到MySQL数据库
    db_connection = pymysql.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=mysql_username,
        passwd=mysql_password,
        db=mysql_db
    )
    cursor = db_connection.cursor()

    # 执行查询等操作
    cursor.execute(sql)
    data = cursor.fetchall()

    # 关闭连接
    cursor.close()
    db_connection.close()
    return data

# insert_record(
#     "INSERT INTO operate (`code`, `operate`, `is_operate`, `gmt_create`) VALUES ('1', '1', '1', '2023-08-31 18:16:57');")
