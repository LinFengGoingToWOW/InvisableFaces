# -*- coding: utf-8 -*-

#爬取清单
class Checklist:    
    def __init__(self):
        self.no = ''
        self.table_name= ''
        self.url = ''
        self.is_checked = False
        self.has_items = False

    def __iter__(self):
        return self

    def __next__(self):
        pass

#电视剧
class TVdrama:
    def __init__(self):
        self.no = ''
        self.url = ''
        self.name = ''
        self.original_release_year = 0
        self.production_year = 0
        self.area = ''

    def __iter__(self):
        return self

    def __next__(self):
        pass

#电视剧演职员
class TVdramaActorStaff:
    def __init__(self):
        self.no = ''
        self.tv_drama_url = ''
        self.type = 0
        self.actor_staff_url = ''

    def __iter__(self):
        return self

    def __next__(self):
        pass 

#演员
class Actor:
    def __init__(self):
        self.no = ''
        self.url = ''
        self.name = ''
        self.gender = 9
        self.birthyear = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        pass     

#职员
class Staff:
    def __init__(self):
        self.no = ''
        self.url = ''
        self.type = 1
        self.name = ''
        self.gender = 9
        self.birthyear = 0

    def __iter__(self):
        return self

    def __next__(self):
        pass



