#encoding=utf-8
import pymysql
import configparser
from os import path

#读取配置配置文件
config_file = path.join(path.dirname(__file__), 'config.conf')
cf = configparser.ConfigParser()
cf.read(config_file)

def insertRecord(sql):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    db.commit()
    db.close()

def deleteRecord():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    deleteSql = "delete from AGU_ZhiShu"
    cursor.execute(deleteSql)
    db.commit()
    db.close()

#insertRecord("INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `zhangdifu`, `30zhi`, `60zhi`) VALUES ('2', '2', '2', '2');")