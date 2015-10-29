# -*- coding: utf-8 -*-
import scrapy
import re, codecs


class FmshSpider(scrapy.Spider):
    name = "zlgmcu_fsl"
    allowed_domains = ["zlgmcu.com"]
    start_urls = (
        'http://new.zlgmcu.com/Category_59/Index.aspx?/',
    )

    def  __init__(self):
        self.sheet = codecs.open(u'zlgmcu/手册/sheet_zlgmcu_fsl.csv', 'w+', 'utf_8_sig')
        title = ['brand', 'Series','FileType', 'Title', 'Url']
        self.sheet.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")

    def parse(self, response):
        for li in response.xpath('//table/tr/td/div[@class="zlg-side"]/div[@class="zlg-trees"]/ul[@class="zlg-trees-wrap"]/li[1]'):
            # print  li.extract()
            li2_list = li.xpath('./ul/li')
            for li2 in li2_list:
                Series2 = li2.xpath('./div/a/span/text()').extract()[0]
                print  Series2
                li3_list = li2.xpath('./ul/li')
                for li3 in li3_list:
                    Series3 = li3.xpath('./div/a/span/text()').extract()[0]
                    print  Series3
                    li4_list = li3.xpath('./ul/li')
                    for li4 in li4_list:
                        Series4 = li4.xpath('./div/a/span/text()').extract()[0]
                        url = li4.xpath('./div/a/@href').extract()[0]
                        Series = Series2 + '---' + Series3.replace(',','，') + '---' + Series4.replace(',','，')
                        print  Series
                        print  url
                        yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta = {'Series' : Series})

    def secondary_parse(self, response):
        dl_list = response.xpath('//div[@class="Tab-space Tab-filter"]/dl')
        for dl in dl_list:
            FileType = dl.xpath('./dt/text()').extract()[0]
            dd_list = dl.xpath('./dd/a')
            for dd in dd_list:
                Title = dd.xpath('./text()').extract()[0]
                url = dd.xpath('./@href').extract()[0]
                csv_str = 'NXP' + ',' + 'MCU---' +  response.meta['Series'] + ',' + FileType +  ',' + Title +  ',' + url + "\n"
                # print csv_str
                self.sheet.write(csv_str)

    def closed(spider, reason):
        spider.sheet.close()