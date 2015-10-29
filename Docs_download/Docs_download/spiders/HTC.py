# -*- coding: utf-8 -*-
import scrapy


class SheetSpider(scrapy.Spider):
    name = "htc"
    #allowed_domains = ["baidu.com"]
    start_urls = (
        'http://www.htckorea.co.kr/chinese/sub02.php',
    )
    def __init__(self):
        self.fp = open('htc/main/htc.csv', 'w+')
        title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet']
        tpl = ['"%s"'] * len(title)
        self.fp.write((','.join(tpl) % tuple(title)) + "\n")

        self.fp1 = open(u'htc/手册/sheet.csv', 'w+')
        title = ['brand', 'Series', 'PartNo', 'FileTpye', 'Url']
        tpl = ['"%s"'] * len(title)
        self.fp1.write((','.join(tpl) % tuple(title)) + "\n")

    def parse(self, response):
        #test = response.xpath('//td/a/strong/text() | //td/strong/a/text() | //td/p/strong/a/text()').extract()
        #url = response.xpath('//td/a[@class="link_6"]/@href | //td/strong/a[@class="link_6"]/@href | //td/p/strong/a[@class="link_6"]/@href').extract()
        #print url, response.urljoin(url[0])
        #print len(test), len(url)
        
        #test = response.xpath('//td[@background="../img/center03.gif"]')
        test = response.xpath('//table[@width="654"]').extract()
        print len(test)
        for tr in response.xpath('//table[@width="654"]'):
            url_lst = response.xpath('.//td/a[@class="link_6"] | .//td/strong/a[@class="link_6"] | .//td/p/strong/a[@class="link_6"]')

            for row in url_lst:
                sn = row.xpath('./strong/text() | ./text()').extract()[0]
                url = row.xpath('./@href').extract()[0]
                yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta = {'sn' : sn})

    def secondary_parse(self, response):
        pdf_url = response.xpath('//td/a[@class="link_6"]/@href').extract()
        pdf_url = map(response.urljoin, pdf_url)
        title = response.xpath('//td[@class="text11-6"]/text()').extract()
        if title:
            title = title[0].split('>')[2]
        else:
            title = '-'
        data = ['htc', title, response.meta['sn'], response.url] + pdf_url
        tpl = ['"%s"'] * len(data)
        self.fp.write((','.join(tpl) % tuple(data)) + "\n")

        data = ['htc', title, response.meta['sn'], 'dataSheet'] + pdf_url
        tpl = ['"%s"'] * len(data)
        self.fp1.write((','.join(tpl) % tuple(data)) + "\n")

    def closed(spider, reason):
        spider.fp.close()
        spider.fp1.close()