# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import DocsDownloadItem


class SheetSpider(scrapy.Spider):
    name = "HTC_Sheet"
    #allowed_domains = ["baidu.com"]
    start_urls = (
        'http://www.htckorea.co.kr/chinese/sub02.php',
    )

    def parse(self, response):
        #test = response.xpath('//td/a/strong/text() | //td/strong/a/text() | //td/p/strong/a/text()').extract()
        url = response.xpath('//td/a[@class="link_6"]/@href | //td/strong/a[@class="link_6"]/@href | //td/p/strong/a[@class="link_6"]/@href').extract()
        #print url, response.urljoin(url[0])
        #print len(test), len(url)
        url_lst = response.xpath('//td/a[@class="link_6"] | //td/strong/a[@class="link_6"] | //td/p/strong/a[@class="link_6"]')
        for row in url_lst:
            sn = row.xpath('./strong/text() | ./text()').extract()[0]
            url = row.xpath('./@href').extract()[0]
            yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta = {'sn' : sn})

    def secondary_parse(self, response):
        pdf_url = response.xpath('//td/a[@class="link_6"]/@href').extract()
        Item = DocsDownloadItem()
        Item['sn'] = response.meta['sn']
        Item['pdf_url'] = map(response.urljoin, pdf_url)
        #print '==========', response.meta['sn']
        #print test

        return Item