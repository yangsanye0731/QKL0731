import common
import common_image
import common_mysqlUtil
import datalab.s1_yueDuZeShi.yueDuZeShi as ydzs


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


def send_image(code, name):
    image_path_ydzs = ydzs.plot_mean_ret(code)
    image_url_ydzs = "http://47.240.11.144/" + image_path_ydzs_sh[6:]

    image_path = common_image.plt_image_geGuZhiBiao(code, name)
    image_url = "http://47.240.11.144/" + image_path[6:]
    print(image_url)
    common.dingding_markdown_msg_2("触发" + name, "触发" + name + " > ![screenshot]("
                                   + image_url + ")" + "![screenshot](" + image_url_ydzs + ")")
    

    ####################################################################################################################
    ##########################################################################################################指数指标图片
    flag = True
    if flag:
        send_image('sh','上证指数')
        send_image('cyb', '创业板指数')
        send_image('399300', '深证指数')
        send_image('300322', '硕贝德')
        send_image('603363', '傲农生物')

        # image_path_ydzs_sh = ydzs.plot_mean_ret('sh')
        # image_url_ydzs_sh = "http://47.240.11.144/" + image_path_ydzs_sh[6:]
        # 
        # image_path_sh = common_image.plt_image_geGuZhiBiao("sh", "上证指数")
        # image_url_sh = "http://47.240.11.144/" + image_path_sh[6:]
        # print(image_url_sh)
        # common.dingding_markdown_msg_2("触发上证指数", "触发上证指数 > ![screenshot]("
        #                                + image_url_sh + ")" + "![screenshot](" + image_url_ydzs_sh + ")")
        # 
        # 
        # image_path_ydzs_cyb = ydzs.plot_mean_ret('cyb')
        # image_url_ydzs_cyb = "http://47.240.11.144/" + image_path_ydzs_cyb[6:]
        # 
        # image_path_399006 = common_image.plt_image_geGuZhiBiao("399006", "创业板指")
        # image_url_399006 = "http://47.240.11.144/" + image_path_399006[6:]
        # print(image_url_399006)
        # common.dingding_markdown_msg_2("触发创业板指数", "触发创业板指数 > ![screenshot]("
        #                                + image_url_399006 + ")" + "![screenshot](" + image_url_ydzs_cyb + ")")
        # 
        # image_path_ydzs_399300 = ydzs.plot_mean_ret('399300')
        # image_url_ydzs_399300 = "http://47.240.11.144/" + image_path_ydzs_399300[6:]
        # image_path_399300 = common_image.plt_image_geGuZhiBiao("399300", "沪深300")
        # image_url_399300 = "http://47.240.11.144/" + image_path_399300[6:]
        # print(image_url_399300)
        # common.dingding_markdown_msg_2("触发深证指数", "触发深证指数\n\n> ![screenshot]("
        #                                + image_url_399300 + ")" + "![screenshot](" + image_url_ydzs_399300 + ")")
        # 
        # 
        # image_path_300322 = common_image.plt_image_geGuZhiBiao("300322", "硕贝德")
        # image_url_300322 = "http://47.240.11.144/" + image_path_300322[6:]
        # print(image_url_300322)
        # common.dingding_markdown_msg_2("触发硕贝德", "触发硕贝德\n\n> ![screenshot]("
        #                                + image_url_300322 + ")")


# strategy("ZXG")
strategy("TOP")
