# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class TencentPipeline:
    def __init__(self):
        self.f=open('51job.json','w')

    def process_item(self, item, spider):
        print("&" * 30)
        print(dict(item))
        print("&" * 30)



        jsondata = json.dumps(dict(item), ensure_ascii=False)+",\n"
        print(jsondata)
        self.f.write(jsondata)
        return item

    def close_spider(self, spider):
        self.f.close()