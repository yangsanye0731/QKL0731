import common
import common_image
import common_mysqlUtil
import datalab.s1_yueDuZeShi.yueDuZeShi as ydzs
import datetime


def send_image_array(code, name, code2, name2, code3, name3, group_name, message='', dingding_group_name="dingding01"):
    image_path = common_image.plt_image_geGuZhiBiao_array(code, name, code2, name2, code3, name3)
    image_url = "http://47.240.11.144/" + image_path[6:]
    print(image_url)
    common.dingding_markdown_msg_final(dingding_group_name,
                                       "触发" + group_name,
                                       "触发" + group_name + message
                                       + " ![screenshot]("
                                       + image_url + ")")


def send_image(code, name, only_qushi_image=False, item_image_url='', message='', dingding_group_name="dingding01"):
    zhangdiefu, price = common.zhangdiefu_and_price(code)
    if only_qushi_image:
        image_path = common_image.plt_image_geGuZhiBiao(code, name)
        image_url = "http://47.240.11.144/" + image_path[6:]
        print(image_url)
        common.dingding_markdown_msg_final(dingding_group_name,
                                           "触发" + name + zhangdiefu,
                                           "触发" + name + zhangdiefu + " 价格：" + price + message
                                           + " ![screenshot]("
                                           + image_url + ")")
    else:
        image_path_ydzs = ydzs.plot_mean_ret(code)
        image_url_ydzs = "http://47.240.11.144/" + image_path_ydzs[6:]

        image_path = common_image.plt_image_geGuZhiBiao(code, name)
        image_url = "http://47.240.11.144/" + image_path[6:]
        print(image_url)
        common.dingding_markdown_msg_final(dingding_group_name,
                                           "触发" + name + zhangdiefu,
                                           "触发" + name + zhangdiefu + " 价格：" + price + message
                                           + " ![screenshot](" + image_url + ")"
                                           + " ![screenshot](" + image_url_ydzs + ")"
                                           + " ![screenshot](" + item_image_url + ")")


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
    str_message = ''
    if data1[0][5] >= 30 or data1[0][6] >= 30:
        flag = True

        # sendMail("30MIN上升数，下降数达到一半", "30MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2("【重要通知，规范流程】" + type + "30MIN上升数:" + str(data1[0][5])
                                       + "，下降数:" + str(data1[0][6]) + "达到一半",
                                       "【重要通知，规范流程】" + type + "30MIN上升数:" + str(data1[0][5])
                                       + "，下降数:" + str(data1[0][6]) + "达到一半")
        str_message = str_message + "@@" + type + "30MIN上升数:" + str(data1[0][5]) + "，下降数:" + str(data1[0][6]) + "达到一半"

    if data1[0][3] >= 30 or data1[0][4] >= 30:
        flag = True
        # sendMail("60MIN上升数，下降数达到一半", "60MIN上升数，下降数达到一半")
        common.dingding_markdown_msg_2("【重要通知，规范流程】" + type + "60MIN上升数:" + str(data1[0][3])
                                       + "，下降数:" + str(data1[0][4]) + "达到一半",
                                       "【重要通知，规范流程】" + type + "60MIN上升数:" + str(data1[0][3])
                                       + "，下降数:" + str(data1[0][4]) + "达到一半")
        str_message = str_message + "@@" + type + "60MIN上升数:" + str(data1[0][3]) + "，下降数:" + str(data1[0][4]) + "达到一半"

    ####################################################################################################################
    ##########################################################################################################指数指标图片
    flag = True
    if flag:
        data_config = common_mysqlUtil.select_agu_config()
        for config_item in data_config:
            print(config_item)
            send_image_array(code=config_item[1], name=config_item[2], code2=config_item[3], name2=config_item[4],
                             code3=config_item[5],
                             name3=config_item[6], group_name=config_item[0],
                             message=str_message, dingding_group_name=config_item[9])


strategy("TOP")
