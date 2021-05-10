#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re
from tables import TVdramaActorStaff
from html_downloader import HtmlDownloader
import tools

def Main(keyword):
    try:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(keyword)
        html = HtmlDownloader().download(url)
        tv_dramas_actors_staffs = []

        # Get the list of TV dramas and actors who have played in these TV dramas. 
        # 取得作品演员名单       
        if len(html.xpath('//div[contains(@class,"drama-actor")]')) != 0:
            actors_elements = html.xpath('//div[contains(@class,"drama-actor")]')[0]
            # return text string that matches the condition
            # 返回满足检索条件的文字列
            actors_str = tools.HtmlToStr(actors_elements)
            actors= re.findall(r"data-lemmaid=\"(\d+.*?)</a>.*[\s]*饰", actors_str)

            for a in actors:
                was = TVdramaActorStaff()
                was.tv_drama_url = keyword
                was.type = 0
                was.actor_staff_url = tools.FindNameNo(a)
                tv_dramas_actors_staffs.append(was)

        # Get the list of TV drams and directors who have joined in production of these TV dramas.
        # 取得作品导演名单
        if len(html.xpath('//div[contains(@class,"basic-info cmn-clearfix")]')) != 0:
            staffs_elements = html.xpath('//div[contains(@class,"basic-info cmn-clearfix")]')[0]
            staffs_str = tools.HtmlToStr(staffs_elements)
            staffs_str_deleted= tools.DeleteSpace(staffs_str)

            directors_href = re.findall(r"导\xa0\xa0\xa0\xa0演(.*?)</dd>", staffs_str_deleted)
            directors_href_str = ''.join(directors_href)
            directors = tools.FindNamesNos(directors_href_str)
            for d in directors:
                was = TVdramaActorStaff()
                was.tv_drama_url = keyword
                was.type = 1
                was.actor_staff_url = d
                tv_dramas_actors_staffs.append(was)

        # Get the list of TV drams and play wrights who have joined in production of these TV dramas.
        #取得作品编剧名单
            playwrights_href = re.findall(r"编\xa0\xa0\xa0\xa0剧.*?</dd>", staffs_str_deleted)
            playwrights_href_str= ''.join(playwrights_href)
            playwrights = tools.FindNamesNos(playwrights_href_str)
            for p in playwrights:
                was = TVdramaActorStaff()
                was.tv_drama_url = keyword
                was.type = 2
                was.actor_staff_url = p
                tv_dramas_actors_staffs.append(was)            

        return tv_dramas_actors_staffs 
    except:
        raise      

#debug
if __name__ == '__main__':
    keyword = input('The keyword is : 查询词语：')
    result = Main(keyword)

    for i in result:
        print(i.tv_drama_url)
        print(i.type)
        print(i.actor_staff_url)

