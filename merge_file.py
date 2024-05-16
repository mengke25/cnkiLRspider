import csv
import os


os.chdir('D:\project\May2025_LRspider')

# 读取基本信息
basic_info = {}
with open('D:/project/May2025_LRspider/基本信息.csv', mode='r', encoding='utf-8') as basic_file:
    basic_reader = csv.reader(basic_file)
    for row in basic_reader:
        basic_info[row[0]] = row[1:]

# 读取页面元素并匹配
with open('D:/project/May2025_LRspider/页面元素.csv', mode='r', encoding='utf-8') as element_file:
    element_reader = csv.reader(element_file)

    # 创建新的 CSV 文件并写入匹配结果
    with open('D:/project/May2025_LRspider/LR.csv', mode='w', encoding='utf-8', newline='') as lr_file:
        lr_writer = csv.writer(lr_file)

        for row in element_reader:
            key = row[0]
            if key in basic_info:
                lr_writer.writerow([key] + basic_info[key] + row[1:])
            else:
                # 如果在基本信息中找不到匹配的 key，则写入空行
                lr_writer.writerow([''] * (len(basic_info[key]) + len(row[1:])))

print("匹配完成，并已将结果保存到 'LR.csv' 文件中。")





