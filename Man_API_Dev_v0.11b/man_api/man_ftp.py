#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 


import os
import sys
import time
from multiprocessing import Process

from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.handlers import FTPHandler 
from pyftpdlib.servers import FTPServer




def man_ftp_servers(ftp_port):
	authorizer = DummyAuthorizer()
	authorizer.add_user('user', '12345', 'C:\\Users\\Administrator\\Desktop\\files_\\file_storages', perm='elradfmwMT')
	# 实例化FTPHandler 
	handler = FTPHandler
	handler.authorizer = authorizer
	# 设定一个客户端链接时的标语
	handler.banner = "Welcome man ftp."
	handler.passive_ports = range(2000, 2333)
	address = ('192.168.2.122', ftp_port)#FTP一般使用21,20端口
	server = FTPServer(address, handler)
	server.max_cons = 256
	server.max_cons_per_ip = 5
	# 是否开启匿名访问 on|off
	ENABLE_ANONYMOUS = 'off'

	# 开启服务器 
	server.serve_forever()

'''
thread.start_new_thread( man_ftp_servers, ( 2121, ) )
thread.start_new_thread( man_ftp_servers, ( 2120, ) )
thread.start_new_thread( man_ftp_servers, ( 2122, ) )
'''
if __name__=='__main__':
	os.getpid()
	p = Process(target=man_ftp_servers, args=(2121,))
	p1 = Process(target=man_ftp_servers, args=(2120,))
	p.start()
	p1.start()
	p.join()
	p1.join()