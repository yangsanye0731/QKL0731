import jieba
from collections import Counter
import openpyxl
import time

workbook = openpyxl.load_workbook('C:\\Users\\yangj\\Desktop\\MyExcel.xlsx')
time_str1 = time.strftime("%Y-%m-%d", time.localtime())
sheet = workbook[time_str1]

# 使用jieba进行中文分词，并计算每行的词语出现次数
line_word_counts = []

for row in sheet.iter_rows(min_row=2, values_only=True):
    column1_value, column2_value, column3_value = row
    words = list(jieba.cut(column3_value))
    # 使用Counter计算词语出现的次数
    word_counts = Counter(words)
    # 删除空格等无关紧要的字符
    del word_counts[' ']
    line_word_counts.append(word_counts)

# 统计整个文本中每个词语的总出现次数
total_word_counts = Counter()

for word_count in line_word_counts:
    total_word_counts += word_count

# 对词语和它们的出现次数进行排序
sorted_word_counts = sorted(total_word_counts.items(), key=lambda x: x[1], reverse=True)

# 打印排序后的结果
for word, count in sorted_word_counts:
    print(f"'{word}': {count} 次")
