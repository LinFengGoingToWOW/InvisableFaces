#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib.request
import urllib.parse
import urllib.error
import re
from lxml import etree
from tables import Checklist
from html_downloader import HtmlDownloader

def Main():
    result = []
    for i in range(1981,2009):
        try:
            result = result + SearchUntil2008(i)   
        except :
            pass
    for i in range(2009,2022):
        try:
            result = result + SearchSince2009(i)
        except :
            pass           
    return result

# Find out the information of TV dramas which were produced until 2008.
# 爬取2008年及以前的电视剧信息

def SearchUntil2008(i):
    # 请求地址
    # Create a URL to send request. 
    keyword =  str(i) + "年中國電視劇集"
    url = 'https://zh.wikipedia.org/zh-cn/Category:' + urllib.parse.quote(keyword)
    html = HtmlDownloader().download(url)

    # Use tags to take out the part of html what I wanted.
    # 根据html标签决定提取对象
    names_makedyear = html.xpath('//div[contains(@class,"mw-category")]')[0]
    names_makedyear_str = etree.tostring(names_makedyear, encoding='utf8', method='html').decode()
    answerList  = []
    nms = re.findall("<a href=.*?>(.*?)</a>",names_makedyear_str.replace('\n',''))
    for name in nms:
        if '(' in name :
            name = ''.join(re.findall(r"(.*?)\(",name))
        c = Checklist()
        c.table_name = 'works'
        c.url = name
        c.has_items = True
        if c.url != '':
            answerList.append(c)
    # 返回checklist型列表  
    return answerList

# Find out the information of TV dramas which were produced since 2009.
# 爬取2009年及以后的电视剧信息
def SearchSince2009(i):
    keyword = "中国大陆电视剧列表_(" + str(i) + "年)"
    url = 'https://zh.wikipedia.org/zh-cn/' + urllib.parse.quote(keyword)
    html = HtmlDownloader().download(url)

    information_list = html.xpath('//table[contains(@class,"wikitable")]')
    answerList = []
    for information in information_list[0:3]:
        records = etree.tostring(information, encoding='utf-8', method='html').decode()
        result = FindInformation(records)
        answerList = answerList + result 

    return answerList

#Take out TV drama's name, original release date and production date from a list of text string, and put them into a 'TVdrama' type.
#从字符串集合中提取剧名、播出年份和出品年份，并生成TVdrama型的result

def FindInformation(records):
    nms = []
    records = re.findall("<tr>(.*?)</tr>",records.replace('\n',''))
    for record in records:
        nys = re.findall("(<td.*?</td>)",record)    
        maked_years = re.findall(">(\d{4})</td>",''.join(nys))
        maked_year = ''.join(maked_years)   
        name = nys[0]

        # If the name is in a href, take out it from the href.
        # 剧名包含超链接时，从超链接中取出剧名：
        if 'href' in name:
            first_name = ''.join(re.findall(r"a href=\".*?title=.*?>(.*?)</a>",name))
            second_name = ''.join(re.findall(r"</a>(.*?)<",name))
            name = first_name + second_name

        # If the name isn't in a href, just get it.
        # 剧名不包含超链接时，直接取得剧名：
        else:
            name = ''.join(re.findall(r"<td>(.*?)</td>",name))

        # If the name contains marks like '/' or '\', just get the text string before these marks. 
        # 剧名包含“/”“\”等重名符号时，只提取符号前的字符串：
        if '/' in name :
            name = ''.join(re.findall(r"(.*?)/",name))
        if '\\' in name:
            name = ''.join(re.findall(r"(.*?)\\",name))

        c = Checklist()
        c.table_name = 'works'
        c.url = name
        c.has_items = True
        if c.url != '':
            nms.append(c)
    return nms


#debug            
if __name__ == '__main__':
    while True:
        try:
            result = Main()
            
            for r in result:
                print ( 'The result is: 结果是:' +  r.url)
        except:
            quit()
    
