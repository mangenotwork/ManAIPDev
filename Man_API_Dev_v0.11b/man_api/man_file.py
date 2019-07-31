#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 


import os
import sys
import time
import json
import shutil
import configparser

class Man_File_handle():
	'''
			对文件操作的类;
			@ file_path : 文件路径；
	'''
	def __init__(self, file_path):
		self.file_path = file_path
	
	#	读取文件所有内容		
	def read_all_data(self):
		if self.examine_file() == True:
			file_all_data = []
			with open( self.file_path, 'r', encoding='utf-8') as file:
				for line in file:
					file_all_data.append(line)
			return file_all_data
		else:
			return self.examine_file()

	#	检查文件是否存在
	def examine_file(self):
		#return os.path.exists(self.file_path)
		if os.path.exists(self.file_path) == False:
			print("文件不存在")
			return "NotFile"
		else:
			return True


	#	写入文件
	#	@datas : 要写入文件的内容
	def write_one_data(self,datas):
		with open( self.file_path, 'a+', encoding='utf-8') as file:
			print(type(datas))
			input_data = str(datas)
			print(type(input_data))
			file.write(input_data+"\n")

	#	对文件写入所有数据
	#	@ data_list : 要写入文件的所有内容
	def write_file_all(self,data_list):
		with open( self.file_path, 'w+', encoding='utf-8') as file:
			for file_data in data_list:
				file.write(file_data)

	#	对文件写入所有数据
	#	@ data_list : 要写入文件的所有内容
	def write_file_all_data(self,datas):
		with open( self.file_path, 'w+', encoding='utf-8') as file:
				file.write(datas)

	#	文件添加一行内容		
	# 	@datas : 要写入文件的内容	
	def add_data(self,datas):
		with open( self.file_path, 'a+', encoding='utf-8') as file:
			input_data = str(datas)
			file.write(input_data+"\n")

	#	获取文件总行数
	def get_file_data_len(self):
		file_all_datas = self.read_all_data()
		if file_all_datas != 'NotFile':
			print(len(file_all_datas))
			return len(file_all_datas)

	#	读取文件指定行数
	# 	@len_number : 指定行数
	def get_file_line_data(self,len_number):
		data_cont = 0
		with open( self.file_path, 'r', encoding='utf-8') as file:
			for line in file:
				if(data_cont == (len_number-1)):
					print(data_cont)
					#print(str(line).encode('gb2312'))
					print(type(line))
					return line
					break
				data_cont+=1
			else:
				print("not find file len Min = 1 ; Max = "+str(data_cont))

	#	修改指定行内容
	# 	@len_number : 指定行数
	# 	@datas : 要写入文件的内容	
	def modif_file_line_data(self,len_number,datas):
		input_data = str(datas)
		input_data = input_data.replace("\'","\"")
		file_all_datas = self.read_all_data()
		if file_all_datas != 'NotFile':
			#修改方法
			file_all_datas[(len_number-1)] = input_data+"\n"
			with open( self.file_path, 'w+', encoding='utf-8') as file:
				for file_data in file_all_datas:
					file.write(file_data)

	#在指定行插入内容
	def add_file_line_data(self,len_number,datas):
		input_data = str(datas)
		input_data = input_data.replace("\'","\"")
		file_all_datas = self.read_all_data()
		if file_all_datas != 'NotFile':
			#插入方法
			file_all_datas.insert( (len_number-1), input_data+"\n")
			self.write_file_all(file_all_datas)

	#删除指定行
	def del_dile_line_data(self,len_number):
		file_all_datas = self.read_all_data()
		if file_all_datas != 'NotFile':
			#删除方法
			del file_all_datas[(len_number-1)]
			self.write_file_all(file_all_datas)

	#清楚空，回车，空格，
	def clear_empty(self):
		file_all_datas = self.read_all_data()
		if file_all_datas != 'NotFile':
			#print(file_all_datas)
			file_all_datas = [x for x in file_all_datas if x != '\n' and x != '']
			#删除 存在多个空格的情况
			kongge = " "
			kongge_number = 0
			while kongge_number < 10:
				str_pipei = kongge * kongge_number + "\n"
				if str_pipei in file_all_datas:
					file_all_datas.remove(str_pipei)
				else:
					kongge_number += 1	
			self.write_file_all(file_all_datas)
	
	#寻找内容在第几行,并返回
	def find_str_coordinate(self,datas):
		find_info = []
		rest = []
		data_cont = 1
		with open( self.file_path, 'r', encoding='utf-8') as file:
			for line in file:
				#line.encoding='gbk'
				if(datas in line):
					find_info.append(data_cont)
					rest.append(line)
				data_cont+=1
		if len(find_info) > 0:
			dic_rest = dict(map(lambda x,y:[x,y],find_info,rest))
			return dic_rest
		else:
			print("not find "+str(datas)+" from file.")
	
	#获取文件属性
	def get_file_attribute_list(self):
		if self.examine_file() == True:
			'''
			st_mode: inode 保护模式
				-File mode: file type and file mode bits (permissions).
			st_ino: inode 节点号。
				-Platform dependent, but if non-zero, uniquely identifies the file for a given value of st_dev.
				——the inode number on Unix,
				——the file index on Windows
			st_dev: inode 驻留的设备。
				-Identifier of the device on which this file resides.
			st_nlink:inode 的链接数。
				-Number of hard links.
			st_uid: 所有者的用户ID。
				-User identifier of the file owner.
			st_gid: 所有者的组ID。
				-Group identifier of the file owner.
			st_size:普通文件以字节为单位的大小；包含等待某些特殊文件的数据。
				-Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte.
			st_atime: 上次访问的时间。
				-Time of most recent access expressed in seconds.
			st_mtime: 最后一次修改的时间。
				-Time of most recent content modification expressed in seconds.
			st_ctime:由操作系统报告的"ctime"。在某些系统上（如Unix）是最新的元数据更改的时间，在其它系统上（如Windows）是创建时间（详细信息参见平台的文档）。
			st_atime_ns
				-Time of most recent access expressed in nanoseconds as an integer
			st_mtime_ns
				-Time of most recent content modification expressed in nanoseconds as an integer.
			st_ctime_ns
				-Platform dependent:
					——the time of most recent metadata change on Unix,
					——the time of creation on Windows, expressed in nanoseconds as an integer.
			--------------------- 
			'''
			attribute_list = os.stat(self.file_path)
			print(attribute_list)
			# 查看文件的修改时间
			file_modif_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(attribute_list.st_mtime))
			print("文件的修改时间 : "+file_modif_time)
			# 查看文件的上次访问时间
			file_access_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(attribute_list.st_atime))
			print("文件的上次访问时间 : "+file_access_time)
			# 文件大小
			file_size = attribute_list.st_size/1024
			print("文件大小 : "+str(file_size)+"KB")
			file_attribute_rest = {"file_size":file_size,"file_modif_time":file_modif_time,"file_access_time":file_access_time}
			return file_attribute_rest

	#获取文件所在目录
	def get_file_dir(self):
		#print(os.path.abspath(self.file_path))
		#print(os.path.dirname(os.path.abspath(self.file_path)))
		return os.path.dirname(os.path.abspath(self.file_path))

	#复制文件
	def copy_file(self, targetDir):
		if self.examine_file() == True:
			input_file = str(self.get_file_dir())
			targetDir_list = targetDir.split("/")
			#如果目录存在这个文件 则从命名
			if targetDir_list == input_file.split("\\"):
				#print(targetDir+" have file")
				file_new_name = self.file_path.split(".")[0]+"_mancopy."+self.file_path.split(".")[1]
				print(file_new_name)
				shutil.copy(self.file_path, file_new_name)
			else:
				#print("copy file")
				shutil.copy(self.file_path, targetDir)
			
	#删除文件
	def del_file(self):
		if self.examine_file() == True:
			os.remove(self.file_path)

	#移动文件
	def move_file(self,dstfile):
		if self.examine_file() == True:
			input_file = str(self.get_file_dir())
			dstfile_list = dstfile.split("/")
			if dstfile_list == input_file.split("\\"):
				pass
			else:
				shutil.move(self.file_path,dstfile)

	


class Json_File_Man(Man_File_handle):
	"""
	    Json 文件 增删改查
		继承 Man_File_handle
	"""
	def __init__(self, file_path):
		#先继承，再构造
		#继承父类的构造方法
		Man_File_handle.__init__(self, file_path)

	def class_name(self):
		print("Json_File_Man --> Man_File_handle.")
	
	#增
	def add_json_data(self,datas):
		if self.examine_file() == True:
			with open( self.file_path, 'a+', encoding='utf-8') as file:
				input_data = str(datas)
				#过滤处理  处理 '\n'
				input_data = input_data.replace("\n","")
				#如果是第一个字符没有 { 最后一个字符没有 } 则加上
				if input_data[0] != '{':
					input_data = '{' + input_data
				if input_data[-1] != '}':
					input_data = input_data + '}'
				# 有与 json 字符串不支持 ' 则改为 "
				input_data = input_data.replace("\'","\"")
				#print(type(input_data))
				file.write(input_data+"\n")

	#删
	def del_json_data(self,datas):
		print('del_json_data')
		if self.examine_file() == True:
			pass

	#改
	def update_json_data(self,datas):
		print('update_json_data')
		if self.examine_file() == True:
			pass

	#查
	def select_json_data(self,datas):
		print('select_json_data')
		if self.examine_file() == True:
			pass


class Ini_File_Man(Man_File_handle):
	"""
	    ini 文件 增删改查
		继承 Man_File_handle
	"""
	def __init__(self, file_path, cfg_debug=False ):
		Man_File_handle.__init__(self, file_path)
		#super(Man_File_handle, self).__init__()
		#self.file_path = file_path
		self.config = configparser.ConfigParser()
		#开启 debug模式
		self.cfg_debug = cfg_debug
		#__read_ini_file #__init__()  无法返回值，能不规避报错，所有写成方法 __read_ini_file()

	#读取 ini 文件  
	def __read_ini_file(self):
		if self.examine_file() == True:
			try:
				self.config.read(self.file_path)
			except Exception as e:
				if self.cfg_debug == True:
					print(e)
				else:
					pass
	
	#input ini 文件 提交操作
	def __submit_operation(self):
		self.config.write(open(self.file_path, "w"))

	def class_name(self):
		print("Ini_File_Man --> Man_File_handle.")

	#获取所有的 sections
	def get_all_sections(self):
		self.__read_ini_file()
		lists_header = self.config.sections()
		return lists_header

	#获取默认值 的所有信息
	def get_default_data(self):
		self.__read_ini_file()
		return self.config.defaults()

	#获取 指定 section item 的值
	def get_section_item_value(self, section, item): 
		self.__read_ini_file()
		try:
			value = self.config.get(section, item) 
			return value
		except Exception as e:
			print("repetition data")
		

	#获取 指定 section 所有 item 
	#返回列表
	def get_section_item(self, section):
		self.__read_ini_file()
		item_list = []
		for item in self.config[section]:
			#print(item)
			item_list.append(item)
		return item_list

	#获取节section点下所有option的key，包括默认option
	def get_section_option(self, section):
		self.__read_ini_file()
		return self.config.options(section)

	#获取取节section点下所有信息
	#输出元组，包括option的key和value
	def get_section_all(self, section):
		self.__read_ini_file()
		return self.config.items(section)

	#判断 section 是否存在  存在 True  不存在 False
	def judge_section(self, section):
		self.__read_ini_file()
		return section in self.config

	#判断 是否存在指定节的选项
	def judge_option(self, section, option):
		self.__read_ini_file()
		boolean = self.config.has_option(section, option)
		return boolean

	#增  分组
	def add_section(self, section):
		self.__read_ini_file()
		self.config.add_section(section)
		self.__submit_operation()

	#增  分组和内容  要判断 如果 option 内容存在则不添加
	def add_a_data(self, section, option, datas):
		self.__read_ini_file()
		if self.judge_section(section) == True:
			pass
		elif self.judge_section(section) == False:
			self.config.add_section(section)
		if self.judge_option(section,option) == False:
			self.config.set(section, option, datas)
			self.__submit_operation()
		elif self.judge_option(section,option) == True:
			print("[Warning] : already exist!")
		else:
			print("[Warning] : unusual!")
			

	#删 section
	def del_section(self, section):
		self.__read_ini_file()
		self.config.remove_section(section)
		self.__submit_operation()

	#删 del_option
	def del_option(self, section, option):
		self.__read_ini_file()
		self.config.remove_option(section,option)
		self.__submit_operation()

	#改
	def update_init_data(self, section, option, datas):
		self.__read_ini_file()
		if self.judge_section(section) == True:
			if self.judge_option(section,option) == True:
				self.config.set(section, option, datas)
				self.__submit_operation()
			elif self.judge_option(section,option) == False:
				print("[Warning] : Not Find "+str(option))
			else:
				print("[Warning] : unusual!")
		elif self.judge_section(section) == False:
			print("[Warning] : Not Find "+str(section))
		

	#查
	def select_init_data(self, datas):
		print('select_init_data')


	'''	
			 # has_section(section)  # 是否存在该节
			 boolean = config.has_section("mysql")
			
			boolean = config.has_option("mysql", "ip")  # 是否存在指定节的选项

			configparser.MAX_INTERPOLATION_DEPTH  # 使用默认插值时,  当raw=false，get()递归插值的最大深度
 
     		config.clear()  # 所有节都包含'DEFAULT'值,对节的清空不会删除'DEFAULT'值
     		config.BOOLEAN_STATES.update({'enabled': True, 'disabled': False})  # 自定义boolean的判断
     		config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")  # 自定义节头的编译与解析的正则表达式(去除左右空格)

     		config.read_file(open('config.ini', encoding="utf-8-sig"))
    		# read_string(string, source='<string>')  # 从字符串解析配置数据
    		config.read_string(config_str)
     		# read_dict(dictionary, source='<dict>')  # 读取字典
     		config.read_dict({'section1': {'key1': 'value1',
                                    'key2': 'value2'},
                       'section2': {'key3': 'value3',
                                   'key4': 'value4'}
     })
	'''


a_file_path = "D:/py_test/yibiao_Auto/unitys/test_json1.json"
b_test = "D:/py_test/yibiao_Auto/logs/test_logs_20190402101742.log"
c_test = 'D:/py_test/yibiao_Auto/unitys/test_json1_mancopy_mancopy.json'
ini_test = 'D:/py_test/yibiao_Auto/unitys/test.ini'

file = "D:/py_test/yibiao_Auto/unitys/test_json.json"
f = Man_File_handle(file)
json = 	Json_File_Man(a_file_path)
ini = Ini_File_Man(ini_test)
#print(json.examine_file())
#print("\n\nclass Man_File_handle:")
#print(dir(f))
#print("\n\nclass Json_File_Man:")
#print(dir(json))
#print("\n\nclass Ini_File_Man:")
#print(dir(ini))


#print(json.read_all_data())

test_datas = """"你好": "2\n","1":'3'"""

#json.add_json_data(test_datas)
#json.del_json_data(test_datas)
#json.update_json_data(test_datas)
#json.select_json_data(test_datas)

#ini.add_init_data(test_datas)
#ini.del_init_data(test_datas)
#ini.update_init_data(test_datas)
#ini.select_init_data(test_datas)

#f.add_data('a')
#json.add_file_data(test_datas)
#a = json.read_json_data()

#print(a)
#json.get_file_data_len()
#json.get_file_line_data(11)
#json.add_file_line_data(20,"asd")
#json.del_dile_line_data(2)
#json.modif_file_line_data(1,{"你好": 1})
#json.modif_file_line_data1(1,{"你好": 1})
#json.get_file_data_len()
#json.clear_empty()
#a = json.find_str_coordinate('a')
#print(a)
#json.class_name()
#ini.class_name()
#print(ini.read_all_data())
#ini.copy_file('D:/py_test/yibiao_Auto/unitys')
#b = ini.find_str_coordinate('a')
#print(b)
#print(json.get_file_attribute_list())
#ini.move_file('D:/py_test/yibiao_Auto')

#print(ini.read_all_data())
#print(ini.get_section_item_value('aa','a1'))
#print(ini.judge_option('aa','a1'))
#print(ini.get_all_sections())
#print(ini.get_default_data())
#print(ini.get_section_item("default"))

#ini.get_section_item("default")
#print(ini.get_section_option("default"))
#print(ini.get_section_all("default"))
#print(ini.judge_section("default1"))
#ini.del_section("A")
#ini.del_option("default","compressionlevel")

#ini.add_section("aa")
#ini.add_a_data("ca",'a3','bbb')
#ini.update_init_data("ca",'a3','bb11111')
#print(ini.get_all_dic())

