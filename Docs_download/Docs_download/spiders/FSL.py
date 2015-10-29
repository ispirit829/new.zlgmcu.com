# -*- coding: utf-8 -*-
import scrapy
import urlparse, json, re, codecs, os


class FslSpider(scrapy.Spider):
    name = "fsl"
    allowed_domains = ["freescale.com"]
    start_urls = (
        'http://www.freescale.com/zh-Hans/webapp/parametricSelector.sp',
    )

    def __init__(self):
        self.sheet = codecs.open(u'fsl/手册/sheet.csv', 'w+', 'utf_8_sig')
        title = 'brand,Series,Series-2,PartNo,FileType,Title,Url \n'
        self.sheet.write(title)
        self.fp = {}
        self.cnt = 0

    def parse(self, response):
        url = 'http://www.freescale.com/webapp/search/loadJSON.sp?c=%s&lang_cd=zh-Hans'
        for ul in response.xpath('//div[@id="prodMenu"]/div/ul'):
            for li in ul.xpath('./li'):
                name = li.xpath('./span/span/text()').extract()
                if len(name) > 1:
                    #name = '®'.join(name)
                    name = ' '.join(name)
                else:
                    name = name[0]
                name = name.strip()
                for li_v in li.xpath('./ul/li'):
                    c_name = name + '---' + li_v.xpath('./span/a/text()').extract()[0].strip()
                    src_url = li_v.xpath('./span/a/@href').extract()[0]
                    result = urlparse.urlparse(src_url)
                    params = urlparse.parse_qs(result.fragment, True)
                    yield scrapy.Request(url % params['c'][0], callback=self.secondary_parse, meta = {'name' : c_name, 'num' : params['c'][0]}, dont_filter=True)
                    #break
                #break
            #break

    def secondary_parse(self, response):
        data = json.loads(response.body)
        detail_url = 'http://www.freescale.com/webapp/search/loadJSON.sp?load=taxoPara&aType=OP&c=%s&lang_cd=zh-Hans&p=%s'
        title = []
        key = []
        tpl = []

        for val in data['paraheader']:
            title.append(val['name'])
            key.append(val['shortName'])
            tpl.append('"%(' + val['shortName'] + ')s"')
        title[0:0] = ['brand', 'Series', 'Series-2', 'PartNo', 'DetailLink', 'Document', 'Description']

        self.fp[response.meta['name']] = codecs.open('fsl/main/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['name']) + '.csv', 'w+', 'utf_8_sig')
        self.fp[response.meta['name']].write(','.join(['"%s"'] * len(title)) % tuple(title) + "\n")

        for pro in data['prod']:
            doc_url = None
            if pro['ProdCode'].has_key('documentationURL'):
                doc_url = response.urljoin(pro['ProdCode']['documentationURL'])
            yield scrapy.Request(detail_url % (response.meta['num'], pro['ProdCode']['Name']), callback=self.quartus_parse, dont_filter=True, meta={
                'name' : response.meta['name'],
                'type_number' : pro['ProdCode']['Name'],
                'tpl' : tpl,
                'key' : key,
                'doc_url' : doc_url
                })


    def tertius_parse(self, response):
        head = '"FSL",' + ','.join(['"%s"'] * 2) % (response.meta['name'], response.meta['type_number'])
        ProdCode = response.meta['ProdCode']
        sheet = codecs.open(u'fsl/手册/tmp/' + re.sub(r'[/:|?*"\\<>]', '&', response.meta['type_number']) + '.csv', 'w+', 'utf_8_sig')
        for section in response.xpath('//section'):
            csv_str = ''
            name = section.xpath('./h2/text()').extract()[0]
            urls = {}
            for tr in section.xpath('./table/tbody/tr'):
                url = tr.xpath('./td[1]/ul[1]/li/a/@href').extract()[0]
                title = tr.xpath('./td[1]/ul[1]/li/a/h3/text()').extract()[0].strip().replace('\n','').replace('"','”').replace(',','，')
                urls[title] = url

            tpl = ['"%s"'] * 4
            for val in ProdCode:
                if 'MK21DN512AVLK5' == val.strip():
                    print val
                cnt = 0
                #csv_str = ''
                for title, url in urls.items():
                    csv_str += (head + ',' + ','.join(tpl) % (val, name, title, url) + "\n")
                    cnt += 1
                    if cnt > 20:
                        sheet.write(csv_str)
                        csv_str = ''
                        cnt = 0
            if csv_str:
                sheet.write(csv_str)
        sheet.close()

    def quartus_parse(self, response):
        data = json.loads(response.body)
        key = response.meta['key']
        tpl = response.meta['tpl']
        tpl_pre = ['"%s"'] * 7
        detail_url = 'http://www.freescale.com/webapp/search.partparamdetail.framework?PART_NUMBER=%s&buyNow=true&fromSearch=true'
        csv_str = ''
        pattern = r'href="(.+?)"'
        regular = re.compile(pattern, re.DOTALL)
        ProdCode = []
        ProdName = ''
        for pro in data['OPNs']:
            if pro.has_key('p775'):
                match = regular.findall(pro['p775'])
                match = map(response.urljoin, match)
                pro['p775'] = '|'.join(match)
            for val in key:
                if not pro.has_key(val) or type(pro[val]) == dict:
                    pro[val] = '-'

            head = [
                'FSL',
                response.meta['name'],
                pro['ProdName'],
                pro['ProdCode'],
                detail_url % pro['ProdName'],
                response.urljoin(pro.get('documentationURL', '-')),
                pro['Desc']
                ]
            csv_str += ((','.join(tpl_pre) % tuple(head)) + ',' + (','.join(tpl) % pro) + "\n")
            ProdCode.append(pro['ProdCode'])
            ProdName = pro['ProdName']
        self.fp[response.meta['name']].write(csv_str)
        self.fp[response.meta['name']].flush()
        if response.meta['doc_url'] and not os.path.exists(u'fsl/手册/tmp/' + re.sub(r'[/:|?*"\\<>]', '&', ProdName) + '.csv'):
            yield scrapy.Request(response.meta['doc_url'], callback=self.tertius_parse, meta={'name' : response.meta['name'], 'type_number' : ProdName, 'ProdCode' : ProdCode}, dont_filter=True)

    def closed(spider, reason):
        spider.sheet.close()
        for val in spider.fp:
            spider.fp[val].close()
