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

rootPath2 = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s3.py')
rootPath3 = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s2.py')

# main_script.py
import subprocess

print("获取实时数据")
args = ['1']

start_time = "08:00:00"
end_time = "20:00:00"

while True:
    current_time = time.strftime("%H:%M:%S")
    if start_time <= current_time < end_time:
        # 调用信息
        # result = subprocess.run(["python", rootPath3] + args)
        # # 获取执行结果
        # output = result.stdout
        # print(output)

        # 在指定的时间范围内执行你的任务
        # 使用 subprocess 运行另一个 Python 文件
        result = subprocess.run(["python", rootPath2] + args)
        # # 获取执行结果
        output = result.stdout
        print(output)

    time.sleep(5)  # 暂停1分钟，避免无限循环过快消耗资源
