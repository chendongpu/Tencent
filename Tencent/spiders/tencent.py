import scrapy
from Tencent.items import TencentItem
from urllib.request import quote
from Tencent.util import dehtml

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['51job.com']
    key = "广州译语言翻译服务有限责任公司"
    offset = 1
    #https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html
    baseURL = "https://search.51job.com/list/000000,000000,0000,00,9,99," + quote(key) + ",2,"

    start_urls = [baseURL + str(offset) + ".html"]

    def parse(self, response):
        node_list = response.xpath("//div[@id='resultList']/div[@class='el'][position()>0]")

        for node in node_list:
            item = TencentItem()

            name = node.xpath("./p/span/a/text()").extract()[0].encode("utf-8")

            name = str(name, encoding="utf-8")

            item['name'] = name.replace('\n', '').replace('\r', '').replace(' ','')

            company= node.xpath("./span[@class='t2']/a/text()").extract()[0].encode("utf-8")
            company = str(company, encoding="utf-8")
            item['company'] = company


            place= node.xpath("./span[@class='t3']/text()").extract()[0].encode("utf-8")
            place = str(place, encoding="utf-8")
            item['place'] = place

            if len(node.xpath("./span[@class='t4']/text()")):
                salary= node.xpath("./span[@class='t4']/text()").extract()[0].encode("utf-8")
                salary = str(salary, encoding="utf-8")
                item['salary'] = salary
            else:
                item['salary'] = ""

            time = node.xpath("./span[@class='t5']/text()").extract()[0].encode("utf-8")
            time = str(time, encoding="utf-8")
            item['time'] = time

            href=node.xpath("./p/span/a/@href").extract()[0].encode("utf-8")
            href = str(href, encoding="utf-8")
            print("=" * 30)
            print(href)
            print("=" * 30)
            if type(href) == str:
                yield scrapy.Request(
                    href,
                    callback=self.parse_detail,
                    meta={"item": item}
                )


        if len(response.xpath("//div[@class='p_in']/ul/li[@class='bk'][position()=2]/a"))!=0:
            url=response.xpath("//div[@class='p_in']/ul/li[@class='bk'][position()=2]/a/@href").extract()[0]
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        # 获取详情页的岗位介绍
        desc=response.xpath("//div[@class='bmsg inbox']/p[@class='fp']/text()").extract()[0].encode("utf-8")
        desc = str(desc, encoding="utf-8")
        print("=" * 30)
        print(desc)
        print("=" * 30)
        item["requirement"] = dehtml(desc)
        yield item