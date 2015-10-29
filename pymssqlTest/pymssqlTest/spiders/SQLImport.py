# -*- coding: utf-8 -*-
import os
import  csv
import pymssql
import codecs, sys
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
    if (infoMain =="elmos"  or infoMain == "exar"   or infoMain == "fmsh"  or infoMain == "fsl"  or infoMain == "mps"  or infoMain == "mxic" ):
        listmain = info + infoMain + '/main/'
        listfile = os.listdir(listmain.decode('utf8'))
        print infoMain
        print listfile
        # print len(listfile)

        for content in listfile:
            csvfile = open(listmain + content, 'r+')
            reader = csv.reader(csvfile)
            tbName ="tb_" + infoMain.upper() + "_" + content \
                .replace('-','_').replace(' ','_').replace(',','').replace('、','').replace('&','_').replace('.csv','').replace('≤','_') \
                .replace('transistors_Low_voltage_low_VCEsat_(BISS)_','').replace('transistors_Low_VCEsat_(BISS)_','').replace('High_Output_Amplifiers_','')

            n = 0
            lenTitle = 0
            data_list=[]
            for line in reader:
                print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                if n == 1:
                    tpl = ['%s varchar(max)'] * len(line)
                    lenTitle = len(line)
                    strTemp = ''.join(line)
                    # print strTemp
                    tm = 0
                    for cell in line:
                        if strTemp.count(cell) > 1:
                            tm = tm + 1
                            if tm > 1:
                                cell = cell + str( tm +1 )    # 去重
                        tpl[m] = '"' + cell  + '"' +  '  varchar(max)'
                        codeTemp = codeTemp + tpl[m] + ','
                        m = m + 1
                    codeTemp = codeTemp.replace('\xef\xbb\xbf','').replace('""','"')
                    # print codeTemp
                    sql_code1 = "if (select object_id('%s')) is not null "\
                                'drop table "%s"' \
                                'CREATE TABLE "%s" ' \
                                '(%s)' % (tbName, tbName, tbName, codeTemp)
                    # print sql_code1
                    # 执行SQL代码
                    cur.execute(sql_code1)
                else :
                    tpl = ['"%s"'] * len(line)
                    for cell in line:
                        if m < len(line) - 1 and m < lenTitle - 1:
                            tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                            codeTemp =  codeTemp + tpl[m] + ','
                            m = m + 1
                        elif m == lenTitle - 1:
                            tpl[m] ="'" + cell.replace('\n','')  + "'"
                            codeTemp =  codeTemp + tpl[m]
                            m = m + 1
                    # 在新表中添加内容
                    sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                    # print sql_code2
                    # 执行SQL代码
                    cur.execute(sql_code2)
            conn.commit()
    if (infoMain =="issi"):
        listmain = info + infoMain + '/main/'
        listfile = os.listdir(listmain.decode('utf8'))
        print infoMain
        print listfile
        # print len(listfile)

        for content in listfile:
            csvfile = open(listmain + content, 'r+')
            reader = csv.reader(csvfile)
            tbName ="tb_" + infoMain.upper() + "_" + content\
                .replace('-','_').replace(' ','_').replace(',','').replace('、','').replace('&','_').replace('.csv','').replace('≤','_')\
                .replace('transistors_Low_voltage_low_VCEsat_(BISS)_','').replace('transistors_Low_VCEsat_(BISS)_','').replace('High_Output_Amplifiers_','')

            n = 0
            lenTitle = 0
            data_list=[]
            for line in reader:
                # print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                if n == 1:
                    tpl = ['%s varchar(max)'] * len(line)
                    lenTitle = len(line)
                    strTemp = ''.join(line)
                    # print strTemp
                    tm = 0
                    for cell in line:
                        if strTemp.count(cell) > 1:
                            tm = tm + 1
                            if tm > 1:
                                cell = cell + str( tm +1 )    # 去重
                        tpl[m] = '"' + cell  + '"' +  '  varchar(max)'
                        codeTemp = codeTemp + tpl[m] + ','
                        m = m + 1
                    codeTemp = codeTemp.replace('\xef\xbb\xbf','').replace('""','"')
                    # print codeTemp
                    sql_code1 = "if  exists (select * from sysobjects where name= '%s') "\
                                'drop table "%s" ' \
                                'create table "%s" ' \
                                '(%s)' % (tbName, tbName, tbName, codeTemp)
                    # 执行SQL代码
                    try:
                        cur.execute(sql_code1)
                    except:
                        cur.execute(sql_code1.encode('utf8'))

                else :
                    if len(line) >= lenTitle:
                        for cell in line:
                            if m < len(line) - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''").replace(",","，")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                            elif m == len(line) - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m]
                                m = m + 1
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        # print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
                    else :
                        # print lenTitle
                        # print len(line)
                        for cell in line:
                            if m <= len(line)-1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                        codeTemp = codeTemp + \
                                   "''" + ",''" * (lenTitle - len(line) -1)
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
            conn.commit()
    if (infoMain =="on"):
        listmain = info + infoMain + '/main/'
        listfile = os.listdir(listmain.decode('utf8'))
        print infoMain
        print listfile
        # print len(listfile)

        for content in listfile:
            csvfile = open(listmain + content, 'r+')
            reader = csv.reader(csvfile)
            tbName ="tb_" + infoMain.upper() + "_" + content\
                .replace('-','_').replace(' ','_').replace(',','').replace('、','').replace('&','_').replace('.csv','').replace('≤','_')\
                .replace('transistors_Low_voltage_low_VCEsat_(BISS)_','').replace('transistors_Low_VCEsat_(BISS)_','').replace('High_Output_Amplifiers_','')

            n = 0
            lenTitle = 0
            data_list=[]
            for line in reader:
                # print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                if n == 1:
                    tpl = ['%s varchar(max)'] * len(line)
                    lenTitle = len(line)
                    strTemp = ''.join(line)
                    # print strTemp
                    tm = 0
                    for cell in line:
                        if strTemp.count(cell) > 1:
                            tm = tm + 1
                            if tm > 1:
                                cell = cell + str( tm +1 )    # 去重
                        tpl[m] = '"' + cell  + '"' +  '  varchar(max)'
                        codeTemp = codeTemp + tpl[m] + ','
                        m = m + 1
                    codeTemp = codeTemp.replace('\xef\xbb\xbf','').replace('""','"')
                    # print codeTemp
                    sql_code1 = "if  exists (select * from sysobjects where name= '%s') "\
                                'drop table "%s" ' \
                                'create table "%s" ' \
                                '(%s)' % (tbName, tbName, tbName, codeTemp)
                    # 执行SQL代码
                    try:
                        cur.execute(sql_code1)
                    except:
                        cur.execute(sql_code1.encode('utf8'))

                else :
                    if len(line) >= lenTitle:
                        for cell in line:
                            if m < lenTitle - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''").replace(",","，")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                            elif m == lenTitle - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m]
                                m = m + 1
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        # print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
                    else :
                        # print lenTitle
                        # print len(line)
                        for cell in line:
                            if m <= len(line)-1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                        codeTemp = codeTemp + \
                                   "''" + ",''" * (lenTitle - len(line) -1)
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        # print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
            conn.commit()
    if (infoMain =="nxp"):
        listmain = info + infoMain + '/main/'
        listfile = os.listdir(listmain.decode('utf8'))
        print infoMain
        print listfile
        # print len(listfile)

        for content in listfile:
            csvfile = open(listmain + content, 'r+')
            reader = csv.reader(csvfile)
            tbName ="tb_" + infoMain.upper() + "_" + content\
                .replace('-','_').replace(' ','_').replace(',','').replace('、','').replace('&','_').replace('.csv','').replace('≤','_')\
                .replace('transistors_Low_voltage_low_VCEsat_(BISS)_','').replace('transistors_Low_VCEsat_(BISS)_','').replace('High_Output_Amplifiers_','')\
                .replace('General_purpose_bipolar_transistors___','').replace('Low_voltage_low_VCEsat_(BISS)_transistors___','').replace('Low_VCEsat_(BISS)_transistors_double___','')\
                .replace('，_filtering_and_signal_conditioning___','').replace('High_Linearity_Amplifiers','HLA').replace('High_Output_Amplifiers','HOA')
            # print tbName
            n = 0
            lenTitle = 0
            data_list=[]
            for line in reader:
                # print line
                codeTemp = ''
                m = 0
                n = n + 1
                temp_new= []
                if n == 1:
                    tpl = ['%s varchar(max)'] * len(line)
                    lenTitle = len(line)
                    strTemp = ''.join(line)
                    # print strTemp
                    tm = 0
                    for cell in line:
                        if strTemp.count(cell) > 1:
                            tm = tm + 1
                            if tm > 1:
                                cell = cell + str( tm +1 )    # 去重
                        tpl[m] = '"' + cell  + '"' +  '  varchar(max)'
                        codeTemp = codeTemp + tpl[m] + ','
                        m = m + 1
                    codeTemp = codeTemp.replace('\xef\xbb\xbf','').replace('""','"')
                    # print codeTemp
                    sql_code1 = "if  exists (select * from sysobjects where name= '%s') "\
                                'drop table "%s" ' \
                                'create table "%s" ' \
                                '(%s)' % (tbName, tbName, tbName, codeTemp)
                    # 执行SQL代码
                    try:
                        cur.execute(sql_code1)
                    except:
                        # print codeTemp
                        sql_code1 = "if  exists (select * from sysobjects where name= '%s') "\
                                    'drop table "%s" ' \
                                    'create table "%s" ' \
                                     '("brand"  varchar(max),"Series"  varchar(max),"PartNo"  varchar(max),"DetailLink"  varchar(max),"dataSheet"  varchar(max),' \
                                    '"Package version"  varchar(max),"Package name"  varchar(max),"frange [min]"  varchar(max),"frange [max]"  varchar(max),"@VCC"  varchar(max),' \
                                    '"ICC [typ]"  varchar(max),"ICC [max]"  varchar(max),"Gp"  varchar(max),"PL(1dB)3"  varchar(max),"IP3O1"  varchar(max),"NF4"  varchar(max),' \
                                    '"@f5"  varchar(max),"Gp6"  varchar(max),"PL(1dB)7"  varchar(max),"IP3O2"  varchar(max),"NF8"  varchar(max),"@f9"  varchar(max),)' % (tbName, tbName, tbName)
                        cur.execute(sql_code1)
                        # cur.execute(sql_code1.encode('utf8'))

                else :
                    if len(line) >= lenTitle:
                        for cell in line:
                            if m < lenTitle - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''").replace(",","，")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                            elif m == lenTitle - 1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m]
                                m = m + 1
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        # print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
                    else :
                        print lenTitle
                        print len(line)
                        for cell in line:
                            if m <= len(line)-1:
                                tpl[m] ="'" + cell.replace('\n','').replace("'","''")  + "'"
                                codeTemp =  codeTemp + tpl[m] + ','
                                m = m + 1
                        codeTemp = codeTemp + \
                                   "''" + ",''" * (lenTitle - len(line) -1)
                        # 在新表中添加内容
                        sql_code2 = 'INSERT INTO "%s" VALUES (%s)' % (tbName, codeTemp)
                        # print codeTemp
                        # 执行SQL代码
                        cur.execute(sql_code2)
            conn.commit()

conn.close()