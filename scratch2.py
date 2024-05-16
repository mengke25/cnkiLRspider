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

# 检索主题
driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span').click()
driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys('数字贸易')
time.sleep(3)

# cssci
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div/label[5]/input').click()
time.sleep(2)

#点击检索
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/input').click()
time.sleep(4)

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
column6_texts = []

# 循环遍历每一页
while True:
    # 获取当前页的元素数量
    elements_count = len(driver.find_elements(By.XPATH, '//*[@id="gridTable"]/div/div/table/tbody/tr'))

    # 遍历当前页的元素，获取文本内容并存储到列表中
    for i in range(1, elements_count + 1):
        # 第一列 文章题目      //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[2]/a
        try:
            element_col1 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[2]/a')
            column1_texts.append(element_col1.text)
        except NoSuchElementException:
            column1_texts.append("NA")

        # 第二列 作者      //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[3]
        try:
            element_col2 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[3]')
            column2_texts.append(element_col2.text)
        except NoSuchElementException:
            column2_texts.append("NA")

        # 第三列 期刊        //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[4]/span/a
        try:
            element_col3 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[4]/span/a')
            column3_texts.append(element_col3.text)
        except NoSuchElementException:
            column3_texts.append("NA")

        # 第四列 时间        //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[5]
        try:
            element_col4 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[5]')
            column4_texts.append(element_col4.text)
        except NoSuchElementException:
            column4_texts.append("NA")

        # 第五列 被引       //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[6]
        try:
            element_col5 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[6]')
            column5_texts.append(element_col5.text)
        except NoSuchElementException:
            column5_texts.append("NA")

        # 第六列 下载       //*[@id="gridTable"]/div/div/table/tbody/tr[1]/td[7]
        try:
            element_col6 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/table/tbody/tr[{i}]/td[7]')
            column6_texts.append(element_col6.text)
        except NoSuchElementException:
            column6_texts.append("NA")



    # 尝试点击下一页按钮
    try:
        driver.find_element(By.ID, 'PageNext').click()
        time.sleep(3)  # 等待页面加载
    except NoSuchElementException:
        break  # 如果找不到下一页按钮，跳出循环

# 写入CSV文件
with open("基本信息.csv", "w", newline="", encoding='utf_8_sig') as csvfile:
    writer = csv.writer(csvfile)  
    for row in zip(column1_texts, column2_texts, column3_texts, column4_texts, column5_texts, column6_texts):
        writer.writerow(row)

# 关闭浏览器
driver.quit()
