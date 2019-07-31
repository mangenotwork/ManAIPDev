# -*- coding:utf8 -*-
#encoding = utf-8


from flask import Flask
from flask import Flask,request,g,render_template,redirect,url_for,abort,session
from flask import Blueprint , render_template

import pymysql
import time

def db_test():
	return "db init funtion"

DB_name = "habl_v1"
user_name = "root"
password = "lm123"

#是否要在 HTML 显示页上显示信息，
#True 要显示 （不能用于生产环境，非 json）， 
#False 不在html上返回 只返回数据信息（返回json用）
#HTML_DEBUG = True
HTML_DEBUG = False

# call funtion
def db_debug_call_funtion(func):
    def wrapper(*args, **kwargs):
        print("[Debug] Call funtion < "+func.__name__+" > .")
        return func(*args, **kwargs)
    return wrapper



class DB():
	@db_debug_call_funtion
	def __init__(self, db_host, db_port, db_name, user_acc, user_psd):
		#打印创建对象的时间,目的是后面性能判断
		print("[CREATE Obj Time] :"+str(time.time()))
		self.con = pymysql.connect(host=db_host,port=int(db_port),user=user_acc,passwd=user_psd,db=db_name)
		self.cursor = self.con.cursor()
		
	@db_debug_call_funtion
	def __del__(self):
		#当对象被销毁时 断开数据连接
		self.cursor.close()
		self.con.close()
		#当对象被销毁时，打印被销毁的时间，目的是后面性能判断
		print("[Del Obj Time] :"+str(time.time()))

	@db_debug_call_funtion
	def db_connect(self,db_host,db_port,db_name,user_acc,user_psd):
		try:
			pymysql.connect(host=db_host,port=db_port,user=user_acc,passwd=user_psd,db=db_name)
			return "connect succeed."
		except:
			return "connect failed."

	
	'''
			# db_init_user_table()
			# 创建用户数据表
	'''
	@db_debug_call_funtion
	def db_init_user_table(self):
		try:
			sql = """
				CREATE TABLE user_table(
			   		user_uuid INT AUTO_INCREMENT,
			   		user_ACC VARCHAR(15)  NOT NULL,
			   		user_password VARCHAR(15) NOT NULL,
			   		user_phone VARCHAR(11) NOT NULL default '0',
			   		user_registor_time DATETIME NOT NULL,
			   		PRIMARY KEY (user_uuid),
			   		UNIQUE (user_ACC)
				)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				"""
			self.cursor.execute(sql)
			self.con.commit()
			if(HTML_DEBUG):
				return "<h1>CREATE user_table ok!</h1><br>"
			else:
				return "CREATE user_table ok!"
		except Exception as e:
			if(HTML_DEBUG):
				error_info = "<h1>[DB Error] CREATE user_table fail</h1><br>"
				error=error_info + str(e)
				return error
			else:
				return e

	'''
			# execute_sql()
			# 执行sql
	'''	
	@db_debug_call_funtion
	def execute_sql(self,sql):
		try:
			self.cursor.execute(sql)
			self.con.commit()
			
			rest_data = self.cursor.fetchall()
			if(HTML_DEBUG):
				return "<h1>"+rest_data+"</h1><br>"
			else:
				return rest_data
		except Exception as e:
			self.con.rollback()
			if(HTML_DEBUG):
				error_sql = "<h1>[SQL Error] "+str(sql)+"</h1><br>"
				error=error_sql + str(e)
				return error
			else:
				return e
