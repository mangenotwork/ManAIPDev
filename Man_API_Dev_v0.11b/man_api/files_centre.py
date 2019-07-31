#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 


import os,sys
import zipfile
import tarfile
import shutil
import filecmp


#获取文件中心路径
Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


File_Centre_Path = Man_API_Path+"/File_storage_center/"

#print(File_Centre_Path)



#创建项目目录
def creat_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		return True
	else:
		return False


def creat_project_dir(project_name):
	path = File_Centre_Path+project_name
	master_path = path+"/Master"
	branch_path = path+"/Branch"
	release_path = path+"/Release"
	historyimage_path = path+"/Historyimage"
	backup_path = path+"/Backup"
	init_master_branch = path+"/Master/"+project_name+"-v0-0"

	if creat_dir(path) == True:
		if creat_dir(master_path) == True:
			if creat_dir(branch_path) == True:
				if creat_dir(release_path) == True:
					if creat_dir(historyimage_path) == True:
						if creat_dir(backup_path) == True:
							if creat_dir(init_master_branch) == True:
								return "creat complete."
							else:
								return "creat init_master_branch fail."
						else:
							return "creat Backup fail."
					else:
						return "creat Historyimage fail."
				else:
					return "creat Release fail."
			else:
				return "creat Branch fail."	
		else:
			return "creat Master fail."	
	else:
		return "creat main dir fail."


#print(creat_project_dir('test2'))

def get_main_path(project_name):
	path = File_Centre_Path+project_name
	if os.path.exists(path):
		return path
	else:
		return False


def get_master_path(project_name):
	path = File_Centre_Path+project_name+"/Master"
	if os.path.exists(path):
		return path
	else:
		return False




def get_branch_path(project_name):
	path = File_Centre_Path+project_name+"/Branch"
	if os.path.exists(path):
		return path
	else:
		return False

def get_release_path(project_name):
	path = File_Centre_Path+project_name+"/Release"
	if os.path.exists(path):
		return path
	else:
		return False


def get_historyimage_path(project_name):
	path = File_Centre_Path+project_name+"/Historyimage"
	if os.path.exists(path):
		return path
	else:
		return False

def get_backup_path(project_name):
	path = File_Centre_Path+project_name+"/Backup"
	if os.path.exists(path):
		return path
	else:
		return False





def get_dev_branch_path(project_name):
	dir_path = get_branch_path(project_name)
	for maindir, subdir, file_name_list in os.walk(dir_path):
		#print(subdir)
		return subdir,file_name_list


'''
print(get_master_path('test2'))
print(get_branch_path('test2'))
print(get_release_path('test1'))
print(get_historyimage_path('test2'))
print(get_backup_path('test2'))
'''


#获取所有目录
def get_all_project_dir():
	dir_path = File_Centre_Path
	for maindir, subdir, file_name_list in os.walk(dir_path):
		return subdir

#print(get_all_project_dir())





'''
	flask  上传文件功能

'''




#拷贝目录

def copytree_dir(source_dir,output_dir):
	try:
		shutil.copytree(source_dir, output_dir)
		return True
	except Exception as e:
		#raise e
		return False






#目录打包
def make_zip(source_dir, output_filename):
	try:
		zipf = zipfile.ZipFile(output_filename, 'w')
		pre_len = len(os.path.dirname(source_dir))
		for parent, dirnames, filenames in os.walk(source_dir):
			for filename in filenames:
				pathfile = os.path.join(parent, filename)
				arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
				zipf.write(pathfile, arcname)
		zipf.close()
		return True
	except Exception as e:
		#raise e
		return False


#删除一个目录
def del_dir_files(sourcepath):
	if os.path.exists(sourcepath) == True:
		#如果存在就删除
		#os.rmdir(file_dir)
		for root,dirs,files in os.walk(sourcepath):
			for file in files:
				print(os.path.join(root,file))
				try:
					os.rmdir(os.path.join(root,file))
				except:
					os.remove(os.path.join(root,file))
		os.rmdir(sourcepath)
		return True
	else:
		return False




#移动目录
def shift_dir_files(sourcepath,destination):
	shutil.move(sourcepath, destination)




#提交上传代码 并执行 部署操作
def commit_file(old_path,ext,projectname,base_path,file_path):
	file_dir = base_path+old_path
	#判断目录是否存在
	if os.path.exists(file_dir) == True:
		#如果存在就删除
		#os.rmdir(file_dir)
		for root,dirs,files in os.walk(file_dir):
			for file in files:
				print(os.path.join(root,file))
				try:
					os.rmdir(os.path.join(root,file))
				except:
					os.remove(os.path.join(root,file))
		os.rmdir(file_dir)		

		#删除后 解压上传文件
		if ext == "zip":
			z = zipfile.ZipFile(file_path, 'r')
			print(file_path)
			z.extractall(path=base_path+"/"+projectname)
			z.close()
			#解压完成后删除原始文件
			os.remove(file_path)
			return True
		elif ext == "tar":
			tar = tarfile.open(file_path, 'r')
			tar.extractall(path=base_path+"/"+projectname)
			tar.close()
			#解压完成后删除原始文件
			os.remove(file_path)
			return True
		else:
			z = zipfile.ZipFile(file_path, 'r')
			print(file_path)
			z.extractall(path=base_path+"/"+projectname)
			z.close()
			return True
	else:
		return False	




#两个目录文件对比差异 1
def contrast_file_difference1(main_dir,aim_dir):
	test=filecmp.dircmp(main_dir,aim_dir)
	print('显示左列表内容: '+str(test.left_list))
	print("显示两个目录共同的文件（文件名相同）: "+str(test.common_files))
	print("显示两个目录内文件名相同但是内容不同的文件 : "+str(test.diff_files))                   #显示两个目录内文件名相同但是内容不同的文件
	print("显示两个目录内子目录相同的目录名 : "+str(test.common_dirs))                 #显示两个目录内子目录相同的目录名
	print("显示两个目录名称相同的文件或者目录 : "+str(test.common))                #显示两个目录名称相同的文件或者目录
	print("显示只有左目录特有的文件: "+str(test.left_only))      #显示只有左目录特有的文件
	print("显示两个目录内文件名相同且内容相同的文件: "+str(test.same_files))                  #显示两个目录内文件名相同且内容相同的文件



#遍历目录所有文件
def get_all_files(main_path):
	all_file_list = []
	print(os.listdir(main_path))
	all_list = os.listdir(main_path)
	for i in range(0,len(all_list)):
		path = os.path.join(main_path,all_list[i])
		if os.path.isfile(path):
			all_file_list.append(all_list[i])
			#print(path)
			#print(all_list[i])
	print(all_file_list)
		

#两个目录文件对比差异 2
#分别把两个目录的所有文件获取在通过list set 等方法做对比
def contrast_file_difference2(main_dir,aim_dir):
	A_list = os.listdir(main_dir)
	B_list = os.listdir(aim_dir)
	
	print("listA对应listB的差集")
	print(set(A_list).difference(set(B_list)))

	print("\n\nlistB对应listA的差集")
	print(set(B_list).difference(set(A_list)))

	print("\n\nlistB对应listA取交集")
	print(set(A_list).intersection(set(B_list)))

	print("\n\nlistB对应listA的差集")
	print(set(A_list).union(set(B_list)))
	print("\n\n")

	#新增 newly
	newly_list = set(B_list).difference(set(A_list))
	#丢失lose file list
	lose_list = set(A_list).difference(set(B_list))
	return newly_list,lose_list

#统计代码行数


#统计文件总个数






'''

afile = r"C:\\Users\\Administrator\\Desktop\\Man_API_Dev_v0.10a\\File_storage_center\\flask1\\Master"
bfile = r"C:\\Users\\Administrator\\Desktop\\Man_API_Dev_v0.10a\\File_storage_center\\tttt\\Master"
c = r"C:\\Users\\Administrator\\Desktop\\Man_API_Dev_v0.10a\\File_storage_center\\man9\\Master"
d = r"C:\\Users\\Administrator\\Desktop\\Man_API_Dev_v0.10a\\static\\flask_templates"
#contrast_file_difference(afile,bfile)

#get_all_files(afile)
#get_all_files(bfile)

newly,lose = contrast_file_difference2(afile,bfile)

print(newly)
print(lose)

'''


'''
	flask  下载文件功能

'''




'''

		通过ftp servers 上传下载文件

'''


