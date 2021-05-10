# -*- coding: UTF-8 -*-

import os
import urllib.request
import urllib.parse
import re
from lxml import etree
from tables import Checklist
from html_downloader import HtmlDownloader

#从义项页中提取每个义项
def Main(keyword):
    try:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(keyword)
        html = HtmlDownloader().download(url)

        # There are three types of pages that we can get from urls.
        # 1.the first type
        # The url is a disambiguation page that lists the full titles of several different articles,
        # but we can't get any specific information (like the production date of a TV drama, etc) from the url itself.  
        # 义项页中没有自己 如：“穿越火线”的百度百科页面
        if  html.xpath('//div[contains(@class,"lemmaWgt-subLemmaListTitle")]'):
            html_item = html.xpath('//ul[contains(@class,"custom_dot  para-list list-paddingleft-1")]')[0]
            html_str = etree.tostring(html_item, encoding='utf8', method='html').decode()
            items = re.findall(r"<a target=.*?data-lemmaid=\"(\d+)\"",html_str)                        
            checklists = []
            for item in items:
                c = Checklist()
                c.table_name = 'items'
                c.url = keyword + '/' + item
                checklists.append(c)
            
        # 2.the second type
        # The url contains links to other articles as same as a disambiguation page, 
        # but we can get some specific information about one of the TV dramas from the url itself.
        #义项页中有自己 如“射雕英雄传”的百度百科页面
        elif html.xpath('//div[contains(@class,"polysemantList-header-title")]'):
            html_item = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]')[0]
            html_str = etree.tostring(html_item, encoding='utf8', method='html').decode()
            my_str = re.findall(r"<span class=\"selected\">(.*?)</span>",html_str)
            checklists = []
            c = Checklist()
            c.table_name = 'items'
            c.url = keyword
            checklists.append(c)
            items = re.findall(r"href=\"/item/.*?(\d+)#",html_str)
            for item in items:
                c = Checklist()
                c.table_name = 'items'
                c.url = keyword + '/' + item
                checklists.append(c)

        #3 the third type
        # The url is not a disambiguation page.
        #没有其他义项 如“山海情”的百度百科页面
        else :
            checklists = []
            c = Checklist()
            c.table_name = 'items'
            c.url = keyword
            checklists.append(c)

        return checklists
    except:
        raise

#debug
if __name__ == '__main__':
    keyword = '穿越火线'
    result = Main(keyword)
    for r in result:
        print(r.url)


