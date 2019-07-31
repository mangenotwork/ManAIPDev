#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 

import os,sys
import shutil
try:
	import man_file
except:
	import man_api.man_file as man_file

#文件存储中心
import man_api.files_centre as filecentre
#

Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
project_list_ini_file = Man_API_Path+"/static/ini_file/project_list.ini"
project_state_ini_file = Man_API_Path+"/static/ini_file/project_state.ini"

#创建目录
def creation_dir(set_path):
	path=set_path.strip()
	path=path.rstrip("\\")
	isExists=os.path.exists(path)
	if not isExists:
		os.makedirs(path)
		print(path+' 创建成功')
		return True
	else:
		print(path+' 目录已存在')
		return False
#拷贝flask模板到新的flask 目录去
def copy_flask_templates(path, out):
    for files in os.listdir(path):
        name = os.path.join(path, files)
        back_name = os.path.join(out, files)
        if os.path.isfile(name):
            if os.path.isfile(back_name):
                if name != back_name:
                    shutil.copy(name,back_name)     
            else:
                shutil.copy(name, back_name)
        else:
            if not os.path.isdir(back_name):
                os.makedirs(back_name) 
            copy_flask_templates(name, back_name)


#创建新的 flask 应用
def create_flask(project_name,project_title,project_port,project_db):
	#创建
	filecentre.creat_project_dir(project_name)
	#project_name_path = Man_API_Path+"/project/"+project_name
	project_name_path = filecentre.get_master_path(project_name)+"/"+project_name
	creation_dir(project_name_path)
	A = Man_API_Path+"/static/flask_templates"
	#print(A)
	B = project_name_path
	copy_flask_templates(A,B)
	project_app_file = B+"/app.py"
	#文件操作
	file_handle =  man_file.Man_File_handle(project_app_file)
	
	#添加 project 信息
	file_handle.modif_file_line_data(13,"Project_Name = \""+project_name+"\"")
	file_handle.modif_file_line_data(14,"Project_Port = "+str(project_port))
	#在project 存储添加信息
	ini_file_handle = man_file.Ini_File_Man(project_list_ini_file)
	ini_file_handle.add_a_data(project_name,"name",project_name)
	ini_file_handle.add_a_data(project_name,"intro",project_title)
	ini_file_handle.add_a_data(project_name,"port",str(project_port))
	ini_file_handle.add_a_data(project_name,"db_name",project_db)
	#添加 project 状态
	#在project 状态 添加状态
	state_file = man_file.Ini_File_Man(project_state_ini_file)
	project_flask_name = project_name+"_flask"
	#state_file.add_section(project_flask_name)
	state_file.add_a_data(project_flask_name,"name",project_name)
	state_file.add_a_data(project_flask_name,"state","off")
	state_file.add_a_data(project_flask_name,"url","0.0.0.0:"+str(project_port))
	return 1

#create_flask("test3","This is test3 falsk.",9003,"test3")

#将 flask 信息写入 project_list.ini
def get_project_list_info():
	project_list_info = []
	list_info = []
	ini_file_handle = man_file.Ini_File_Man(project_list_ini_file)
	project_section = ini_file_handle.get_all_sections()
	for sect in project_section:
		#print(sect)
		project_item = ini_file_handle.get_section_option(sect)
		#print(project_item)
		for item_valu in project_item:
			#print(item_valu)
			get_data = ini_file_handle.get_section_item_value(sect,item_valu)
			list_info.append(get_data)
		project_list_info.append(list(list_info))
		list_info = []
		'''
		for item in project_item:
			print(item)
		'''
		#print(list(project_item))
		#print(project_item.__str__())
	#print(project_list_info)
	return project_list_info

#print(get_project_list_info())


#获取项目目录与文件
allfile = []
def get_all_file(dirname):
	
    result = []#所有的文件

    for maindir, subdir, file_name_list in os.walk(dirname):

        print("1:",maindir) #当前主目录
        print("2:",subdir) #当前主目录下的所有目录
        print("3:",file_name_list)  #当前主目录下的所有文件

        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)

    return result

#获取项目下一级目录与文件
def get_dir_list(branch,project_name,dirname):
	print(dirname)
	print(project_name)
	if branch == 'Master':
		dir_path = filecentre.get_master_path(project_name)+"/"+dirname
		print(dir_path)
		#dir_path = Man_API_Path+"/project/"+dirname
		for maindir, subdir, file_name_list in os.walk(dir_path):
			#print(subdir)
			return subdir,file_name_list


def get_main_dir_list(branch,project_name):
	print(branch)
	print(project_name)
	if branch == 'Master':
		dir_path = filecentre.get_master_path(project_name)
		print(dir_path)
		for maindir, subdir, file_name_list in os.walk(dir_path):
			#print(subdir)
			return subdir,file_name_list



#project_name_pathtest1 = Man_API_Path+"/project/test1"
#project_name_pathtest2 = Man_API_Path+"/project/test1/templates"
#get_dir_list(project_name_pathtest1)
#get_file_list(project_name_pathtest1)

#a,b = get_dir_list(project_name_pathtest2)
#print(a)
#print(b)

'''
for file_n in get_dir_list(project_name_path):
	print(file_n)
'''
