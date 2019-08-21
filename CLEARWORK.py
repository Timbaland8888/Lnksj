#!/bin/env python
# -*- coding: utf-8 -*-
#function:远程关机
#Author:Timberland
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re
import winrm
import subprocess
import pymysql,time
import ConfigParser, codecs
import logging
# 连接mysql数据库参数字段
cf = ConfigParser.ConfigParser()
cf.readfp(codecs.open('config.ini', "r", "utf-8-sig"))
logger = logging.getLogger()
logger.setLevel('DEBUG')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler() # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('debug.log') # 输出到文件的handler
fhlr.setFormatter(formatter)
logger.addHandler(chlr)
logger.addHandler(fhlr)

con = None
db = pymysql.connect(host=cf.get('hj_db', 'db_host'), user=cf.get('hj_db', 'db_user'), passwd=cf.get('hj_db', 'db_pwd'), db=cf.get('hj_db', 'db'), port=cf.getint('hj_db', 'db_port'), charset='utf8')
cursor = db.cursor()
vm_name = []
vm_room = []
# 获取教室里面的虚拟机信息
query_vm = '''SELECT vm.vm_name,dg.dg_name
from hj_vm vm 
INNER JOIN hj_dg dg on dg.id = vm.dg_id
WHERE vm.del_flag= 0 and vm.vm_type=1
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
        # print 'del /F /S /Q %s:\\*'%(cf.get('dis_flag','flag_name'))
        # print 'rd  /S /Q %s:\\'%(cf.get('dis_flag','flag_name'))
        # print 'rd  /S /Q %s:\\'%(cf.get('dis_flag','flag_name'))
        # p = subprocess.Popen('ping 192.168.49.222',stdout=subprocess.PIPE).stdout.read()
        result = os.popen('ping %s.%s'%(vm_name[vm_id],cf.get('domain','domain_name')))
        # print 'ping %s.%s'%(vm_name[vm_id],cf.get('domain','domain_name'))
        p = result.read()
        logger.info(p)
        # print len(re.findall('TTL',p))
        if  len(re.findall('TTL',p)) != 0:
            win7 = winrm.Session('http://%s.%s:5985/wsman'%(vm_name[vm_id],cf.get('domain','domain_name')),auth=(cf.get('vm_info','vm_acount'),cf.get('vm_info','vm_pwd')))

            logger.info ('%s is  delete now'%(vm_name[vm_id]))

            logger.info (win7.run_cmd('del /F /S /Q %s:\\*'%(cf.get('dis_flag','flag_name'))).std_out)

            logger.info(win7.run_cmd('rd  /S /Q %s:\\'%(cf.get('dis_flag','flag_name'))).std_out)
            logger.info(win7.run_cmd('rd  /S /Q %s:\\'%(cf.get('dis_flag','flag_name'))).std_out)
            time.sleep(5)
            logger.info ('%s is  finish'%(vm_name[vm_id]))
        else:
            logger.info(' %s.%s 网络不通'%(vm_name[vm_id],cf.get('domain','domain_name')))

# print dir(win2012)
# r = win2012.run_cmd('del /F /S /Q  D:\D01-063\* ')
# print  r.status_code
# print(r.std_out) # 打印获取到的信息
# print(r.std_err) #打印错误信息

