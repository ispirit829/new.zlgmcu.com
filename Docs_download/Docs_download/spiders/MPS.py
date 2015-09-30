# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import DocsDownloadItem
import json, re
import time
import libxml2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SheetMpsSpider(scrapy.Spider):
    name = "MPS_Sheet"
    allowed_domains = ["monolithicpower.com"]
    start_urls = (
        'http://www.monolithicpower.com/',
    )

    def __init__(self):
        self.cnt = 0
        self.relation = open('relation.csv', 'w+')
        title = '"型号", "地址", "系列", "原厂链接"\n'
        self.relation.write(title.encode('gbk'))
        self.field_enum = {}
        doc = libxml2.parseFile('enum.xml')
        for val in doc.xpathEval('//Field'):
            shortname = val.xpathEval('@shortName')[0].content
            self.field_enum[shortname] = {}
            for item in val.xpathEval('Enum/Item'):
                label = item.xpathEval('Label/text()')[0].content
                value = item.xpathEval('Value/text()')[0].content
                self.field_enum[shortname][value] = label
        print self.field_enum
        doc.freeDoc()


    def parse(self, response):
        fp = open('category.json', 'r+')
        category = json.load(fp)
        fp.close()
        index_category = {}
        for val in category['Data']:
            index_category[val['CategoryID']] = val

        url_third = 'http://www.monolithicpower.com/Desktopmodules/Product/Ajax.ashx?method=getColumns&categoryID=%s'
        for val in category['Data']:
            _url_third = url_third % val['CategoryID']
            name = val['Name'].strip()
            tmp = val
            while 0 != tmp['ParentID']:
                tmp = index_category[tmp['ParentID']]
                name = tmp['Name'].strip() + '-' + name

            yield scrapy.Request(_url_third, callback=self.third_parse, cookies={
                '.ASPXANONYMOUS' : '9bMi0aYq0QEkAAAAZDBjMzQ2Y2YtN2EwYS00ZGVjLWFmZmQtNTlkM2IzNmNlNDRm0',
                'ASP.NET_SessionId' : 'akutighgwey5ja1x0zakf4k5',
                'authentication' : 'DNN',
                'dnn_IsMobile' : 'False',
                '.DOTNETNUKE' : '09C50769BCC212917BB1C2012B064B8A58EF855249ACB4F1989E85CB6247251E3B5C613AC7E86E32F82A7BB064974B9CDFEDCAE7E170DBA635D453C266C0257A70E4665AC23204A400850709F327883F63E0B9C9EC2FCC9C18ADE8777CAB4365BBA5E86BA20327DA1A534EFB37A4DDD320D9752F4B2E44FD065D2C1641839D9F452F44D6',
                '_ga' : 'GA1.2.1508715189.1442802415',
                '_gat' : '1',
                'language' : 'en-US'
                }, meta={'name' : name, 'CategoryID' : val['CategoryID']})
        

    def secondary_parse(self, response):
        product = json.loads(response.body)
        if len(product['Data']) > 0:
            #print len(product['Data'])
            base_url = 'http://new.zlgmcu.com/mps_datasheet/'
            item = DocsDownloadItem()
            item['filename'] = {}
            item['file_urls'] = []
            sheet = open('sheet/' + re.sub(r'[\/\\><]', '_', response.meta['name'].strip()) + '.csv', 'w+')
            sheet.write(','.join(response.meta['field_name']) + "\n")
            for val in product['Data']:
                url = response.urljoin(val['datasheet_url'])
                item['filename'][url] = val['partnumber']
                item['file_urls'].append(url)

                #relation.csv
                self.relation.write(','.join(['"' + val['partnumber'] + '"', '"' + base_url + val['partnumber'] + '.pdf"', '"' + response.meta['name'] + '"', '"' + url + '"']) + "\n")

                #sheet
                lst_csv = ['"%s"'] * len(response.meta['field']);
                lst = []
                for field in response.meta['field']:
                    if self.field_enum.has_key(field) and self.field_enum[field].has_key(val[field]):
                        lst.append(self.field_enum[field][val[field]])
                    else:
                        lst.append(val[field] if val[field] else '')
                    #print response.meta['field']
                    #print response.meta['field_name']
                    #print val

                str_csv = (','.join(lst_csv)) % tuple(lst)
                sheet.write(str_csv.decode('utf8') + "\n")


                self.cnt += 1
                #print self.cnt
                if 0 == self.cnt % 20:
                    self.relation.flush()

            sheet.close()
            #return item

    def third_parse(self, response):
        body = response.body

        pattern = r'^define\(function\s*\(\)\s*\{return\s*\{\s*Data\s*:\s*(.+)\s*,\s*"Status"\s*:\s*0\s*,\s*"Message":null\s*\}\s*\}\s*\);\s*$'
        regular = re.compile(pattern, re.DOTALL)
        match = regular.findall(body)
        if match:
            match =re.sub(r'function\(value,item\)\s*\{.+?\}','1',match[0])
            data = eval(match.replace('null', 'None'))
            if data:
                field = []
                field_name = []
                for val in data:
                    if 'Parametrics' == val['group'] or 'partnumber' == val['shortname'] or 'status_enumdesc' == val['shortname']:
                        field.append(val['shortname'].decode('utf8'))
                        if 'status_enumdesc' == val['shortname']:
                            field_name.append('"Note For Status"')
                        else:
                            field_name.append('"' + val['name'] + '"')
                url = 'http://www.monolithicpower.com/Desktopmodules/Product/Ajax.ashx?method=getProducts&categoryID=%s&_=%d'
                _url = url % (response.meta['CategoryID'], (time.time() * 1000))
                yield scrapy.Request(_url, callback=self.secondary_parse, cookies={
                    '.ASPXANONYMOUS' : '9bMi0aYq0QEkAAAAZDBjMzQ2Y2YtN2EwYS00ZGVjLWFmZmQtNTlkM2IzNmNlNDRm0',
                    'ASP.NET_SessionId' : 'akutighgwey5ja1x0zakf4k5',
                    'authentication' : 'DNN',
                    'dnn_IsMobile' : 'False',
                    '.DOTNETNUKE' : '09C50769BCC212917BB1C2012B064B8A58EF855249ACB4F1989E85CB6247251E3B5C613AC7E86E32F82A7BB064974B9CDFEDCAE7E170DBA635D453C266C0257A70E4665AC23204A400850709F327883F63E0B9C9EC2FCC9C18ADE8777CAB4365BBA5E86BA20327DA1A534EFB37A4DDD320D9752F4B2E44FD065D2C1641839D9F452F44D6',
                    '_ga' : 'GA1.2.1508715189.1442802415',
                    '_gat' : '1',
                    'language' : 'en-US'
                    }, meta={'name' : response.meta['name'], 'field' : field, 'field_name' : field_name})
        else:
            print "Not match!"

        

    def closed(spider, reason):
        spider.relation.close()