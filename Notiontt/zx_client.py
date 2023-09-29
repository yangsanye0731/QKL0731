# client.py
import rpyc

import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)
import common

import warnings

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


def execute_remote_command(command):
    conn = rpyc.connect("192.168.233.128", 18861)  # 替换为服务器的IP地址
    # conn = rpyc.connect("localhost", 18862)  # 替换为服务器的IP地址
    conn._config['sync_request_timeout'] = 1200
    remote_service = conn.root

    result = remote_service.exposed_execute_command(command)
    conn.close()
    return result


string_input = "python "
type_input = input("请输入您要操作的类型：s、b、 d、mysql、o ：")
if type_input == 'd':
    string_input = string_input + "autoDischarge.py"
    print("操作命令：" + string_input)
    output = execute_remote_command(string_input)
    # print("Remote command output:")
    # print(output)
elif type_input == 'o':
    string_input = string_input + "autoopen.py"
    print("操作命令：" + string_input)
    output = execute_remote_command(string_input)
elif type_input == 'mysql':
    string_input = string_input + "client_script.py"
else:
    code_input = input("请输入名称：")
    zhangdiefu, price = common.zhangdiefu_and_price(code_input)
    price_input = str(price)
    count_input = "1000"

    if type_input == 's':
        string_input = string_input + "autosell.py " + code_input + " " + price_input + " " + count_input
    elif type_input == 'b':
        string_input = string_input + "zx_autobuy.py " + code_input + " " + price_input + " " + count_input
    print("操作命令：" + string_input)
    output = execute_remote_command(string_input)
    # print("Remote command output:")
    # print(output)
