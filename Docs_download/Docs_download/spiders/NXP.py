# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import CsvDataItem
import json, re, copy, codecs


class NxpSpider(scrapy.Spider):
    name = "nxp"
    allowed_domains = ["nxp.com"]
    start_urls = (
        'http://www.nxp.com/products/',
    )

    def __init__(self):
        self.fp = codecs.open(u'nxp/手册/sheet.csv', 'wb+', 'utf_8_sig')
        title = 'brand,Series,PartNo,FileType,Title,Url \n'
        self.fp.write(title)
        # self.fp = {}

    def parse(self, response):
        for h3 in response.xpath('//div[@class="article-content"]/h3/a'):
            url = h3.xpath('./@href').extract()[0]
            name = h3.xpath('./text()').extract()[0]
            yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta = {'name' : name})
            # break

    def secondary_parse(self, response):
        ul_list = []
        ul_list.append({
            'name' : response.meta['name'],
            'ul' : response.xpath('//div[@id="module_productTreeExpanded"]/div/ul')
            })
        while len(ul_list) > 0:
            ul_dic = ul_list.pop()
            for li in ul_dic['ul'].xpath('./li'):
                series_name = li.xpath('./a[@class="nxp-white"]/text()').extract()
                if series_name:
                    name = ul_dic['name'].replace(',','，') + '---' + series_name[0].replace(',','，').strip()
                    ul = li.xpath('./ul')
                    if ul:
                        ul_list.append({
                            'name' : name,
                            'ul' : ul
                            })
                    else:
                        url = li.xpath('./a[@class="nxp-white"]/@href').extract()[0]
                        id = li.xpath('./@id').extract()[0]
                        product_id = id.split('-')[1]
                        yield scrapy.Request(response.urljoin(url), callback=self.tertius_parse, meta = {'name' : name, 'product_id' : product_id})
                    # break

    def tertius_parse(self, response):
        product_info = {}
        table = response.xpath('//div[@id="section_products"]/div[@class="article-content"]/table/tbody')
        if table:
            for tr in table.xpath('.//tr[@class="odd"] | .//tr[@class="even"]'):
                type_number = tr.xpath('./td[1]/a/text()').extract()[0]
                detail_url = tr.xpath('./td[1]/a/@href').extract()[0]
                name = re.sub(r'\(\s*[0-9]+\s*\)', '', response.meta['name']).strip()

                yield scrapy.Request(response.urljoin(detail_url), callback=self.fifth, meta={'name' : name, 'type_number' : type_number})

                sheet_url = tr.xpath('./td[4]/a[@title="Download datasheet"]/@href').extract()
                if sheet_url:
                    sheet_url = response.urljoin(sheet_url[0])
                else:
                    sheet_url = 'No full datasheet available'

                product_info[type_number] = [
                    'nxp',
                    name,
                    type_number,
                    response.urljoin(detail_url),
                    sheet_url
                ]

            data_url = 'http://www.nxp.com/parametrics/psdata/?p=1&s=0&c=&rpp=&fs=0&sc=&so=&es=&type=initial&i=%s'
            yield scrapy.Request(data_url % response.meta['product_id'], callback=self.quartus_parse, meta={'product_info' : product_info, 'name' : name})

    def quartus_parse(self, response):
        data = json.loads(response.body)
        filters = data['filters']
        results = data['results']
        title = []
        for t in filters:
            title.append(re.sub(r'</?sub>', '', t['f']).strip())
        title[0:1] = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet']

        i = 0
        csv_data = []
        for result in results:
            n = 0
            for val in result['rs']:
                if val.has_key('rs'):
                    for v in val['rs']:
                        if 0 == i:
                            csv_data.append(copy.deepcopy(response.meta['product_info'][v['l']]))
                        else:
                            csv_data[n].append(v['l'])
                        n += 1
                else:
                    if 0 == i:
                        csv_data.append(copy.deepcopy(response.meta['product_info'][val['l']]))
                    else:
                        csv_data[n].append(val['l'])
                    n += 1

            i += 1

        #print len(csv_data)
        csv_str = ','.join(['"%s"'] * len(title)) + "\n"

        fp = codecs.open('nxp/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
        n = 1
        fp.write(csv_str % tuple(title))
        for val in csv_data:
            try:
                fp.write(csv_str % tuple(val))
            except:
                print val
            if n > 20:
                fp.flush()

        fp.close()

    def fifth(self, response):
        table = response.xpath('//div[@id="section_linkedDocuments"]/div[@class="article-content"]/table/tbody')
        tpl = ['"%s" '] * 5
        csv_str = ''
        if table:
            for tr in table.xpath('.//tr'):
                sheet_url = tr.xpath('./td[1]/a/@href').extract()
                # Description = tr.xpath('./td[2]/span/text()').extract()[0]
                # print Description
                if sheet_url:
                    sheet_url = sheet_url[0]
                else:
                    sheet_url = tr.xpath('./td[1]/a/@class').extract()[0]
                    pattern = r"docurl:'(/.+?\.(?:pdf|zip))'"
                    regular = re.compile(pattern, re.DOTALL)
                    match = regular.findall(sheet_url)
                    print match
                    sheet_url = match[0]
                titleName = tr.xpath('./td[2]/span/text()').extract()[0].strip().replace('\n','').replace('"','”')
                type = tr.xpath('./td[3]/text()').extract()[0]
                # print titleName
                csv_str +="NXP" + ',' + (','.join(tpl) % (response.meta['name'], response.meta['type_number'], type, titleName, response.urljoin(sheet_url)) + "\n")

            self.fp.write(csv_str)
            #self.fp.flush()

    def closed(spider, reason):
        spider.fp.close()