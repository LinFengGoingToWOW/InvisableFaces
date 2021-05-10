#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import htmlpaser_wiki,htmlpaser_wiki_to_item,htmlpaser_item_to_information
import htmlpaser_tv_drama_actor_staff,htmlpaser_actor,htmlpaser_staff
from tables import Checklist
from dao import Dao

#1.I extracted a list of Chinese television TV dramas between 1981 and 2021(until 2021.3.31),and insert them into table 'checklists'.
#1.从维基百科爬取1981-2021年的电视剧剧名，插入表“爬取清单”
def FromWikiToChecklistTVdrama():  
    checklists = htmlpaser_wiki.Main()
    try:
        dao = Dao()
        iis = dao.Insert('checklists',checklists)
        dao.Commit()
        
    except: 
        print("Unexpected error:", str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2]))
        dao.Rollback()
        
#2.Then I searched the names of TV dramas in table 'checklists' in Baidu Baike
# (an online encyclopedia owned by Baidu, a Chinese search engine,
# from what I can get more information about actors who have played in Chinese TV dramas) 
# and got a list of links from disambiguation pages. 
# Then, I added them to the table 'checklists'.
#2.从表“爬取清单”中取出剧名，在百度百科中查找义项（因为电视剧的百度百科能够关联更多演员主页），并将义项插入表“爬取清单”中。
def FromChecklistTVdramaToChecklistItem(sort):
    try:
        s = DetermineSort(sort)
        dao = Dao()
        checklists = dao.Select('SELECT TOP 10 * FROM checklists WITH (ROWLOCK, XLOCK) WHERE is_checked = \'False\' and has_items = \'True\' ORDER BY no ' + s)             
        if (len(checklists) == 0):
            raise IndexError
        itemss = []
        for c in checklists:
            items = htmlpaser_wiki_to_item.Main(c.url)
            itemss = itemss + items
            c.is_checked = True
        dao.Insert('checklists',itemss)
        dao.Update('checklists',checklists)
        dao.Commit()
    except :
        dao.Rollback()
        raise
        
#3.To find out the TV dramas, I used the disambiguation pages with links what I'd got in step 2 
#to get some information about them, and inserted this information into table 'tv_dramas'.
#3.为了从这些义项中筛选出所有的电视剧，从表“爬取清单”中找出义项，在百度百科中查询该义项的各项信息，把结果插入作品表中
def FromChecklistItemToTVdrama(sort):
    try:
        s = DetermineSort(sort)
        dao = Dao()
        checklists = dao.Select(' SELECT TOP 10 * FROM checklists WITH (ROWLOCK, XLOCK) WHERE table_name = \'items\' AND is_checked = \'False\' ORDER BY no ' + s)
        if (len(checklists) == 0):
            raise IndexError
        items = []
        for c in checklists:
            t = htmlpaser_item_to_information.Main(c.url)
            items.append(t)
            c.is_checked = True
        dao.Insert('tv_dramas',items)
        #todo
        dao.Update('checklists',checklists)
        dao.Commit()
    except :
        dao.Rollback()
        raise
        
# Because that I had to make sure that all these TV dramas are produced in mainland China,  
# I choose to use sql to delete some tv_dramas what are produced only in HongKong, Macau, Taiwan or the other Coutries before starting this step.
# However, I didn't delete the ones, if a part of them are produced in HongKong, Macau, Taiwan or the other Countries.
# 注：由于须手工筛选“制片地区”为大陆，或包括大陆在内的地区，故第三步完成后，先通过sql确定制片地区，将制片地区只包含国外或港澳台的作品删除。

# 4.I seleted TV dramas from the disambiguation pages with links by confirming that each of the items has an original release date and a production date. 
# Then I inserted them into table 'checklists'.
# 4.通过确定播出时间和出品时间，在作品表中筛选出作为电视剧的义项。然后把该部分行复制到爬取清单。

def FromTVdramaToChecklistItem():
    try:
        dao = Dao()
        tv_dramas = dao.Select( 'SELECT * FROM tv_dramas WITH (ROWLOCK, XLOCK) WHERE original_release_year <>0 and production_year <>0')
        checklists = []
        for t in tv_dramas:
            c = Checklist()
            c.table_name = 'tv_dramas_actors_staffs'
            c.url = t.url
            checklists.append(c)
        uw = dao.Insert('checklists',checklists)
        dao.Commit()
        
    except :
        print("Unexpected error:", str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2]))
        dao.Rollback()
        
# 5.I took out TV dramas from table 'checklists' that I got in step 4 to find out actors, directors and playwrights, and put them into table 'tv_dramas_actors_staffs'.  
# 5.从表“爬取清单”中取出④中提取出的作为电视剧的义项，以此为基础查找演职员，并插入“作品演职员”表。
def FromChecklistItemToTVdramaActorStaff(sort):
    try:
        s = DetermineSort(sort)
        dao = Dao()
        tv_dramas = dao.Select(' SELECT TOP 10 * FROM checklists WITH (ROWLOCK, XLOCK) WHERE table_name = \'tv_dramas_actors_staffs\' AND is_checked = \'False\' ORDER BY no ' + s)  
        if (len(tv_dramas) == 0):
            raise IndexError
        tass = []
        for t in tv_dramas:
            t.is_checked = True
            tas = htmlpaser_tv_drama_actor_staff.Main(t.url)
            tass = tass + tas
        uc = dao.Insert('tv_dramas_actors_staffs',tass)
        uc = dao.Update('checklists',tv_dramas)
        dao.Commit()
    except :
        dao.Rollback()
        raise
        
#6. As is generally known, an actor usually play roles in more than one TV drama, I maked a list of actors from table 'tv_dramas_actors_staffs', and inserted them into table 'checklists' to get number and information of actors.
#6.因为一个演员可能出演不止一部作品，所以为了确定演员的人数和信息，我们从作品演职员表中整理出参加过演出的演员名单，并放入表“爬取清单”中。
def FromTVdramaActorStaffToChecklistActor():
    try:
        dao = Dao()
        tass = dao.Select( 'SELECT distinct actor_staff_url FROM tv_dramas_actors_staffs WITH (ROWLOCK, XLOCK) WHERE 1=1 and type = 0')
        checklists = []
        for t in tass:
            c = Checklist()
            c.table_name = 'actors'
            c.url = t.actor_staff_url
            checklists.append(c)
        uw = dao.Insert('checklists',checklists)
        dao.Commit()
        
    except :
        print("Unexpected error:", str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2]))
        dao.Rollback()
        
#7.I took out actors from table 'checklists', found out the birth year and the gender of these actors, and inserted them into table 'actors'. 
#7.从表“爬取清单”中取出演员，查找他们的出生年份、性别等消息，并放入演员表中
def FromChecklistActorToActor(sort):
    try:
        s = DetermineSort(sort)
        dao = Dao()
        checklists = dao.Select(' SELECT TOP 10 * FROM checklists WITH (ROWLOCK, XLOCK) WHERE table_name = \'actors\' AND is_checked = \'False\' order by no ' + s)  
        if (len(checklists) == 0):
            raise IndexError
        actors = []
        for c in checklists:
            c.is_checked = True  
            a = htmlpaser_actor.Main(c.url)
            actors.append(a)
        uc = dao.Update('checklists',checklists)
        uc = dao.Insert('actors',actors)
        dao.Commit()  
    except :
        dao.Rollback()
        raise
         
#8.As is generally known, a director or a play wright usually join production of more than one TV drama, I maked a list of directors and play wrights from table 'tv_dramas_actors_staffs', and inserted them into table 'checklists'.
#8.因为一个职员可能参与不止一部作品的制作，所以我们从作品演职员表中整理出参加过作品制作的职员名单，并放入表“爬取清单”中。
def FromTVdramaActorStaffToChecklistStaff():
    try:
        dao = Dao()
        tass_directors = dao.Select('SELECT DISTINCT actor_staff_url FROM tv_dramas_actors_staffs WITH (ROWLOCK, XLOCK) WHERE type = 1')
        tass_play_wrights = dao.Select('SELECT DISTINCT actor_staff_url FROM tv_dramas_actors_staffs WITH (ROWLOCK, XLOCK) WHERE type = 2')        
        checklists = []
        for wd in tass_directors:
            c = Checklist()
            c.table_name = 'staffs_1'
            c.url = wd.actor_staff_url
            checklists.append(c)

        for wp in tass_play_wrights:
            c = Checklist()
            c.table_name = 'staffs_2'
            c.url = wp.actor_staff_url
            checklists.append(c)

        uw = dao.Insert('checklists',checklists)
        dao.Commit() 
        
    except :
        print("Unexpected error:", str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2]))
        dao.Rollback()
                   
#9.I took out directors and play wrights from table 'checklists', found out the birth year and the gender of these directors and play wrights, and inserted them into table 'staffs'. 
#9.从表“爬取清单”中取出职员，查找他们的出生年份、性别等消息，并放入职员表中
def FromChecklistStaffToStaff(sort):
    try:
        s = DetermineSort(sort)
        dao = Dao()
        #todo
        checklists = dao.Select('SELECT TOP 10 * FROM checklists WITH (ROWLOCK, XLOCK) WHERE table_name like \'staff%\' AND is_checked = \'False\' order by no ' + s)                 
        if (len(checklists) == 0):
            raise IndexError
        staffs = []
        for c in checklists:
            c.is_checked = True
            if c.table_name == 'staffs_1':
                type = 1
            else:
                type = 2
            s = htmlpaser_staff.Main(c.url,type)
            staffs.append(s)
        uc = dao.Update('checklists',checklists)
        uc = dao.Insert('staffs',staffs)
        dao.Commit()
    except :
        dao.Rollback()
        raise

 #todo
 # select for update       

def DetermineSort(sort):
    if sort == 0 :
        return ''
    else:
        return 'desc'

#debug
# Task 1,4,6 and 8 don't take a long time to run, so you can just run it in this class. Each of them will complete in 2 minutes.
# 任务1、4、6、8耗时不长，所以可以在这个文件中直接运行。每个任务耗时基本不超过两分钟。
# 1
#FromWikiToChecklistTVdrama();
# 4
#FromTVdramaToChecklistItem();
# 6
# FromTVdramaActorStaffToChecklistActor();
# 8
#FromTVdramaActorStaffToChecklistStaff();
