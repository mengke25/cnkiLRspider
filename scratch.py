import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import os

os.chdir('D:\project\May2025_LRspider')

# 初始化WebDriver
driver = webdriver.Edge()
url = 'https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS'
driver.get(url)
time.sleep(5)

# 点击知网检索输入栏，并输入“数字贸易”
driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span').click()
driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys('数字贸易')
time.sleep(3)

# 选中CSSCI类论文
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div/label[5]/input').click()
time.sleep(2)

# 进行检索
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/input').click()
time.sleep(4)

# 显示详细信息，为了爬取摘要、关键词
driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/ul[2]/li[1]/i').click()
time.sleep(2)

# 每页显示条数改成50
driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/div/i').click()
driver.find_element(By.XPATH,'//*[@id="perPageDiv"]/ul/li[3]/a').click()
time.sleep(5)

# 创建空列表以存储所有元素的文本内容
column1_texts = []
column2_texts = []
column3_texts = []
column4_texts = []
column5_texts = []

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

        # 第二列 第一作者
        try:
            element_col2 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/div/p/a')
            column2_texts.append(element_col2.text)
        except NoSuchElementException:
            column2_texts.append("NA")

        # 第三列 单位
        try:
            element_col3 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/div/p/span/a')
            column3_texts.append(element_col3.text)
        except NoSuchElementException:
            column3_texts.append("NA")

        # 第四列 期刊
        try:
            element_col4 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/p[1]/span[1]/a')
            column4_texts.append(element_col4.text)
        except NoSuchElementException:
            column4_texts.append("NA")

        # 第五列 关键词
        try:
            element_col5 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/dl/dd[{i}]/div[2]/p[3]')
            column5_texts.append(element_col5.text)
        except NoSuchElementException:
            column5_texts.append("NA")

    # 尝试点击下一页按钮
    try:
        driver.find_element(By.ID, 'PageNext').click()
        time.sleep(3)  # 等待页面加载
    except NoSuchElementException:
        break  # 如果找不到下一页按钮，跳出循环

# 写入CSV文件
with open("页面元素.csv", "w", newline="", encoding='utf_8_sig') as csvfile:
    writer = csv.writer(csvfile)  # 创建一个写入器
    # 将不同列的元素逐行写入CSV文件的相应列
    for row in zip(column1_texts, column2_texts, column3_texts, column4_texts, column5_texts):
        writer.writerow(row)

# 关闭浏览器
driver.quit()
