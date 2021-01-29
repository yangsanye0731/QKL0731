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
        common.dingding_markdown_msg_02("触发" + name + zhangdiefu, "触发" + name + zhangdiefu + " 价格：" + price
                                        + " ![screenshot]("
                                        + image_url + ")")
    else:
        image_path_ydzs = ydzs.plot_mean_ret(code)
        image_url_ydzs = "http://47.240.11.144/" + image_path_ydzs[6:]

        image_path = common_image.plt_image_geGuZhiBiao(code, name)
        image_url = "http://47.240.11.144/" + image_path[6:]
        print(image_url)
        common.dingding_markdown_msg_02("触发" + name + zhangdiefu, "触发" + name + zhangdiefu + " 价格：" + price
                                        + " ![screenshot](" + image_url + ")"
                                        + " ![screenshot](" + image_url_ydzs + ")"
                                        + " ![screenshot](" + item_image_url + ")")


def strategy(gainian_name):
    # 获取实时数据
    data1 = common_mysqlUtil.select_all_code_by_gainian(gainian_name)
    print(data1)

    for i in range(data1.__len__()):
        try:
            item_code = data1[i][0]
            item_name = data1[i][1]
            print(item_code)
            print(gainian_name + " " + item_name)
            send_image(code=item_code, name=gainian_name + "_" + item_name, only_qushi_image=False)
        except (ValueError, AttributeError, IOError, TypeError, NameError, IndexError, Exception) as e:
            print(e)


# 1月份
# strategy("仿制药")
# strategy("青蒿素")
# strategy("芬太尼")
# strategy("眼科医疗")
# strategy("生物疫苗")
# strategy("动物疫苗")
#
# strategy("小米概念")
# strategy("消费电子")
# strategy("无线耳机")
# strategy("华为概念")
#
# strategy("超清视频")
# strategy("超级真菌")
# strategy("超级品牌")
#
# strategy("横琴新区")
# strategy("国产航母")
# strategy("边缘计算")

# 1月中旬
# strategy("农业种植")
strategy("石油")
