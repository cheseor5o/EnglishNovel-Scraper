# 依赖环境

- Python 3
- Scrapy
- random, json, csv, codecs,elasticsearch...
- Elasticsearch-7.11.1 (port:9200     jdk:1.8 ES自带)

# 项目结构

- **mySpider** ：爬虫项目的主要文件夹
- **novelData**：爬取的数据存放文件夹
- **scrapy.cfg**：爬虫项目的配置文件

# 项目说明

`(以下仅说明几个项目中重要编写的文件,其他均以框架自动生成不做叙述)`

1. **mySpider**

   ​	-spiders

   ​		**-EnglishNovel.py**：爬虫项目的主要文件, 解析网页、分析路径、跳转链接、选择目录

   ​	**-items.py**：定义爬虫要获取的四个数据（小说名字、目录、作者及介绍）

   ​	**-piplines.py**：以流水线的形式处理爬虫引擎传来的item，并进行写入json、csv文件和保存在ES中的处理

   ​	**-settings.py**：设置爬虫的文件，这里仅设置启动了此爬虫的管道文件

2. **novelData**

   ​	`cd D:\dev\mySpider\novelData` 在此文件夹下进入`cmd`命令行输入 `scrapy crawl EnglishNovel` 即可启动爬虫项目并将数据集储存在此文件夹下
   
   ​	在此文件夹下有一个`DataToES.py`文件，运行后可以将`csv`格式的文件数据导入到`ElasticSearch`的索引中去；在`piplines.py`文件中已经完成将数据导入到`ES`中，这一步提供另一种导入的方法

