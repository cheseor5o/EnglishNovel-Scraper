import scrapy
from mySpider.items import EnglishNovelItem
import random


class EnglishnovelSpider(scrapy.Spider):
    # 这个name是整个爬虫的项目名
    name = 'EnglishNovel'
    allowed_domains = ['novel.tingroom.com']
    domain = "http://novel.tingroom.com"
    # 该小说网站下一共有以下几个类别的分类,并且每个分类下的小说不一样,因此想要爬光全部小说不仅涉及到翻页还得选择目录
    '''经典:jingdian,双语:shuangyu,名人:mingren,励志:lizhi,短篇:duanpian,科幻:kehuan,儿童:ertong,宗教:zongjiao'''

    # 创建了一个包含各个目录的列表,然后随机选择一个目录并从列表里去除,再将其与index.html拼接成一个具体类别的定位符
    catalog = ["jingdian", "shuangyu", "mingren", "lizhi", "duanpian", "kehuan", "ertong", "zongjiao"]
    next_catalog = random.choice(catalog)
    catalog.remove(next_catalog)
    next_url = "/" + next_catalog + "/index.html"

    # 爬虫开始爬取的第一个网站
    start_urls = [domain + next_url]

    # 解析网页的函数
    def parse(self, response):
        # 分析网页发现,整整一页可以有10个小说信息,并且都在相同的父xpath节点组中,接下来遍历这个组中的每个节点即可得到每一个具体的小说信息
        node_list = response.xpath("//div[@class='list']")
        for node in node_list:
            # 实例化在管道文件里定义的所要爬取的项目
            item = EnglishNovelItem()

            # 小说名称
            name = node.xpath("./div[@class='text']/h6/a/text()").extract()[0]
            # 小说分类
            catalog = node.xpath("./div[@class='text']/p/a/text()").extract()[0]
            # 小说介绍
            instruction = node.xpath("./div[@class='text']/p[@class='intro11']/text()").extract()[0]
            # 小说作者, 因为观察得到有些小说没有作者,所以得进行一个判断: 有作者的小说xpath里会有作者具体的href来跳转查看作者信息,无作者的则无href,即可判断
            if len(node.xpath("./div[@class='text']/p/span[@class='point']/a/text()")):
                author = node.xpath("./div[@class='text']/p/span[@class='point']/a/text()").extract()[0]
            else:
                author = "Unknown 未知"

            # 将数据赋值给item项目
            item['NovelName'] = name
            item['NovelCatalog'] = catalog
            item['NovelAuthor'] = author
            item['NovelInstruction'] = instruction

            # 返回数集,并进行下一个节点的遍历和数据提取
            yield item

        # 当这一页的全部小说信息都获取完之后也就是节点遍历完之后则会运行到这里来进行翻页跳转或选择下一个目录的处理
        # 这里获取网页中 '上一页'的url,并判断这个url中有没有index子字符串,因为我们是从第一页开始爬取的也就是index.html开始爬的
        # 为什么不获取 '下一页'的url:因为每个分类下 '下一页'具体的xpath不同但是'上一页'永远是第一个位置
        self.next_url = "http://novel.tingroom.com" + str(
            response.xpath("//div[@class='pages']/a[1]/@href").extract()[0])
        # 如果没有index,则跳转下一个url并且回调parse()解析函数继续遍历节点提取数据
        if "index" not in self.next_url:
            yield scrapy.Request(self.next_url, callback=self.parse)
        # 这一步的条件是已经遍历完一整个目录下的页数然后进行选择下一个目录的处理; 先判断目录是否为空,因为每次选择一个目录都会在列表中删去这个目录
        elif (self.catalog != []):
            self.next_catalog = random.choice(self.catalog)
            self.catalog.remove(self.next_catalog)
            # 随机选择目录后并拼接成一个url回调parse()解析函数然后继续重复以上的递归直到目录列表为空
            yield scrapy.Request(self.domain + "/" + self.next_catalog + "/index.html", callback=self.parse)
        # 结束
        else:
            return
