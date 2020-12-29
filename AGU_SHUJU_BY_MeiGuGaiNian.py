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


def strategy(gainian_name):
    # 获取实时数据
    data1 = common_mysqlUtil.select_all_code_by_gainian(gainian_name)

    for i in range(data1.__len__()):
        item_code = data1[i][0]
        item_name = data1[i][1]
        print(item_code)
        print(item_name)
        send_image(code=item_code, name=item_name, only_qushi_image=False)

# strategy("ZXG")
strategy("仿制药")
