import time
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import main
import sys

#Task manager, with what I can manage multiple tasks at the same time.
#Task 1, task 4, task 6 and task 8 are not long running, so I took them out from this task manager.
#You can just run it in the 'main' file by deleting the '#' from the last part of the file. 
#任务管理器。可同时运行多个任务。因任务1、4、6、8耗时不长，所以未列入任务列表中。通过main文件下的debug部分手动运行即可。

# If the length of list returned by select query is 0, the task will be ignored.  
# 当剩余待检索行数为0时，任务将因为取不到值而被跳过。
# If the length of list returned by select query is less than 0, 
# the task may be ignored because the rows the task need to lock have already locked by another task.
# 当剩余待检索行数小于10行时，由于sql server锁原因，可能导致个别任务取不到值而被跳过。
# 2
def FromChecklistTVdramaToChecklistItem():
    try:
        main.FromChecklistTVdramaToChecklistItem(0)
        print('task 2-0 is completed at ' + GetTS())
    except IndexError:
        print('task 2-0 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 2-0 is failed at ' + GetTS()) 
        PrintRollBackError()

def FromChecklistTVdramaToChecklistItem1():
    try:
        main.FromChecklistTVdramaToChecklistItem(1)
        print('task 2-1 is completed at ' + GetTS())
    except IndexError:
        print('task 2-1 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 2-1 is failed at ' + GetTS()) 
        PrintRollBackError()
# 3
def FromChecklistItemToTVdrama():
    try:
        main.FromChecklistItemToTVdrama(0)
        print('task 3-0 is completed at ' + GetTS())
    except IndexError:
        print('task 3-0 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 3-0 is failed at ' + GetTS()) 
        PrintRollBackError()

def FromChecklistItemToTVdrama1():
    try:
        main.FromChecklistItemToTVdrama(1)
        print('task 3-1 is completed at ' + GetTS())
    except IndexError:
        print('task 3-1 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 3-1 is failed at ' + GetTS()) 
        PrintRollBackError()
# 5
def FromChecklistItemToTVdramaActorStaff():
    try:
        main.FromChecklistItemToTVdramaActorStaff(0)
        print('task 5-0 is completed at ' + GetTS())
    except IndexError:
        print('task 5-0 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 5-0 is failed at ' + GetTS()) 
        PrintRollBackError()   
def FromChecklistItemToTVdramaActorStaff1():
    try:
        main.FromChecklistItemToTVdramaActorStaff(1)
        print('task 5-1 is completed at ' + GetTS())
    except IndexError:
        print('task 5-1 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 5-1 is failed at ' + GetTS()) 
        PrintRollBackError()
# 7
def FromChecklistActorToActor():
    try:
        main.FromChecklistActorToActor(0)
        print('task 7-0 is completed at ' + GetTS())
    except IndexError:
        print('task 7-0 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 7-0 is failed at ' + GetTS()) 
        PrintRollBackError()

def FromChecklistActorToActor1():
    try:
        main.FromChecklistActorToActor(1)
        print('task 7-1 is completed at ' + GetTS())
    except IndexError:
        print('task 7-1 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 7-1 is failed at ' + GetTS()) 
        PrintRollBackError()
# 9
def FromChecklistStaffToStaff():
    try:
        main.FromChecklistStaffToStaff(0)
        print('task 9-0 is completed at ' + GetTS())
    except IndexError:
        print('task 9-0 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 9-0 is failed at ' + GetTS()) 
        PrintRollBackError()

def FromChecklistStaffToStaff1():
    try:
        main.FromChecklistStaffToStaff(1)
        print('task 9-1 is completed at ' + GetTS())
    except IndexError:
        print('task 9-1 is failed at ' + GetTS())
        PrintIndexError()
    except:
        print('task 9-1 is failed at ' + GetTS()) 
        PrintRollBackError()

def GetTS():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return ts

def PrintIndexError():
        print('We can\'t find what you are looking for. I\'m sorry to telling you that the task will be ignored.')
        print('因此次没有取得所需数值，所以任务将被跳过。')
def PrintRollBackError():
        print('Cannot commit transaction because it was marked for rollback error.',str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2]))
        print('因出现需要回滚的错误，我们无法提交事务。')

def dojob():   
    bs = BlockingScheduler()
    bs.add_job(FromChecklistTVdramaToChecklistItem, 'interval', seconds = 15, id='task2-0')
    bs.add_job(FromChecklistTVdramaToChecklistItem1, 'interval', seconds = 15, id='task2-1') 
    bs.add_job(FromChecklistItemToTVdrama, 'interval', seconds = 15, id='task3-0')
    bs.add_job(FromChecklistItemToTVdrama1, 'interval', seconds = 15, id='task3-1')   
    #bs.add_job(FromChecklistItemToTVdramaActorStaff, 'interval', seconds = 15, id='task5-0')
    #bs.add_job(FromChecklistItemToTVdramaActorStaff1, 'interval', seconds = 15, id='task5-1')
    #bs.add_job(FromChecklistActorToActor, 'interval', seconds = 15, id='task7-0')
    #bs.add_job(FromChecklistActorToActor1, 'interval', seconds = 15, id='task7-1')
    #bs.add_job(FromChecklistStaffToStaff, 'interval', seconds = 15, id='task9-0')     
    #bs.add_job(FromChecklistStaffToStaff1, 'interval', seconds = 15, id='task9-1')     
    bs.start()

dojob()

''' 
#debug  
if __name__=='__main__':
    
    sched = BackgroundScheduler()
    sched.add_job(ItemsFromBaiduToWorks, 'interval', id='15_second_job', seconds=15)
    sched.start()

'''
