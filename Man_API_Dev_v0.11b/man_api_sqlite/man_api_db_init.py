#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 


import os
import sys
import time
import sqlite3
Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
rootPath = Man_API_Path+'/man_api_sqlite'
os.chdir(rootPath)

man_api_user_conn = sqlite3.connect('man_api_user.db')
man_api_sys_conn = sqlite3.connect('man_api_sys.db')
man_api_project_conn = sqlite3.connect('man_api_project.db')


man_api_user_conn.close()
man_api_sys_conn.close()
man_api_project_conn.close()


class Man_API_Sqlite():
	def __init__(self,dbname):
		self.conn = sqlite3.connect(dbname)
		self.cursor = self.conn.cursor()
		self.class_name = self.__class__.__name__
		print(self.class_name+"启用")

	def set_table_init(self,create_table_sql):
		try:
			self.cursor.execute(create_table_sql)
			self.conn.commit()
			print("创建表成功")
			return "pass"
		except Exception as e:
			if "already exists" in str(e):
				print("表已存在")
				return "fail"

	#删除表
	def del_table(self,table_name):
		try:
			del_table_sql = "DROP TABLE "+table_name+";"
			self.cursor.execute(del_table_sql)
			self.conn.commit()
			print("Del Table Passed.")
			return "pass"
		except Exception as e:
			print("Del Table Failed.")
			return "fail"
		

	def get_all_table(self):
		get_table_names_sql = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""
		self.cursor.execute(get_table_names_sql)
		table_names = self.cursor.fetchall()
		for table_name in table_names:
			print("[Table name] : "+str(table_name))

	def get_table_structure(self,table_name):
		print("( Table Name = "+table_name+")")
		table_structure_sql = "PRAGMA  table_info('"+table_name+"');"
		self.cursor.execute(table_structure_sql)
		table_structure = self.cursor.fetchall()
		#print(table_structure)
		for i in table_structure:
			print(i)

	def execute_sql(self,sql_string):
		'''
		try:
			print("( SQL commend = "+sql_string+")")
			self.cursor.execute(sql_string)
			self.conn.commit()
			print("[Succeed] Execute SQL succeed.")
			return 'pass'
		except Exception as e:
			#raise e
			print("[Error] Execute SQL Fail.")
			return 'fail'
		'''
		print("( SQL commend = "+sql_string+")")
		self.cursor.execute(sql_string)
		self.conn.commit()
		print("[Succeed] Execute SQL succeed.")
		return 'pass'
	
	def select_sql(self,sql_string):
		'''
		try:
			print("( SQL commend = "+sql_string+")")
			self.cursor.execute(sql_string)
			select_data = self.cursor.fetchall()
			print("[Succeed] Execute SQL succeed.")
			return select_data
		except Exception as e:
			#raise e
			print("[Error] Execute SQL Fail.")
			return 'fail'
		'''
		print("( SQL commend = "+sql_string+")")
		self.cursor.execute(sql_string)
		select_data = self.cursor.fetchall()
		print("[Succeed] Execute SQL succeed.")
		return select_data

	def __del__(self):
		self.conn.close()
		print(self.class_name+"销毁")


#init
'''
user_DB = Man_API_Sqlite('man_api_user.db')
#user_DB.set_table_init(user_table_sql)
#user_DB.get_all_table()
#user_DB.get_table_structure('man_api_user_table')
#user_DB.del_table('man_api_user_table')
#user_DB.get_all_table()


#初始化 系统表
sys_DB = Man_API_Sqlite('man_api_sys.db')

sys_DB.set_table_init(user_access_table_sql)
sys_DB.set_table_init(user_department_table_sql)
sys_DB.set_table_init(user_group_table_sql)

#sys_DB.set_table_init(user_group_table_sql)
sys_DB.get_all_table()

sys_DB.del_table('access_table')
sys_DB.del_table('department_table')
#sys_DB.del_table('department_group_table')

#sys_DB.del_table('department_group_table')
#初始话 系统表数据

'''
#sys_DB.execute_sql()


def man_sys_db_ini():

	#初始化表
	man_api_init_table()
	
	#初始话数据

	#系统初始化用户权限
	sys_user_access_init_sql = ["INSERT INTO access_table (access_id,access_introduce,access_class) VALUES (1, 'root权限：用户增删改查,项目增删改查', 3);",
								"INSERT INTO access_table (access_id,access_introduce,access_class) VALUES (2, 'IT权限：用户改查,项目增删改查', 2);",
								"INSERT INTO access_table (access_id,access_introduce,access_class) VALUES (3, '运营权限：用户改查,项目查', 1);"]
	#系统初始化部门
	sys_user_department_init_sql = ["INSERT INTO department_table (department_id,department_name,department_introduce) VALUES (1, '研发', '研发部门，IT部门');",
									"INSERT INTO department_table (department_id,department_name,department_introduce) VALUES (2, '市场', '运营推广部门');",
									"INSERT INTO department_table (department_id,department_name,department_introduce) VALUES (3, '管理员', '系统管理员');"]
	#系统初始化部门
	sys_user_group_init_sql = ["INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (1, 1, '产品','产品');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (2, 1, '后台','后台开发');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (3, 1, '前端','前端开发');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (4, 1, 'ETL(DB)','数据开发');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (5, 1, '测试','测试');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (6, 1, '运维','运维');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (7, 2, '运营','市场运营');",
								"INSERT INTO group_table (group_id,department_id,group_name,group_introduce) VALUES (8, 3, '管理员','系统管理员');"]

	#查看系统表初始值
	sys_table_all_init_data_sql = ["SELECT access_id,access_introduce,access_class from access_table;",
									"SELECT department_id,department_name,department_introduce from department_table;",
									"SELECT group_id,department_id,group_name,group_introduce from group_table;"]

	root_user = "INSERT INTO man_api_user_table (user_uuid,user_name,user_password,user_department,user_group,user_employ,user_access) VALUES (1, 'man', '123456','管理员','管理员',1,3);"


	user_DB = Man_API_Sqlite('man_api_user.db')
	sys_DB = Man_API_Sqlite('man_api_sys.db')
	project_DB = Man_API_Sqlite('man_api_project.db')


	for access_init_sql in sys_user_access_init_sql:
		print(access_init_sql)
		sys_DB.execute_sql(access_init_sql)

	time.sleep(0.5)
	for department_init_sql in sys_user_department_init_sql:
		print(department_init_sql)
		sys_DB.execute_sql(department_init_sql)
	time.sleep(0.5)
	for group_init_sql in sys_user_group_init_sql:
		print(group_init_sql)
		sys_DB.execute_sql(group_init_sql)
	time.sleep(0.5)
	#查看所有增加数据
	for init_data_sql in sys_table_all_init_data_sql:
		print(init_data_sql)
		data_list = sys_DB.select_sql(init_data_sql)
		#print(data_list)
		for data in data_list:
			print(data)
	time.sleep(0.5)
	user_DB.execute_sql(root_user)

#man_sys_db_ini()


#初始化表
def man_api_init_table():
	#创建用户表
	user_table_sql = """
	CREATE TABLE man_api_user_table(
	   user_uuid INT PRIMARY KEY NOT NULL,/* 主键 用户唯一id */
	   user_name CHAR(10) NOT NULL,/* 用户名称 */
	   user_password CHAR(20) NOT NULL,/* 用户密码 */
	   user_department CHAR(20) NOT NULL,/* 用户部门 */
	   user_group CHAR(20) NOT NULL DEFAULT none,/* 用户组 */
	   user_employ INT NOT NULL DEFAULT 1,/* 用户是否启用 1启用默认 0不启用 */
	   user_head CHAR(35) NOT NULL DEFAULT 0,/* 用户头像静态图像路径 */
	   user_access INT NOT NULL DEFAULT 2/* 用户权限 3:增删改查 2:增改查 1:增查 0:查 */
	);
	"""

	#创建系统—用户权限表
	user_access_table_sql="""
	CREATE TABLE access_table(
	   access_id INT PRIMARY KEY NOT NULL,/* 主键 权限唯一id */
	   access_introduce CHAR(40) NOT NULL,/* 权限介绍 */
	   access_class INT NOT NULL/* 权限等级 */
	);
	"""

	#创建系统—部门表
	user_department_table_sql="""
	CREATE TABLE department_table(
	   department_id INT PRIMARY KEY NOT NULL,/* 主键 部门唯一id */
	   department_name CHAR(40) NOT NULL,/* 部门名称 */
	   department_introduce CHAR(40) NOT NULL/* 部门介绍 */
	);
	"""

	#创建系统—组表
	user_group_table_sql="""
	CREATE TABLE group_table(
	   group_id INT PRIMARY KEY NOT NULL,/* 主键 组唯一id */
	   department_id INT NOT NULL,/* 从属部门 */
	   group_name CHAR(40) NOT NULL,/* 组名称 */
	   group_introduce CHAR(40) NOT NULL/* group介绍 */
	);
	"""

	#项目信息表
	project_info_table_sql="""
	CREATE TABLE project_info_table(
	   project_uuid INT PRIMARY KEY NOT NULL,/* 主键 组唯一id */
	   project_name CHAR(30) NOT NULL,/* 项目名称 */
	   project_path CHAR(50) NOT NULL,/* 项目./ */
	   project_owner CHAR(10) NOT NULL,/* 项目创始人 */
	   project_access INT NOT NULL DEFAULT 1,/* 项目权限 默认公开  1：公开(可见可下载可协助开发)  0:私有(可见,不可下载,私有完成) 2:保密(完全对自己可见)*/
	   project_date TEXT NOT NULL/* 项目创始时间 */
	);
	"""

	#项目分支信息表
	project_branch_table_sql="""
	CREATE TABLE project_branch_table(
	   branch_uuid INT PRIMARY KEY NOT NULL,/* 主键 组唯一id */
	   project_uuid INT NOT NULL,/* 项目id */
	   project_name CHAR(30) NOT NULL,/* 项目名称 */
	   branch_name CHAR(30) NOT NULL,/* 分支名称./ */
	   branch_type CHAR(10) NOT NULL,/* 分支类型 */
	   parent_branch_name CHAR(30) NOT NULL,/* 父分支名称 */
	   branch_path CHAR(50) NOT NULL,/*分支存储路径*/
	   branch_date TEXT NOT NULL/* 分支创始时间 */
	);
	"""

	#项目操作空间状态表
	project_handle_table_sql="""
	CREATE TABLE project_handle_table(
	   project_uuid INT PRIMARY KEY NOT NULL,/* 主键 组唯一id */
	   project_name CHAR(30) NOT NULL,/* 项目名称 */
	   project_handle CHAR(30) NOT NULL,/* 项目当前的操作空间 */
	   handle_date TEXT NOT NULL,/* 上一次操作时间 */
	   handle_user CHAR(10) NOT NULL/* 上一次操作人员名称 */
	);
	"""

	#项目 上传更改  迭代更改权限表
	project_useraccess_table_sql="""
	CREATE TABLE project_useraccess_table(
	   project_uuid INT PRIMARY KEY NOT NULL,/* 主键 组唯一id */
	   project_name CHAR(30) NOT NULL,/* 项目名称 */
	   project_useraccess CHAR(10) NOT NULL/* 可以操作该项目的用户名 */
	);
	"""

	#分支关系表
	branch_relation_table_sql="""
	CREATE TABLE branch_relation_table(
	   relation_uuid INT PRIMARY KEY NOT NULL,/* 分支关系 组唯一id */
	   project_name CHAR(30) NOT NULL, /* 项目名称 */
	   begin_branch CHAR(30) NOT NULL,/* 起始点 */
	   finish_branch CHAR(30) NOT NULL/* 结束点 */
	);
	"""


	user_DB = Man_API_Sqlite('man_api_user.db')
	sys_DB = Man_API_Sqlite('man_api_sys.db')
	user_DB.set_table_init(user_table_sql)
	time.sleep(0.5)
	user_DB.get_all_table()
	sys_DB.set_table_init(user_access_table_sql)
	sys_DB.set_table_init(user_department_table_sql)
	sys_DB.set_table_init(user_group_table_sql)
	time.sleep(0.5)
	sys_DB.get_all_table()
	
	project_DB = Man_API_Sqlite('man_api_project.db')
	project_DB.set_table_init(project_info_table_sql)
	project_DB.set_table_init(project_branch_table_sql)
	project_DB.set_table_init(project_handle_table_sql)
	project_DB.set_table_init(project_useraccess_table_sql)
	project_DB.set_table_init(branch_relation_table_sql)
	time.sleep(0.5)
	project_DB.get_all_table()


#man_api_init_table()



def man_sys_db_reset():
	user_DB = Man_API_Sqlite('man_api_user.db')
	sys_DB = Man_API_Sqlite('man_api_sys.db')
	user_DB.del_table('man_api_user_table')
	sys_DB.del_table('access_table')
	sys_DB.del_table('department_table')
	sys_DB.del_table('department_group_table')
	man_sys_db_ini()


def get_root_user():
	user_DB = Man_API_Sqlite('man_api_user.db')
	sql_cmd = "SELECT * from man_api_user_table;"
	data_list = user_DB.select_sql(sql_cmd)
	for data in data_list:
		print(data)

#get_root_user()