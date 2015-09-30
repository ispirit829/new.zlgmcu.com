# -*- coding: utf-8 -*-
import scrapy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Docs_download.items import DocsDownloadItem

class SheetSpider(scrapy.Spider):
    name = "ISSI_Sheet"
    start_urls = (
        "http://www.issi.com/US/index.shtml",
    )

    def __init__(self):
        self.cnt = 0
        self.ISSI = open('ISSI.csv', 'wb+')
        title = 'brand,Series,DetailLink,PartNo,datasheet,Den,Org,Vcc,Speed,PkgPins,V_Status,Models,Comment \n'
        self.ISSI.write(title)
        self.field_enum = {}

    def parse(self, response):
        # test = response.xpath('//div[@class="products-nav"]/ul/li[@class="sub-nav"]/ul/li/a/text()').extract()
        # print test, len(test)
        #
        # url = response.xpath('//div[@class="products-nav"]/ul/li[@class="sub-nav"]/ul/li/a/@href').extract()
        # print url, response.urljoin(url[0])
        # print  len(url)

        url_lst = response.xpath('//div[@class="products-nav"]/ul/li[@class="sub-nav"]/ul/li/a ')
        for url_row in url_lst:
            sn = url_row.xpath('./text()').extract()[0]
            url = url_row.xpath('./@href').extract()[0]
            yield scrapy.Request(response.urljoin(url),callback=self.secondary_parse, meta = {'sn' : sn, 'url' :url})

    def secondary_parse(self, response):
        sec_code = response.xpath('//div[@id="jumpTable"]/article')
        secName = sec_code.xpath('./h2/a/text()')
        # print secName

        for nSec in sec_code:
            pdf_url = nSec.xpath('./table/tr/td[@class="partNumber"]/a/@href').extract()
            pdf_name = nSec.xpath('./table/tr/td[@class="partNumber"]/a/text()').extract()
            DetailLink = response.meta['url']
            Den = nSec.xpath('./table/tr/td[1]/text()').extract()
            Org = nSec.xpath('./table/tr/td[2]/text()').extract()
            Vcc = nSec.xpath('./table/tr/td[4]/text()').extract()
            Speed = nSec.xpath('./table/tr/td[5]/text()').extract()
            PkgPins = nSec.xpath('./table/tr/td[6]/text()').extract()
            V_Status = nSec.xpath('./table/tr/td[7]/text()').extract()
            Models = nSec.xpath('./table/tr/td[8]/a/text()').extract()
            Comment = nSec.xpath('./table/tr/td[9]/a/text()').extract()

            Item = DocsDownloadItem()
            Item['sn'] = response.meta['sn']
            Item['pdf_url'] = map(response.urljoin, pdf_url)

            nCnt=len(pdf_url)
            print '==========', Item['sn'],'=========='
            print '==========', nCnt,'=========='
            for nCnt in range(0,nCnt):
                if Item['sn'] != "":
                    self.ISSI.write('ISSI')
                    self.ISSI.write(",")
                    self.ISSI.write(Item['sn'].replace(',','/').strip())
                    self.ISSI.write(",")
                    self.ISSI.write("http://www.issi.com" + DetailLink)
                    self.ISSI.write(",")
                    if pdf_name[nCnt] != '':
                        self.ISSI.write(pdf_name[nCnt].replace(',','/').strip())
                        self.ISSI.write(",")
                    if pdf_url[nCnt] != '':
                        self.ISSI.write("http://www.issi.com" + pdf_url[nCnt])
                        self.ISSI.write(",")
                    # if Den[nCnt] != '\xa0':
                    #     self.ISSI.write(Den[nCnt].replace(',','/').strip())
                    #     self.ISSI.write(",")
                    # else:
                    #     self.ISSI.write(Den[nCnt-1].replace(',','/').strip())
                    #     self.ISSI.write(",")
                    # self.ISSI.write(Org[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(Vcc[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(Speed[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(PkgPins[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(V_Status[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(Models[nCnt].replace(',','/').strip())
                    # self.ISSI.write(",")
                    # self.ISSI.write(Comment[nCnt].replace(',','/').strip())
                    self.ISSI.write("\n" )
        # return Item


def closed(spider, reason):
        spider.ISSI.close()
