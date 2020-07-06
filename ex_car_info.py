#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
该程序是为了进行姓氏、金额、和电话号码的提取的工作，因为这些内容的提取会比较固化；
'''
import re
import os
import sys

#些类是为了解决汽车类的标注内容而设定的，通过正则的方式提取姓氏、金额、电话等内容;
class ex_car_info:
    nkey = {}
    rkey = {}

    #提取姓氏
    def ex_person(self, str):
        pattern = re.compile("([\u4e00-\u9fa5]{0,1})(女士|先生)")  #    
        m = pattern.findall(str)
        stmp = ''
        for rs in m:
            if rs[0] not in ["", "好", "请", "个", "您", "个"]:      #为了去掉一些不合规的姓氏
                stmp = rs[0]
            stmp = stmp + rs[1]
            self.nkey[stmp] = "name"
            break   
        return

    #提取32万、43万以及多少期贷款这种格式的数据
    def ex_price1(self, str):
        pattern = re.compile("\\d{2,3}[万|期]")  # 
        m = pattern.findall(str)

        for rs in m:
            self.nkey[rs] = "price"
        return

    #提取10,234这种格式的数据
    def ex_price2(self, str):
        pattern = re.compile("\\d{2,4},\\d{3}")  # 
        m = pattern.findall(str)
        for rs in m:
            self.nkey[rs] = "price"
        return

    #提取纯数字如:1000,这种格式的金额
    def ex_price3(self, str):
        pattern = re.compile("\\d{3}\\d{1,2}")  # 
        m = pattern.findall(str)
        for rs in m:
            self.nkey[rs] = "price"
        return

    #提取手机号码,11位数字，为从1打头
    def ex_mobile(self, str):
        pattern = re.compile("1[34578]\\d{7,10}")  # 
        m = pattern.findall(str)
        for rs in m:
            self.nkey[rs] = "phone"
        return

    #提取400或者800号码，这类号码是营销电话，不需提取，只需要消除掉即可，需要在提取金额前替换掉
    def ex_48phone(self, str):
        pattern = re.compile("[4|8]00\\d{5,7}")  # 
        m = pattern.findall(str)
        for rs in m:
            self.nkey[rs] = "phone"
        return

    def ch_ex_dir(self):
        print(self.nkey)
        for key, value in self.nkey.items():
            v = self.rkey.get(value, "")
            if v == "":
                self.rkey[value] = key
            else:
                self.rkey[value] = v+" "+key
                
    def ex_file(self, filename):

        infile = filename
        try:
            inf = open(infile,'r')
        except:
            print('文件打开错误')
            exit(2)

        fstr = ""
        lines =  inf.readlines() #依次读取每行
        for line in lines: #依次读取每行
            self.ex_person(line)
            self.ex_48phone(line)
            self.ex_mobile(line)
            self.ex_price1(line)
            self.ex_price2(line)
            self.ex_price3(line)
        self.ch_ex_dir()
        print(self.rkey)


if __name__ == "__main__":
    ex = ex_car_info()
    ex.ex_file("./al")
