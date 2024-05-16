import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import os
import pandas as pd


os.chdir('D:\project\May2025_LRspider')


# 初始化WebDriver
driver = webdriver.Edge()
url = 'https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS'
driver.get(url)
time.sleep(5)

# 设置检索条件为作者单位，逻辑关系为“OR”
driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span').click()
driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys('数字贸易')
time.sleep(3)

# cssci
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div/label[5]/input').click()
time.sleep(2)

#点击检索
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/input').click()
time.sleep(4)

# 显示详细信息
driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/ul[2]/li[1]/i').click()
time.sleep(2)

# 每页显示条数改成50
driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/div/i').click()
driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/ul/li[3]/a').click()
time.sleep(5)

# 创建空列表以存储所有元素的文本内容
column1_texts = []
column2_texts = []

# 循环遍历每一页
while True:
    # 获取当前页的元素数量
    elements_count = len(driver.find_elements(By.XPATH, '//*[@id="gridTable"]/div/div/dl/dd'))

    # 遍历当前页的元素，获取文本内容并存储到列表中
    for i in range(1, elements_count + 1):
        # 第一列 文章题目       
        try:
            element_col1 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/h6/a')
            column1_texts.append(element_col1.text)
        except NoSuchElementException:
            column1_texts.append("NA")

        # 第二列 摘要           //*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/p[2]/span[2]
        try:
            element_col2 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/p[2]/span[2]')
            column2_texts.append(element_col2.text)
        except NoSuchElementException:
            column2_texts.append("NA")

    # 尝试点击下一页按钮
    try:
        driver.find_element(By.ID, 'PageNext').click()
        time.sleep(3)  # 等待页面加载
    except NoSuchElementException:
        break  # 如果找不到下一页按钮，跳出循环

# 写入CSV文件
with open("摘要.csv", "w", newline="", encoding='utf_8_sig') as csvfile:
    writer = csv.writer(csvfile)  # 创建一个写入器
    # 将不同列的元素逐行写入CSV文件的相应列
    for row in zip(column1_texts, column2_texts):
        writer.writerow(row)

# 关闭浏览器
driver.quit()
