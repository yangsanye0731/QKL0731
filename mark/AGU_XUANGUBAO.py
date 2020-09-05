#encoding=utf-8
import common_mysqlUtil

def strategy():
    # 获取实时数据
    data = common_mysqlUtil.select_xuangubao()
    # 数据遍历
    for i in range(len(data)):
        code = str(data[i][0])
        name = str(data[i][1])
        plate = str(data[i][2])
        mark = str(data[i][3])
        common_mysqlUtil.insert_zhishu_record(code, name, name,  plate, mark, "XGB")

common_mysqlUtil.deleteTopRecord("XGB")
common_mysqlUtil.insert_ZhiShuLog_record("======", "======", "XGB", "====", "========", "============", "======", "")
strategy()


