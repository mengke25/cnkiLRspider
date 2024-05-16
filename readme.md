readme:
运行顺序

##### 0.说明

我们拟分三批抓取论文信息

* 首先抓取详细信息，包括文章的`题目`，`第一作者`，`单位`，`期刊`，`关键词`
* 其次抓取简要信息，包括文章的`题目`，`全部作者`，`期刊名称`，`发表时间`，`被引次数`，`下载次数`
* 最后抓取文章的`题目`和`摘要`

这里要说明的是，我分三次抓取的最主要原因是，知网详细界面和简略界面所显示的内容有所差异，为了全方位获取文章的信息，我们分批次抓取，最后可根据`文章题目`按需横向合并（merge）

##### 1.scratch.py：爬取详细信息

##### 2.scratch2.py：爬取简略信息

##### 3.scratch3.py：爬取文章摘要

##### 4.dataanalyse.R：基于R处理数据，绘制云图

##### 5.dataanalysedo：基于stata分析不同来源期刊、作者、机构的发文情况

