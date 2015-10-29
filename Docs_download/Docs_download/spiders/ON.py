# -*- coding: utf-8 -*-
import scrapy
import re, csv, codecs, re, copy


class OnSpider(scrapy.Spider):
    name = "on"
    allowed_domains = ["onsemi.cn"]
    start_urls = (
        'http://www.onsemi.cn/PowerSolutions/products.do',
    )

    def __init__(self):
        self.fp = codecs.open(u'on/手册/sheet.csv', 'w+', 'utf_8_sig')
        title = ['"brand"', '"Series"', '"Series-2"', '"PartNo"', '"FileType"', '"Url"']
        csv_str = ','.join(title) + "\n"
        self.fp.write(csv_str)

    def parse(self, response):
        urls = response.xpath('//table[@id="productMapHome"]').xpath('.//a[contains(@href, "/PowerSolutions/taxonomy.do?id=")]/@href').extract()
        special = []
        pattern = 'type=Family'
        regular = re.compile(pattern, re.DOTALL)
        
        for url in urls:
            if regular.findall(url):
                special.append(url)
                print url
                continue
            yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse)
            #break
        
    def secondary_parse(self, response):
        name = response.xpath('//h1[@class="taxonomyTitle"]/text()').extract()[0].strip()
        name = re.sub(r'\s*\[.+\]\s*', '', name)
        a_tag = response.xpath('//a[@style="color:#fff;font-size:14px;"]')

        for val in a_tag:
            url = val.xpath('./@href').extract()[0]
            c_name = val.xpath('./text()').extract()
            if len(c_name) > 1:
                c_name = name + '---' + val.xpath('./sub/text()').extract()[0].join(c_name).strip()
            else:
                c_name = name + '---' + c_name[0].strip()
            param = '&action=excelCsv&actionData=undefined&sortOrder=asc&sortProperty=&currPage=1&pageSize=0'
            
            yield scrapy.Request(response.urljoin(url) + param, method='POST', callback=self.tertius_parse, meta={'name' : c_name, 'url' : response.urljoin(url)})
            #break

    def tertius_parse(self, response):
        param = '&action=setPageSize&actionData=0&sortOrder=asc&sortProperty=&currPage=1&pageSize=0'
        csv_lst = response.body.strip('"\n').split('"\n"')

        return scrapy.Request(response.meta['url'] + param, method='POST', callback=self.quartus_parse, meta={'name' : response.meta['name'], 'csv_lst' : csv_lst})

        #fp = open('on/sheet/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+')
        #fp.write(response.body)
        #fp.close()

    def quartus_parse(self, response):
        sheet = {
            '应用注释' : 'AppNotes',
            '辅助小册子' : 'Brochures',
            '遵从性报告' : 'Conformance Report',
            '数据表' : 'Datasheets',
            '设计注释' : 'Design Notes',
            '设计和开发工具' : 'tools',
            'Errata' : 'Errata/Addendum',
            '评估板文档' : 'boards',
            '封装图纸' : 'drawing',
            '参考设计' : 'Reference Designs', 
            '参考手册' : 'manuals',
            '仿真模型' : 'models',
            '培训教材' : 'Tutorials',
            '视频' : 'Video',
            '软件' : 'software',
            '白皮书' : 'White Papers'
        }
        sheet_url = 'http://www.onsemi.cn/PowerSolutions/supportDoc.do?type=%s&part=%s&action=setPageSize&actionData=0&sortOrder=asc&sortProperty=&currPage=1&pageSize=0'
        detail_url = 'http://www.onsemi.cn/PowerSolutions/product.do?id=%s'
        csv_lst = response.meta['csv_lst']
        title = '"' + csv_lst[0] + '"'
        title = title.split(',')
        title[0:1] = ['"brand"', '"Series"', '"Series-2"', '"PartNo"', '"DetailLink"', '"dataSheet"', '"Descrption"']
        del csv_lst[0]

        csv_str = ','.join(title) + "\n"
        path = '//tr[@rpnid="%s"]/td[@class="productDocIcon"]/a/@href'
        path_2 = '//tr[@class="oddListItem opn_%s opnDetail"]'

        for val in csv_lst:
            val = '"' + val + '"'
            val_lst = val.split(',')
            id = val_lst[0]
            type_num = id.split(' ')[0].strip('"')
            try:
                dataSheet_url = response.xpath(path % type_num).extract()[0]
            except:
                dataSheet_url = '-'
            #val_lst[0:1] = ['"on"', '"' + response.meta['name'] + '"', id, '"%s"', '"' + detail_url + '"', '"' + dataSheet_url + '"']

            for tr in response.xpath(path_2 % type_num):
                part_num = tr.xpath('./td[2]/text()').extract()
                if part_num:
                    part_num = part_num[0]
                    copy_lst = copy.deepcopy(val_lst)
                    desc = tr.xpath('./td[6]/a/text()').extract()[0].strip()
                    copy_lst[0:1] = ['"on"', '"' + response.meta['name'] + '"', id, '"' + part_num + '"', '"' + (detail_url % part_num) + '"', '"' + dataSheet_url + '"', '"' + desc + '"']
                    csv_str += ','.join(copy_lst) + "\n"
                    for (key,val) in sheet.items():
                        yield scrapy.Request(sheet_url % (val, part_num), method='POST', callback=self.fifth, meta={'name' : response.meta['name'], 'type' : key, 'type_num' : type_num, 'part_num' : part_num})

            #break

            

        fp = codecs.open('on/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
        fp.write(csv_str)
        fp.close()

    def fifth(self, response):
        csv_str = ''
        for tr in response.xpath('//tr[@id]'):
            if tr.extract():
                sheet_url = tr.xpath('./td[1]/a/@href').extract()[0]
                data = ['on', response.meta['name'], response.meta['type_num'], response.meta['part_num'], response.meta['type'], response.urljoin(sheet_url)]
                csv_str += ','.join(['"%s"'] * len(data)) % tuple(data) + "\n"
               
        self.fp.write(csv_str) 

    def closed(spider, reason):
        spider.fp.close()