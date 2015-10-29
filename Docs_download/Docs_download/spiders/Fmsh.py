# -*- coding: utf-8 -*-
import scrapy
import re, codecs


class FmshSpider(scrapy.Spider):
    name = "fmsh"
    allowed_domains = ["fmsh.com"]
    start_urls = (
        'http://www.fmsh.com/products.shtml',
    )

    def  __init__(self):
        self.sheet = codecs.open(u'fmsh/手册/sheet.csv', 'w+', 'utf_8_sig')
        title = ['brand', 'Series', 'PartNo', 'FileTpye', 'Url']
        self.sheet.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")

    def parse(self, response):
        for dl in response.xpath('//div[@class="products"]/dl'):
            name = dl.xpath('./dt/a/text()').extract()[0]
            for dd in dl.xpath('./dd'):
                c_name = name + '---' + dd.xpath('./a/text()').extract()[0]
                url = dd.xpath('./a/@href').extract()[0]
                
                if name == '安全与识别芯片':
                    yield scrapy.Request(response.urljoin(url), callback=self.tertius_parse, meta={'name' : name})
                    break
                else:
                    yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta={'name' : c_name})
            # break

    def secondary_parse(self, response):
        pattern = r'var data = \s*\'(.+?)\';'
        regular = re.compile(pattern, re.DOTALL)
        head = regular.findall(response.body)
        if head:
            title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet'] + head[0].split(',')
            csv_str = ','.join(['"%s"'] * len(title)) % tuple(title) + "\n"
            sheet_str = ''

            for tr in response.xpath('//tr[@class="xunhuan"]'):
                type_num = tr.xpath('./td[1]/a/text()').extract()[0]
                sheet_url = tr.xpath('./td[1]/a/@href').extract()[0]
                data = []
                for td in tr.xpath('./td'):
                    text = td.xpath('./text()').extract()
                    if text:
                        data.append(text[0])
                    else:
                        data.append('-')
                del data[0]
                del data[0]
                data = ['fmsh', response.meta['name'], type_num, response.url, response.urljoin(sheet_url)] + data
                tpl = ['"%s"'] * len(data)
                csv_str += ','.join(tpl) % tuple(data) + "\n"
                sheet_data = ['fmsh', response.meta['name'], type_num, 'Datasheet', response.urljoin(sheet_url)]
                sheet_str += ','.join(['"%s"'] * len(sheet_data)) % tuple(sheet_data) + "\n"

            self.sheet.write(sheet_str)

            fp = codecs.open('fmsh/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
            fp.write(csv_str)
            fp.close()


    def tertius_parse(self, response):
        dd = response.xpath('//li[@class="now"]/dl/dd[1]')
        path_a = './a[%s]/text()'
        path_div = './div[%s]/a'

        for x in xrange(1,4):
            name = dd.xpath(path_a % x).extract()[0]
            for a in dd.xpath(path_div % x):
                c_name = response.meta['name'] + '---' + name + '---' + a.xpath('./text()').extract()[0]
                url = a.xpath('./@href').extract()[0]
                yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta={'name' : c_name})
            #     break
            # break

    def closed(spider, reason):
        spider.sheet.close()