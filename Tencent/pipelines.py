# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class TencentPipeline:
    def __init__(self):
        print("#" * 30)
        print("这里是TencentPipeline的__init__")
        print("#" * 30)
        self.f=open('51job.json','w')

    def process_item(self, item, spider):
        jsondata = json.dumps(dict(item), ensure_ascii=False)+",\n"
        print(jsondata)
        self.f.write(jsondata)
        print("@" * 30)
        print("这里是TencentPipeline的process_item")
        print("@" * 30)
        return item

    def close_spider(self, spider):
        print("#" * 30)
        print("这里是TencentPipeline的close_spider")
        print("#" * 30)
        self.f.close()



import logging
from pymysql import cursors
from twisted.enterprise import adbapi
import time
import copy
class MySQLPipeline:
    def __init__(self,db_pool):
        self.db_pool = db_pool
        print("&"*30)
        print("这里是MySQLPipeline的__init__")
        print("&" * 30)

    @classmethod
    def from_settings(cls, settings):
        """类方法，只加载一次，数据库初始化"""
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        print("!" * 30)
        print(db_params)
        print("!" * 30)
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        print("@" * 30)
        print("这里是MySQLPipeline的process_item")
        print("@" * 30)

        logging.warning(item)
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        asynItem = copy.deepcopy(item)
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, asynItem)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)
        return item

    def close_spider(self, spider):
        print("#" * 30)
        print("这里是MySQLPipeline的close_spider")
        print("#" * 30)

    # 处理sql函数
    def insert_into(self, cursor, item):
        createtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 创建sql语句
        sql = "INSERT INTO position (`name`,company,place,salary,`time`,createtime) " \
              "VALUES ('{}','{}','{}','{}','{}','{}')".format(item['name'], item['company'], item['place'], item['salary'],item['time'], createtime)
        # 执行sql语句
        cursor.execute(sql)
        # 错误函数

    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)
