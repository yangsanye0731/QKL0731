#encoding=utf-8
import pymysql
import configparser
from os import path
import common_zhibiao
import common
import time

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
    deleteSql = "delete from AGU_ZhiShu where type =\'ZXG\'"
    cursor.execute(deleteSql)
    db.commit()
    db.close()

def deleteTopRecord():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    deleteSql = "delete from AGU_ZhiShu where type =\'TOP\'"
    cursor.execute(deleteSql)
    db.commit()
    db.close()

def insert_strategy_record(code, strategy_name, chushi_cash, jieshu_cash):
    sql = "INSERT INTO `superman`.`HUICE_Strategy`(strategy_name`, `code`, `chushi_cash`, `jieshu_cash`, `input_date`) VALUES (" \
          "'" + strategy_name + "', " \
          "'" + code + "', " \
          "'" + chushi_cash + "', " \
          "'" + jieshu_cash + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)

def insert_zhishu_record(code, name, fullName, mark, type):
    price, MA20_titile, MA30_titile, qushi_5_10_20_30, KDJ_J_title, MACD_title, BULL_title = common_zhibiao.zhibiao(code, 'D')
    price_60, MA20_titile_60, MA30_titile_60, qushi_5_10_20_30_60, KDJ_J_title_60, MACD_title_60, BULL_title_60 = common_zhibiao.zhibiao(code, '60')
    price_30, MA20_titile_30, MA30_titile_30, qushi_5_10_20_30_30, KDJ_J_title_30, MACD_title_30, BULL_title_30 = common_zhibiao.zhibiao(code, '30')
    zhangdiefu = common.zhangdiefu(code)
    print(fullName + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    title = fullName + zhangdiefu + MACD_title + KDJ_J_title + MA20_titile + " "
    content = "#### **<font color=#FF0000 size=6 face=\"微软雅黑\">" + fullName
    # + " " + "%.3f" % closeArray[-1] + " " + zhangdiefu + "</font>**\n" + MIN30_60MA_content + str15QuShi_content + str30QuShi_content + strBULL60
    # print(time.localtime().tm_hour)
    # if (time.localtime().tm_hour > 14):
    #    common_image.plt_image_geGuZhiBiao(code, fullName)
    mingcheng = fullName
    sql = "INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `code`, `price`, `zhangdiefu`, `type`, " \
          "`ri_qushi_20junxian`, `ri_qushi_30junxian`, `ri_qushi_5_10_20_30`, `ri_MACD`, `ri_KDJ`, `ri_BULL`, " \
          "`60_qushi_20junxian`, `60_qushi_30junxian`, `60_qushi_5_10_20_30`, `60_MACD`, `60_KDJ`, `60_BULL`, " \
          "`30_qushi_20junxian`, `30_qushi_30junxian`, `30_qushi_5_10_20_30`, `30_MACD`, `30_KDJ`, `30_BULL`,`beizhu`, `insert_time`) VALUES (" \
          "'" + mingcheng + "', " \
          "'" + code + "', " \
          "'" + price + "', " \
          "'" + zhangdiefu + "', " \
          "'" + type + "', " \
          "'" + MA20_titile + "', " \
          "'" + MA30_titile + "', " \
          "'" + qushi_5_10_20_30 + "', " \
          "'" + MACD_title + "', " \
          "'" + KDJ_J_title + "', " \
          "'" + BULL_title + "', " \
          "'" + MA20_titile_60 + "', " \
          "'" + MA30_titile_60 + "', " \
          "'" + qushi_5_10_20_30_60 + "', " \
          "'" + MACD_title_60 + "', " \
          "'" + KDJ_J_title_60 + "', " \
          "'" + BULL_title_60 + "', " \
          "'" + MA20_titile_30 + "', " \
          "'" + MA30_titile_30 + "', " \
          "'" + qushi_5_10_20_30_30 + "', " \
          "'" + MACD_title_30 + "', " \
          "'" + KDJ_J_title_30 + "', " \
          "'" + BULL_title_30 + "', " \
          "'" + mark + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"

    print(sql)
    insertRecord(sql)
    return title, content

#insertRecord("INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `zhangdifu`, `30zhi`, `60zhi`) VALUES ('2', '2', '2', '2');")