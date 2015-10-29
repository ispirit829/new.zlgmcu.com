# -*- coding: utf-8 -*-
import os
import codecs

wFile = codecs.open(u'fsl/手册/sheet.csv', 'a+', 'utf_8_sig', 'ignore')
for file in os.listdir(u'fsl/手册/tmp/') :
    #遇到非法字符时，不报错，直接读入后继续执行
    rFile = codecs.open(u'fsl/手册/tmp/' + file, 'r', 'utf_8_sig', 'ignore')
    #写入文件内容
    wFile.writelines(rFile.readlines())
    rFile.close()
wFile.close
