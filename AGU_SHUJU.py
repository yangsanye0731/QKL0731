import common
import common_image
import common_mysqlUtil
import datalab.s1_yueDuZeShi.yueDuZeShi as ydzs


def send_image(code, name, only_qushi_image=False, item_image_url=''):
    zhangdiefu, price = common.zhangdiefu_and_price(code)
    if only_qushi_image:
        image_path = common_image.plt_image_geGuZhiBiao(code, name)
        image_url = "http://47.240.11.144/" + image_path[6:]
        print(image_url)
        common.dingding_markdown_msg_2("触发" + name + zhangdiefu, "触发" + name + zhangdiefu + " 价格：" + price
                                       + " ![screenshot]("
                                       + image_url + ")")
    else:
        image_path_ydzs = ydzs.plot_mean_ret(code)
        image_url_ydzs = "http://47.240.11.144/" + image_path_ydzs[6:]

        image_path = common_image.plt_image_geGuZhiBiao(code, name)
        image_url = "http://47.240.11.144/" + image_path[6:]
        print(image_url)
        common.dingding_markdown_msg_2("触发" + name + zhangdiefu, "触发" + name + zhangdiefu + " 价格：" + price
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
    flag = True
    if flag:
        send_image(code='sh', name='上证指数')
        send_image(code='cyb', name='创业板指数')
        send_image(code='399300', name='深证指数')
        # send_image(code='300322', name='【跨越5月线】硕贝德', only_qushi_image=False)
        send_image(code='603363', name='【猪周期，跨越5周线，主力持仓增长】傲农生物', only_qushi_image=False,
                   item_image_url='http://47.240.11.144/software/QKL0731/resource/images/ANSW1.png')
        # send_image(code='002548', name='【猪周期，跨越5周线】金新农', only_qushi_image=False)
        send_image(code='600332', name='【仿制药】白云山', only_qushi_image=False)


# strategy("ZXG")
strategy("TOP")
