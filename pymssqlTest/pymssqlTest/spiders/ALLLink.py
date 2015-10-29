# -*- coding: utf-8 -*-
import os
import  csv
import pymssql
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#使用SQL Server身份验证的话需要输入用户名和密码，host是服务器的ip地址，如果是本机可以用"."
# conn=pymssql.connect(host=".",user=".",password=".",database=".")
#如采用windows身份验证，可使用如下命令：  192.168.1.229
conn = pymssql.connect(host="10.169.138.121",database="zlgweb_tst",charset='utf8')
cur = conn.cursor()

info = 'C:/Users/Administrator/Desktop/test/'.encode('gbk')
listdir = os.listdir(info)
print listdir
for infoMain in listdir:
    if infoMain == 'fsl':
        # 创建表格
        tbName ="dt_FSL_sheet"
        sql_code1 = "if (select object_id('%s')) is not null "\
                    'drop table "%s"' \
                    'CREATE TABLE "%s" ' \
                    '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"Title"  varchar(max),"URL"  varchar(max))'% (tbName, tbName, tbName)
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 6:
                            if m == 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")
                                codeTemp =  codeTemp + tpl[m]
                            elif m == 2:
                                tpl[m] =cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + '---' + tpl[m] + ','
                            else:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 6:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'nxp':
        # 创建表格
        tbName ="dt_NXP_sheet"
        sql_code1 = "if (select object_id('dt_NXP_sheet')) is null CREATE TABLE " + tbName +\
                               '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"Title"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName,codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()

    if infoMain == 'mps':
        # 创建表格
        tbName ="dt_MPS_sheet"
        sql_code1 = "if (select object_id('dt_MPS_sheet')) is null CREATE TABLE " + tbName +\
                               '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"DetailLink"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/main/'
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'elmos':
        # 创建表格
        tbName ="dt_ELMOS_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'exar':
        # 创建表格
        tbName ="dt_EXAR_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartSeries"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'fmsh':
        # 创建表格
        tbName ="dt_FMSH_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'htc':
        # 创建表格
        tbName ="dt_HTC_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    try:
                        tpl = ['"%s"'] * len(line)
                        for cell in line:
                            if m < 4:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                            elif m == 4:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m]
                                m = m + 1
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        print sql_code2
                        # 执行SQL代码
                        cur.execute(sql_code2)
                    except:
                        pass
                    # break
        conn.commit()
    if infoMain == 'issi':
        # 创建表格
        tbName ="dt_ISSI_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 4:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'mxic':
        # 创建表格
        tbName ="dt_MXIC_sheet"
        sql_code1 = "if (select object_id('%s')) is null CREATE TABLE " % tbName + tbName +\
                       '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))'
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    if len(line) >= 5:
                        for cell in line:
                            if m < 4:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''").replace(",","，")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                            elif m ==  4:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m]
                                m = m + 1
                    else :
                        for cell in line:
                            if m <= len(line)-1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                        codeTemp = codeTemp  + "'" + '' + "'"
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
    if infoMain == 'on':
        # 创建表格
        tbName ="dt_ON_sheet"
        sql_code1 = "if (select object_id('%s')) is not null "\
                    'drop table "%s"' \
                    'CREATE TABLE "%s" ' \
                    '("brand"  varchar(max),"Series"  varchar(max),"PartSeries"  varchar(max),"PartNo"  varchar(max),"FileType"  varchar(max),"URL"  varchar(max))' % (tbName, tbName, tbName)
        print sql_code1
        cur.execute(sql_code1)
        # 插入数据
        listmain = info + infoMain + '/手册/'.encode('gbk')
        listfile = os.listdir(listmain)
        print infoMain

        for content in listfile:
            csvfile = file(listmain + content, 'rb+')
            reader = csv.reader(csvfile)

            n = 0
            lenTitle = 0
            data_list=[]

            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                sql_code1 = ""
                print sql_code1
                # 执行SQL代码
                if n > 1 :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == 5:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
                    # break
        conn.commit()
conn.close()
