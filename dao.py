# -*- coding: utf-8 -*-

from tables import TVdrama,Actor,Staff,TVdramaActorStaff,Checklist
import pyodbc
import re

class Dao:
    def __init__(self):
        server = 'localhost' 
        database = 'InvisableFaces' 
        username = 'user' 
        password = 'password' 
        message = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
        self.conn = pyodbc.connect(message)
        self.conn.autocommit = False
        self.cur = self.conn.cursor()

    def Select(self,selectWords):
#        self.cur.execute("BEGIN TRANSACTION")  
        self.cur.execute(selectWords)

        colnames = [desc[0] for desc in self.cur.description]     
        fromTable = ''.join(re.findall(r'FROM (.*?) WITH', selectWords))
        result = self.TableMapping(fromTable)   
        keys = [] 
        for key in result.__dict__.keys():
            keys.append(key)
        answerList = []
 
        list = self.cur.fetchall()
        for i in list:   
            result = self.TableMapping(fromTable)   
            # if a property of the element 'i' and a column of the table 'fromTable' are equal, put the column's value into the property's value.           
            #类的属性与表的属性名相等时，令类的该属性的值等于表的该属性的值。
            for k in keys:
                # If the number of properties is more than that of columns, 
                # the initial values of the properties which have not the same name as one of the columns won't be changed.
                # If the number of properties is less than that of columns, 
                # the values of columns which have not the same name as one of the properties won't be put into the properties.
                #若类的属性数>sql得到的属性数，则类的其他属性为初始属性； 若类的属性数<sql得到的属性数，sql的其他属性不会被插入类中。
                try:
                    setattr(result, k, i[colnames.index(k)]) 
                except:
                    pass    
            answerList.append(result)
        return answerList
                    
    def Insert(self,tableName,list):
        keys = []
        for key in list[0].__dict__.keys():
            keys.append(key)
        keysStr = ','.join(keys[1:])   

        # if a property of the element 'i' and a column of the table 'fromTable' are equal, put the column's value into the property's value.           
        #类的属性与表的属性名相等时，令类的该属性的值等于表的该属性的值。    
        for i in list:
            values = []
            for value in i.__dict__.values():
                if value == '':
                    value = 'null'
                elif type(value) is str:
                    value = "N'" + value + "'"
                elif type(value) is bool:
                    value = "'" + str(value) + "'"
                else:
                    value = str(value)
                values.append(value)
            valuesStr = ','.join(values[1:])

            sql = 'INSERT INTO ' + ' ' + tableName + '(' + keysStr + ')' + ' VALUES ' + '(' + valuesStr + ')'
            self.cur.execute(sql)

    def Update(self,tableName,list):       
        no_value = ''
        # if a property of the element 'i' and a column of the table 'fromTable' are equal, put the column's value into the property's value.           
        #类的属性与表的属性名相等时，令类的该属性的值等于表的该属性的值。    
        for i in list:
            sql = 'UPDATE' + ' ' + tableName + ' SET '
            keys_values = []
            for key,value in i.__dict__.items():
                if key == 'no' :
                    no_value = value
                else:
                    if value == '':
                        value = 'null'
                    elif type(value) is str:
                        value = "N'" + value + "'"
                    elif type(value) is bool:
                        value = "'" + str(value) + "'"
                    else:
                        value = str(value)              

                    key_value = key + '=' + value
                    keys_values.append(key_value)
            sql = sql + ','.join(keys_values) + ' WHERE no=' + str(no_value) 
            self.cur.execute(sql) 

    def TableMapping(self,tablename):
        values = {
            'checklists':Checklist(),
            'tv_dramas':TVdrama(),
            'tv_dramas_actors_staffs':TVdramaActorStaff(),
            'actors':Actor(),
            'staffs':Staff()
        }
        return values[tablename]                             

    def Commit(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def Rollback(self):
        self.conn.rollback()
        self.cur.close()
        self.conn.close()

'''
#debug
try:
    dao = Dao()
    list = []
    w = TVdrama()
    w.name = 'test'
    w.url = 'test/url'
    w.original_release_year = 'abc'
    list.append(w)
    uc = dao.Insert('tv_dramas',list)
    dao.Commit();
    print('事务已提交。')
    print('The transaction is committed')
except:
    dao.Rollback();
    print('事务已回滚。')
    print('The transaction is rolled back.')
'''



        



