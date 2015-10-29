# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DocsDownloadItem(scrapy.Item):
    sn = scrapy.Field()
    sec_name = scrapy.Field()
    pdf_url = scrapy.Field()

class FilesItem(scrapy.Item):
    """docstring for  FilesItem"""
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()
    filename = scrapy.Field()

class CsvDataItem(scrapy.Item):
    title = scrapy.Field()
    data = scrapy.Field()