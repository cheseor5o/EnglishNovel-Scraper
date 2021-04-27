# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EnglishNovelItem(scrapy.Item):
    #定义具体的要获取的爬虫数据
    NovelName = scrapy.Field()
    NovelCatalog = scrapy.Field()
    NovelAuthor = scrapy.Field()
    NovelInstruction = scrapy.Field()
