#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2017-12-26
import subprocess
import sys,wmi,time,datetime
reload(sys)
sys.setdefaultencoding('utf8')
#错误日志文件
logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
#DDC01上远程创建MCS桌面脚本
filename =[r"C:\mcs_script\createServerCatalog.bat",r"C:\mcs_script\createAppDesktopGroup.bat",r"C:\mcs_script\deleteAppDesktopGroup.bat",r"C:\mcs_script\deleteCatalog.bat"]
#定时生成MCS的时间：01:00
set_time = ['01:00','10:37']
#获取当前时间
now_date = datetime.datetime.now().strftime('%H:%M')
#远程控制DDC01登入
def call_remote_bat(ipaddress,username,password,file):
    try:
        #用wmi接口连接到远程ddc01
        conn = wmi.WMI(computer=ipaddress, user=username, password=password)
        #调用DDC脚本名称
        cmd_callbat=r"cmd /c call %s"%file
        conn.Win32_Process.Create(CommandLine=cmd_callbat)  #执行bat文件
        print "执行成功!"
        return True
    except Exception,e:
        log = open(logfile, 'a')
        log.write(('%s, call  Failed!\r\n') % ipaddress)
        log.close()
        return False
    return False

if __name__=='__main__':

    while True:
        if now_date in set_time:
            #到点开始删除交付组
            try:
                del_desktop_flag = call_remote_bat('172.25.1.8','lnxdjx\\xyadmin','1qaz@WSX',filename[3])
                print filename[0]
                # print  "删除MM交付组成功"
                #等待删除完毕
                # print '等待删除完毕'
                time.sleep(30)
            except Exception ,e:
                print e + "MM交付组不存在"
                with open ('logfile', 'a') as log:
                    log.write((' MM交付组不存在，请检查!\r\n') )
                    log.close()
            #      #删除交付组后开始删除交付目录
            #  if del_desktop_flag == True:
            #      try:
            #          del_catalog_flag = call_remote_bat('172.25.1.8', 'lnxdjx\\xyadmin', '1qaz@WSX', filename[2])
            #          print  "删除MM交付目录成功"
            #
            #      except Exception, e:
            #          print e + "MM交付组不存在"
            #          with open('logfile', 'a') as log:
            #              log.write((' MM交付组不存在，请检查 !\r\n'))
            #              log.close()
            #       #等待删除完毕
            #              print '等待删除完毕'
            #              time.sleep(30)
            #  #开始创建交付目录：
            # try:
            #     create_catalog_flag = call_remote_bat('172.25.1.8', 'lnxdjx\\xyadmin', '1qaz@WSX', filename[0])
            #     print  "创建mm交付目录成功"
            #
            # except Exception, e:
            #     print e + "mm交付目录已经存在"
            #     with open('logfile', 'a') as log:
            #         log.write((' MM交付组存在，请检查 !\r\n'))
            #         log.close()
            #         # 等待创建完毕
            #         print '创建完毕'
            #         time.sleep(30)
            # if  create_catalog_flag  == True:
            #     # 开始创建交付组：
            #     try:
            #         create_catalog_flag = call_remote_bat('172.25.1.8', 'lnxdjx\\xyadmin', '1qaz@WSX', filename[0])
            #         print  "创建mm交付组成功"
            #
            #     except Exception, e:
            #         print e + "mm交付组已经存在"
            #         with open('logfile', 'a') as log:
            #             log.write((' MM交付组存在，请检查 !\r\n'))
            #             log.close()
            #             # 等待创建完毕
            #             print '创建完毕'
            #
        print  '还未到执行时间，请等待'