# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import DocsDownloadItem
# import libxml2
# import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SheetSpider(scrapy.Spider):
    name = "FMSH_Sheet"
    start_urls = (
        "http://www.fmsh.com/ea78de2e-2f5a-e700-2221-7101cff37d8d/",
    )

    def __init__(self):
        self.cnt = 0
        self.relation = open('FMSH_EEPROM.csv', 'wb+')
        title = '芯片型号, Datasheet, 容量,接口,频率,电压范围,封装形式,状态 \n'
        self.relation.write(title.encode('gbk'))
        self.field_enum = {}

    def parse(self, response):
        name_url = response.xpath('//tr[@class="xunhuan"]/td[1]/a/text() ').extract()
        sheet_url = response.xpath('//tr[@class="xunhuan"]/td[1]/a/@href ').extract()
        cap_url = response.xpath('//tr[@class="xunhuan"]/td[3]/text() ').extract()
        port_url = response.xpath('//tr[@class="xunhuan"]/td[4]/text() ').extract()
        freq_url = response.xpath('//tr[@class="xunhuan"]/td[5]/text() ').extract()
        vrange_url = response.xpath('//tr[@class="xunhuan"]/td[6]/text() ').extract()
        pack_url = response.xpath('//tr[@class="xunhuan"]/td[7]/text() ').extract()
        state_url = response.xpath('//tr[@class="xunhuan"]/td[8]/text() ').extract()

        maxCnt=len(name_url)
        print  len(name_url)
        print sheet_url
        for nCnt in range(0,maxCnt):
            print '==========',name_url[nCnt],'=========='
            self.relation.write(name_url[nCnt].replace(',','/'))
            self.relation.write(",")
            self.relation.write("http://www.fmsh.com" + sheet_url[nCnt])
            self.relation.write(",")
            self.relation.write(cap_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write(",")
            self.relation.write(port_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write(",")
            self.relation.write(freq_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write(",")
            self.relation.write(vrange_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write(",")
            self.relation.write(pack_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write(",")
            self.relation.write(state_url[nCnt].replace(',','/').strip('\n'))
            self.relation.write("\n" )

def closed(spider, reason):
        spider.relation.close()
