#######################################################################################################################
# ############################################################################################### 配置程序应用所需要环境PATH
import sys
import os
import time

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)

curPath1 = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath1)[0]
sys.path.append(rootPath1)

tradingview_path = os.path.join(rootPath1, 'crontab', 'TradingView')
rootPath_sell = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s3.py')
rootPath_buy = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s2.py')
rootPath_dongfangcaifu_top1000 = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s5.py')
rootPath_server = os.path.join(rootPath1, 'Notiontt', 'server.py')

# main_script.py
import subprocess
import threading

# ###########################################################################################################启动 server
result = subprocess.Popen(["python", rootPath_server])
output = result.stdout
print(output)


# ###########################################################################################################启动

# ###########################################################################################################启动 11：40、15：30启动
def exe_dfcf_top1000():
    args_1 = ['1']

    start_time_0 = "11:40:00"
    end_time_0 = "12:00:00"

    start_time_1 = "15:30:00"
    end_time_1 = "16:00:00"

    while True:
        current_time = time.strftime("%H:%M:%S")
        if start_time_0 <= current_time < end_time_0 or start_time_1 <= current_time < end_time_1:
            result = subprocess.Popen(["python", rootPath_dongfangcaifu_top1000] + args_1, cwd=tradingview_path)
            output = result.stdout
            print(output)
            break

        time.sleep(900)  # 暂停1分钟，避免无限循环过快消耗资源


# ###########################################################################################################循环校验 卖出
def exe_sell():
    args = ['1']
    start_time = "09:00:00"
    mid_time1 = "11:30:00"
    mid_time2 = "13:00:00"
    end_time = "16:00:00"
    while True:
        current_time = time.strftime("%H:%M:%S")
        if start_time <= current_time < mid_time1 or mid_time2 <= current_time < end_time:
            result = subprocess.Popen(["python", rootPath_sell] + args)
            output = result.stdout
            print(output)

        time.sleep(150)  # 暂停1分钟，避免无限循环过快消耗资源


# ###########################################################################################################循环校验 买入
def exe_buy():
    args = ['1']
    start_time = "09:00:00"
    mid_time1 = "11:30:00"
    mid_time2 = "13:00:00"
    end_time = "16:00:00"
    while True:
        current_time = time.strftime("%H:%M:%S")
        if start_time <= current_time < mid_time1 or mid_time2 <= current_time < end_time:
            result = subprocess.Popen(["python", rootPath_buy] + args)
            output = result.stdout
            print(output)

        time.sleep(150)  # 暂停1分钟，避免无限循环过快消耗资源


t1 = threading.Thread(target=exe_dfcf_top1000)
t2 = threading.Thread(target=exe_sell)
t3 = threading.Thread(target=exe_buy)
t1.start()
t2.start()
t3.start()
