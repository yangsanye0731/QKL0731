import easyocr
from PIL import ImageGrab
import time
from pathlib import Path

import logging

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


def ocr(image_file_path):
    reader = easyocr.Reader(['ch_sim', 'en'])  # 指定支持的语言，'ch_sim' 表示简体中文

    results = reader.readtext(image_file_path)

    for (bbox, text, prob) in results:
        # print(f'Text: {text} (Probability: {prob:.2f})')
        return text


if __name__ == "__main__":
    # screenshot = ImageGrab.grab()
    #
    # # 指定要创建的文件夹的路径
    # folder_path = "images\\filepath"
    #
    # # 使用 Path() 创建文件夹
    # path = Path(folder_path)
    # path.mkdir(parents=True, exist_ok=True)
    # absolute_path = path.resolve()
    # print(absolute_path)
    #
    # # 保存截图为文件
    # screenshot.save("C:\\Users\\yangj\\Desktop\\screenshot.png")

    text = ocr('C:\\Users\\yangj\\Desktop\\2.jpg')
    print(text)
