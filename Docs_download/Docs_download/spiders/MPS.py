# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import FilesItem
import json, re
import time
import libxml2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SheetMpsSpider(scrapy.Spider):
    name = "mps"
    allowed_domains = ["monolithicpower.com"]
    start_urls = (
        'http://www.monolithicpower.com/',
    )

    def __init__(self):
        self.cnt = 0
        self.field_enum = {}
        doc = libxml2.parseFile('enum.xml')
        for val in doc.xpathEval('//Field'):
            shortname = val.xpathEval('@shortName')[0].content
            self.field_enum[shortname] = {}
            for item in val.xpathEval('Enum/Item'):
                label = item.xpathEval('Label/text()')[0].content
                value = item.xpathEval('Value/text()')[0].content
                self.field_enum[shortname][value] = label
        # print self.field_enum
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
                name = tmp['Name'].strip() + '---' + name

            yield scrapy.Request(_url_third, callback=self.third_parse, cookies={
                '.ASPXANONYMOUS' : 'tEosW6o30QEkAAAANmQ5Yjg4MGEtY2Y5Ny00ZTFjLTgyYTktOGEyNGNkNDVlNTQ10',
                'ASP.NET_SessionId' : 's5fydptdnlo45utbk2zgz0mg',
                'authentication' : 'DNN',
                'dnn_IsMobile' : 'False',
                '.DOTNETNUKE' : '240F519DB2458029FC44C84BB5161BA1BF19C48F447DBB4D841FF20A333150E8C73BECC70FF8F87E475FFC89C3A99F8F61D841406471434A34DAC9236FCE9D04C6F1A9A560092614074BB488F9BC32B9BC503A23C9F5BFB64D68C8A92BF733655969B827354220AF63CAB552C8C27A83AC9DA775EA99CBB077E5CEAEE98447A53C011506',
                '_ga' : 'GA1.2.603964860.1444233118',
                '_gat' : '1',
                'language' : 'en-US'
                }, meta={'name' : name, 'CategoryID' : val['CategoryID']})
        

    def secondary_parse(self, response):
        product = json.loads(response.body)
        if len(product['Data']) > 0:
            base_url = 'http://new.zlgmcu.com/mps_datasheet/'
            detail_url = 'http://www.monolithicpower.com/Products/Product-Detail?ProductID=%s'
            title = ['brand', 'Series', 'PartNo', 'DetailLink', 'dataSheet', '原厂链接']
            item = FilesItem()
            item['filename'] = {}
            item['file_urls'] = []
            sheet = open('mps/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name'].strip()) + '.csv', 'w+')
            sheet.write(','.join(title + response.meta['field_name']) + "\n")
            for val in product['Data']:
                url = response.urljoin(val['datasheet_url'])
                item['filename'][url] = val['partnumber']
                item['file_urls'].append(url)

                head = ','.join(['"mps"', '"' + response.meta['name'] + '"', '"' + val['partnumber'] + '"', '"' + (detail_url % val['productid']) + '"', '"' + base_url + val['partnumber'] + '.pdf"', '"' + url + '"'])

                #sheet
                lst_csv = ['"%s"'] * len(response.meta['field']);
                lst = []
                for field in response.meta['field']:
                    if self.field_enum.has_key(field) and self.field_enum[field].has_key(val[field]):
                        lst.append(self.field_enum[field][val[field]])
                    else:
                        lst.append(val[field] if val[field] else '')

                str_csv = head + ',' + ((','.join(lst_csv)) % tuple(lst))
                sheet.write(str_csv.decode('utf8') + "\n")


                self.cnt += 1

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
                    '.ASPXANONYMOUS' : 'tEosW6o30QEkAAAANmQ5Yjg4MGEtY2Y5Ny00ZTFjLTgyYTktOGEyNGNkNDVlNTQ10',
                    'ASP.NET_SessionId' : 's5fydptdnlo45utbk2zgz0mg',
                    'authentication' : 'DNN',
                    'dnn_IsMobile' : 'False',
                    '.DOTNETNUKE' : '240F519DB2458029FC44C84BB5161BA1BF19C48F447DBB4D841FF20A333150E8C73BECC70FF8F87E475FFC89C3A99F8F61D841406471434A34DAC9236FCE9D04C6F1A9A560092614074BB488F9BC32B9BC503A23C9F5BFB64D68C8A92BF733655969B827354220AF63CAB552C8C27A83AC9DA775EA99CBB077E5CEAEE98447A53C011506',
                    '_ga' : 'GA1.2.603964860.1444233118',
                    '_gat' : '1',
                    'language' : 'en-US'
                    }, meta={'name' : response.meta['name'], 'field' : field, 'field_name' : field_name})
        else:
            print "Not match!"