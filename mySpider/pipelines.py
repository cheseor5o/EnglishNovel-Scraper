# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch

import json
import csv
import codecs


class EnglishNovelPipeline:
    # 初始化函数,一次创建json和csv文件
    def __init__(self):
        self.f = open("Novel.json", "wb+")
        self.g = codecs.open("Novel.csv", "w", "utf_8_sig")  # 防止中文乱码
        self.writer = csv.writer(self.g)

        # 这步之前要提前启动好Elasticsearch,且端口好防止被占用
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # 写数据进文件的函数,多次调用
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        # 写入json文件,并防止中文乱码
        self.f.write(content.encode("utf-8"))

        # 按行依次写入csv文件
        self.writer.writerow([item["NovelName"], item["NovelCatalog"], item["NovelAuthor"], item["NovelInstruction"]])

        # 写入ES索引, 索引名为 englishnovel (全小写),类型为 'novel'
        self.es.index(index='englishnovel', doc_type="novel",
                      body={'NovelName': item["NovelName"], 'NovelCatalog': item["NovelCatalog"],
                            'NovelAuthor': item["NovelAuthor"], "NovelInstruction": item["NovelInstruction"]})

        # 接下来也还可以继续写入其他类型数据库或文件类型的操作,类似Mysql,txt什么的

        # 返回给引擎,让爬虫继续工作
        return item

    # 关闭
    def close_spider(self, spider):
        self.f.close()
        self.g.close()
