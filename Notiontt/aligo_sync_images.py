# import requests
#
# url = 'https://hook.us1.make.com/r7gj5cb1go2l7x23i44tnyivdj7sy7ei'
# data = {
#     's_code': '300482',
#     's_name': 'WanFuShengWu',
#     's_type': '60min'
# }
#
# response = requests.post(url, data=data)

from aligo import Aligo
import sys
import os

project_name = 'QKL0731'
rootPath = str(os.path.abspath(os.path.dirname(__file__)).split(project_name)[0]) + project_name
sys.path.append(rootPath)
images_path = rootPath + os.sep + "images"
print("项目地址" + rootPath + os.sep + "images")

if __name__ == '__main__':
    ali = Aligo()  # 第一次使用，会弹出二维码，供扫描登录

    user = ali.get_user()  # 获取用户信息
    print(user.user_name, user.nick_name, user.phone)  # 打印用户信息

    ll = ali.get_file_list()  # 获取网盘根目录文件列表
    for file in ll:  # 遍历文件列表
        print(file.file_id, file.name, file.type)  # 打印文件信息

    # folder_path = "test0730/sub_filepath"
    folder_path = "【04】Linux数据/【01】QKL_images"
    folder = ali.get_folder_by_path(folder_path)
    if folder is None:
        create_folder = input('云盘文件夹[%s]不存在，是否创建?(yes)：' % folder_path)
        if create_folder.lower() == 'yes':
            folder = ali.create_folder(folder_path)
            print('云盘文件夹[%s]创建完成' % folder_path)
        else:
            print('云盘文件夹[%s]不存在，同步已取消' % folder_path)
            os.system('pause')
            exit(1)

    directory = images_path
    print('本地目录：%s' % directory)
    print('远程目录：https://www.aliyundrive.com/drive/folder/%s' % folder.file_id)
    ali.sync_folder(directory, folder.file_id)
