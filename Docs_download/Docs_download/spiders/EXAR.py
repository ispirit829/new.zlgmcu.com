# -*- coding: utf-8 -*-
import scrapy
import codecs, re

class ExarSpider(scrapy.Spider):
    name = "exar"
    allowed_domains = ["exar.com"]
    start_urls = (
        'http://www.exar.com/power-management/technical-documentation/',
        'http://www.exar.com/data-compression/technical-documentation/',
        'http://www.exar.com/connectivity/technical-documentation/',
        'http://www.exar.com/high-performance-analog/technical-documentation/',
        'http://www.exar.com/communications/technical-documentation/',
        'http://www.exar.com/network-security/technical-documentation/',
    )

    def  __init__(self):
        self.fp = {}
        self.sheet = codecs.open(u'exar/手册/sheet.csv', 'w+', 'utf_8_sig')
        title = ['brand', 'Series', 'Series-2', 'PartNo', 'Type', 'Url']
        self.sheet.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
        
        self.doc = {
            'power-management' : {},
            'data-compression' : {},
            'connectivity' : {},
            'high-performance-analog' : {},
            'communications' : {},
            'network-security' : {}
        }
        self.crawl_list = {
            'power-management' : {
                'Power Management---Universal PMICs' : 'http://www.exar.com/power-management/universal-pmics/',
                'Power Management---Power Modules' : 'http://www.exar.com/power-management/power-modules/',
                'Power Management---Power Conversion' : 'http://www.exar.com/power-management/power-conversion/',
                'Power Management---System Controls' : 'http://www.exar.com/power-management/system-controls/',
                'Power Management---LED Lighting' : 'http://www.exar.com/power-management/led-lighting/',
            },
            'data-compression' : {
                'Data Compression---Networking Data Security & Compression' : 'http://www.exar.com/network-security/data-security-and-compression/',
            },
            'connectivity' : {
                'Connectivity---UART & Bridging Solutions' : 'http://www.exar.com/connectivity/uart-and-bridging-solutions/',
                'Connectivity---Serial Transceivers' : 'http://www.exar.com/connectivity/transceiver/',
                'Connectivity---Data Converters' : 'http://www.exar.com/connectivity/data-converters/',
            },
            'high-performance-analog' : {
                'High Performance Analog---Amplifiers, Comparators & Switches' : 'http://www.exar.com/high-performance-analog/amplifiers-comparators-and-switches/',
                'High Performance Analog---Sensor Products' : 'http://www.exar.com/high-performance-analog/sensor-products/',
                'High Performance Analog---Data Converter Products' : 'http://www.exar.com/high-performance-analog/data-converter-products/',
            },
            'communications' : {
                'Communications---PDH' : 'http://www.exar.com/communications/pdh/',
                'Communications---SDH/SONET' : 'http://www.exar.com/communications/sdh-sonet/',
                'Communications---Timing and Data I/F' : 'http://www.exar.com/communications/timing/',
            },
            'network-security' : {
                'Network Security---Networking Data Security & Compression' : 'http://www.exar.com/network-security/data-security-and-compression/',
            }
        }

    def special_work(self, response):
        series = response.meta['series']
        for table in response.xpath('//table[@class="productview-table"]'):
            c_name = response.meta['name'] + '---' + table.xpath('.//tr[1]/th[2]/text()').extract()[0].strip()
            i = 1
            for table_inside in table.xpath('.//table[@class="dstable"]'):
                title = []
                for th in table_inside.xpath('.//tr[1]/th'):
                    title.append(' '.join(th.xpath('./text()').extract()))
                title[0:1] = ['brand', 'Series', 'PartNo', 'DataSheet', 'DetailLink']

                fp = codecs.open('exar/main/' + re.sub(r'[/:|?*"\\<>]', '&', c_name) + ('-%s.csv' % i), 'w+', 'utf_8_sig')
                fp.write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
                csv_str = ''

                for tr in table_inside.xpath('.//tr[position() > 1]'):
                    detail_url = tr.xpath('.//td[1]/a/@href').extract()[0]
                    part_num = tr.xpath('.//td[1]/a/text()').extract()[0]
                    type_num = part_num
                    data = []
                    for td in tr.xpath('.//td[position() > 1]'):
                        data.append(' '.join(td.xpath('./text()').extract()))
                    data = ['exar', c_name, part_num, '-', response.urljoin(detail_url)] + data
                    tpl = ['"%s"'] * len(data)
                    csv_str += ((','.join(tpl) % tuple(data)) + "\n")
                    sheet_str = ''

                    if self.doc[series].has_key(type_num):
                        for val in self.doc[series][type_num]:
                            sheet_data = ['exar', c_name, type_num, part_num, val['type'], val['sheet_url']]
                            tpl = ['"%s"'] * len(sheet_data)
                            sheet_str += ((','.join(tpl) % tuple(sheet_data)) + "\n")
                    self.sheet.write(sheet_str)

                fp.write(csv_str)
                fp.close()
                i += 1

    def parse(self, response):
        series = response.url.split('/')[3]
        panel = response.xpath('//div[@id="ContentPlaceHolder1_UpdatePanel1"]')
        head_table = panel.xpath('./table//tr[@class="rowTitle"]/td[1]/text()').extract()
        div = panel.xpath('./div[@id]')
        num = len(head_table)
        for x in xrange(1, num + 1):
            type = head_table[x - 1]
            for tr in div[x - 1].xpath('.//tr[position() > 1]'):
                type_num = tr.xpath('./td[@class="name"]/a/text()').extract()[0]
                sheet_url = tr.xpath('./td[@class="wrap"]/a/@href').extract()[0]
                if not self.doc[series].has_key(type_num):
                    self.doc[series][type_num] = []
                self.doc[series][type_num].append({'sheet_url' : response.urljoin(sheet_url), 'type' : type})

        crawl_list = self.crawl_list[series]

        if 'data-compression' == series or 'network-security' == series:
            for (name,url) in crawl_list.items():
                yield scrapy.Request(url, callback=self.special_work, meta={'name' : name, 'series' : series}, dont_filter=True)
        else:
            for (name,url) in crawl_list.items():
                yield scrapy.Request(url, callback=self.secondary_parse, meta={'name' : name, 'series' : series})
                #break

    def secondary_parse(self, response):
        div = response.xpath('//div[@id="ContentPlaceHolder1_upProductFamilies"]')
        header = div.xpath('./div[@class="category-header"]')
        num = len(header)
        div_path = './div[@id="ContentPlaceHolder1_rptProductFamilies_upProducts_%s"]'
        for x in xrange(1, num + 1):
            text = header[x - 1].xpath('./a/text()').extract()
            if text:
                name = response.meta['name'] + '-' + text[0]
            else:
                name = response.meta['name']
            div_table = div.xpath(div_path % (x - 1)).xpath('./div[@id]')
            num_table = len(div_table)
            for k in xrange(1, num_table + 1):
                text_list = div_table[k - 1].xpath('./div/div[@class="subcategory-header"]/div[1]/text()').extract()
                c_name = name + '-' + ' '.join(text_list).strip()

                title = ['brand', 'Series', 'Series-2', 'PartNo', 'DataSheet', 'DetailLink', 'Description']
                for a in div_table[k - 1].xpath('./div/table//a[@class="column-header"]'):
                    title.append(' '.join(a.xpath('./text()').extract()))

                self.fp[c_name] = codecs.open('exar/main/' + re.sub(r'[/:|?*"\\<>]', '&', c_name) + '.csv', 'w+', 'utf_8_sig')
                self.fp[c_name].write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")
                i = 1
                for a in div_table[k - 1].xpath('./div/table//a[@class="product-white"]'):
                    type_num = a.xpath('./text()').extract()[0]
                    desc = a.xpath('./@title').extract()[0]
                    url  = a.xpath('./@href').extract()[0]
                    tr = div_table[k - 1].xpath('./div/table//div[@class="body"]//tr[%s]' % i)
                    params = [desc]
                    i += 1
                    for td in tr.xpath('./td'):
                        val = td.xpath('./div/text()').extract()
                        if val:
                            params.append(' '.join(val))
                        else:
                            params.append('-')
                    yield scrapy.Request(response.urljoin(url), callback=self.tertius_parse, meta={'name' : c_name, 'type_num' : type_num, 'params' : params, 'series' : response.meta['series']})
                    #break
                #break
            #break

    def tertius_parse(self, response):
        #title = response.xpath('//td[@class="option-header"]/text()').extract()
        csv_str = ''
        sheet_str = ''
        type_num = response.meta['type_num']
        for tr in response.xpath('//div[@id="content-left"]/div[last()-1]//tr[@class]'):
            text = tr.xpath('./td[1]/text()').extract()
            if text:
                part_num = text[0]
                sheet_url = response.xpath('//a[contains(@href, "datasheet")]/@href').extract()
                sheet_url = sheet_url[0] if sheet_url else '-'

                csv_data = ['exar', response.meta['name'], type_num, part_num, response.urljoin(sheet_url), response.url] + response.meta['params']
                tpl = ['"%s"'] * len(csv_data)
                csv_str += ((','.join(tpl) % tuple(csv_data)) + "\n")
                series = response.meta['series']

                if self.doc[series].has_key(type_num):
                    for val in self.doc[series][type_num]:
                        sheet_data = ['exar', response.meta['name'], type_num, part_num, val['type'], val['sheet_url']]
                        tpl = ['"%s"'] * len(sheet_data)
                        sheet_str += ((','.join(tpl) % tuple(sheet_data)) + "\n")
        self.fp[response.meta['name']].write(csv_str)
        self.sheet.write(sheet_str)

    def closed(spider, reason):
        spider.sheet.close()
        for val in spider.fp:
            spider.fp[val].close()