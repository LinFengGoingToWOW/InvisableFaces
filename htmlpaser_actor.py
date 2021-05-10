# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re
from lxml import etree
from tables import Actor
import tools
from html_downloader import HtmlDownloader

def Main(keyword):
    try:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(keyword)
        html = HtmlDownloader().download(url)

        a = Actor()
        a.url = keyword
        url_name = ''.join(re.findall(r"(.*?)\/",keyword))
        if url_name != '':
            a.name = url_name
        else:
            a.name = keyword

        # 性别
        # gender
        sen_list = html.xpath('//div[contains(@class,"lemma-summary")]//text()')
        sen_list_str = ''.join(sen_list)
        first_sentence = sen_list_str.split('。')[0]

        if '男' in first_sentence:
            a.gender = 1
        elif '女' in first_sentence:
            a.gender = 0

        #出生日期
        # birth year
        birthyear =  html.xpath('//div[contains(@class,"basic-info cmn-clearfix")]//text()')
        birthyear_space_deleted = tools.DeleteSpace(''.join(birthyear))
        birthyear_str = re.findall("出生日期(\d{4})", birthyear_space_deleted)
        if birthyear_str:
            a.birthyear = int(''.join(birthyear_str))

        return a
    except:
        raise
#debug
if __name__ == '__main__':
    keyword = input('The keyword is: 查询词语：')
    result = Main(keyword)
    print(result.name)
    print(result.gender)
    print(result.birthyear)
   