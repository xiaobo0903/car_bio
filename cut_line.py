#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
把空行的内容删除掉,因为在生成训练时会产生很多无标记的内容，为了节省训练时间去掉空行；
'''
import re
import configparser
import os
import pymysql
import sys
import getopt


#生成BIO格式的文件 1、从txt文件中按行读取，然后进行分析和替换后生成swp文件，该步骤对于标识词进行提取；2对于swp文件进行处理，主要是生成BIO格式；
def cut_line(txtfile):
    
    infile = txtfile
    bfile = infile+"_bio.txt"

    inf = None
    bf = None
    flag = 0
    kwlist = []

    try:
        inf = open(infile,'r')
        bf = open(bfile, 'w')
    except:
        print('文件打开错误')
        exit(2)

    pattern = re.compile("(B-|I-)")  #

    for line in inf.readlines(): #依次读取每行
        if not line:
            continue
        
        kwlist.append(line)
        m = pattern.findall(line)
        if m != []:
           flag = 1 
        if line == "\n":
           if flag == 1:   
              bf.write("".join(kwlist)) 
           flag = 0
           kwlist = []
    
    inf.close()
    bf.close()

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
        print("usage:python cut_line.py -i <input_file>")
        sys.exit(2) 
    #ex_person("你好，先生！你好张先生，你好女士这是你的，这个王女士是我们的")
    cut_line(inputfile)
