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

def deleteTopRecord(type):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    deleteSql = "delete from AGU_ZhiShu where type =\'" + type + "\'"
    cursor.execute(deleteSql)
    db.commit()
    db.close()

def insert_strategy_record(code, name, rongzibi, epsup, yingyeup, wuzhouxian, strategy_name, chushi_cash, jieshu_cash):
    sql = "INSERT INTO `superman`.`HUICE_Strategy`(`strategy_name`, `name`, `code`, `rongzibi`,`epsup`, `yingyeup`,`wuzhouxian`,`chushi_cash`, `jieshu_cash`, `input_date`) VALUES (" \
          "'" + strategy_name + "', " \
          "'" + name + "', " \
          "'" + code + "', " \
          "'" + rongzibi + "', " \
          "'" + epsup + "', " \
          "'" + yingyeup + "', " \
          "'" + wuzhouxian + "', " \
          "'" + chushi_cash + "', " \
          "'" + jieshu_cash + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)

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

def selectCountRecord(type):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "select count(1) AS `总数`," \
          "count((case when locate('均线5、10、20、30齐升',`AGU_ZhiShu`.`ri_qushi_5_10_20_30`) then 1 else NULL end)) AS `上升数`," \
          "count((case when locate('均线5、10、20、30齐降',`AGU_ZhiShu`.`ri_qushi_5_10_20_30`) then 1 else NULL end)) AS `下降数`," \
          "count((case when locate('均线5、10、20、30齐升',`AGU_ZhiShu`.`60_qushi_5_10_20_30`) then 1 else NULL end)) AS `60上升数`," \
          "count((case when locate('均线5、10、20、30齐降',`AGU_ZhiShu`.`60_qushi_5_10_20_30`) then 1 else NULL end)) AS `60下降数`," \
          "count((case when locate('均线5、10、20、30齐升',`AGU_ZhiShu`.`30_qushi_5_10_20_30`) then 1 else NULL end)) AS `30上升数`," \
          "count((case when locate('均线5、10、20、30齐降',`AGU_ZhiShu`.`30_qushi_5_10_20_30`) then 1 else NULL end)) AS `30下降数` " \
          "from `AGU_ZhiShu` where (`AGU_ZhiShu`.`type` = '" + type + "')"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def insert_zhishu_record(code, name, fullName, mark, type):
    price, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, KDJ_J_title, MACD_title, BULL_title, BULL_middleband = common_zhibiao.zhibiao(code, 'D')
    price_60, MA20_titile_60, MA30_titile_60, MA60_titile_60, qushi_5_10_20_30_60, KDJ_J_title_60, MACD_title_60, BULL_title_60, BULL_middleband_60 = common_zhibiao.zhibiao(code, '60')
    price_30, MA20_titile_30, MA30_titile_30, MA60_titile_30, qushi_5_10_20_30_30, KDJ_J_title_30, MACD_title_30, BULL_title_30, BULL_middleband_30 = common_zhibiao.zhibiao(code, '30')
    zhangdiefu = common.zhangdiefu(code)
    print(fullName + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    title = fullName + zhangdiefu + " "
    content = fullName + zhangdiefu + qushi_5_10_20_30_30 + "<br>"
    # + " " + "%.3f" % closeArray[-1] + " " + zhangdiefu + "</font>**\n" + MIN30_60MA_content + str15QuShi_content + str30QuShi_content + strBULL60
    # print(time.localtime().tm_hour)
    # if (time.localtime().tm_hour > 14):
    #    common_image.plt_image_geGuZhiBiao(code, fullName)
    mingcheng = fullName
    sql = "INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `code`, `price`, `zhangdiefu`, `type`, " \
          "`ri_qushi_20junxian`, `ri_qushi_30junxian`, `ri_qushi_60junxian`, `ri_qushi_5_10_20_30`, `ri_MACD`, `ri_KDJ`, `ri_BULL`, `ri_BULL_middle`, " \
          "`60_qushi_20junxian`, `60_qushi_30junxian`, `60_qushi_5_10_20_30`, `60_MACD`, `60_KDJ`, `60_BULL`, " \
          "`30_qushi_20junxian`, `30_qushi_30junxian`, `30_qushi_60junxian`, `30_qushi_5_10_20_30`, `30_MACD`, `30_KDJ`, `30_BULL`, `30_BULL_middle`, `beizhu`, `insert_time`) VALUES (" \
          "'" + mingcheng + "', " \
          "'" + code + "', " \
          "'" + price + "', " \
          "'" + zhangdiefu + "', " \
          "'" + type + "', " \
          "'" + MA20_titile + "', " \
          "'" + MA30_titile + "', " \
          "'" + MA60_titile + "', " \
          "'" + qushi_5_10_20_30 + "', " \
          "'" + MACD_title + "', " \
          "'" + KDJ_J_title + "', " \
          "'" + BULL_title + "', " \
          "'" + BULL_middleband + "', " \
          "'" + MA20_titile_60 + "', " \
          "'" + MA30_titile_60 + "', " \
          "'" + qushi_5_10_20_30_60 + "', " \
          "'" + MACD_title_60 + "', " \
          "'" + KDJ_J_title_60 + "', " \
          "'" + BULL_title_60 + "', " \
          "'" + MA20_titile_30 + "', " \
          "'" + MA30_titile_30 + "', " \
          "'" + MA60_titile_30 + "', " \
          "'" + qushi_5_10_20_30_30 + "', " \
          "'" + MACD_title_30 + "', " \
          "'" + KDJ_J_title_30 + "', " \
          "'" + BULL_title_30 + "', " \
          "'" + BULL_middleband_30 + "', " \
          "'" + mark + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"

    print(sql)
    insertRecord(sql)

    if (("60均线上行" in MA60_titile_30) and "下穿布林线下沿" in BULL_title_30):
        insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发30分钟60均线上行，下穿30分钟布林线下沿")

    if (("60均线上行" in MA60_titile) and "下穿布林线下沿" in BULL_title):
        insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发60日均线上行，下穿日布林线下沿")

    if ("创业板指" in mingcheng or "深证成指" in mingcheng or "ETF" in mingcheng):
        if ("上穿布林线上沿" in BULL_title_30):
            insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发上穿30分钟布林线上沿")
        if ("上穿布林线上沿" in BULL_title_60):
            insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发上穿60分钟布林线上沿")
        if ("上穿布林线上沿" in BULL_title):
            insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发上穿日数据布林线上沿")

    if ("ZHISHU" in type):
        # if ("60均线上行" in MA60_titile):
        #     common.dingding_markdown_msg_2(mingcheng + "触发60日均线上行", mingcheng + "触发60日均线上行")
        #     insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发60日均线上行")

        if ("下穿布林线下沿" in BULL_title):
            common.dingding_markdown_msg_2(mingcheng + code +  "触发下穿日线布林线下沿", mingcheng + code + "触发下穿日线布林线下沿")
            insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发下穿日线布林线下沿")

        if ("下穿布林线下沿" in BULL_title_60):
            common.dingding_markdown_msg_2(mingcheng + code +  "触发下穿60分钟布林线下沿", mingcheng + code + "触发下穿60分钟布林线下沿")
            insert_ZhiShuLog_record(code, mingcheng, type, price, zhangdiefu, "触发下穿60分钟布林线下沿")

    return title, content

def insert_zhishu_count_record(type):
    data = selectCountRecord(type)
    sql = "INSERT INTO `superman`.`AGU_ZhiShu_Count`(`type`, `count`, `ri_up_count`, `ri_down_count`, `60_up_count`, `60_down_count`, `30_up_count`, `30_down_count`, `insert_time`) VALUES (" \
          "'" + type + "', " \
          "'" + str(data[0][0]) + "', " \
          "'" + str(data[0][1]) + "', " \
          "'" + str(data[0][2]) + "', " \
          "'" + str(data[0][3]) + "', " \
          "'" + str(data[0][4]) + "', " \
          "'" + str(data[0][5]) + "', " \
          "'" + str(data[0][6]) + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)

def select_zhishu_count_record(type):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `count`, `ri_up_count`, `ri_down_count`, `60_up_count`, `60_down_count`, `30_up_count`, `30_down_count` FROM `superman`.`AGU_ZhiShu_Count` WHERE `type` = \'" + type + "\' ORDER BY insert_time ASC limit 1"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def deleteXiangSiDuRecord():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    deleteSql = "delete from AGU_XiangSiDu"
    cursor.execute(deleteSql)
    db.commit()
    db.close()

def insert_xiangsidu_record(code, name, xiangsidu, zhangdiefu):
    sql = "INSERT INTO `superman`.`AGU_XiangSiDu`(`code`, `name`, `xiangsidu`, `zhangdiefu`, `input_time`) VALUES (" \
          "'" + code + "', " \
          "'" + name + "', " \
          "'" + xiangsidu + "', " \
          "'" + zhangdiefu + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)

def insert_ZhiShuLog_record(code, name, type, price, zhangdiefu, chufa):
    sql = "INSERT INTO `superman`.`AGU_ZhiShu_Log`(`code`, `name`, `type`, `price`, `zhangdiefu`, `chufa`, `insert_time`) VALUES (" \
          "'" + code + "', " \
          "'" + name + "', " \
          "'" + type + "', " \
          "'" + price + "', " \
          "'" + zhangdiefu + "', " \
          "'" + chufa + "', " \
          "'" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)

#insertRecord("INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `zhangdifu`, `30zhi`, `60zhi`) VALUES ('2', '2', '2', '2');")
# data = select_zhishu_count_record()
# for count in data:
#     print(count)