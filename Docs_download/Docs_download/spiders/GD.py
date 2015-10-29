# -*- coding: utf-8 -*-
import scrapy


class GdSpider(scrapy.Spider):
    name = "gd"
    allowed_domains = ["gigadevice.com"]
    start_urls = (
        'http://www.gigadevice.com/',
    )

    def parse(self, response):
        test = response.xpath('//div[@class="product_m"]').extract()
        crawl_list = {
            'NOR Flash-SPI NOR Flash-3.0 Volt' : 'http://www.gigadevice.com/product-series/5.html?locale=zh_CN',
            'NOR Flash-SPI NOR Flash-2.5 Volt' : 'http://www.gigadevice.com/product-series/12.html?locale=zh_CN',
            'NOR Flash-SPI NOR Flash-1.8 Volt' : 'http://www.gigadevice.com/product-series/6.html?locale=zh_CN',
            'SPI NAND Flash-GD5F' : 'http://www.gigadevice.com/product-series/7.html?locale=zh_CN'
        }
        crawl_api_list = {

        }
        print test
