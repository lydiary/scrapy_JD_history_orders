# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from ..items import JdItem


class JdspiderSpider(scrapy.Spider):
    name = 'jdspider'
    allowed_domains = ['jd.com']
    start_urls = ['https://order.jd.com/center/list.action?search=0&d=2017&s=4096']
    page_number = 1

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, meta={'browser': True}, callback=self.parse)

    def parse(self, response):
        print('scrapying %dth page' % self.page_number)
        self.page_number += 1

        selector = Selector(text=response.text)
        jditem = JdItem()
        items = selector.xpath('//*[@id="order02"]/div[2]/table/tbody')
        for item in items:
            try:
                status = item.xpath('.//span[@class="order-status ftx-03"]/text()').extract_first().strip(' \n\t')
                if status != '已完成':
                    continue

                jditem['status'] = status
                jditem['id'] = item.xpath('@id').extract_first().split('-')[-1]
                jditem['product_name'] = item.xpath('.//div[@class="p-name"]/a/text()').extract_first()
                jditem['receive_user'] = item.xpath('.//span[@class="txt"]/text()').extract_first()
                jditem['number'] = int(item.xpath('.//div[@class="goods-number"]/text()').extract_first().strip(' \n').split('x')[-1])
                jditem['price'] = float(item.xpath('.//div[@class="amount"]/span/text()').extract_first().strip(' ').split('总额 ¥')[-1])
                jditem['dealtime'] = item.xpath('.//span[@class="dealtime"]/text()').extract_first()
                yield jditem
            except:
                continue

        next_page = selector.xpath('//a[@class="next"]/@href')
        if next_page:
            yield response.follow(url=next_page.extract_first(),
                                  meta={'browser': True},
                                  callback=self.parse)
