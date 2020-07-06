#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
该和序是为了解决汽车新零售中，对于销售环节的语音信息进行分析和数据提取，语音数据信息首先经过格式整理后，通过BIO的标识后，
进行训练然后再能过BERT机器学习后，生成相应的信息提取模型，进行数据的分析；
所以对于原始数据的BIO标识工作尤为重要，本程序就是为了自动的生成BIO格式的内容；
在mysql数据库中有entity数据表，保存的是实体内容的数据，对于汽车的：品牌、型号、配件、动力等内容进行了标识；
别外还需要提取对话过程中的电话号码，以及金额等，对于金额需要提取三个维度，一个是十万以上的（与车价相关），一个是带，号的十万以上的；还有就是十万以下的数字组成的内容；
'''
import re
import configparser
import os
import pymysql
import sys
import getopt

kwlist = {}

#把传入的字符串进行匹配，根据entity字典中的关键字做标记；
def ex_keyword(str):
    
    if not kwlist:
        get_entity_kw()

    for key in kwlist:
        if not key:
            continue
        #print(key)
        str = str.replace(key, "["+kwlist[key]+"]")
    
    #print(str)
    return str

#生成BIO格式的文件 1、从txt文件中按行读取，然后进行分析和替换后生成swp文件，该步骤对于标识词进行提取；2对于swp文件进行处理，主要是生成BIO格式；
def mk_bio(txtfile):
    
    infile = txtfile
    swpfile = infile+"_swp"
    bfile = infile+"_bio.txt"

    inf = None
    sf = None
    bf = None

    try:
        inf = open(infile,'r')
        sf = open(swpfile, 'w')
    except:
        print('文件打开错误')
        exit(2)

    for line in inf.readlines(): #依次读取每行
        if not line:
            continue
        line = line.strip() #去掉每行头尾空白
        line = ex_keyword(line)  #处理关键字的内容
        line = line.replace("[", "\n[")
        line = line.replace("]", "]\n")
        #line = line.replace("\n\n", "\n")   #增加此行是为了防止有多个空行的情况，会导致句子的关系混乱  
        sf.write(line)    #因为BIO的需求，每行中间有一个换行
        sf.write("\n\n") 
    
    inf.close()
    sf.close() 
    #####在此把相关的内容标记完成，下面需要对于文档进行BIO格式的处理
    try:
        sf = open(swpfile, 'r')
        bf = open(bfile, 'w')
    except:
        print('文件打开错误')
        exit(2)
        
    lines = sf.readlines()
    for line in lines:
        line = line.replace('\r','').replace('\n','').replace('\t','')
        if line == "":
            bf.write("\n")
            continue
        mlist = list(line)
        if mlist[0] == '[':
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace(",", "\n")+"\n"
            bf.write(line)
        else:
            if " " in mlist:
                mlist.remove(" ")
            line1 = " O\n".join(mlist)+" O\n"
            bf.write(line1)
    sf.close()
    bf.close()

def get_entity_kw():
    
    cur_path = os.path.dirname(os.path.realpath(__file__))
    #获取config.ini的路径
    config_path = os.path.join(cur_path,'db.ini')
    conf = configparser.ConfigParser()
    conf.read(config_path)
    dbhost = conf.get('mysql', 'dbhost')
    dbport = conf.get('mysql', 'dbport')
    dbname = conf.get('mysql', 'dbname')
    dbuser = conf.get('mysql', 'dbuser')
    dbpasswd = conf.get('mysql', 'dbpasswd')        

    dbconnect = pymysql.connect(host=dbhost, port=int(dbport),
        database=dbname, user=dbuser, password=dbpasswd)

    cursor = dbconnect.cursor()
 
    # SQL 查询语句
    sql = "SELECT ename, com FROM entity WHERE status = 1 order by ename desc"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

    for row in results:
        kwlist[row[0]] = row[1]     

if __name__ == "__main__":
    
    inputfile = ''
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'i:')
    except getopt.GetoptError:
        print("usage:python car_bio.py -i <input_file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i'):
            inputfile = arg
    if inputfile == '':
        print("usage:python car_bio.py -i <input_file>")
        sys.exit(2) 
    #ex_person("你好，先生！你好张先生，你好女士这是你的，这个王女士是我们的")
    mk_bio(inputfile)
