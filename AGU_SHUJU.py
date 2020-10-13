import common
import common_image
import common_mysqlUtil


def strategy(type):
    # 获取实时数据
    data1 = common_mysqlUtil.selectCountRecord(type)
    print("实时数据：" + str(data1))

    # 获取已经入库的历史数据
    data2 = common_mysqlUtil.select_zhishu_count_record(type)
    print("已入库的历史数据:" + str(data2))

    # 如果历史数据为空，插入数据
    print(len(data2))
    if (len(data2) == 0):
        common_mysqlUtil.insert_zhishu_count_record(type)
        data2 = common_mysqlUtil.select_zhishu_count_record(type)

    # 插入日志信息
    common_mysqlUtil.insert_zhishu_count_record(type)

    # 30MIN上升数大于下降数，且上升数增加
    print("上升数：" + str(data1[0][5]))
    print("下降数：" + str(data1[0][6]))
    print("总数：" + str(data1[0][0]))
    print("总数618：" + str(int(data1[0][0] * 0.6)))

    flag = False
    if (data1[0][5] >= 30 or data1[0][6] >= 30):
        flag = True

        # sendMail("30MIN上升数，下降数达到一半", "30MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2("【重要通知，规范流程】" + type + "30MIN上升数:" + str(data1[0][5])
                                       + "，下降数:" + str(data1[0][6]) + "达到一半",
                                       "【重要通知，规范流程】" + type + "30MIN上升数:" + str(data1[0][5])
                                       + "，下降数:" + str(data1[0][6]) + "达到一半")

    if (data1[0][3] >= 30 or data1[0][4] >= 30):
        flag = True
        # sendMail("60MIN上升数，下降数达到一半", "60MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2("【重要通知，规范流程】" + type + "60MIN上升数:" + str(data1[0][3])
                                       + "，下降数:" + str(data1[0][4]) + "达到一半",
                                       "【重要通知，规范流程】" + type + "60MIN上升数:" + str(data1[0][3])
                                       + "，下降数:" + str(data1[0][4]) + "达到一半")

    ####################################################################################################################
    ##########################################################################################################指数指标图片
    if flag:
        image_path_399006 = common_image.plt_image_geGuZhiBiao("399006", "创业板指")
        image_url_399006 = "http://47.240.11.144/" + image_path_399006[6:]
        common.dingding_markdown_msg_2("创业板指数\n\n> ![screenshot]("
                                       + image_url_399006 + ")")

        image_path_399300 = common_image.plt_image_geGuZhiBiao("399300", "沪深300")
        image_url_399300 = "http://47.240.11.144/" + image_path_399300[6:]
        common.dingding_markdown_msg_2("深证指数\n\n> ![screenshot]("
                                       + image_url_399300 + ")")


# strategy("ZXG")
strategy("TOP")
