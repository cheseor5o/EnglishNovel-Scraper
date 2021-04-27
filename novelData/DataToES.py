from elasticsearch import Elasticsearch
import csv

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
with open("Novel.csv") as f:
    reader = csv.reader(f)

    for item in reader:
        es.index(index='englishnovel1', doc_type="novel1",body={'NovelName': item[0], 'NovelCatalog': item[1],'NovelAuthor': item[2], "NovelInstruction": item[3]})

print("数据完成导入ElasticSearch")