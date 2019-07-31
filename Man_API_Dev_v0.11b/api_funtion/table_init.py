# -*- coding:utf8 -*-
#encoding = utf-8


import sys,os
#db方法
import db.db_init as dbinit
import debug
'''
#查看对象调用的哪个class 
def debug_call_class(obj):
	print("[Debug] Call class  "+str(obj.__class__)+" .")
'''
def init():
	#实例化 DB
	db = dbinit.DB()
	#查看 实例化的哪个类
	debug.debug_call_class(db)
	#执行创建用户表
	#init_db = db.db_init_user_table()
	#创建表的举例
	sql = """
		CREATE TABLE IF NOT EXISTS user_table(
			user_uuid INT AUTO_INCREMENT,
			user_ACC VARCHAR(15)  NOT NULL,
			user_password VARCHAR(15) NOT NULL,
			user_phone VARCHAR(11) NOT NULL default '0',
			user_registor_time DATETIME NOT NULL,
			PRIMARY KEY (user_uuid),
			UNIQUE (user_ACC)
		)ENGINE=InnoDB DEFAULT CHARSET=utf8;
		"""
	#用户表 < user_table >
	sql_user_table_init = """
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
	#角色表 <role_table>
	sql_role_table_init = """
		CREATE TABLE role_table(
			role_uuid INT AUTO_INCREMENT,
			role_name VARCHAR(12)  NOT NULL,
			role_sex INT NOT NULL,
			role_vocation VARCHAR(15) NOT NULL,
			role_plot VARCHAR(30) NOT NULL,
			role_site VARCHAR(25) NOT NULL,
			role_lv_number INT NOT NULL,
			role_avatar_imgpath VARCHAR(50) NOT NULL,
			role_now_hp INT NOT NULL,
			role_now_ep INT NOT NULL,
			role_xp INT NOT NULL,
			role_basics_id INT NOT NULL,
			role_talent_id INT NOT NULL,
			role_attribute_id INT NOT NULL,
			role_skill_id INT NOT NULL,
			role_equipment_id INT NOT NULL,
			role_task_id INT NOT NULL,
			role_create_time DATETIME NOT NULL,
			PRIMARY KEY (role_uuid),
			UNIQUE (role_name)
		)ENGINE=InnoDB DEFAULT CHARSET=utf8;

		"""
	#用户角色表 < user_role_list >



	init_db =db.execute_sql(sql_user_table_init)
	init_db_role_table = db.execute_sql(sql_role_table_init)
	return_init = "user_table :"+str(init_db)
	return_init += "<br>role_table :"+str(init_db_role_table)
	del db
	'''
	if(init_db):
		return str(init_db)
	else:
		return str(init_db)
	'''
	return return_init