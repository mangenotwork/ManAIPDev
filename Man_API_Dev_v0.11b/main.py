# -*- coding:utf8 -*-
#encoding = utf-8

import man_api_sqlite.man_api_db_init as man_sys_db

from flask import Flask
from flask import Flask,request,g,render_template,redirect,url_for,abort,session
from flask import make_response,Response
import redis
from redis import StrictRedis
from flask_session import Session
import sys,os
import json
import time
from datetime import datetime,timedelta
#db 方法
import db.db_init as dbinit
#debug 方法
import debug
#一个测试方法
from api_funtion.test import test
# img_do api
from api_funtion.img_do import img
# man_api 项目导入
from man_api.api import api
#reload(sys)
#sys.setdefaultencoding('gbk')
#导入 json 数据 增删改查 方法
import man_api.json_data as json_data

from io import StringIO, BytesIO

#文件操作方法
import man_api.man_file as man_file
# ./
Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#系统操作库
import man_api.cmd as apicmd


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=60*60*24 #session长期有效，则设定session生命周期，整数秒，默认大概不到3小时。

app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
#app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀
app.config['SESSION_REDIS'] = StrictRedis(host='127.0.0.1', port='6379')#, password='')  # 用于连接redis的配置

#上传文件最大 1024MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024



#声明 蓝图
app.register_blueprint(test)
app.register_blueprint(img)
app.register_blueprint(api)

#json 文件 增删改查
json_file = json_data.Json_data()

Session(app)

'''
# API 主界面	
@app.route('/api_show', methods=['POST','GET'])
def api_show():
    api_data_list = []
    api_number = 0
    while api_number < json_file.get_api_all_line():
        api_data_info = json_file.get_all_json_data()[api_number]
        #print(api_data_info)
        if(api_data_info != ""):
            api_data_list.append(json.loads(api_data_info))
        api_number+=1
    
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
    
    return render_template('api_show.html',api_data_list = api_data_list)
'''
def Response_headers(content):  
    resp = Response(content)  
    resp.headers['Access-Control-Allow-Origin'] = '*'  
    return resp  


#添加 API
@app.route('/add_api', methods=['POST','GET'])
def add_api():
    '''
    if request.method == "POST":
        api_name = request.form.get('api_name')
        api_title = request.form.get('api_title')
        api_info = request.form.get('api_info')
        api_type = request.form.get('api_type')
        api_data = request.form.get('api_data')
    print(api_name)
    print(api_title)
    print(api_info)
    print(api_type)
    print(api_data)
    '''
    if request.method == "POST":
        datax = request.form.to_dict()
        #print(datax["api_name"])
        content = str(datax)  
        #print(content)
        #resp = Response_headers(content)
    api_id = datax["api_id"]
    #api_name = datax["api_name"]
    api_name = api_id
    api_title = datax["api_title"]
    api_type = datax["api_type"]
    #print(str(api_name)+str(api_title)+str(api_type))
    api_info = []
    api_data = []
    #获取到 api_info  api_data
    for api_info_key in datax:
        #print(api_info_key)
        if "api_info" in api_info_key:
            api_info.append(datax[api_info_key])
        if "api_data" in api_info_key:
            api_data.append(datax[api_info_key])
    #print(api_info)
    #print(api_data)
    #print(resp)
    #暂时开发 post get
    if api_type not in ["POST","GET"]:
        return_data = "api_type Error."
    else:
        return_data = "success"
    json_file.add_json_data(api_id, api_name, api_title, api_info, api_type, api_data)
    response_info = {"return_data":return_data}
    return json.dumps(response_info)


#修改 API
#@ api_id
@app.route('/updata_api', methods=['POST','GET'])
def updata_api():
    print("[Debug] Function updata_api()")
    if request.method == "POST":
        datax = request.form.to_dict()
        #print(datax["api_name"])
        content = str(datax)
    api_id = datax["updata_api_id"]
    api_name = api_id
    api_title = datax["updata_api_title"]
    api_type = datax["updata_api_type"]
    api_info = []
    api_data = []
    #获取到 api_info  api_data
    for api_info_key in datax:
        if "updata_api_info" in api_info_key:
            api_info.append(datax[api_info_key])
        if "updata_api_data" in api_info_key:
            api_data.append(datax[api_info_key])
    if api_type in ["POST","GET"]:
        doing_update_json_data = json_file.update_json_data(api_id,api_name,api_title,api_info,api_type,api_data)
        print(doing_update_json_data)
        if doing_update_json_data == 1:
            return_data = "success"
        else:
            return_data = "fail"
    else:
        return_data = "api_type Error."
        
    
    #json_file.add_json_data(api_id, api_name, api_title, api_info, api_type, api_data)
    print({"api_id":api_id, "api_name":api_name, "api_title":api_title, "api_info":api_info, "api_type":api_type, "api_data":api_data})
    response_info = {"return_data":return_data}
    return json.dumps(response_info)


#获取 API 个数

#获取指定 API ID 的信息
#@ api_id
@app.route('/get_api_info/', methods=['POST','GET'])
def get_api_info():
    if request.method == 'GET':
        api_id = request.args.get('api_id')
        print(api_id)
        api_info = json_file.get_api_id_data(api_id)
    return_data = api_info
    print(return_data)
    response_info = {"return_data":return_data,"api_id":api_id}
    return json.dumps(response_info)


#删除 指定API ID 的 API
#@ api_id
@app.route('/del_api/', methods=['POST','GET'])
def del_api():
    if request.method == 'GET':
        api_id = request.args.get('api_id')
        print(api_id)
        if json_file.del_api(api_id) == 1:
            return_data = "success"
        else:
            return_data = "fail"
    response_info = {"return_data":return_data,"api_id":api_id}
    return json.dumps(response_info)

# api 测试
@app.route('/api_test', methods=['POST','GET'])
def api_test():
    #return dbinit.db_test()
    '''
    code: 0为成功，非0为失败
    msg: 当code为非0时，获取错误信息。当code为0时，msg一般为”success”。
    data: 当code为0时，获取结果，全部以json方式表示。当code为非0时，data没有数据
    href : 接口访问路径

    '''
    data = {
      "href":  "/api_test",
      "code" : 0,
      "msg" : "success",
      "return_data" : {
                "api_test":"success",
                "api_test1":"success"
                }
        }
    return json.dumps(data)


#测试db库调用是否没问题
# db import test
@app.route('/db_test', methods=['POST','GET'])
def db_test():
	#return dbinit.db_test()
	data = {"api_name":"db_test",
			"Response":"ok"}
	return json.dumps(data)

@app.route('/db_init', methods=['POST','GET'])
def init_db_table():
    import api_funtion.table_init as sys_init
    return sys_init.init()

@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    # resp = Response(content)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    resp = Response_headers(content)
    return resp
    # return "error_code:400"

@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp

@app.route('/test1')
def test():
    session['key'] = 'test'
    return 'ok'


@app.route('/gettest1')
def default():
    return session.get('key', 'not set')    
    



if __name__ == '__main__':
    #man_sys_db.man_sys_db_reset()
    #man_sys_db.man_sys_db_ini()
    apicmd.start_man_api()
    app.run(host="0.0.0.0",port=9888,debug=True,threaded=True)