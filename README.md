## Scrapy 教程
Scrapy框架降低了爬虫开发难度，加强了程序设计的可扩展性，加大了学习难度。带着学习态度，我们可以看看这个框架设计的美妙之处。
项目详情请访问 https://www.geekclub.cc/2022/01/1338

## 相关版本信息
MacOS Monterty 12.1
Chip：Apple M1 Max
Python 3.8
Scrapy 2.5.1 - project: canadaJob

```shell
scrapy startproject canadaJobs # 创建项目
cd canadaJobs
~/canadaJobs$ scrapy genspider JobbankSpider https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=Moncton&sort=D # 创建对应数据源的蜘蛛，数据源和爬虫文件名规律相关，未来业务扩展还会有其他爬取源

# 目录创建完成
├── README.md
├── canadaJobs
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   └── settings.cpython-38.pyc
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── JobbankSpider.py
│       ├── __init__.py
│       └── __pycache__
│           └── __init__.cpython-38.pyc
└── scrapy.cfg

```
## items.py 设计数据字典
- 选择你要爬取的网页，观察分析GET、POST、HEADER请求参数
- https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=Moncton&sort=D

- 我们需要获取每条招聘详情的字段如下：
  - 职位名
  - 公司名
  - 工作地点
  - 薪资
  - 发布时间

因此，我们需要根据这些来定义一个CanadajobsItem词典，也就是一条爬取下来的数据结构信息。 参考items.py文件内的CanadajobsItem词典
```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义了一个名字叫 CanadajobsItem 的字典，然后给这个字典定义了6个键
class CanadajobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    company   = scrapy.Field()
    job_href  = scrapy.Field()
    location  = scrapy.Field()
    salary    = scrapy.Field()
    post_date = scrapy.Field()
    pass

```

## spiders/JobSpider.py
使用scrapy创建项目和爬虫获取了规范的项目命名和目录，设计确定了我们想要的字典数据结构，接下来设计和处理爬虫程序。

在写程序前，梳理一下逻辑思路
- 替换数据源网址中的关键参数，请求爬取页面；
- 使用selector对页面解析过滤，把所需字段装载到准备好的字典数据结构中，通过pipeline来进行处理；
- 找到下一页的anchor标签的链接地址；
- 如果能找到下一页的话，就递归回到第一步；

开始编写 spiders/JobSpider.py
- from导入之前准备好的词典数据结构
- 通过start_urls开始爬取
- 扩展parse函数


### scrapy 的 selector对象
爬取网页，最常见的任务是从HTML源码中提取数据，Scrapy不是唯一的工具，有以下可选和优缺点使用场景，
- BeautifulSoup网页分析库，缺点慢
- lxml 是一个基于 ElementTree (不是Python标准库的一部分)的python化的XML解析库(也可以解析HTML)。

Scrapy提取数据有自己的一套机制。它们被称作选择器(seletors)，因为他们通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分。Scrapy选择器构建于 lxml 库之上，这意味着它们在速度和解析准确性上非常相似。


## pipelines.py
pipelines用来处理scrapy爬取完页面然后解析出来的item。很多人不理解程序设计上，为什么有pipelines这个环境，甚至觉得多一个环境麻烦。pipelines环节可以清洗、去重、合并、加工数据然后进行存储。如果程序项目随着时间推移，你的项目经验越丰富，你会越感受到好处。


## settings.py
- 项目设置，DEFAULT_REQUEST_HEADERS 可以给定默认的请求头。可以参考Request Headers；
- ITEM_PIPELINES 开启 pipelines

## 运行项目架构
软件开发的个人习惯是不同的，我比较习惯先设计后编码，再优化，良好的结构快速部分实现，上线小步快跑。这里每个类里的函数方法，不需要花很多时间特别具体实现，print对应信息也可以。良好的架构有助于个人能力提升，提高项目的寿命和可维护性，同时也会减少自己的开发压力，降低公司成本。如果你觉得你开发的需求很凌乱，那么这个不在技术讨论范围内。
需求凌乱造成的系统程序结构崩溃不易于维护，这个属于产品和项目、技术管理范围内容。

在项目根目录，我们执行如下命令
```python
    scrapy crawl JobbankSpider # JobbankSpider 是创建蜘蛛爬虫文件的名称
    scrapy crawl JobbankSpider -t csv -o JobbankSpider.csv --loglevel=INFO # 到处CSV
```

## 剩余的细节
- 数据清洗，例如不规范的价格
- 数据去重，相同的内容ID只保留一次
- 异常处理，网络异常、数据解析异常，中断后如何让爬虫继续
- 页面和数据分析，爬取和反爬取