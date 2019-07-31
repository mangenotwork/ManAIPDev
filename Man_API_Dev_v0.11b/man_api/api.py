# -*- coding:utf8 -*-
#encoding = utf-8

import man_api_sqlite.man_api_db_init as man_sys_db

from flask import Flask
from flask import Flask,request,g,render_template,redirect,url_for,abort,session,jsonify,current_app

from flask import make_response,Response 
from flask import Blueprint , render_template

import sys,os,time
import json

#db 方法
import db.db_init as dbinit
import man_api.add_project as addproject
import redis
import man_api.cmd as apicmd

import man_api.man_file as man_file

from cryptography.fernet import Fernet

#md5
import hashlib

api = Blueprint('api',__name__)


Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

man_redis = redis.Redis(host='127.0.0.1', port=6379)

#json 文件 增删改查
import man_api.json_data as json_data
json_file = json_data.Json_data()

#文件存储中心
import man_api.files_centre as filecentre

#文件上传下载
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['rar', 'zip','7z'])


from werkzeug.utils import secure_filename

#字符串 模板
from string import Template



'''
	两种请求值的获取
@app.route("/login",methods = ['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print username
        print password
        return u'POST'+'+'+username+'+'+password
    if request.method == "GET":
        print 'call get now'
 
        username = request.args.get('username')
        password = request.args.get('password')
        print username
        print password
        return  username

'''


'''
		function : man_token_create(strings)
		@strings 字符串
		描述： 生成 token 加密 密文
		Return : 
'''
def man_token_create(strings):
	key = Fernet.generate_key()
	#print(key)
	man_token_string = Fernet(key)
	set_b = bytes(strings, encoding = "utf8")
	token_string_b = man_token_string.encrypt(set_b)
	keys = str(key, encoding = "utf8")
	return str(token_string_b, encoding = "utf8"),keys


'''		
		function : man_token_decode(strings,key)
		@strings : 密文
		@key : 秘钥
		#解密 token 解密成明文
'''
def man_token_decode(strings,key):
	#print(key)
	key_s = bytes(key, encoding = "utf8")
	man_token_string = Fernet(key_s)
	set_s = bytes(strings, encoding = "utf8")
	token_string_s = man_token_string.decrypt(set_s)
	return token_string_s

'''		
		function : man_token_decode2(strings,key)
		@strings : 密文
		@key : 秘钥 b''
		#解密 token 解密成明文
'''
def man_token_decode2(strings,key_b):
	#print(key)
	key_s = key_b
	man_token_string = Fernet(key_s)
	set_s = bytes(strings, encoding = "utf8")
	token_string_s = man_token_string.decrypt(set_s)
	return str(token_string_s, encoding = "utf8")


'''		
		function : man_token_decode2(strings,key)
		@strings : 密文
		@key : 秘钥 b''
		#解密 token 解密成明文
'''
def man_token_decode3(strings,key_b):
	#print(key)
	key_s = key_b
	man_token_string = Fernet(key_s)
	set_s = bytes(strings, encoding = "utf8")
	token_string_s = man_token_string.decrypt(set_s)
	return token_string_s


#用户认证 如果为登陆跳转到登陆界面
# 这个是一个用户认证的装饰器
# 每次用户访问则解密 Token 匹配用户是否是存在 session 里的 Token 的用户
# 如果不是用户则 退到登陆界面
# 如果是改用户则重新颁发 加密Token,并存入秘钥到 redis
# 这里这个认证功能会 影响一些速度，但是保证了访问安全
def Authentication(func=None, param=None):
	def deco(func):
		def wrapper(*args,**kwargs):
			#获取客户端 token
			name=request.cookies.get('man_user_token')
			if name != None:
				print("[Cookies] = "+name)
			#获取 session 存储的 session
			keys = session.get('token')

			#如果其中存在丢失则判定为用户过期则重新登陆
			if keys == None or name == None:
				return render_template('index.html')
			else:
				#token 验证，验证失败则登陆，验证成功则重新颁发 token
				if name[0:98] == keys[0:98]:
					name_tokens = name[0:98]+"=="
					#获取用户name
					#如果用户name是在线 重新颁发 tokens
					print(name_tokens)
					print("[man_token_userkey] = "+str(man_redis.get(name_tokens)))
					print(man_token_decode2(name_tokens,man_redis.get(name_tokens)))
					get_user_names = man_token_decode2(name_tokens,man_redis.get(name_tokens))
					if man_redis.get(get_user_names) == b'use':
						#重新颁发 token
						man_token_username,man_token_userkey=man_token_create(get_user_names)
						#保存新的 token 到 redis
						man_redis.set(man_token_username, man_token_userkey,ex=3600)
						#删除旧的session 存入新的session
						session.pop('token')
						session['token'] = man_token_username
						resp = make_response()
						resp.status_code = 200
						#返回新的 cookie 保存 token
						resp.set_cookie('man_user_token',man_token_username,max_age=3600)
						resp.response = func(user_name = get_user_names,*args,**kwargs)
						return resp
					else:
						return render_template('index.html')
				else:
					return render_template('index.html')
		wrapper.__name__ = func.__name__
		return wrapper
	return deco if not func else deco(func)



# 登陆界面
@api.route('/', methods=['POST','GET'])
def man_api_login():
	'''
	if 'User' in session:
		print(session['User'])
		return render_template('man_api_home.html')
	else:
	'''
	#获取 ip

	ip = request.remote_addr
	print(ip)
	resp = make_response()
	resp.status_code = 200
	resp.headers['content-type']='text/html'
	resp.response = render_template('index.html')
	print("[Login_user] = "+str(man_redis.get('man')))
	name=request.cookies.get('man_user_token')
	print("[Get Cookies] = "+str(name))
	keys = session.get('token')
	if keys == None or name == None:
		return resp
	else:
		if name[0:98] == keys[0:98]:
			return render_template('man_api_home.html')
		else:
			return resp
	

#退出登陆
@api.route('/login_quit',methods=['POST','GET'])
def login_quit():
	name=request.cookies.get('man_user_token')
	#获取 session 存储的 session
	keys = session.get('token')
	if keys != None and name != None:
		if name[0:98] == keys[0:98]:
			name_tokens = name[0:98]+"=="
			get_user_names = man_token_decode2(name_tokens,man_redis.get(name_tokens))
			man_redis.get(get_user_names)
			print("[get_user_names] = "+str(get_user_names))
			print(man_redis.get(get_user_names))
			man_redis.delete(get_user_names)
			resp = make_response()
			resp.status_code = 200
			resp.delete_cookie('man_user_token')
			resp.response = render_template('index.html')
			return resp
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')
	'''
	login_user_session = man_redis.get('man')
	print(man_redis.get('man'))
	man_redis.delete('man')
	resp=make_response()
	resp.delete_cookie('man_user_token')
	resp.response = str(login_user_session)
	return resp
	'''

#获取当前用户
@api.route('/getusername',methods=['POST','GET'])
def get_user_name():
	name=request.cookies.get('man_user_token')
	if name != None:
		name_tokens = name[0:98]+"=="
		get_user_names = man_token_decode2(name_tokens,man_redis.get(name_tokens))
		return json.dumps(get_user_names)
	else:
		return json.dumps("login_timeout")


# man api home
@api.route('/home',methods=['POST','GET'])
@Authentication
def home(user_name):
	'''
	print("[Login_user] = "+str(man_redis.get('man')))
	name=request.cookies.get('man_user_token')
	keys = session.get('token')
	print(keys)
	#return keys

	if keys == None or name == None:
		return render_template('index.html')
	else:
		if name[0:98] == keys[0:98]:
			return render_template('man_api_home.html')
		else:
			render_template('index.html')
	'''
	all_project_numbers = get_all_project_number()
	all_user_numbers = get_all_user_number()
	return render_template('man_api_home.html',all_project_number = all_project_numbers,all_user_number = all_user_numbers)


# 部门组管理
@api.route('/man_dg_manage', methods=['POST','GET'])
@Authentication
def man_dg_manage_show(user_name):
	return render_template('dg_manage.html')


# API 主界面	
@api.route('/api_show', methods=['POST','GET'])
def api_show():
    api_data_list = []
    api_number = 0
    while api_number < json_file.get_api_all_line():
        api_data_info = json_file.get_all_json_data()[api_number]
        #print(api_data_info)
        if(api_data_info != ""):
            api_data_list.append(json.loads(api_data_info))
        api_number+=1
    '''
    register={
            'api_id':'register',
            'api_name':'register',
            'api_title':'账号注册',
            'api_info':["user_ACC : 账号 （1.长度5~15，2.账号密码都不能为中文和特殊字符）",
            			"user_password : 密码 （1.长度5~15）",
            			"user_password_1 : 确认密码 （1.确认密码 = 密码）",
            			"user_phone : 手机号码  （可以为空，默认值 0）"
            			],
            'api_bk_color':"#ACD6FF",
            'api_type_bk_style':'info',#get -> success  post -> info
            'api_type_button_style':'btn-info',# get -> btn-success post -> btn-info
            'api_type':'POST',
            'api_data':["user_ACC","user_password","user_password_1","user_phone"]
        }
    '''
    return render_template('api_show.html',api_data_list = api_data_list)


# API 主界面	
@api.route('/api_conn_db', methods=['POST','GET'])
def conn_db():

	session.permanent=True  #默认session的时间持续31天

	print("[debug] call bark conn_db()")
	
	if request.method == "POST":
		host = request.form.get('host_data')
		port = request.form.get('port_data')
		db_name = request.form.get('db_name_data')
		acc = request.form.get('acc_data')
		password = request.form.get('password_data')
	return_rest = "host:"+str(host)+",port:"+str(port)+",db_name:"+str(db_name)\
	+",acc:"+str(acc)+",password:"+str(password)
	print(return_rest)
	#try:
	db = dbinit.DB(host,port,db_name,acc,password)
	session['db_conn_user_name'] = acc
	session['db_conn_password'] = password
	session['db_conn_host'] = host
	session['db_conn_port'] = port
	session['db_conn_db_name'] = db_name
	rest_info = 'db connect succeed.'
	'''
	except Exception as e:
		rest_info = str(e)
	'''
	print(rest_info)
	return json.dumps(rest_info)
	
	#return "/api_conn_db"

#api 管理界面
@api.route('/man_api_manage', methods=['POST','GET'])
@Authentication
def man_api_Manage(user_name):
	all_project_list = addproject.get_project_list_info()
	print(all_project_list)
	return render_template('manage_home.html',all_project_list=all_project_list)



#获取 api 数据库连接 session
@api.route('/get_db_conn_user')
def get_dbconn_username():
	print("[debug] call bark get_dbconn_username()")
	rest_data = session.get('db_conn_user_name')
	return json.dumps(rest_data)

#删除 api 数据库连接 session


#清楚 api 数据库连接 session




#进入数据库数据库操作界面
@api.route('/db_doing')
@Authentication
def goto_db_doing(user_name):
	print("[debug] call bark goto_db_doing()")
	
	return render_template('db_home.html')

#查看数据数据库所有表
@api.route('/show_table')
def show_tables():
	db_session_host = session.get('db_conn_host')
	db_session_port = session.get('db_conn_port')
	db_session_dbname = session.get('db_conn_db_name')
	db_session_username = session.get('db_conn_user_name')
	db_session_password = session.get('db_conn_password')

	db = dbinit.DB(db_session_host,int(db_session_port),db_session_dbname,db_session_username,db_session_password)
	sql = "SHOW TABLES;"
	table_list = db.execute_sql(sql)
	print("[debug] call bark goto_db_doing()")
	print("table_list : ")
	print(table_list[0])
	return json.dumps(table_list)


#查看表的字段信息
@api.route('/show_table_info')
def show_table_infos():
	pass


#查看表所有数据
@api.route('/show_table_all_data')
def show_table_all_datas():
	pass

#创建flask 项目
@api.route('/add_project', methods=['POST','GET'])
def add_project():
	if request.method == "POST":
		datax = request.form.to_dict()
		content = str(datax)
	project_name = datax["project_name"]
	project_title = datax["project_title"]
	project_port = datax["project_port"]
	project_db = datax["project_db"]
	user = datax["flask_user_name"]
	if addproject.create_flask(project_name,project_title,project_port,project_db) == 1:
		#将信息传入数据库中
		uuid_md5 = hashlib.md5()   
		uuid_md5.update((user+project_name).encode("utf-8"))
		project_uuid = uuid_md5.hexdigest()
		project_owner = user
		project_access = datax["flask_project_acc"]
		project_path = project_name
		project_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		#将信息写入数据库
		project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
		creat_project_init_sql = "INSERT INTO project_info_table (project_uuid,project_name,project_path,project_owner,project_access,project_date) \
								VALUES ('"+project_uuid+"', '"+project_name+"', '"+project_path+"','"+project_owner+"','"+project_access+"','"+project_date+"');"
		if project_DB.execute_sql(creat_project_init_sql) == 'pass':	
			return_info_datas = "succees"
			return_dat = "succeed"
		else:
			return_info_datas = 1
			return_dat = "failed"
	response_info = {"return_data":return_dat}
	return json.dumps(response_info)


#打开 flask 项目
@api.route('/open_project', methods=['POST','GET'])
def open_project():
	if request.method == "POST":
		datax = request.form.to_dict()
		content = str(datax)
	project_name = datax["project_name"]

	open_project_state = apicmd.open_project(project_name)
	time.sleep(1)
	response_info = {"return_data":project_name}
	return json.dumps(open_project_state)

# get flask 项目 状态
@api.route('/get_project_state', methods=['POST','GET'])
def get_project_state():
	all_project_state_dic = apicmd.get_all_project_state()
	return json.dumps(all_project_state_dic)



# flask 项目关机
@api.route('/close_project', methods=['POST','GET'])
def close_project():
	if request.method == "POST":
		datax = request.form.to_dict()
		content = str(datax)
	project_name = datax["project_name"]
	response_info = apicmd.off_project(project_name)
	time.sleep(1)
	return json.dumps(response_info)



project_list_ini_file = Man_API_Path+"/static/ini_file/project_list.ini"
project_list = man_file.Ini_File_Man(project_list_ini_file)

#获取 flask name list
@api.route('/get_flask_list_name', methods=['POST','GET'])
def get_flask_list_name():
	flask_list_names = project_list.get_all_sections()
	return json.dumps(flask_list_names)


#统计系统项目总个数
def get_all_project_number():
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	project_number_sql = "SELECT count(project_uuid) from project_info_table;"
	project_number = project_DB.select_sql(project_number_sql)
	print(project_number[0][0])
	return project_number[0][0]


#获取当前系统总用户数
def get_all_user_number():
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	all_user_number_sql = 'SELECT count(user_name) from man_api_user_table;'
	all_user_number = user_DB.select_sql(all_user_number_sql)
	return all_user_number[0][0]

# man api code pg
@api.route('/code',methods=['POST','GET'])
@Authentication
def code_pg(user_name):
	if request.method == "GET":
		get_pgnumber = request.args.get('pgnumber')
	if get_pgnumber == None:
		get_pgnumber = 1
	print(user_name)
	#获取flask 项目
	#flask_list_names = project_list.get_all_sections()
	flask_list_names=[]
	#1. 先获取自己的项目
	#2. 在获取公开的项目
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	#get_my_project_path_sql = "SELECT project_name from project_info_table where project_owner = '"+user_name+"';"# where project_access = '1';"
	#get_project_path = project_DB.select_sql(get_my_project_path_sql)
	
	#项目个数
	project_numbers_sql = "SELECT count(project_uuid) from project_info_table where project_owner = '"+user_name+"' OR project_access = '1';"
	project_numbers = project_DB.select_sql(project_numbers_sql)
	project_numbers = project_numbers[0][0]

	#项目总页数
	project_pg = int(project_numbers/5)+1
	print("[项目页数] = "+str(project_pg))
	#项目当前页数
	project_now_pg = get_pgnumber
	print("[项目当前页数] = "+str(project_now_pg))

	#页标
	pg_s = (int(project_now_pg)-1)*5
	pg_n = int(get_pgnumber)*5

	#多条件查询
	get_my_project_duo_sql = "SELECT project_name from project_info_table where project_owner = '"+\
							user_name+"' OR project_access = '1' limit "+str(pg_s)+","+str(pg_n)+";"
	get_project_duo_path = project_DB.select_sql(get_my_project_duo_sql)
	print("[多条件查询] = "+str(len(get_project_duo_path)))

	for project_path_name in get_project_duo_path:
		flask_list_names.append(' '.join(project_path_name))

	flask_list_names = list(set(flask_list_names))
	print("[flask_list_names] = "+str(flask_list_names))
	#循环遍历 当前项目所在的操作空间
	project_list_infos = []
	project_list_info = []
	
	#获取当前项目的活动空间
	for doing_project_names in set(flask_list_names):
		print(doing_project_names)
		#当前的活动空间
		#print(get_project_handle(doing_project_names))
		#project_list_info.update({"name":doing_project_names})
		#project_list_info.update({"doing":get_project_handle(doing_project_names)})
		project_list_info.append(doing_project_names)
		project_list_info.append(get_project_handle(doing_project_names))
		project_list_infos.append(project_list_info)
		project_list_info = []

	pgs_show = []
	pg_show = []
	#所有列表
	if int(project_now_pg) < 5:
		all_pgs = list(range(1,project_pg+1))
		for pg in all_pgs:
			if pg == int(project_now_pg):
				pg_show.append(pg)
				pg_show.append(1)
				pgs_show.append(pg_show)
			else:
				pg_show.append(pg)
				#pg_show.append(0)
				pgs_show.append(pg_show)
			pg_show = []
	else:
		all_pgs = list(range(int(project_now_pg)-3,int(project_now_pg)+3))
		for pg in all_pgs:
			if pg == int(project_now_pg):
				pg_show.append(pg)
				pg_show.append(1)
				pgs_show.append(pg_show)
			else:
				pg_show.append(pg)
				#pg_show.append(0)
				pgs_show.append(pg_show)
			pg_show = []
	print(pgs_show)
	return render_template('code_dev.html',flask_list_names=project_list_infos,project_number=project_numbers,
							all_pg = pgs_show,now_pg = int(project_now_pg),maxpg=project_pg)



#获取 目录下一级目录与文件
@api.route('/get_dir',methods=['GET'])
def get_dir():
	if request.method == "GET":
		print('call get now')
		project_name = request.args.get('project_names')
		project_branch = request.args.get('branch')
		dirname = request.args.get('open_project')
		print(project_name)
		print(project_branch)
		print(dirname)
	print("[get dir () 请求]")
	dir_path_number = dirname.count('$')
	#print(dirname.count('$'))
	if dirname.count('$') > 0:
		returndirname = dirname.replace("$", "/")
		dirnames = dirname.split("$")
		dir_name = "/".join(dirnames[1:])
		print("[Debug dirnames] ="+str(dirnames))
		print("[Debug dir_name] = "+dir_name)
		dir_list,file_list = addproject.get_dir_list(project_branch,project_name,dir_name)
		response_info = {"dirname":returndirname,"dirpathnumber":dir_path_number,"dirlist":dir_list,"filelist":file_list}
		print(response_info)
		return json.dumps(response_info)
	else:
		dir_list,file_list = addproject.get_main_dir_list(project_branch,project_name)
		'''
		dir_list,file_list = addproject.get_dir_list(project_name,dirname)
		print("[Dir list] = "+str(dir_list))
		print("[File list] = "+str(file_list))
		'''
		response_info = {"dirname":dirname,"dirpathnumber":dir_path_number,"dirlist":dir_list,"filelist":file_list}
		return json.dumps(response_info)
		#return json.dumps("ok")



#登陆 
@api.route('/user_login', methods=['POST','GET'])
def user_login():

	if request.method == "POST":
		datax = request.form.to_dict()
		print(str(datax))
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	#sys_DB = man_sys_db.Man_API_Sqlite('man_api_sys.db')
	user_name = datax['username']
	#如果当前用户正在使用则登陆失败
	#print("[Login_user_token] = "+session.get(user_name))
	user_login_satate_session = session.get(user_name)
	#如果当前用户是登陆状态 并且 session 还未失效，那么当前用户不能在继续登陆，不支持多端登陆
	if man_redis.get(user_name) == b'use' and user_login_satate_session != None:
		response_info = {"response":2}
		return json.dumps(response_info)

	user_password = datax['password']
	match_user_sql = 'SELECT user_password from man_api_user_table where user_name = "'+user_name+'";'
	get_user_password = user_DB.select_sql(match_user_sql)
	#print(get_user_password)

	if get_user_password == []:
		#不存在的账号
		response_info = {"response":0}
		return json.dumps(response_info)
	else:
		#print(get_user_password[0])
		#print(type(get_user_password[0]))
		get_user_password = get_user_password[0]
		if get_user_password[0] == str(user_password):
			#登陆成功
			#随机生成一个 name 加密 token
			man_token_username,man_token_userkey=man_token_create(user_name)
			print(man_token_username)
			print(type(man_token_username))
			print(man_token_userkey)
			print(type(man_token_userkey))
			#存入解密秘钥
			print("[man_token_username] = "+man_token_username)
			man_redis.set(man_token_username, man_token_userkey,ex=3600)
			print("[Sven Session]\n")
			#存入 session
			session['token'] = man_token_username
			print(session.get('token'))
			session[user_name] = man_token_username
			print(session.get(user_name))
			print("\n\n\n")
			#time.sleep(0.5)
			#print("[man_token_userkey] = "+str(man_redis.get(man_token_username)))
			#print(man_token_decode2(man_token_username,man_redis.get(man_token_username)))
			#将登陆的用户状态存入redis
			#session['login_user'] = user_name
			man_redis.set(user_name, 'use',ex=3600)
			#返回与 session 相同的 token 提供前端 存入 cookie
			response_info = {"response":100,"userToken":man_token_username}
			return json.dumps(response_info)
			
		else:
			#密码错误
			response_info = {"response":1}
			return json.dumps(response_info)

	#return json.dumps(datax)




#分支管理
# 1. 三大分支,活动空间：  Master(主分支)  Branch(开发分支)  Release(发布分支)
# 2. 两大备份空间：  Historyimage(历史备份,自动备份主分支)    Backup(拷贝分支,备份当前活动空间的源码)
# 3. 版本控制  Master ->  项目名+v+发布迭代版本+主分支迭代版本  man-v0-0
# 4. 版本控制  Release -> 项目名+v+发布迭代版本  man-v1
# 5. 版本控制  Branch -> 项目名+v+发布迭代版本+主分支迭代版本+dev+开发迭代号  man-v1-1-dev-0
@api.route('/managebranch/<projectname>', methods=['POST','GET'])
@Authentication
def manage_branch(user_name,projectname):
	#print(user_name)
	#print(projectname)
	#  获取分支信息  branch_data
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	get_all_project_DB_sql = "SELECT branch_name,branch_type,parent_branch_name,branch_date from project_branch_table where project_name='"+projectname+"';"
	get_all_project_DB = project_DB.select_sql(get_all_project_DB_sql)
	#print(get_all_project_DB)
	#用于存储
	#project_DB_list = []
	#link_info_list = []
	#数据模板   不可行
	#project_DB_Master = Template('{name: "${branch_name}",x: 10,y: 300,itemStyle: {color: "#0066CC"},value:" ${branch_date}"}')
	#link_info_datas_Master = Template('{source: \"${now_branch_name}\",target: \"${parent_branch_name}\"}')
	#遍历重组数据返回给前端
	return_project_data_list = []
	return_project_data_dic = {}
	return_project_data_test = []
	#branch_name_list = []
	link_info_list = []
	link_info_dic = {}

	init_x_M = 0
	#init_y_M = 300

	for project_DB_data in get_all_project_DB:

		

		#三种分支空间在y轴上显示的位置
		if project_DB_data[1] == "Master":
			init_y_M = 300
			init_x_M += 10
			color_data = "#0066CC"
		if project_DB_data[1] == "Branch":
			init_y_M = 310
			init_x_M += 5
			color_data = "red"
		if project_DB_data[1] == "Release":
			init_y_M = 290
			init_x_M += 5
			color_data = "#01B468"


		#存入字典
		return_project_data_dic.update({"project_name_val":project_DB_data[0]})
		return_project_data_dic.update({"project_time_val":project_DB_data[3]})
		return_project_data_dic.update({"x_val":init_x_M})
		return_project_data_dic.update({"y_val":init_y_M})
		return_project_data_dic.update({"color_val":color_data})

		return_project_data_list.append(return_project_data_dic)
		'''
		if project_DB_data[2] != "null":
			link_info_dic.update({"now_branch_name":project_DB_data[0]})
			link_info_dic.update({"parent_branch_name":project_DB_data[2]})
			link_info_list.append(link_info_dic)
		'''
		return_project_data_dic = {}
		#link_info_dic = {}
	#print(json.dumps(project_DB_list))
	#print(json.dumps(link_info_list))
	print(return_project_data_list)
	#print(set(return_project_data_list))
	print(link_info_list)


	#分支结构数据
	get_all_branch_relation_sql = "SELECT finish_branch,begin_branch from branch_relation_table where project_name='"+projectname+"';"
	get_all_branch_relation = project_DB.select_sql(get_all_branch_relation_sql)
	print(get_all_branch_relation)
	for branch_relation_info in get_all_branch_relation:
		link_info_dic.update({"now_branch_name":branch_relation_info[0]})
		link_info_dic.update({"parent_branch_name":branch_relation_info[1]})
		link_info_list.append(link_info_dic)
		link_info_dic = {}

	#当前项目操作空间
	projectname_work = get_project_handle(projectname)


	return render_template('branch_manage.html', project_name=projectname, project_work = projectname_work,
							return_project_link_info=link_info_list,return_project_data_dic=return_project_data_list )




#创建开发分支  add Branch
# 1. 只能在当前主分支创建 开发分支
# 2. 设置开发分支版本号与名称规则  主分支版本号+开发分支迭代号  man-v0-1-dev-0
# 3. 更新项目当前操作空间 为开发分支
# 4. 拷贝 主分支源码 到 创建分支
# 5. 开始迭代操作
@api.route('/addbranch', methods=['POST','GET'])
def add_branch():
	if request.method == "POST":
		datax = request.form.to_dict()
		print(str(datax))
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	#判断当前活动空间是否为主分支
	project_working = get_project_handle(datax['project_name'])
	print(project_working)
	if project_working != "Master":
		return json.dumps("not Master")#当前活动空间不是主分支空间,无法创建开发分支
	#获取当前的主分支
	dir_list,file_list = addproject.get_main_dir_list(datax['now_work'],datax['project_name'])
	now_branch = dir_list[0]
	print("[当前分支] = "+now_branch)
	#设置开发分支版本号
	now_dev = now_branch+"-dev-"+str(0)
	print("[创建开发分支] = "+now_dev)
	#主分支路径
	master_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Master/"+now_branch+"/")
	print("[主分支路径] = "+master_path)
	#开发分支路劲
	dev_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Branch/"+now_dev+"/")
	print("[开发分支路径] = "+dev_path)
	#将当前主分支的源码目录拷贝到创建的开发分支
	if filecentre.copytree_dir(master_path,dev_path) == True:
		# 当拷贝成功后 增加新的迭代分支
		
		# branch_uuid_md5
		branch_uuid_md5 = hashlib.md5() 
		branch_uuid_md5.update((now_dev).encode("utf-8"))
		branch_uuid = branch_uuid_md5.hexdigest()
		# project_uuid get得到
		'''
		get_project_uuid_sql = "SELECT project_uuid from project_info_table where project_name = '"+datax['project_name']+"';"
		project_uuid = project_DB.select_sql(get_project_uuid_sql)
		project_uuid = "".join(project_uuid[0])
		print("[project_uuid Type]")
		print(project_uuid)
		print(type(project_uuid))
		'''
		project_uuid = get_project_uuid(datax['project_name'])
		# project_name
		project_name = datax['project_name']
		# branch_name
		branch_name = now_dev
		#  branch_type
		branch_type = "Branch"
		#  parent_branch_name
		parent_branch_name = now_branch
		#  branch_path
		branch_path = branch_type + '/' + branch_name
		branch_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

		add_branch_doing = add_iter_info(branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date)
		'''
		add_branch_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,\
										branch_type,parent_branch_name,branch_path,branch_date) \
										VALUES ('"+branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+branch_name+"','"+branch_type+"',\
										'"+parent_branch_name+"', '"+branch_path+"', '"+branch_date+"');"
		'''
		# 添加新的分支信息
		add_branch_relation_doing = add_branch_relation_info(project_name,parent_branch_name,branch_name)

		#当拷贝成功后，更新当前项目的工作状态
		#当前操作空间
		project_handle_data = branch_type
		#操作时间
		update_handle_time = branch_date
		#操作人
		update_handle_user = datax['user_name']
		update_project_handle_doing = update_project_handle(project_handle_data,update_handle_time,update_handle_user,project_uuid)
		'''
		update_project_handle_sql = "UPDATE project_handle_table \
									SET project_handle = '"+project_handle_data+"',handle_date = '"+update_handle_time+"',handle_user = '"+update_handle_user+"' \
									where project_uuid = '"+project_uuid+"';"
		'''

		if add_branch_doing == True and update_project_handle_doing == True and add_branch_relation_doing == True:
			return_info_datas = "succees"
	
		
	return json.dumps(datax)





#合并分支  merge to Master
# 1. 只能在当前操作空间为开发分支才能合并到主分支
# 2. 在合并之前对比前后文件差异
# 3. 提示文件差异记录并提示
# 4. 确认后 将要合并的开发分支迭代到主分支下个版本 (与在主分支上传文件类似)
# 5. 删除开发分支的源码并保存到历史
@api.route('/mergetomaster', methods=['POST','GET'])
def merge_to_master():
	if request.method == "POST":
		datax = request.form.to_dict()
		print(str(datax))
	#判断当前是否处于开发分支
	project_working = get_project_handle(datax['project_name'])
	print(project_working)
	if project_working != "Branch":
		return json.dumps("not Branch")#当前活动空间不是开发分支空间,无法合并到主分支

	#获取当前主分支路径
	dir_list,file_list = addproject.get_main_dir_list("Master",datax['project_name'])
	now_branch = dir_list[0]
	print("[当前分支] = "+now_branch)
	master_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Master/"+now_branch+"/")
	print("[主分支路径] = "+master_path)
	#获取当前开发分支路径
	dev_dir_list,dev_file_list = filecentre.get_dev_branch_path(datax['project_name'])
	dev_now_branch = dev_dir_list[0]
	print("[当前开发分支] = "+dev_now_branch)
	dev_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Branch/"+dev_now_branch+"/")
	print("[开发分支路径] = "+dev_path)

	#开发分支与当前主分支对比文件差异性
	newly,lose = filecentre.contrast_file_difference2(master_path,dev_path)
	#print("[新增] = "+str(newly))
	#print("[减少] = "+str(lose))

	#删除当前主分支的内容
	#吧当前开发分支的内容移动到新的主分支
	#获取分支版本
	v_list = now_branch.rsplit('-')
	#print("[V list] = "+str(v_list))
	main_versions = v_list[-2]
	ite_versions = v_list[-1]
	#print(type(main_versions))
	#print("[main_versions] = "+str(main_versions))
	print("[ite_versions] = "+str(int(ite_versions)+1))
	#版本迭代
	# v0-0 规则： 
	#   Release  v0 -> v1
	#   普通迭代  v0-0 -> v0-1
	new_versions = datax['project_name']+"-"+main_versions+"-"+str(int(ite_versions)+1)
	print("[合并迭代主分支] = "+new_versions)
	new_versions_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Master/"+new_versions+"/")
	print("[合并迭代主分支路径] = "+new_versions_path)
	filecentre.shift_dir_files(dev_path,new_versions_path)
	
	#删除旧的 主分支
	filecentre.del_dir_files(master_path)

	#打包新的合并的主分支到历史存储空间
	#主分支存储保存位置
	history_new_versions_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Historyimage/"+new_versions+".zip")
	filecentre.make_zip(new_versions_path,history_new_versions_path)

	
	# project_name
	project_name = datax['project_name']
	#获取当前项目的 uuid
	project_uuid = get_project_uuid(project_name)
	# 操作时间
	branch_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	#记录新的迭代主分支
	#new_master_branch_info
	# new_master_branch_uuid_md5
	new_master_branch_uuid_md5 = hashlib.md5() 
	new_master_branch_uuid_md5.update((new_versions_path).encode("utf-8"))
	new_master_branch_uuid = new_master_branch_uuid_md5.hexdigest()
	
	# branch_name
	new_master_branch_name = new_versions
	#  branch_type
	new_master_branch_type = "Master"
	#  parent_branch_name
	new_master_parent_branch_name = now_branch
	#  branch_path
	new_master_branch_path = new_master_branch_type + '/' + new_master_branch_name
	
	'''
	add_branch_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date) \
					VALUES ('"+new_master_branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+new_master_branch_name+"','"+new_master_branch_type+"',\
					'"+new_master_parent_branch_name+"', '"+new_master_branch_path+"', '"+branch_date+"');"
	'''

	add_new_master = add_iter_info(new_master_branch_uuid,project_uuid,project_name,new_master_branch_name,
		new_master_branch_type,new_master_parent_branch_name,
		new_master_branch_path,branch_date)

	add_new_master_relation = add_branch_relation_info(project_name,new_master_parent_branch_name,new_master_branch_name)

	merge_parent_branch_name = dev_now_branch
	add_new_merge_relation =  add_branch_relation_info(project_name,merge_parent_branch_name,new_master_branch_name)
	'''
	#记录合并分支迭代信息
	merge_branch_uuid_md5 = hashlib.md5() 
	merge_branch_uuid_md5.update((dev_now_branch+new_versions).encode("utf-8"))
	merge_branch_uuid = merge_branch_uuid_md5.hexdigest()

	merge_parent_branch_name = dev_now_branch
	add_iter_info(merge_branch_uuid,project_uuid,project_name,new_master_branch_name,
		new_master_branch_type,merge_parent_branch_name,
		new_master_branch_path,branch_date)
	'''

	#更新当前项目的工作空间
	if add_new_master==True and add_new_master_relation==True and add_new_merge_relation==True:
		print("ok")
		#更新活动空间
		update_project_handle("Master",branch_date,datax['user_name'],project_uuid)

	#合并成功后返回文件差异性
	return json.dumps(datax)



#记录迭代信息
def add_iter_info(branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	add_branch_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date) \
						VALUES ('"+branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+branch_name+"','"+branch_type+"',\
						'"+parent_branch_name+"', '"+branch_path+"', '"+branch_date+"');"
	if project_DB.execute_sql(add_branch_sql) == 'pass':
		return True
	else:
		return False

#记录分支信息
def add_branch_relation_info(project_name,begin_branch_name,finish_branch_name):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	relation_uuid_md5 = hashlib.md5() 
	relation_uuid_md5.update((begin_branch_name+finish_branch_name).encode("utf-8"))
	relation_uuid = relation_uuid_md5.hexdigest()
	add_branch_relation = "INSERT INTO branch_relation_table (relation_uuid,project_name,begin_branch,finish_branch) \
						VALUES ('"+relation_uuid+"', '"+project_name+"','"+begin_branch_name+"', '"+finish_branch_name+"');"
	if project_DB.execute_sql(add_branch_relation) == 'pass':
		return True
	else:
		return False


#获取项目的uuid
def get_project_uuid(project_name):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	get_project_uuid_sql = "SELECT project_uuid from project_info_table where project_name = '"+project_name+"';"
	project_uuid = project_DB.select_sql(get_project_uuid_sql)
	project_uuid = "".join(project_uuid[0])
	print("[project_uuid Type]")
	print(project_uuid)
	print(type(project_uuid))
	return project_uuid


#更新活动空间
def update_project_handle(project_handle_data,update_handle_time,update_handle_user,project_uuid):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	update_project_handle_sql = "UPDATE project_handle_table \
									SET project_handle = '"+project_handle_data+"',handle_date = '"+update_handle_time+"',handle_user = '"+update_handle_user+"' \
									where project_uuid = '"+project_uuid+"';"
	if project_DB.execute_sql(update_project_handle_sql) == 'pass':
		return True
	else:
		return False


#发布版本  release edition
# 1. 只能发布主分支的版本，并且当前无开发分支
# 2. 发布类型为 zip 文件
# 3. 发布的内容加入到 Release 存储空间里  man-Release.v1.zip
# 4. 主分支迭代 版本+1   man-v0-2 -> man-v1-0
@api.route('/releaseedition', methods=['POST','GET'])
def release_edition():
	if request.method == "POST":
		datax = request.form.to_dict()
		print(str(datax))
	#判断当前是否处于 主分支的工作空间
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	#判断当前活动空间是否为主分支
	project_working = get_project_handle(datax['project_name'])
	print(project_working)
	if project_working != "Master":
		return json.dumps("not Master")#当前活动空间不是主分支空间,无法创建开发分支
	#获取当前的主分支
	dir_list,file_list = addproject.get_main_dir_list(datax['now_work'],datax['project_name'])
	now_branch = dir_list[0]
	print("[当前分支] = "+now_branch)
	#设置发布版本的名称
	#获取分支版本
	v_list = now_branch.rsplit('-')
	print("[V list] = "+str(v_list))
	main_versions = v_list[-2]
	ite_versions = v_list[-1]
	print(type(main_versions))
	main_versions_number = int(main_versions[1:])

	print("[main_versions] = "+str(main_versions))
	print(type(main_versions_number))
	print("[main_versions_number] = "+str(main_versions_number))
	print("[ite_versions] = "+str(int(ite_versions)+1))
	# release 版本
	# 规则 main_versions_number +=1
	main_versions_number+=1
	release_versions = datax['project_name']+"-Release.v"+str(main_versions_number)+".zip"
	print("[release_versions] = "+str(release_versions))
	#主分支源码路径
	master_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Master/"+now_branch+"/")
	print("[主分支路径] = "+master_path)
	# release 存储空间路径
	release_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Release/"+release_versions)
	print("[release 存储空间路径] = "+release_path)
	if filecentre.make_zip(master_path,release_path) == False:
		return json.dumps("Release Fail")

	#发布成功后将分支信息存入数据库里
	# branch_uuid_md5
	release_branch_uuid_md5 = hashlib.md5() 
	release_branch_uuid_md5.update((release_versions).encode("utf-8"))
	release_branch_uuid = release_branch_uuid_md5.hexdigest()
	# project_uuid get得到
	'''
	get_project_uuid_sql = "SELECT project_uuid from project_info_table where project_name = '"+datax['project_name']+"';"
	project_uuid = project_DB.select_sql(get_project_uuid_sql)
	project_uuid = "".join(project_uuid[0])
	'''
	project_uuid = get_project_uuid(datax['project_name'])
	# project_name
	project_name = datax['project_name']
	# branch_name
	release_branch_name = release_versions
	#  branch_type
	release_branch_type = "Release"
	#  parent_branch_name
	parent_branch_name = now_branch
	#  branch_path
	release_branch_path = release_branch_type + '/' + release_branch_name
	release_branch_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	release_add_branch_doing = add_iter_info(release_branch_uuid,project_uuid,project_name,release_branch_name,release_branch_type,parent_branch_name,release_branch_path,release_branch_date)
	'''
	release_add_branch_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date) \
						VALUES ('"+release_branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+release_branch_name+"','"+release_branch_type+"',\
						'"+parent_branch_name+"', '"+release_branch_path+"', '"+release_branch_date+"');"
	'''
	
	add_release_branch_relation2 = add_branch_relation_info(project_name,parent_branch_name,release_branch_name)

	#发布成功后迭代 主分支
	#规则：  man-v0-1 -> man-v1-0
	# 1. 复制一份 迭代版本到主分支
	#迭代版本目录名称
	ite_main_v = datax['project_name']+"-v"+str(main_versions_number)+"-0"
	print("[迭代主分支名称] = "+ ite_main_v)
	#迭代主分支路径
	ite_master_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+datax['project_name']+"/Master/"+ite_main_v+"/")
	print("[迭代主分支路径] = "+ite_master_path)
	
	#迭代版本
	if release_add_branch_doing == True and filecentre.copytree_dir(master_path,ite_master_path) == True and add_release_branch_relation2 == True:
		# 当拷贝成功后 删除旧的主分支
		filecentre.del_dir_files(master_path)

		#将新的主分支信息存入数据库里
		new_branch_uuid_md5 = hashlib.md5()
		new_branch_uuid_md5.update((ite_main_v).encode("utf-8"))
		new_branch_uuid = new_branch_uuid_md5.hexdigest()
		new_branch_name = ite_main_v
		new_branch_type = "Master"
		new_branch_path = new_branch_type + '/' + new_branch_name
		new_add_branch_doing = add_iter_info(new_branch_uuid,project_uuid,project_name,new_branch_name,new_branch_type,parent_branch_name,new_branch_path,release_branch_date)
		'''
		new_add_branch_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date) \
						VALUES ('"+new_branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+new_branch_name+"','"+new_branch_type+"',\
						'"+parent_branch_name+"', '"+new_branch_path+"', '"+release_branch_date+"');"
		'''
		#记录分支结构
		add_release_branch_relation = add_branch_relation_info(project_name,parent_branch_name,new_branch_name)

		if new_add_branch_doing == True and add_release_branch_relation == True:

			return json.dumps(now_branch)

	else:
		return json.dumps(0)#0 代表 失败





#查 所有用户
def get_all_users_number():
	pass

#查 所有用户列表  用户名 权限 部门 组
def get_all_users_info():
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	sql_cmd = "SELECT user_name,user_access,user_department,user_group,user_employ from man_api_user_table;"
	all_users_info_list = user_DB.select_sql(sql_cmd)
	print(all_users_info_list)
	return all_users_info_list

#查 系统所有部门
def get_all_department_info():
	sys_DB = man_sys_db.Man_API_Sqlite('man_api_sys.db')
	sql_cmd = "SELECT department_name from department_table;"
	all_department_list = sys_DB.select_sql(sql_cmd)
	return all_department_list

#查 系统权限
def get_all_user_access_info():
	sys_DB = man_sys_db.Man_API_Sqlite('man_api_sys.db')
	sql_cmd = "SELECT access_id,access_introduce from access_table;"
	all_department_list = sys_DB.select_sql(sql_cmd)
	return all_department_list

@api.route('/get_all_users_info_test', methods=['POST','GET'])
def get_all_users_info_test():
	#get_all_users_info()
	return json.dumps(get_all_department_info())


#用户管理
@api.route('/usermanage', methods=['POST','GET'])
def user_manage():
	user_list = get_all_users_info()
	user_number = len(user_list)
	print("[user_number] = "+str(user_number))
	department_list = get_all_department_info()
	access_list = get_all_user_access_info()
	return render_template('user_manage.html',
							users_list = user_list[1:],
							departments_list = department_list,
							access_list = access_list[1:],
							user_number = str(user_number-1))

#查 对应部门的组
def get_group_info(department_names):
	sys_DB = man_sys_db.Man_API_Sqlite('man_api_sys.db')
	get_department_id_sql_cmd = "SELECT department_id from department_table where department_name = '"+department_names+"';"
	department_id_data = sys_DB.select_sql(get_department_id_sql_cmd)
	
	get_group_info_cmd = "SELECT group_name from group_table where department_id = '"+str(department_id_data[0][0])+"';"
	all_group_list = sys_DB.select_sql(get_group_info_cmd)
	return all_group_list
	
	#return department_id_data[0][0]

#获取对应部门的组
@api.route('/usergroup_info', methods=['POST','GET'])
def get_user_group_info():
	if request.method == "GET":
		department = request.args.get('department_name')
	return json.dumps(get_group_info(department))


#创建用户
@api.route('/add_user', methods=['POST','GET'])
def add_user():
	if request.method == "POST":
		datax = request.form.to_dict()
	user_name_val = datax["user"]
	uuid_md5 = hashlib.md5()   
	uuid_md5.update(user_name_val.encode("utf-8"))
	user_uuid_md5 = uuid_md5.hexdigest()
	user_password_val = datax["user_password"]
	user_department_val = datax["user_department"]
	user_group_val = datax["user_group"]
	user_access_val = datax["user_access"]
	add_user_sql_cmd = """INSERT INTO man_api_user_table 
						(user_uuid,user_name,user_password,user_department,user_group,user_access) 
						VALUES ('"""+user_uuid_md5+"""','"""+user_name_val+"""', '"""+user_password_val+"""', 
						'"""+user_department_val+"""','"""+user_group_val+"""',
						'"""+user_access_val+"""');"""
	print(add_user_sql_cmd)
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	add_user_return = user_DB.execute_sql(add_user_sql_cmd)
	if add_user_return == 'pass':
		return_info_datas = "succees"
	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(response_info)


#获取用户信息
@api.route('/user_info/<username>', methods=['POST','GET'])
def get_user_info(username):
	print(username)
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	get_user_info_sql = "SELECT user_uuid,user_name,user_password,user_department,user_group,user_employ,user_head,user_access from man_api_user_table where user_name = '"+str(username)+"';"
	user_info_datas = user_DB.select_sql(get_user_info_sql)
	response_info = {"user_uuid":user_info_datas[0][0],"user_name":user_info_datas[0][1],"user_password":user_info_datas[0][2],
					"user_department":user_info_datas[0][3],"user_group":user_info_datas[0][4],"user_employ":user_info_datas[0][5],
					"user_head":user_info_datas[0][6],"user_access":user_info_datas[0][7]}
	print(user_info_datas[0])
	if user_info_datas[0] != None:
		print(user_info_datas[0][0])


	return json.dumps(response_info)



#修改用户部门或组
@api.route('/updata_user_department', methods=['POST','GET'])
def modify_user_dg():
	if request.method == "POST":
		datax = request.form.to_dict()
	user_name = datax["username_val"]
	new_user_department = datax["user_department_dg"]
	new_user_group = datax["user_group1"]
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	modify_user_dg_sql = "UPDATE man_api_user_table SET user_department = '"+new_user_department+"',user_group = '"+new_user_group+"' WHERE user_name = '"+user_name+"';"
	if user_DB.execute_sql(modify_user_dg_sql) == 'pass':
		return_info_datas = "succees"

	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(return_info_datas)


#修改用户权限
@api.route('/updata_user_access', methods=['POST','GET'])
def modify_user_access():
	if request.method == "POST":
		datax = request.form.to_dict()
	user_name = datax["acc_username_val"]
	user_access = datax["user_access_data"]
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	modify_user_access_sql = "UPDATE man_api_user_table SET user_access = '"+user_access+"' WHERE user_name = '"+user_name+"';"
	if user_DB.execute_sql(modify_user_access_sql) == 'pass':
		return_info_datas = "succees"

	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(response_info)	



#禁用用户
@api.route('/forbidden_user',methods=['POST','GET'])
def modify_user_employ_forbidden():
	if request.method == "POST":
		datax = request.form.to_dict()
	user_name = datax["user_names_val"]
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	modify_user_access_sql = "UPDATE man_api_user_table SET user_employ = 0 WHERE user_name = '"+user_name+"';"
	if user_DB.execute_sql(modify_user_access_sql) == 'pass':
		return_info_datas = "succees"
	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(response_info)

#启用用户
@api.route('/shift_user/<username>',methods=['POST','GET'])
def modify_user_employ_shift(username):
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	modify_user_employ_shift_sql = "UPDATE man_api_user_table SET user_employ = 1 WHERE user_name = '"+username+"';"
	if user_DB.execute_sql(modify_user_employ_shift_sql) == 'pass':
		return_info_datas = "succees"
	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(response_info)


#删除用户
@api.route('/del_user',methods=['POST','GET'])
def del_user():
	if request.method == "POST":
		datax = request.form.to_dict()
	user_name = datax["user_names_val"]
	user_DB = man_sys_db.Man_API_Sqlite('man_api_user.db')
	del_user_sql = "DELETE FROM man_api_user_table WHERE user_name = '"+user_name+"';"
	if user_DB.execute_sql(del_user_sql) == 'pass':
		return_info_datas = "succees"
	else:
		return_info_datas = 0
	response_info = {"return_data":return_info_datas}
	return json.dumps(response_info)





#获取部门和组的信息












#创建项目文件存储中心
@api.route('/creatproject_init',methods=['POST','GET'])
def creat_project_init():
	if request.method == "POST":
		datax = request.form.to_dict()
	user = datax["c_user_name"]
	project_name = datax["project_names"]
	project_access = datax["project_acc"]
	if project_name != "":
		doing_creat = filecentre.creat_project_dir(project_name)
		if doing_creat == "creat complete.":
			uuid_md5 = hashlib.md5()   
			uuid_md5.update((user+project_name).encode("utf-8"))
			project_uuid = uuid_md5.hexdigest()
			project_path = project_name
			project_owner = user
			project_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			#将信息写入数据库
			project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
			creat_project_init_sql = "INSERT INTO project_info_table (project_uuid,project_name,project_path,project_owner,project_access,project_date) \
									VALUES ('"+project_uuid+"', '"+project_name+"', '"+project_path+"','"+project_owner+"','"+project_access+"','"+project_date+"');"
			if project_DB.execute_sql(creat_project_init_sql) == 'pass':
				#将初始话 项目主分支分支信息
				#init_project
				branch_name = project_name+"-v0-0"
				branch_uuid_md5 = hashlib.md5() 
				branch_uuid_md5.update((user+branch_name).encode("utf-8"))
				branch_uuid = branch_uuid_md5.hexdigest()
				#project_uuid
				#project_name
				branch_type = 'Master'
				parent_branch_name = 'null' #null 表示没有父分支，自己就是父分支
				branch_path = 'Master/'+branch_name
				branch_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				print("[creat_project branch_name] = "+str(branch_name))
				print("[creat_project branch_uuid] = "+str(branch_uuid))
				#存入默认分支初始话 信息 到数据库

				init_project_branch_init = add_iter_info(branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date)
				
				if init_project_branch_init == True:
					#记录 初始  项目操作空间状态
					project_handle = branch_type
					handle_date = project_date
					handle_user = project_owner
					add_new_project_handle_sql = "INSERT INTO project_handle_table (project_uuid,project_name,project_handle,handle_date,handle_user)\
												VALUES ('"+project_uuid+"', '"+project_name+"', '"+project_handle+"','"+handle_date+"', '"+handle_user+"');"

					#记录 默认  项目操作人
					project_useraccess = project_owner
					add_new_project_useraccess_sql = "INSERT INTO project_useraccess_table (project_uuid,project_name,project_useraccess)\
												VALUES ('"+project_uuid+"', '"+project_name+"', '"+project_useraccess+"');"

					if project_DB.execute_sql(add_new_project_handle_sql) == 'pass' and project_DB.execute_sql(add_new_project_useraccess_sql) == 'pass':
						#成功后返回一个成功的信息
						return_info_datas = "succees"
					else:
						return_info_datas = 1
				else:
					return_info_datas = 1
			else:
				return_info_datas = 1
		else:
			return_info_datas = 2#代表本地存储中以存在这个文件
	else:
		return_info_datas = 0#0代表输入项目名称为空

	return json.dumps(return_info_datas)




'''
       文件上传
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''
#文件上传接口 测试
@api.route('/uploadfile/<pathname>/<projectname>', methods=['GET', 'POST'])
def upload_file(pathname,projectname):
    print("[Path_name] = "+str(pathname))
    print("[Project_name] = "+str(projectname))
    if request.method == 'POST':
        file = request.files['uploadfilename']
        username = request.form.get('name')
        descname = request.form.get('desc')
        print("[username] = "+str(username))
        print("[descname] = "+str(descname))
       
    print("[ File Nmae] = "+str(file))
    return json.dumps(file.filename)
'''


'''

		分支权限操作，文件存储中心操作

'''

#检查用户是否拥有上传权限
def get_user_updata_access(user_name,project_name):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	# 1. 通过用户名 在权限表里找 项目名
	get_useraccess_pr_id_sql = "SELECT project_useraccess from project_useraccess_table where project_name = '"+project_name+"';"
	get_useraccess_pr_id = project_DB.select_sql(get_useraccess_pr_id_sql)
	print(get_useraccess_pr_id)
	access_user_list = []
	for useraccess in get_useraccess_pr_id:
		access_user_list.append(' '.join(useraccess))
	print(access_user_list)
	#get_useraccess_pr_id = get_useraccess_pr_id[0]
	#get_useraccess_pr_id = ''.join(get_useraccess_pr_id)
	#print("****** [get_useraccess_pr_id] = "+get_useraccess_pr_id)
	# 3. 匹配项目名
	if user_name in access_user_list:
		print("user 可以操作")
		return True
	else:
		print("user 不可操作")
		return False
	#return get_project_name_sql

#获取项目当前的上传空间，操作空间
def get_project_handle(project_name):
	project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
	project_handle_sql = "SELECT project_handle from project_handle_table where project_name = '"+project_name+"';"
	project_handle = project_DB.select_sql(project_handle_sql)
	project_handle = project_handle[0]
	project_handle = ''.join(project_handle)
	return project_handle


#上传文件
# 只支持Master&Branch
# 
@api.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['uploadfilename']
        filename = request.form.get('name')
        projectname = request.form.get('project_name')
        #branchname = request.form.get('branch_name')
        username = request.form.get('user_handle_name')
    else:
    	print("[Error] ******* = 传入参数异常")
    	return json.dumps("传入参数异常")

    #检查用户是否支持上传操作
    #print("get_useraccess_pr_id = " + str(get_user_updata_access(username,projectname)))
    if get_user_updata_access(username,projectname) == False:
    	print("[Error] ******* = 你没有权限")
    	return json.dumps("你没有权限")

    #获取该项目当前的上传空间，操作空间
    print("该项目当前的操作空间 = " + str(get_project_handle(projectname)))
    # 操作对象空间 名称
    branchname = get_project_handle(projectname)
    print("[Debug branchname] = "+branchname)
    #获取当前的分支
    if branchname == "Master":
        dir_list,file_list = addproject.get_main_dir_list(branchname,projectname)
        print("[当前分支] = "+dir_list[0])
        now_branch = dir_list[0]
        #获取分支版本
        v_list = now_branch.rsplit('-')
        print("[V list] = "+str(v_list))
        main_versions = v_list[-2]
        ite_versions = v_list[-1]
        print(type(main_versions))
        print("[main_versions] = "+str(main_versions))
        print("[ite_versions] = "+str(int(ite_versions)+1))
        #版本迭代
        # v0-0 规则： 
        #   Release  v0 -> v1
        #   普通迭代  v0-0 -> v0-1
        new_versions = projectname+"-"+main_versions+"-"+str(int(ite_versions)+1)
        print("[new_versions] = "+new_versions)
    elif branchname == "Branch":
        dir_list,file_list = filecentre.get_dev_branch_path(projectname)
        print("[当前分支] = "+dir_list[0])
        #获取分支版本
        now_branch = dir_list[0]
        v_list = now_branch.rsplit('-')
        print("[V list] = "+str(v_list))
        ite_versions = v_list[-1]
        print("[ite_versions] = "+str(int(ite_versions)+1))
        v_list[-1] = str(int(ite_versions)+1)
        print("[V list] = "+str(v_list))
        new_versions = "-".join(v_list)
        print("[new_versions] = "+new_versions)
    else:
    	return json.dumps("项目操作空间异常")
    
    
    #验证文件类型
    if file and allowed_file(file.filename):
        base_path = os.path.abspath(Man_API_Path+"/File_storage_center/"+projectname+"/"+branchname+"/")
        print(base_path)
        #获取文件后缀
        fname = secure_filename(file.filename)
        ext = fname.rsplit('.',1)[1]
        save_file_path = base_path + new_versions+'.'+ext
        file.save(save_file_path)
        #如果是 'Master' 在历史目录下保存一份
        #Historyimage
        if branchname == "Master":
            save_file_historyimage_path = Man_API_Path+"/File_storage_center/"+projectname+"/Historyimage/"+ new_versions+'.'+ext
            save_historyimage = man_file.Man_File_handle(save_file_path)
            save_historyimage.copy_file(save_file_historyimage_path)
        #更新处理
        #print(filecentre.commit_file(now_branch,ext,new_versions,base_path,save_file_path))
        #如果更新成功，将新的迭代 存入 分支表
        if filecentre.commit_file(now_branch,ext,new_versions,base_path,save_file_path) == True:
            print("**********更新成功，将新的迭代 存入 分支表**********")
            #存入默认分支初始话 信息 到数据库
            project_DB = man_sys_db.Man_API_Sqlite('man_api_project.db')
            # branch_uuid_md5
            branch_uuid_md5 = hashlib.md5() 
            branch_uuid_md5.update((projectname+new_versions).encode("utf-8"))
            branch_uuid = branch_uuid_md5.hexdigest()
            # project_uuid get得到
            '''
            get_project_uuid_sql = "SELECT project_uuid from project_info_table where project_name = '"+projectname+"';"
            project_uuid = project_DB.select_sql(get_project_uuid_sql)
            project_uuid = project_uuid[0]
            project_uuid = ''.join(project_uuid)
            '''
            project_uuid = get_project_uuid(projectname)
            # project_name
            project_name = projectname
            # branch_name
            branch_name = new_versions
            #  branch_type
            branch_type = branchname
            #  parent_branch_name
            parent_branch_name = now_branch
            #  branch_path
            branch_path = projectname + '/' + branch_name
            #  branch_date 日期

            
            # 当上传成功后 增加新的迭代分支
            branch_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            add_project_branch_init = add_iter_info(branch_uuid,project_uuid,project_name,branch_name,branch_type,parent_branch_name,branch_path,branch_date)

            #添加分支路径
            add_branch_relation = add_branch_relation_info(project_name,parent_branch_name,branch_name)

            '''
            add_project_branch_init_sql = "INSERT INTO project_branch_table (branch_uuid,project_uuid,project_name,branch_name,\
                                            branch_type,parent_branch_name,branch_path,branch_date) \
                                            VALUES ('"+branch_uuid+"', '"+project_uuid+"', '"+project_name+"','"+branch_name+"','"+branch_type+"',\
                                            '"+parent_branch_name+"', '"+branch_path+"', '"+branch_date+"');"
            '''
            if add_project_branch_init == True and add_branch_relation == True:
                return_info_datas = "succees"
        print("[file name] = "+str(filename))
        print("[project name] = "+str(projectname))  
        print("[branch name] = "+str(branchname)) 
        print("[user name] = "+str(username)) 
        print("[ File Nmae] = "+str(file))
        return json.dumps(return_info_datas)
    else:
        return json.dumps("file error")
    '''
    return json.dumps("file error")
    '''


#验证当前用户是否有项目的操作权限
@api.route('/get_acc_doing', methods=['GET', 'POST'])
def get_acc_doing():
    if request.method == "GET":
        username = request.args.get('user')
        projectname = request.args.get('project')
    print(username)
    print(projectname)
    print(get_user_updata_access(username,projectname))
    
    if get_user_updata_access(username,projectname) == False:
        print("[Error] ******* = 你没有权限")
        return json.dumps(0)
    elif get_user_updata_access(username,projectname) == True:
        return json.dumps(1)
    else:
        return json.dumps(2)
    
    #return json.dumps(1)



#我的API   my api
@api.route('/myapihome', methods=['GET', 'POST'])
def my_api_home():
	return render_template('my_api.html')

