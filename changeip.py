# -*- ecoding:utf-8 -*-
#Function：
#Arthur:Timbaland
#version:1.0
#Date:2018-09-13
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
        #1、无法访问目标主机 2、请求超时
        if re.findall(r'无法访问目标主机',result[1]) == [r'无法访问目标主机', r'无法访问目标主机'] or re.findall(r'请求超时',result[1]) == [ r'请求超时',r'请求超时']:
            # print('时间:{} ip地址:{} ping fail'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping fail'.format(current_time, ipaddr)

        else:
            print('时间:{} ip地址:{} ping ok'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping ok'.format(current_time, ipaddr)

            return ipaddr
        fnull.close()

    def asynchronous(self,ping_call): # 异步

        g_l = [gevent.spawn(ping_call, i) for i in range(1, 256)]

        gevent.joinall(g_l)

    # 远程控制win7登入
    def call_remote_bat(self,host,user,pwd,mask,gateway,dns):
        logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        try:
            # 用wmi连接到远程win7系统
            conn = wmi.WMI(computer=host, user=user, password=pwd)
            cmd_IP = 'netsh interface ip set address name="本地连接" source="static" addr="%s" mask="%s" gateway="%s" \n netsh interface ip set dns name="本地连接" source="static" addr="%s"'%(host,mask,gateway,dns)
            # cmd_dns= 'netsh interface ip set dns name="本地连接" source="static" addr="%s"'%(dns)
            conn.Win32_Process.Create(CommandLine=cmd_IP)  # CHANGE IP

            # conn.Win32_Process.Create(CommandLine=cmd_dns)  # CHANGE DNS
            print("修改IP\DNS成功!")

            return True
        except Exception as e:
            print(host+'机器已经关机')
            log = open(logfile, 'a')
            log.write(('%s %s call  Failed!\r\n') % (host, e))
            log.close()
            return False
        finally:
            print('continue')
if __name__ == '__main__':
    start_time = time.time()
    mask = '255.255.255.0'
    gateway = '192.168.0.222'
    dns = '202.96.128.86'
    #远程主机user
    user = 'administrator'
    # 远程主机密码
    pwd = '123'
    p = IPV4('192.168.0.')
    p.asynchronous(p.ping_call)
    #获取IP集合
    m_ip = []
    for ip in range(1,256):
        if p.ping_call(ip) is not None:
            m_ip.append(p.ping_call(ip))

    print(m_ip)
    # p.call_remote_bat(m_ip[0],user,pwd,mask,gateway,dns)

    print('协程执行-->耗时{:.2f}'.format(time.time() - start_time))