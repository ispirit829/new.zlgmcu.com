# -*- coding: utf-8 -*-
import scrapy
import codecs, re


class MxicSpider(scrapy.Spider):
    name = "mxic"
    allowed_domains = ["macronix.com"]
    start_urls = (
        'http://www.macronix.com/en-us/Product/NORFlash/pages/UltraLowPowerFlash.aspx',
    )

    def __init__(self):
        self.crawl_list = {
            'NOR Flash---Ultra Low Power Flash' : 'http://www.macronix.com/_layouts/15/ajaxfeed/ajax_ProductUltraLowPower.aspx',
            'NOR Flash---Serial NOR Flash' : 'http://www.macronix.com/CachePages/en-us-Product-NORFlash-SerialFlash.aspx#1Gb',
            'NOR Flash---Parallel NOR Flash' : 'http://www.macronix.com/CachePages/en-us-Product-NORFlash-ParallelFlash.aspx#1Gb',
            'NOR Flash---MCP' : 'http://www.macronix.com/en-us/Product/NORFlash/Pages/MCP.aspx',
            'NOR Flash---WLCSP' : 'http://www.macronix.com/_layouts/15/ajaxfeed/ajax_ProductWLCSP.aspx',
            'NAND Flash---SLC NAND' : 'http://www.macronix.com/CachePages/en-us-Product-NANDFlash-SLCNAND.aspx#8Gb',
            'NAND Flash---Serial NAND' : 'http://www.macronix.com/en-us/Product/NANDFlash/pages/SerialNAND.aspx?ProdCat=Serial%20NAND#2Gb',
            'NAND Flash---MCP' : 'http://www.macronix.com/en-us/Product/NANDFlash/Pages/MCP.aspx',
            'ROM (Read-Only Memory)' : 'http://www.macronix.com/CachePages/en-us-Product-ROM-default.aspx#128Mb',
            'PCN/EOL' : 'http://www.macronix.com/CachePages/en-us-Product-PCNEOL-default.aspx'
        }
        self.sheet = codecs.open(u'mxic/手册/sheet.csv', 'w+', 'utf_8_sig')
        title = ['brand', 'Series', 'PartNo', 'FileTpye', 'Url']
        self.sheet.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")

    def parse(self, response):
        for (name,url) in self.crawl_list.items():
            yield scrapy.Request(url, callback=self.secondary_parse, meta={'name' : name})
            #break

    def secondary_parse(self, response):
        if 'NOR Flash---Ultra Low Power Flash' == response.meta['name'] or 'NOR Flash---WLCSP' == response.meta['name']:
            title = response.xpath('//tr[1]/td/text()').extract()
            title = title[1:-1]
            title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet'] + title
            fp = codecs.open(u'mxic/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
            fp.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
            csv_str = ''
            for tr in response.xpath('//tr[position()>1]'):
                part_num = tr.xpath('./td[1]/a/text()').extract()
                if not part_num:
                    continue
                else:
                    part_num = part_num[0]
                detail_url = tr.xpath('./td[1]/a/@href').extract()[0]
                sheet_url = tr.xpath('./td[last()]/a/@href').extract()[0]
                data = []
                for td in tr.xpath('./td[position()>1]'):
                    text= td.xpath('./text()').extract()
                    if text:
                        data.append(' '.join(text))
                    else:
                        data.append('-')
                data = ['mxic', response.meta['name'], part_num, response.urljoin(detail_url), response.urljoin(sheet_url)] + data
                csv_str += ','.join(['"%s"'] * len(data)) % tuple(data) + "\n"
                yield scrapy.Request(response.urljoin(detail_url), callback=self.tertius_parse, meta={'name' : response.meta['name'], 'part_num' : part_num}, dont_filter=True)
            fp.write(csv_str)
            fp.close()
        elif 'NOR Flash---MCP' == response.meta['name'] or 'NAND Flash---MCP' == response.meta['name']:
            name = response.meta['name']
            type = {'NOR Flash---MCP' : 1, 'NAND Flash---MCP' : 2}
            table = response.xpath('//div[@id="DeltaPlaceHolderMain"]//table[%s]' % type[name])
            title = []
            for th in table.xpath('.//tr[1]/td'):
                text = th.xpath('./text()').extract() + th.xpath('./sub/text()').extract()
                if text:
                    title.append(' '.join(text))
                else:
                    title.append('-')
            title = title[1:-1]
            title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet'] + title
            fp = codecs.open(u'mxic/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
            fp.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
            csv_str = ''
            sheet_str = ''
            for tr in table.xpath('.//tr[position()>1]'):
                if len(tr.xpath('./td').extract()) < 2:
                    continue
                part_num = tr.xpath('./td[1]/text()').extract()[0]
                sheet_url = tr.xpath('./td[last()]/a/@href').extract()
                if sheet_url:
                    sheet_url = response.urljoin(sheet_url[0])
                else:
                    sheet_url = '-'
                data = []
                for td in tr.xpath('./td[position()>1]'):
                    text= td.xpath('./text()').extract()
                    if text:
                        data.append(' '.join(text))
                    else:
                        data.append('-')
                data = ['mxic', response.meta['name'], part_num, response.url, sheet_url] + data
                csv_str += ','.join(['"%s"'] * len(data)) % tuple(data) + "\n"
                if '-' != sheet_url:
                    sheet_data = ['mxic', response.meta['name'], part_num, 'Datasheets', sheet_url]
                    sheet_str += ','.join(['"%s"'] * len(sheet_data)) % tuple(sheet_data) + "\n"
            self.sheet.write(sheet_str)
            fp.write(csv_str)
            fp.close()
        else:
            title = []
            for th in response.xpath('//div[contains(@id, "Table")][1]//tr[1]/td'):
                text = th.xpath('./text()').extract() + th.xpath('./sub/text()').extract()
                if text:
                    title.append(' '.join(text))
                else:
                    title.append('-')
            title = title[1:-1]
            title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet', 'Density'] + title
            fp = codecs.open(u'mxic/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
            fp.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
            csv_str = ''
            for table in response.xpath('//div[contains(@id, "Table")]'):
                name = response.meta['name']
                vol = table.xpath('./@id').extract()[0].split('Table')[1]

                for tr in table.xpath('.//tr'):
                    part_num = tr.xpath('./td[1]/a/text()').extract()
                    if not part_num:
                        continue
                    else:
                        part_num = part_num[0]
                    detail_url = tr.xpath('./td[1]/a/@href').extract()[0]
                    sheet_url = tr.xpath('./td[last()]/a/@href').extract()
                    if sheet_url:
                        sheet_url = response.urljoin(sheet_url[0])
                    else:
                        sheet_url = '-'
                    data = []
                    for td in tr.xpath('./td[position()>1]'):
                        text= td.xpath('./text()').extract()
                        if text:
                            data.append(' '.join(text))
                        else:
                            data.append('-')
                    data = ['mxic', response.meta['name'], part_num, response.urljoin(detail_url), sheet_url, vol] + data
                    csv_str += ','.join(['"%s"'] * len(data)) % tuple(data) + "\n"
                    yield scrapy.Request(response.urljoin(detail_url), callback=self.tertius_parse, meta={'name' : response.meta['name'], 'part_num' : part_num}, dont_filter=True)
            fp.write(csv_str)
            fp.close()

    def tertius_parse(self, response):
        sheet_str = ''
        for div in response.xpath('//div[re:test(@id, "T[1-6]")]'):
            type = div.xpath('.//tr[1]/td/span/text()').extract()[0]
            urls = div.xpath('.//tr[2]/td/a/@href').extract()
            urls = map(response.urljoin, urls)
            sheet_data = ['mxic', response.meta['name'], response.meta['part_num'], type] + urls
            sheet_str += (','.join(['"%s"'] * len(sheet_data)) % tuple(sheet_data) + "\n")
        self.sheet.write(sheet_str)
    def closed(spider, reason):
        spider.sheet.close()