#!/bin/env python
# -*- coding: utf-8 -*-
#function:远程关机
#Author:Timberland

import winrm
import pymysql,time
# 连接mysql数据库参数字段
con = None
ip = '172.25.1.13'
user = 'root'
password = '123456'
dbname = 'hj3_backend'
port = 3306
charset = 'utf8'

db = pymysql.connect(host=ip, user=user, passwd=password, db=dbname, port=port, charset=charset)
cursor = db.cursor()
vm_name = []
vm_room = []
# 获取教室里面的虚拟机信息
query_vm = '''SELECT vm.vm_name,dg.dg_name
from hj_vm vm 
INNER JOIN hj_dg dg on dg.id = vm.dg_id
WHERE dg.dg_name = 'c407' and vm.del_flag= 0 and vm.vm_type=1
'''
try:
    cursor.execute(query_vm)
    result = cursor.fetchall()
    # 获取教室云桌面数量
    vm_count = len(result)
    # print unicode('A、B、C、D教室云桌面数量共{0}台'.format(vm_count),'utf-8')
    # print len(cursor.fetchall())
    # cursor.execute(query_vm)
    for vm_id in range(0,vm_count,1):
        # print result[vm_id][0]
        # print result[vm_id][1]
        vm_name.append(result[vm_id][0])
        vm_room.append(result[vm_id][1])

    # print type(cursor.fetchall()[0])

    db.commit()

except ValueError:
    db.roolback
    print ('error')
# 关闭游标和mysql数据库连接
cursor.close()
db.close()
for vm_id in range(0,vm_count,1):

    win7 = winrm.Session('http://%s.lnxdjx.com:5985/wsman'%('JSWIN7-290'),auth=('administrator','1qaz@WSX'))
    print ('%s is  delete'%(vm_name[vm_id]))
    # print (win7.run_cmd('dir e:\\').std_out)
    print (win7.run_cmd('del /F /S /Q E:\\*').std_out)
    print(win7.run_cmd('rd  /S /Q E:\\').std_out)
    print(win7.run_cmd('rd  /S /Q E:\\').std_out)
    time.sleep(5)
    print ('%s is  finish'%(vm_name[vm_id]))



# print dir(win2012)
# r = win2012.run_cmd('del /F /S /Q  D:\D01-063\* ')
# print  r.status_code
# print(r.std_out) # 打印获取到的信息
# print(r.std_err) #打印错误信息

