# -*- coding: utf-8 -*-
import scrapy
from Docs_download.items import DocsDownloadItem
# import libxml2
# import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SheetSpider(scrapy.Spider):
    name = "NXP_Sheet"
    start_urls = (
        "http://www.nxp.com/products/",
    )

    def __init__(self):
        self.cnt = 0
        self.NXP = open('NXP.csv', 'wb+')
        title = 'brand,Series,DetailLink,PartNo,datasheet \n'
        self.NXP.write(title)
        self.field_enum = {}

    def parse(self, response):
        # test = response.xpath('//div[@class="noborder"]/div[@class="article-content"]/ul[@class="bullet-orange-list"]/li/a/text()').extract()
        # print test, len(test)

        # url = response.xpath('//div[@class="noborder"]/div[@class="article-content"]/ul[@class="bullet-orange-list"]/li/a/@href').extract()
        # print url, response.urljoin(url[0])
        # print  len(url)

        url_lst = response.xpath('//div[@class="noborder"]/div[@class="article-content"]/ul[@class="bullet-orange-list"]/li/a ')
        for url_row in url_lst:
            sn = url_row.xpath('./text()').extract()[0]
            url = url_row.xpath('./@href').extract()[0]
            yield scrapy.Request(response.urljoin(url), callback=self.secondary_parse, meta = {'sn' : sn, 'url' :url})

    def secondary_parse(self, response):
        code_seg = response.xpath('//tbody/tr')
        for ncode_seg in code_seg:
            DetailLink = ncode_seg.xpath('./td/a[not(@class)]/@href').extract()
            series_name = ncode_seg.xpath('./td/a[not(@class)]/text()').extract()
            series_url = ncode_seg.xpath('./td/a[@title="Download datasheet"]/@href | ./td/a[@title="Download short datasheet"]/@href').extract()

            DetailLink_partNum = ncode_seg.xpath('./td/table/tr/td/a[not(@class)]/@href').extract()
            partNum_name = ncode_seg.xpath('./td/table/tr/td/a[not(@class)]/text()').extract()
            partNum_url = ncode_seg.xpath('./td/table/tr/td/a[@title="Download datasheet"]/@href | ./td/table/tr/td/a[@title="Download datasheet"]/@href').extract()

            Item = DocsDownloadItem()
            Item['sn'] = response.meta['sn'].decode('utf8').encode('gbk')
            Item['pdf_url'] = map(response.urljoin, series_url)

            # self.NXP.write(series_url + "\n")
            maxSerCnt=len(series_name)
            maxSerUrl=len(series_url)
            maxPrtNumCnt=len(partNum_name)
            maxPrtNumUrl=len(partNum_url)
            
            # if Item['sn'] == 'Digital radio processors' or Item['sn'] == 'AM/FM radio & audio':
            if Item['sn'] != '':
                if maxSerCnt > 0:
                    print '==========', Item['sn'],'=========='
                    print  series_name
                    print  series_url
                    print  maxSerCnt
                    for nCnt in range(0,maxSerCnt):
                        self.NXP.write("\n" )
                        self.NXP.write('NXP')
                        self.NXP.write(",")
                        if Item['sn'] != '':
                            self.NXP.write(Item['sn'].replace(',','/').strip())
                        self.NXP.write(",")
                        if DetailLink[nCnt] != '':
                            self.NXP.write("http://www.nxp.com" + DetailLink[0])
                        self.NXP.write(",")
                        self.NXP.write(series_name[nCnt].replace(',','/').replace(' ','').replace(';','/').strip())
                        self.NXP.write(",")
                        if maxSerUrl > 0:
                            self.NXP.write("http://www.nxp.com" + series_url[nCnt])
                        self.NXP.write(",")
                if maxPrtNumCnt > 0:
                    print '==========', Item['sn'],'=========='
                    print  partNum_name
                    print  partNum_url
                    print  maxPrtNumCnt
                    for nCnt in range(0,maxPrtNumCnt):
                        self.NXP.write("\n" )
                        self.NXP.write('NXP')
                        self.NXP.write(",")
                        if Item['sn'] != '':
                            self.NXP.write(Item['sn'].replace(',','/').strip())
                        self.NXP.write(",")
                        if DetailLink_partNum[nCnt] != '':
                            self.NXP.write("http://www.nxp.com" + DetailLink_partNum[0])
                        self.NXP.write(",")
                        self.NXP.write(partNum_name[nCnt].replace(',','/').replace(' ','').replace(';','/').strip())
                        self.NXP.write(",")
                        if maxPrtNumUrl > 0:
                            self.NXP.write("http://www.nxp.com" + partNum_url[nCnt])
                        self.NXP.write(",")
                        # print '******************************************************************************'
                        # print series_name[nCnt]
                        # print '******************************************************************************'
                        # print "http://www.nxp.com"+series_url[nCnt]
                        # print '******************************************************************************'
                        # return Item


def closed(spider, reason):
        spider.NXP.close()