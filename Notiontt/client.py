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
import common_notion

dic = common_notion.find_config_item_from_database("18fcc6b54f574e97b1d6fe907260d37a")

import warnings

# Suppress the FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


def execute_remote_command(command):
    conn = rpyc.connect("192.168.233.128", 18861)  # 替换为服务器的IP地址
    # conn = rpyc.connect("localhost", 18861)  # 替换为服务器的IP地址
    conn._config['sync_request_timeout'] = 12000
    remote_service = conn.root

    result = remote_service.exposed_execute_command(command)
    conn.close()
    return result


def auto_operate(p_type, p_code, p_price, p_count):
    string_input = "python "
    p_price = str(p_price)
    p_count = str(p_count)
    if p_type == 's':
        string_input = string_input + "autosell.py " + p_code + " " + p_price + " " + p_count
    elif p_type == 'b':
        string_input = string_input + "autobuy.py " + p_code + " " + p_price + " " + p_count
    print("操作命令：" + string_input)
    output = execute_remote_command(string_input)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        string_input = "python "
        type_input = sys.argv[1]
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
        else:
            print("请输入正确类型")
    elif len(sys.argv) == 3:
        string_input = "python "
        type_input = sys.argv[1]
        code_input = sys.argv[2]
        zhangdiefu, price = common.zhangdiefu_and_price(code_input)
        price_input = str(price)
        count_input = "1000"

        my_list = dic.get('auto_list').split(",")
        for item in my_list:
            item_list = item.split(":")
            if item_list[0] == code_input:
                count_input = item_list[1]
                break;

        if type_input == 's':
            string_input = string_input + "autosell.py " + code_input + " " + price_input + " " + count_input
        elif type_input == 's1':
            string_input = string_input + "autosell_quick.py " + code_input + " " + price_input + " " + 5000 + " " + "1"
        elif type_input == 's2':
            string_input = string_input + "autosell_quick.py " + code_input + " " + price_input + " " + 10000 + " " + "2"
        elif type_input == 'b':
            string_input = string_input + "autobuy.py " + code_input + " " + price_input + " " + count_input
        elif type_input == 'b1':
            string_input = string_input + "autobuy_quick.py " + code_input + " " + price_input + " " \
                           + "3000" + " " + "3"
        elif type_input == 'b2':
            string_input = string_input + "autobuy_quick.py " + code_input + " " + price_input + " " \
                           + "6000" + " " + "6"

        print("操作命令：" + string_input)
        output = execute_remote_command(string_input)
        # print("Remote command output:")
        # print(output)
    elif len(sys.argv) == 4:
        string_input = "python "
        type_input = sys.argv[1]
        code_input = sys.argv[2]
        zhangdiefu, price = common.zhangdiefu_and_price(code_input)
        price_input = str(price)
        count_input = sys.argv[3]

        if type_input == 's':
            string_input = string_input + "autosell.py " + code_input + " " + price_input + " " + count_input
        elif type_input == 'b':
            string_input = string_input + "autobuy.py " + code_input + " " + price_input + " " + count_input
        print("操作命令：" + string_input)
        output = execute_remote_command(string_input)
        # print("Remote command output:")
        # print(output)
    else:
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
                string_input = string_input + "autobuy.py " + code_input + " " + price_input + " " + count_input
            print("操作命令：" + string_input)
            output = execute_remote_command(string_input)
            # print("Remote command output:")
            # print(output)
