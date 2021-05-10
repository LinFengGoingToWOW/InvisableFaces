#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from lxml import etree

    # change element to string
    # 把xml转换为字符串
def HtmlToStr(element):
    result = etree.tostring(element, encoding='utf8', method='html').decode()
    return result

    # delete space
    # 删除空格    
def DeleteSpace(str):
    result = str.replace('\n','')
    return result

   # Take out names and serial numbers from hrefs starting with '<a target = '.
   # 从“<a target = ”开头的n条超链接中提取出人名和编号
def FindNamesNos(str):
    names = re.findall(r"data-lemmaid=\"(\d+.*?)</a>",str)
    name_list = []
    for name in names:
        result =FindNameNo(name)
        name_list.append(result)
    return name_list

    # Take out name and serial number from text string starting with 'serial number/name'.
    #从“ 编号">姓名 ”格式的字符串中提取姓名和编号
def FindNameNo(str):
    result = FindName(str) + FindNo(str)
    return result

    # Find name.
    # 提炼姓名 
def FindName(file):
    name = re.findall(r'">(.*)', file)
    result = ''.join(name)
    return result

    # regex for integer
    # 提炼数字
def FindNo(file):
    no = re.findall(r'[\d]',file)
    result = '/' + ''.join(no)
    return result
    
