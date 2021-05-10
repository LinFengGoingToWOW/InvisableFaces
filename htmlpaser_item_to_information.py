# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re
from lxml import etree
from tables import TVdrama
from html_downloader import HtmlDownloader
    
def Main(keyword):
    try:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(keyword)
        html = HtmlDownloader().download(url)
        information_list = html.xpath('//div[contains(@class,"basic-info cmn-clearfix")]//text()')
        information_str = ''.join(information_list)
        t = TVdrama()

        # url
        t.url = keyword

        # name
        # 作品名
        keyword_name = ''.join(re.findall(r"(.*?)\/",keyword))
        if keyword_name != '':
            t.name = keyword_name
        else:
            t.name = keyword

        # area
        # 制片地区
        t.area= ''.join(re.findall(r"制片地区\s*(.*)\s", information_str))

        # Original Release Date
        # 播出时间
        if ''.join(re.findall(r"首播时间\s*?(\d{4})",information_str)) != '':    
            original_release_year = ''.join(re.findall(r"首播时间\s*?(\d{4})",information_str)[0:1])
            t.original_release_year = int(original_release_year)
        elif ''.join(re.findall(r"播出时间\s*?(\d{4})",information_str)) != '':    
            original_release_year = ''.join(re.findall(r"播出时间\s*?(\d{4})",information_str)[0:1])
            t.original_release_year = int(original_release_year)

        # Production Date
        # 出品时间
        production_year = ''.join(re.findall(r"出品时间\s*?(\d{4})",information_str)[0:1])
        if production_year != '':
            t.production_year = int(production_year)  

        return t
    except :
        raise

#debug
if __name__ == '__main__':
    keyword = '白狼/231469'
    result = Main(keyword)

    print ( '结果是:' +  result.name,result.original_release_year,result.production_year)
