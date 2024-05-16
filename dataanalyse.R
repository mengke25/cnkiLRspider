library(haven)
library(tidyr)
library(conflicted)
library(dplyr)
library(readxl)
library(tidyverse)
library(skimr)
library(conflicted)
conflict_prefer("filter", "dplyr")
conflict_prefer("lag", "dplyr")

library(RStata)
options("RStata.StataPath"='D:/stata18/StataMP-64')
options("RStata.StataVersion"=18)

library(esquisse)
set_i18n("cn")

library(scales)
library(wordcloud2)
library(jiebaR)
library(tm)
library(NLP)
library(jiebaRD)

##### LR analyse ##### 

rm(list = ls())
setwd("D:\\project\\May2025_LRspider")
rootpath = "D:\\project\\May2025_LRspider"

lr <- read.csv(paste0(rootpath,"\\LR.csv"), header = FALSE) %>%
  rename(title=V1, author = V2, journal = V3, 
         time = V4, cited = V5,
         downloads = V6, author_f= V7, 
         institure = V8, journal2 = V9, keywords = V10) %>%
  select(-journal2) %>% 
  mutate(year = substr(time,1,4)) %>%
  mutate(keywords = gsub("[关键词：]","",keywords)) %>%
  mutate(keywords = gsub("[.:_?？《》<>,…“”]", "", keywords)) %>% 
  mutate(keywords = gsub(" ", "", keywords))

write_dta(lr,paste0(rootpath,"\\lr.dta"))


##### 关键词 #####

keywords <- lr %>% 
  select(keywords, year)
keywords_long <- separate(keywords, col = "keywords", into = paste0("keyword_", 1:5), sep = ";") %>%
  pivot_longer(cols = starts_with("keyword_"), names_to = "keyword_id", values_to = "keyword_value") %>%
  select(-keyword_id) %>%
  filter(is.na(keyword_value) != 1)  
keywords_count <- keywords_long %>%
  group_by(keyword_value,year) %>%
  summarise(count = n())

write_dta(keywords_count,paste0(rootpath,"\\keywords_year_count.dta"))

keywords_count <- keywords_long %>%
  group_by(keyword_value,year) %>%
  summarise(count = n()) %>%
  filter(year == 2024)

# keywords_count <- keywords_long %>%
#   group_by(keyword_value,year) %>%
#   summarise(count = n())


# 绘制词云图
keywords_count_sorted <- keywords_count[order(-keywords_count$count), ]
wordcloud_data <- data.frame(word = keywords_count_sorted$keyword_value,
                             freq = keywords_count_sorted$count)
wordcloud2(wordcloud_data)




##### 机构/作者 #####

## 机构 不区分年 ## 
inst <- lr %>% 
  select(institure) %>%
  filter(is.na(institure)==0)
inst_count <- inst %>%
  group_by(institure) %>%
  summarise(count = n()) %>%
  mutate(institure = ifelse(institure=="对外经济贸易大学中国WTO研究院","中国WTO研究院",institure) )

inst_count_sorted <- inst_count[order(-inst_count$count), ]
wordcloud_data <- data.frame(word = inst_count_sorted$institure,
                             freq = inst_count_sorted$count)
wordcloud2(wordcloud_data)




## 作者 区分年 ## 
author <- lr %>% 
  select(author_f) %>%
  filter(is.na(author_f)==0)
author_count <- author %>%
  group_by(author_f) %>%
  summarise(count = n()) 

author_count_sorted <- author_count[order(-author_count$count), ]
wordcloud_data <- data.frame(word = author_count_sorted$author_f,
                             freq = author_count_sorted$count)
wordcloud2(wordcloud_data)




keywords <- "实证|数据库|回归|定量"

data2<- read.csv(paste0(rootpath,"\\摘要.csv"), header = FALSE)
temp <- data2 %>%
  rename(title=V1, abstract = V2) %>%
  mutate(empirical= ifelse(grepl(keywords, abstract), 1, 0)) %>%
  select(-abstract) 

write_dta(temp,paste0(rootpath,"\\is_empirical.dta"))

