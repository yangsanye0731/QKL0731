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

rootPath2 = os.path.join(rootPath1, 'crontab', 'TradingView', 'webhook_s1.py')

# main_script.py
import subprocess
print("获取实时数据")
args = ['2']
# 使用 subprocess 运行另一个 Python 文件
result = subprocess.run(["python", rootPath2] + args)
# # 获取执行结果
output = result.stdout
print(output)
