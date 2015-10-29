# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, os
import scrapy
from scrapy.pipelines import files
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
from scrapy.utils.misc import md5sum
from Docs_download.items import FilesItem

class DocsDownloadPipeline(object):
    def open_spider(self, spider):
        self.json = []

    def process_item(self, item, spider):
        self.json.append(dict(item))

    def close_spider(self, spider):
        print self.json
        fp = open('result.json', 'w+')
        fp.write(json.dumps(self.json))
        fp.close()

class  FilesPipeline(files.FilesPipeline):
    """FilesPipeline"""
    def open_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)
        self.json = {}
        self.json['filename'] = {}
        self.json['file_urls'] = []

    def close_spider(self, spider):
        print self.json
        fp = open('retry.json', 'w+')
        fp.write(json.dumps(self.json))
        fp.close()

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, cookies={
                '.ASPXANONYMOUS' : 'tEosW6o30QEkAAAANmQ5Yjg4MGEtY2Y5Ny00ZTFjLTgyYTktOGEyNGNkNDVlNTQ10',
                'ASP.NET_SessionId' : 's5fydptdnlo45utbk2zgz0mg',
                'authentication' : 'DNN',
                'dnn_IsMobile' : 'False',
                '.DOTNETNUKE' : '240F519DB2458029FC44C84BB5161BA1BF19C48F447DBB4D841FF20A333150E8C73BECC70FF8F87E475FFC89C3A99F8F61D841406471434A34DAC9236FCE9D04C6F1A9A560092614074BB488F9BC32B9BC503A23C9F5BFB64D68C8A92BF733655969B827354220AF63CAB552C8C27A83AC9DA775EA99CBB077E5CEAEE98447A53C011506',
                '_ga' : 'GA1.2.603964860.1444233118',
                '_gat' : '1',
                'language' : 'en-US'
                }, meta={'filename' : item['filename'][file_url]})

    def file_downloaded(self, response, request, info):
        path = 'full/' + request.meta['filename'] + '.pdf'
        buf = BytesIO(response.body)
        self.store.persist_file(path, buf, info)
        checksum = md5sum(buf)
        size = os.path.getsize(path)
        if size < 100:
            self.json['filename'][response.url] = request.meta['filename']
            self.json['file_urls'].append(response.url)

        return checksum

    def item_completed(self, results, item, info):
        file_paths = {}
        for ok, x in results:
            if ok:
                file_paths[x['url']] = x['path']

        if not file_paths:
            print "Item contains no files"
        item['file_paths'] = file_paths
        return item