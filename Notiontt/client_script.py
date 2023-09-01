# encoding=utf-8
import time
import subprocess

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
import common_mysqlSSHUtil


# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

while True:
    try:
        sql = "SELECT operate_id, code, operate, is_operate, gmt_create FROM `superman`.`operate` WHERE `is_operate` = '否' order by gmt_create asc"
        data = common_mysqlSSHUtil.select_record(sql)
        if data.__len__() < 1:
            logging.info("操作日志异常,待操作记录为空，请稍后")
            time.sleep(30)
            continue

        if data.__len__() > 1:
            common.dingding_markdown_msg_03("触发操作日志异常", "触发操作日志异常,有操作没有执行完成，请稍后")
            logging.info("操作日志异常,有操作没有执行完成，请稍后")
            time.sleep(60)
            continue
        for config_item in data:
            logging.info("操作日志命令：%s", config_item[2])
            return_code = subprocess.call(config_item[2], shell=True)
            print(return_code)
            logging.info("更新操作日志状态")
            common_mysqlSSHUtil.insert_record("update operate set is_operate='是' where operate_id=" + str(config_item[0]) + ";")
            time.sleep(60)
    except subprocess.CalledProcessError as e:
        print("Error executing command: {e.output}")
    time.sleep(60)
