# -*- ecoding:utf-8 -*-
#Function：
#Arthur:Timbaland
#version:1.0
#Date:2018-09-13

from gevent import monkey;monkey.patch_all()
import gevent
import os,wmi
import time
import subprocess
import re
ip_list = []
class IPV4(object):

    IPLIST = []
    def __init__(self,ippre):
        self.ippre = ippre

    def ping_call(self,num):
        fnull = open(os.devnull, 'w')
        ipaddr = self.ippre + str(num)
        result = subprocess.getstatusoutput('ping '+ ipaddr + ' -n 2')
        current_time = time.strftime('%Y%m%d-%H:%M:%S', time.localtime())
        ip_list = []

        if re.findall(r'请求超时。',result[1]) == ['请求超时。', '请求超时。']:
            # print('时间:{} ip地址:{} ping fail'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping fail'.format(current_time, ipaddr)

        else:
            print('时间:{} ip地址:{} ping ok'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping ok'.format(current_time, ipaddr)
            ip_list.append(ipaddr)
            return ip_list
        fnull.close()

    def asynchronous(self,ping_call): # 异步

        g_l = [gevent.spawn(ping_call, i) for i in range(1, 256)]

        gevent.joinall(g_l)

    # 远程控制win7登入
    def call_remote_bat(self,host):
        logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        try:
            # 用wmi连接到远程win7系统
            conn = wmi.WMI(computer='127.0.0.1', user='b309\\b309-005', password="Root@123")
            cmd1 = r"net use \\%s\ipc$ 123456 /user:administrator |  " % (host)
            cmd2 = r"shutdown -m \\%s -f -s -t  0" % (host)
            os.remove('c:\\app\shutdown.bat')
            with open('c:\\app\shutdown.bat', 'a') as f:
                f.write(cmd1)
                f.write(cmd2)
            filename = r"c:\app\shutdown.bat"
            cmd_callbat = r"cmd /c call %s" % filename
            conn.Win32_Process.Create(CommandLine=cmd_callbat)  # 执行bat文件
            print("执行成功!")

            print(cmd1)
            print(cmd2)

            return True
        except Exception as e:
            log = open(logfile, 'a')
            log.write(('%s %s call  Failed!\r\n') % (host, e))
            log.close()
            return False
if __name__ == '__main__':
    start_time = time.time()
    mask = '255.255.255.0'
    geteway = '192.168..46.254'
    dns = '88.88.88.88'
    p = IPV4('192.168.46.')
    p.asynchronous(p.ping_call)
    #获取IP集合
    print(p.ping_call(2))

    print('协程执行-->耗时{:.2f}'.format(time.time() - start_time))