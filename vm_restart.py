#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2017-11-26

# from dateutil import parser
import MySQLdb,sys, os,time,datetime,re
from vm_tool import connect,exec_commands
import winrm
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 连接mysql数据库参数字段
con = None
ip = '172.25.1.13'
user = 'root'
password = '123456'
dbname = 'hj21_backend'
port = 3306
charset = 'utf8'

db = MySQLdb.connect(host=ip, user=user, passwd=password, db=dbname, port=port, charset=charset)
cursor = db.cursor()
vm_name = []
vm_room = []
#服务器清单
host = ['172.25.1.5','172.25.1.4','172.25.1.3','172.25.1.2','172.25.1.1']
#底层硬重启命令
# cmd = 'xe vm-reboot force=true name-label='
cmd = ['xe vm-start force=true name-label=','xe vm-reboot force=true name-label=']
#

# 获取教室里面的虚拟机信息
query_vm = '''SELECT CONCAT(wtc.terminal_name,'-V'),room.classroom_name
from wtc_terminal wtc
INNER  JOIN wtc_classroom room on wtc.classroom_id =room.id
'''
try:
    cursor.execute(query_vm)
    result = cursor.fetchall()
    # 获取教室云桌面数量
    vm_count = len(result)
    print unicode('A、B、C、D、E 教室云桌面数量共{0}台'.format(vm_count),'utf-8')
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
    print 'error'
# 关闭游标和mysql数据库连接
cursor.close()
db.close()
if __name__ == '__main__':

    #获取当前时间
    now_date = datetime.datetime.now().strftime('%H:%M')
    # print now_date
    # cure_date = datetime.datetime.strptime(now_date,'%Y-%m-%d %H:%M:%S')
    # print now_date
    #自定义重启时间
    set_retime = ['01:30','01:31','12:00']
    conn = connect(host=host[2])
    while True:
        now_date = datetime.datetime.now().strftime('%H:%M:%S')
        #判断星期六星期天不重启时间：0、6
        week = time.strftime("%w", time.localtime())
        if datetime.datetime.now().strftime('%H:%M') in set_retime:
            # if datetime.datetime.now().strftime('%H:%M') in set_retime and week not in [0, 6]:

            #批量重启虚拟机
            for vm_id in range(0,vm_count,1):
                # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
                recmd ='xe vm-reboot force=true name-label=%s' %(vm_name[vm_id])
                scmd = 'xe vm-start force=true name-label=%s' % (vm_name[vm_id])
                result=exec_commands(connect(host=host[0]), cmd=recmd)
                if re.findall(r"halted",result,re.M|re.I):
                    exec_commands(conn, cmd=scmd)
                    print unicode('{0}的{1}正在开机，请等待注册\n'.format(vm_room[vm_id].encode('utf-8'), vm_name[vm_id].encode('utf-8')),'utf-8')
                    continue
                print unicode('现在正在重启{0}的{1}请等待注册\n'.format(vm_room[vm_id].encode('utf-8'),vm_name[vm_id].encode('utf-8')),'utf-8')
                time.sleep(10)
            p = winrm.Session('http://172.25.1.33:5985/wsman', auth=('administrator', '1qaz@WSX'))
            for vm_id in range(0, vm_count, 1):
                filename = vm_name[vm_id].split('-V')[0]
                # print filename
                try:

                    p.run_cmd('del /F /S /Q  D:\%s\* '% (filename))
                except Exception,e:
                    print e
                finally:
                    print filename

            print p.run_cmd(r'del /S /Q  D:\teacher\1403\* ')
            print p.run_cmd(r'del /S /Q  D:\teacher\1404\* ')
            print p.run_cmd(r'del /S /Q  D:\teacher\1405\* ')
            print p.run_cmd(r'del /S /Q  D:\teacher\1406\* ')
            print p.run_cmd(r'del /S /Q  D:\teacher\1407\* ')
        else:
            print  unicode('现在时间：{0}，还未到重启时间{1} {2}，请等待\n'.format(now_date.encode('utf-8'),\
                    set_retime[0].encode('utf-8'), set_retime[2].encode('utf-8')),'utf-8')
            time.sleep(15)
        print unicode('A、B、C、D、E  教室云桌面数量共{0}台'.format(vm_count),'utf-8')