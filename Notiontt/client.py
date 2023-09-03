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


def execute_remote_command(command):
    conn = rpyc.connect("192.168.233.129", 18861)  # 替换为服务器的IP地址
    conn._config['sync_request_timeout'] = 1200
    remote_service = conn.root

    result = remote_service.exposed_execute_command(command)
    conn.close()
    return result


string_input = "python "
type_input = input("请输入您的信息：s  b  d：")
if type_input == 'd':
    string_input = string_input + "autoDischarge.py"
    output = execute_remote_command(string_input)
    # print("Remote command output:")
    # print(output)
else:
    code_input = input("请输入您的信息：")
    price_input = input("请输入您的信息：")
    count_input = input("请输入您的信息：")

    if type_input == 's':
        string_input = string_input + "autosell.py " + code_input + " " + price_input + " " + count_input
    elif type_input == 'b':
        string_input = string_input + "autobuy.py " + code_input + " " + price_input + " " + count_input

    output = execute_remote_command(string_input)
    # print("Remote command output:")
    # print(output)
