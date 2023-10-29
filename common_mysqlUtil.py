# encoding=utf-8
import configparser
import time

import pymysql

import common
import common_zhibiao
#######################################################################################################################
################################################################################################配置程序应用所需要环境PATH
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

#######################################################################################################################
############################################################################################################读取配置文件
systemconfig_file_path = rootPath + '//resource//config//systemconfig.ini'
cf = configparser.ConfigParser()
cf.read(systemconfig_file_path, encoding='utf-8')


def acquire_lock():
    sql = "INSERT INTO `superman`.`AGU_All_Code`(`code`, `name`) VALUES ('" + "mylock_lock" + "','" + "mylock_lock" + "\')"
    # print(sql)
    insertRecord(sql)


def release_lock():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    deleteSql = "delete from `superman`.`AGU_All_Code` where code =\'" + "mylock_lock" + "\'"
    cursor.execute(deleteSql)
    db.commit()
    db.close()


def insertRecord(sql):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    url = cf.get("MySql", "url")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
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
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
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
                                                                                                                                                                     "'" + time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)


def deleteRecord():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    url = cf.get("MySql", "url")
    # 打开数据库连接
    db = pymysql.connect(url, userName, password, "superman")
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


def insert_zhishu_record(code, name, fullName, plate, mark, type):
    if ("USDT" in code):
        print("TODO")
        # price, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, MACD_title, BULL_title, BULL_middleband = common_zhibiao_BTC.zhibiao(code, '4h')
        # price_60, MA20_titile_60, MA30_titile_60, MA60_titile_60, qushi_5_10_20_30_60, MACD_title_60, BULL_title_60, BULL_middleband_60 = common_zhibiao_BTC.zhibiao(code, '1h')
        # price_30, MA20_titile_30, MA30_titile_30, MA60_titile_30, qushi_5_10_20_30_30, MACD_title_30, BULL_title_30, BULL_middleband_30 = common_zhibiao_BTC.zhibiao(code, '30m')
        # zhangdiefu = "0%"
        # print(fullName + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # title = ""
        # content = ""
        # KDJ_J_title = "10000"
        # KDJ_J_title_60 = "10000"
        # KDJ_J_title_30 = "10000"
    else:
        price_W, MA5_titile_W, MA20_titile_W, MA30_titile_W, MA60_titile_W, qushi_5_10_20_30_W, KDJ_J_title_W, MACD_title_W, BULL_title_W, BULL_middleband_W, ene_qushi_W = common_zhibiao.zhibiao(
            code, 'W')
        price, MA5_titile, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, KDJ_J_title, MACD_title, BULL_title, BULL_middleband, ene_qushi = common_zhibiao.zhibiao(
            code, 'D')
        price_60, MA5_titile_60, MA20_titile_60, MA30_titile_60, MA60_titile_60, qushi_5_10_20_30_60, KDJ_J_title_60, MACD_title_60, BULL_title_60, BULL_middleband_60, ene_qushi_60 = common_zhibiao.zhibiao(
            code, '60')
        price_30, MA5_titile_30, MA20_titile_30, MA30_titile_30, MA60_titile_30, qushi_5_10_20_30_30, KDJ_J_title_30, MACD_title_30, BULL_title_30, BULL_middleband_30, ene_qushi_30 = common_zhibiao.zhibiao(
            code, '30')

        data = select_xuangubao_one(code)
        huanshoulv = ""
        epsup = ""
        print(data)
        if len(data) > 0:
            huanshoulv = "@换手：" + data[0][4] + "%"
            # epsup = "@EPS：" + data[0][5] + "%"
        zhangdiefu = common.zhangdiefu(code) + huanshoulv + epsup
        print(fullName + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        title = fullName + zhangdiefu + " "
        content = fullName + zhangdiefu + qushi_5_10_20_30_30 + "<br>"
    # + " " + "%.3f" % closeArray[-1] + " " + zhangdiefu + "</font>**\n" + MIN30_60MA_content + str15QuShi_content + str30QuShi_content + strBULL60
    # print(time.localtime().tm_hour)
    # if (time.localtime().tm_hour > 14):
    #    common_image.plt_image_geGuZhiBiao(code, fullName)
    mingcheng = fullName
    sql = "INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `code`, `price`, `zhangdiefu`, `type`, `plate`, " \
          "`ri_qushi_20junxian`, `ri_qushi_30junxian`, `ri_qushi_60junxian`, `ri_qushi_5_10_20_30`, `ri_MACD`, `ri_KDJ`, `ri_BULL`, `ri_BULL_middle`, `ri_ENE`," \
          "`60_qushi_20junxian`, `60_qushi_30junxian`, `60_qushi_5_10_20_30`, `60_MACD`, `60_KDJ`, `60_BULL`, " \
          "`30_qushi_20junxian`, `30_qushi_30junxian`, `30_qushi_60junxian`, `30_qushi_5_10_20_30`, `30_MACD`, `30_KDJ`, `30_BULL`, `30_BULL_middle`, `beizhu`, `insert_time`) VALUES (" \
          "'" + mingcheng + "', " \
                            "'" + code + "', " \
                                         "'" + price + "', " \
                                                       "'" + zhangdiefu + "', " \
                                                                          "'" + type + "', " \
                                                                                       "'" + plate + "', " \
                                                                                                     "'" + MA20_titile + "', " \
                                                                                                                         "'" + MA30_titile + "', " \
                                                                                                                                             "'" + MA60_titile + "', " \
                                                                                                                                                                 "'" + qushi_5_10_20_30 + "', " \
                                                                                                                                                                                          "'" + MACD_title + "', " \
                                                                                                                                                                                                             "'" + KDJ_J_title + "', " \
                                                                                                                                                                                                                                 "'" + BULL_title + "', " \
                                                                                                                                                                                                                                                    "'" + BULL_middleband + "', " \
                                                                                                                                                                                                                                                                            "'" + ene_qushi + "', " \
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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       "'" + time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()) + "')"

    print(sql)
    insertRecord(sql)

    i = 0
    if (("60均线上行" in MA60_titile_30) and "下穿布林线下沿" in BULL_title_30):
        insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发30分钟60均线上行，下穿30分钟布林线下沿")

    j = 0
    if ("下穿布林线下沿" in BULL_title_60):
        insert_ZhiShuLog_record(code, "==60==" + mingcheng, type, price, plate, mark, zhangdiefu,
                                "触发60分钟60均线上行，下穿60分钟布林线下沿")
        j = j + 1

    if ("下穿布林线下沿" in BULL_title):
        insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发60日均线上行，下穿日布林线下沿")
        i = i + 1

    if ("创业板指" in mingcheng or "深证成指" in mingcheng or "ETF" in mingcheng):
        if ("上穿布林线上沿" in BULL_title_30):
            insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发上穿30分钟布林线上沿")
        if ("上穿布林线上沿" in BULL_title_60):
            insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发上穿60分钟布林线上沿")
        if ("上穿布林线上沿" in BULL_title):
            insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发上穿日数据布林线上沿")

    if (float(KDJ_J_title) < 2):
        insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发KDJ在0度以下" + KDJ_J_title)
        i = i + 1

    if (float(KDJ_J_title_60) < 0):
        insert_ZhiShuLog_record(code, "==60==" + mingcheng, type, price, plate, mark, zhangdiefu,
                                "触发60分钟KDJ在0度以下" + KDJ_J_title_60)
        j = j + 1

    # if (i == 2):
    #    common.dingding_markdown_msg_2(mingcheng + zhangdiefu + "_触发下穿日布林线下沿&KDJ在0度以下" + KDJ_J_title, mingcheng + zhangdiefu + "_触发下穿日布林线下沿&KDJ在0度以下" + KDJ_J_title)

    if ("5均线上穿" in MA5_titile_W):
        insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发5周线上穿, 前两周五周线处于下降阶段")

    if ("ENE" in ene_qushi):
        insert_ZhiShuLog_record(code, mingcheng, type, price, plate, mark, zhangdiefu, "触发ENE趋势向上")

    # if ("ENE" in ene_qushi_60):
    #     insert_ZhiShuLog_record(code, "==60==" + mingcheng, type, price, plate, mark, zhangdiefu, "触发ENE趋势向上")

    # if (j == 2):
    # common.dingding_markdown_msg_2(mingcheng + zhangdiefu + "_触发下穿60分钟布林线下沿&KDJ在0度以下" + KDJ_J_title_60, mingcheng + zhangdiefu + "_触发下穿60分钟布林线下沿&KDJ在0度以下" + KDJ_J_title_60)
    return title, content


def insert_zhishu_count_record(type):
    data = selectCountRecord(type)
    sql = "INSERT INTO `superman`.`AGU_ZhiShu_Count`(`type`, `count`, `ri_up_count`, `ri_down_count`, `60_up_count`, `60_down_count`, `30_up_count`, `30_down_count`, `insert_time`) VALUES (" \
          "'" + type + "', " \
                       "'" + str(data[0][0]) + "', " \
                                               "'" + str(data[0][1]) + "', " \
                                                                       "'" + str(data[0][2]) + "', " \
                                                                                               "'" + str(
        data[0][3]) + "', " \
                      "'" + str(data[0][4]) + "', " \
                                              "'" + str(data[0][5]) + "', " \
                                                                      "'" + str(data[0][6]) + "', " \
                                                                                              "'" + time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
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


def select_xuangubao():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `code`, `name`, `plate`, `mark` FROM `superman`.`AGU_Code` order by insert_time ASC"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_all_code():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `code`, `name`, `plate`, `mark` FROM `superman`.`AGU_All_Code` order by insert_time ASC"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_report_news():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `id`, `title`, `type`, `mark` FROM `superman`.`Report_News` where status = '20' order by insert_time ASC"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_xuangubao_one(code):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `code`, `name`, `plate`, `mark`, `huanshoulv`, `epsup`, `yingyeup` FROM `superman`.`AGU_Code` WHERE `code` = " + code
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_all_code_one(code):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `code`, `name`, `plate`, `mark`, `huanshoulv`, `epsup`, `yingyeup` FROM `superman`.`AGU_All_Code` WHERE `code` = " + code
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_all_code_by_gainian(gainian_name):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT `code`, `name`, `plate`, `mark`, `huanshoulv`, `epsup`, `yingyeup` FROM `superman`.`AGU_All_Code` WHERE `plate` like '%" + gainian_name + "%'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def select_agu_config(type='1'):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect("localhost", userName, password, "superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL
    sql = ''
    if type == '1':
        sql = "SELECT `group_name`, `code1`, `name1`, `code2`, `name2`, `code3`, `name3`, `code4`, `name4`, `code5`, `name5`, " \
              "`dingding_group_name`, `status`, `index` FROM `superman`.`AGU_Config` WHERE `status` = '1' order by `index` asc"
    if type == '2':
        sql = "SELECT `group_name`, `code1`, `name1`, `code2`, `name2`, `code3`, `name3`, `code4`, `name4`, `code5`, `name5`, " \
              "`dingding_group_name`, `status`, `index` FROM `superman`.`AGU_Config` WHERE `status` = '1' or `status` = '2' order by `index` asc"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def update_xuangubao(name, shizhi, shiyinglv, huanshoulv, code, epsup, yingyeup):
    sql = ""
    if (len(name) == 0):
        sql = "UPDATE `superman`.`AGU_Code` SET " \
              "`shizhi` = '" + shizhi + "', " \
                                        "`shiyinglv` = '" + shiyinglv + "', " \
                                                                        "`epsup` = '" + epsup + "', " \
                                                                                                "`yingyeup` = '" + yingyeup + "', " \
                                                                                                                              "`insert_time` = '" + time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()) + "', " \
                                                     "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                         time.localtime()) + "', " \
                                                                                                             "`huanshoulv` = '" + huanshoulv + "' " \
                                                                                                                                               "WHERE `code` = " + code
    else:
        sql = "UPDATE `superman`.`AGU_Code` SET " \
              "`name` = '" + name + "', " \
                                    "`shizhi` = '" + shizhi + "', " \
                                                              "`shiyinglv` = '" + shiyinglv + "', " \
                                                                                              "`epsup` = '" + epsup + "', " \
                                                                                                                      "`yingyeup` = '" + yingyeup + "', " \
                                                                                                                                                    "`insert_time` = '" + time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()) + "', " \
                                                     "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                         time.localtime()) + "', " \
                                                                                                             "`huanshoulv` = '" + huanshoulv + "' " \
                                                                                                                                               "WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def update_all_code(name, shizhi, shiyinglv, huanshoulv, code, epsup, yingyeup):
    sql = ""
    if (len(name) == 0):
        sql = "UPDATE `superman`.`AGU_All_Code` SET " \
              "`shizhi` = '" + shizhi + "', " \
                                        "`shiyinglv` = '" + shiyinglv + "', " \
                                                                        "`epsup` = '" + epsup + "', " \
                                                                                                "`yingyeup` = '" + yingyeup + "', " \
                                                                                                                              "`insert_time` = '" + time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()) + "', " \
                                                     "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                         time.localtime()) + "', " \
                                                                                                             "`huanshoulv` = '" + huanshoulv + "' " \
                                                                                                                                               "WHERE `code` = " + code
    else:
        sql = "UPDATE `superman`.`AGU_All_Code` SET " \
              "`name` = '" + name + "', " \
                                    "`shizhi` = '" + shizhi + "', " \
                                                              "`shiyinglv` = '" + shiyinglv + "', " \
                                                                                              "`epsup` = '" + epsup + "', " \
                                                                                                                      "`yingyeup` = '" + yingyeup + "', " \
                                                                                                                                                    "`insert_time` = '" + time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()) + "', " \
                                                     "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                         time.localtime()) + "', " \
                                                                                                             "`huanshoulv` = '" + huanshoulv + "' " \
                                                                                                                                               "WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def insert_all_code(code, name):
    sql = "INSERT INTO `superman`.`AGU_All_Code`(`code`, `name`) VALUES ('" + code + "','" + name + "\')"
    print(sql)
    insertRecord(sql)


def update_all_code_plate(code, plate):
    sql = ""
    sql = "UPDATE `superman`.`AGU_All_Code` SET " \
          "`plate` = '" + plate + "', " \
                                  "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "' " \
                                                                                                               "WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def insert_all_code_sub(code, name, plate):
    sql = "INSERT INTO `superman`.`AGU_All_Code_Sub`(`code`, `name`,`plate`) VALUES ('" + code + "','" + name + "','" + plate + "')"
    print(sql)
    insertRecord(sql)


def update_all_code_huanshoulv(code, huanshoulv):
    sql = ""
    sql = "UPDATE `superman`.`AGU_All_Code` SET " \
          "`huanshoulv` = '" + huanshoulv + "', " \
                                            "`update_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                time.localtime()) + "' " \
                                                                                                    "WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


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
                                                                         "'" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                             time.localtime()) + "')"
    print(sql)
    insertRecord(sql)


def insert_ZhiShuLog_record(code, name, type, price, plate, mark, zhangdiefu, chufa):
    sql = "INSERT INTO `superman`.`AGU_ZhiShu_Log`(`code`, `name`, `type`, `price`, `plate`, `mark`, `zhangdiefu`, `chufa`, `insert_time`) VALUES (" \
          "'" + code + "', " \
                       "'" + name + "', " \
                                    "'" + type + "', " \
                                                 "'" + price + "', " \
                                                               "'" + plate + "', " \
                                                                             "'" + mark + "', " \
                                                                                          "'" + zhangdiefu + "', " \
                                                                                                             "'" + chufa + "', " \
                                                                                                                           "'" + time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()) + "')"
    print(sql)
    insertRecord(sql)


def insert_codeitem(codeitem, type, strategy, endstr):
    sql = ""
    sql = "INSERT INTO `superman`.`codeitem`(`codeitem`, `type`, `strategy`, `insert_time`) VALUES (" \
          "'" + codeitem + "', " \
                           "'" + type + "', " \
                                        "'" + strategy + "', " \
                                                         "'" + endstr + "')"
    print(sql)
    insertRecord(sql)


def select_buy():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL
    sql = ''
    sql = "SELECT code, name, modify_time from `superman`.`buy` WHERE `is_delete` = 0 order by 60_fanzhuan desc, modify_time desc"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def update_buy(code):
    sql = "UPDATE `superman`.`buy` SET `modify_time` = '" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                          time.localtime()) + "' WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def update_buy_60_fanzhuan(code, type):
    sql = "UPDATE `superman`.`buy` SET `60_fanzhuan` = " + type + " WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def update_buy_60_fanzhuan_NULL(code):
    sql = "UPDATE `superman`.`buy` SET `60_fanzhuan` = NULL WHERE `code` = " + code
    print(sql)
    insertRecord(sql)


def select_sell():
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL
    sql = ''
    sql = "SELECT code, name, channel, count, sell_id, modify_time from `superman`.`sell` WHERE `is_delete` = 0"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def update_sell(id, update_count):
    sql = "UPDATE `superman`.`sell` SET `count` = '" + update_count + "' WHERE `sell_id` = " + str(id)
    insertRecord(sql)


def get_config(config_key):
    userName = cf.get("MySql", "userName")
    password = cf.get("MySql", "password")
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user=userName, password=password, database="superman")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL
    sql = ''
    sql = "SELECT config_id, config_key, config_value from `superman`.`config` WHERE `config_key` = '" + config_key + "'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def update_config(config_key, config_value):
    sql = "UPDATE `superman`.`config` SET `config_value` = '" + config_value + "' WHERE `config_key` = '" + config_key + "'"
    insertRecord(sql)

# insertRecord("INSERT INTO `superman`.`AGU_ZhiShu`(`mingcheng`, `zhangdifu`, `30zhi`, `60zhi`) VALUES ('2', '2', '2', '2');")
# data = select_zhishu_count_record()
# for count in data:
#     print(count)
# select_xuangubao()
# data = select_agu_config()
# print(data)
