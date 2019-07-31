# -*- coding:utf8 -*-
#encoding = utf-8

import json
import os,sys
from string import Template


#add_json_data(api_id_val="aa1",api_name_val="aa",api_title_val="你好",api_info_list=["1","2"],api_type_val="POST",api_data_val="1")

JsonFile = "/static/json_file/api_data.json"

class Json_data():
	def __init__(self):
		self.path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
		self.json_file = self.path + JsonFile
		self.api_json_template = Template('{"api_id":"${api_id_key}","api_name":"${api_name_key}","api_title":"${api_title_key}",\
						"api_info":${api_info_list_key},"api_bk_color":"${api_bk_color_key}","api_type_bk_style":"${api_type_bk_style_key}",\
						"api_type_button_style":"${api_type_button_style_key}","api_type":"${api_type_key}","api_data":${api_data_key}}\n')
	
	# 私有  __write_data
	#末尾写入一行字符串
	# @datas 字符串
	def __write_data(self,datas):
		with open(self.json_file, 'a', encoding='utf-8') as json_file:
			json_file.write(datas)

	#	私有  __write_all
	#	对文件写入所有数据
	#	@ data_list : 要写入文件的所有内容   list
	def __write_all(self, data_list):
		with open(self.json_file, 'w+', encoding='utf-8') as json_file:
			for file_data in data_list:
				json_file.write(file_data)

	#	私有  __formatting_data
	#	对输入的数据格式化
	def __formatting_data(self, api_id_val, api_name_val, api_title_val, api_info_list, api_bk_color_val, api_type_bk_style_val,\
		api_type_button_style_val, api_type_val, api_data_val):
		input_json_data = self.api_json_template.substitute( api_id_key=str(api_id_val), api_name_key=str(api_name_val),\
				api_title_key=str(api_title_val), api_info_list_key=str(api_info_list), api_bk_color_key=str(api_bk_color_val),\
				api_type_bk_style_key=str(api_type_bk_style_val), api_type_button_style_key=str(api_type_button_style_val),\
				api_type_key=str(api_type_val), api_data_key=str(api_data_val))
		input_json_data = input_json_data.replace('\'', '\"')
		return input_json_data
		


	#检查 api_id 是否存在
	#@api_id_val   api id
	def judge_api_id(self, api_id_val):
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			for line in json_file:
				if '"api_id":"'+api_id_val+'"' in line:
					#print("have Api ID: "+api_id_val)
					return False
			else:
				return True

	#返回 api id 在第几行
	#@api_id_val   api id
	def get_api_line(self, api_id_val):
		data_cont = 0
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			for line in json_file:
				if'"api_id":"'+api_id_val+'"' in line:
					#print("have Api ID: "+api_id_val)
					return data_cont
				data_cont+=1
			else:
				return False

	#获取所有json 行数
	def get_api_all_line(self):
		data_cont = 0
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			for line in json_file:
				data_cont+=1
		return data_cont

	#检查 api_name 是否存在
	#@api_name_val   api name
	def judge_api_name(self, api_name_val):
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			for line in json_file:
				if '"api_name":"'+api_name_val+'"' in line:
					#print("have Api Name: "+api_name_val)
					return False
			else:
				return True

	#检查api 数据类型
	#@api_type_val   api type
	def judge_api_type(self, api_type_val):
		if api_type_val == 'GET' or api_type_val == 'get':
			api_bk_color_val = "#C1FFE4"
			api_type_bk_style_val = "success"
			api_type_button_style_val = "btn-success"
		elif api_type_val == 'POST' or api_type_val == 'post':
			api_bk_color_val = "#ACD6FF"
			api_type_bk_style_val = "info"
			api_type_button_style_val = "btn-info"
		else:
			return False
		return api_bk_color_val,api_type_bk_style_val,api_type_button_style_val

	#写入api 数据 到文件
	def add_json_data(self, api_id_val, api_name_val, api_title_val, api_info_list, api_type_val, api_data_val):
		if self.judge_api_id(api_id_val) == True and self.judge_api_name(api_name_val) == True:
			if self.judge_api_type(api_type_val) == False:
				return "API Type Error!"
			else:
				api_bk_color_val,api_type_bk_style_val,api_type_button_style_val = self.judge_api_type(api_type_val)
				input_json_data = self.__formatting_data(api_id_val, api_name_val, api_title_val, api_info_list, api_bk_color_val,\
									api_type_bk_style_val, api_type_button_style_val, api_type_val, api_data_val)
				self.__write_data(input_json_data)

	#获取所有json 数据 返回 list
	def get_all_json_data(self):
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			json_data_list = []
			for line in json_file:
				if(line != ""):
					json_data_list.append(line)
		return json_data_list

	#查看 api id
	#获取指定 api id 的数据
	def get_api_id_data(self, api_id_val):
		with open(self.json_file, 'r', encoding='UTF-8') as json_file:
			json_data_list = []
			for line in json_file:
				if '"api_id":"'+api_id_val+'"' in line:
					return json.loads(line)
		return False

	#修改json id
	def update_json_data(self, api_id_val, api_name_val='', api_title_val='', api_info_list='', api_type_val='', api_data_val=''):
		if self.judge_api_id(api_id_val) == False:
				#数据处理
				olad_json_data = self.get_api_id_data(api_id_val)
				if api_name_val == '':
					api_name_val = olad_json_data["api_name"]
				if api_title_val == '':
					api_title_val = olad_json_data["api_title"]
				if api_info_list == '':
					api_info_list = olad_json_data["api_info"]
				if api_type_val == '':
					api_type_val = olad_json_data["api_type"]
				if api_data_val == '':
					api_data_val = olad_json_data["api_data"]

				if self.judge_api_type(api_type_val) == False:
					return "API Type Error!"
				else:
					api_bk_color_val,api_type_bk_style_val,api_type_button_style_val = self.judge_api_type(api_type_val)
					input_json_data = self.__formatting_data(api_id_val, api_name_val, api_title_val, api_info_list, api_bk_color_val,\
									api_type_bk_style_val, api_type_button_style_val, api_type_val, api_data_val)
					all_json_data = self.get_all_json_data()
					update_json_line = self.get_api_line(api_id_val)
					if update_json_line != False:
						all_json_data[update_json_line] = input_json_data
						print("update_json Debug!")

						self.__write_all(all_json_data)
						return 1
		else:
			return "json data not find."

	#删除 api id
	def del_api(self, api_id_val):
		if self.judge_api_id(api_id_val) == False:
			all_json_data = self.get_all_json_data()
			api_line = self.get_api_line(api_id_val)
			if api_line != False:
				all_json_data.remove(all_json_data[api_line])
				self.__write_all(all_json_data)
				return 1
			else:
				return 0
		else:
			return 0




#json_file = Json_data()
#print(json_file.judge_api_id("aa2"))
#print(json_file.judge_api_type("GET"))
#json_file.update_json_data(api_id_val="aa3",api_name_val="cc",api_title_val="你好",api_info_list=["1","2"],api_type_val="POST",api_data_val="1")
#json_file.del_api(api_id_val="aa3")
#print(json_file.get_all_json_data("aa3"))
#print(json_file.get_all_json_data("aa3")["api_id"])
#print(json_file.get_all_json_data())
#print(json_file.get_api_all_line())




