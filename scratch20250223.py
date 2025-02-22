
## ！！！！！！！！！！！！！！！！！！！！！！！！！！！##
## 爬取【特定主题】知网文献，并一键生成文献综述！！！！！##
## ！！！！！！！！！！！！！！！！！！！！！！！！！！！##
#%%
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import os
import pandas as pd

#%%
os.chdir('D:\\py_proj\\lr_review')
search_key = 'ESG 绿色转型'


# 初始化WebDriver
driver = webdriver.Edge()
url = 'https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS'
driver.get(url)
time.sleep(5)

driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span').click()
driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys(search_key)
time.sleep(3)

# cssci
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/label[5]/input').click()
time.sleep(2)

#点击检索
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[3]/div/input').click()
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
column3_texts = []
column4_texts = []

# 循环遍历每一页
while True:
    # 获取当前页的元素数量
    try:
        elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div/div/dl/dd')
        elements_count = len(elements)
        print(f"页面中找到的元素数量为: {elements_count}")
    except NoSuchElementException:
        print("未找到任何元素。")


    ## elements_count = len(driver.find_elements(By.XPATH, '//*[@id="gridTable"]/div/div/dl/dd'))
    time.sleep(2)
    print(f"当前页有{elements_count}条记录")

    # 遍历当前页的元素，获取文本内容并存储到列表中
    for i in range(1, elements_count + 1):
        # 第一列 文章题目       
        try:
            element_col1 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/dl/dd[{i}]/div[2]/h6/a')
            column1_texts.append(element_col1.text)
            print(f"题目: {element_col1.text}")
        except NoSuchElementException:
            column1_texts.append("NA")
            print("题目: NA")

        # 第二列 摘要
        try:
            element_col2 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/dl/dd[{i}]/div[2]/p[2]/span[2]')
            column2_texts.append(element_col2.text)
            print(f"摘要: {element_col2.text}")
        except NoSuchElementException:
            column2_texts.append("NA")
            print("摘要: NA")

        # 第三列作者单位 
        try:
            element_col3 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/dl/dd[{i}]/div[2]/div/p/span/a')
            column3_texts.append(element_col3.text)
            print(f"单位: {element_col3.text}")
        except NoSuchElementException:
            column3_texts.append("NA")
            print("单位: NA")


    # 尝试点击下一页按钮
    try:
        driver.find_element(By.ID, 'PageNext').click()
        time.sleep(3)  # 等待页面加载
    except NoSuchElementException:
        break  # 如果找不到下一页按钮，跳出循环

# 写入xlsx文件
data = {
    "题目": column1_texts,
    "摘要": column2_texts,
    "单位": column3_texts
}
df = pd.DataFrame(data)
# df.to_excel("abstract.xlsx", index=False, encoding='utf_8_sig')
df.to_excel("abstract.xlsx", index=False)

# 关闭浏览器
driver.quit()

#%%

####################################
############### info ###############
####################################



# 初始化WebDriver
driver = webdriver.Edge()
url = 'https://kns.cnki.net/kns8/AdvSearch?dbcode=CFLS'
driver.get(url)
time.sleep(5)

# 设置检索条件为作者单位，逻辑关系为“OR”
driver.find_element(By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span').click()
driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys(search_key)
time.sleep(3)

# cssci
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/label[5]/input').click()
time.sleep(2)

#点击检索
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[3]/div/input').click()
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

# 循环遍历每一页
while True:
    # 获取当前页的元素数量 
    try:
        elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr')
        elements_count = len(elements)
        print(f"页面中找到的元素数量为: {elements_count}")
    except NoSuchElementException:
        print("未找到任何元素。")

    time.sleep(2)
    print(f"当前页有{elements_count}条记录")

    # 遍历当前页的元素，获取文本内容并存储到列表中
    for i in range(1, elements_count + 1):
        # 第一列 文章题目       
        try:
            element_col1 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/table/tbody/tr[{i}]/td[2]/a')
            column1_texts.append(element_col1.text)
            print(f"题目: {element_col1.text}")
        except NoSuchElementException:
            column1_texts.append("NA")
            print("题目: NA")

        # 第二列 作者
        try:
            element_col2 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/table/tbody/tr[{i}]/td[3]')
            column2_texts.append(element_col2.text)
            print(f"作者: {element_col2.text}")
        except NoSuchElementException:
            column2_texts.append("NA")
            print("作者: NA")

        # 第三列期刊
        try:
            element_col3 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/table/tbody/tr[{i}]/td[4]/span/a')
            column3_texts.append(element_col3.text)
            print(f"期刊: {element_col3.text}")
        except NoSuchElementException:
            column3_texts.append("NA")
            print("期刊: NA")

        # 第四列时间
        try:
            element_col4 = driver.find_element(By.XPATH, f'//*[@id="gridTable"]/div/div/div/table/tbody/tr[{i}]/td[5]')
            column4_texts.append(element_col4.text)
            print(f"时间: {element_col4.text}")
        except NoSuchElementException:
            column4_texts.append("NA")
            print("时间: NA")


    # 尝试点击下一页按钮
    try:
        driver.find_element(By.ID, 'PageNext').click()
        time.sleep(3)  # 等待页面加载
    except NoSuchElementException:
        break  # 如果找不到下一页按钮，跳出循环

# 写入xlsx文件
data = {
    "题目": column1_texts,
    "作者": column2_texts,
    "期刊": column3_texts,
    "时间": column4_texts
}

df = pd.DataFrame(data)
# df.to_excel("info.xlsx", index=False, encoding='utf_8_sig')
df.to_excel("info.xlsx", index=False)


# 关闭浏览器
driver.quit()

#%%
#####################################
############### merge ###############
#####################################


info_df = pd.read_excel('info.xlsx')
abstract_df = pd.read_excel('abstract.xlsx')

# 合并两个表格，基于第一列（第一列名称为 'key'，）
merged_df = pd.merge(info_df, abstract_df, on=info_df.columns[0], how='inner')
merged_df.to_excel(r"D:\py_proj\lr_review\LR_INFO.xlsx", index=False)
df = pd.read_excel('LR_INFO.xlsx')
df['INFO'] = "作者：" + df.iloc[:, 1] + " 时间：" + df.iloc[:, 3].astype(str) + " 题目：" + df.iloc[:, 0] + " 摘要：" + df.iloc[:, 4]
df.to_excel('LR_INFO.xlsx', index=False)







# %%
