#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 

import os,sys,re
import time
import subprocess
try:
    import man_file
except:
    import man_api.man_file as man_file


Man_API_Path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


Project_Path = Man_API_Path+"/File_storage_center/"
#print(Project_Path)



Python_cmd = "python "

project_state_ini_file = Man_API_Path+"/static/ini_file/project_state.ini"
project_list_ini_file = Man_API_Path+"/static/ini_file/project_list.ini"
temp_cmd_pid = Man_API_Path+"/static/ini_file/temp_cmd_pid.temp"


#状态ini
state = man_file.Ini_File_Man(project_state_ini_file)
#项目ini
project_list = man_file.Ini_File_Man(project_list_ini_file)
#cmd.exe pid temp
cmd_temp_file = man_file.Man_File_handle(temp_cmd_pid)


test_1_py = "D:/py_test/yibiao_Auto/test_case/test_1.py"
args = "python "+test_1_py
args1 = "ping 8.8.8.8 "

#杀掉进程
def kill(pid):
    try:
        #kill_p = subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i"%pid , shell=True)
        kill_p = subprocess.Popen("taskkill /PID %i -t -f"%pid , shell=True)
        #print("[debug] ++++ PID ++++ = "+str(kill_p.pid))
        time.sleep(1)
        kill_p.kill()
        return 'kill pass'
    except:
        #print('no process')
        return 'no process'

#运行 py 文件
def open_py(args):
    open_py_p = subprocess.Popen(args, shell=True)
    #print("Run "+str(args)+" PID : "+str(open_py_p.pid))
    #print("[debug] ++++ PID ++++ = "+str(open_py_p.pid))
    #all_line = open_py_p.stdout.read()
    #print("[PID Debug] open_py() = "+all_line.decode('utf-8'))
    time.sleep(1)
    open_py_p.kill()
    return open_py_p.pid







#获取指定端口的 pid 状态
def getport(port):
    #print("[Debug] port = "+str(port))
    cmd = 'netstat -ano | findstr :"'+str(port)+'"'
    getport_p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE )
    #print("[debug] ++++ PID ++++ = "+str(getport_p.pid))
    #print("Run "+str(args)+" PID : "+str(getport_p.pid))
    line = getport_p.stdout.readline()
    #print(line)
    time.sleep(1)
    getport_p.kill()
    if "TIME_WAIT" in str(line):
        print("TIME_WAIT")
        return "timewait"
    elif line == b'':
        print("not find port")
        return "notopen"
    else:
        print("open")
        return "open"


#获取指定端口的 pid
def get_pid(port):
    #print("[Debug] port = "+str(port))
    cmd = 'netstat -ano | findstr :"'+str(port)+'"'
    p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE )
    #print("[debug] ++++ PID ++++ = "+str(p.pid))
    #print("Run "+str(args)+" PID : "+str(p.pid))
    line = p.stdout.readline()
    all_line = p.stdout.read()
    #print("[PID Debug] get_pid() = "+all_line.decode('utf-8'))
    print(line)
    time.sleep(1)
    p.kill()
    if "TIME_WAIT" in str(line):
        print("TIME_WAIT")
        return "timewait"
    elif line == b'':
        print("not find port")
        return "notopen"
    else:
        print("open")
        cmd_return_data = line.decode('utf-8')
        #cmd_return_data = str(line)
        
        str_list = cmd_return_data.split(" ")
        #print(str_list)
        while '' in str_list:
            str_list.remove('')
        print(str_list[-1].strip('\r\n'))
        pid_number = str_list[-1].strip('\r\n')
        return pid_number


#打开指定 名称 project 项目
def open_project(project_name):
    print(Project_Path+project_name+"/Master/"+project_name+"/app.py")
    open_project_flask = Project_Path+project_name+"/Master/"+project_name+"/app.py"
    pid_number = open_py(open_project_flask)

    port_number = project_list.get_section_item_value(project_name,"port")
    #print(port_number)

    #将 启动项目的 PID写入临时 ini
    #清除启动名称 PID标记
    #state.del_option("DEFAULT",project_name)
    #写入启动项目名称的PID标记
    #state.add_a_data("DEFAULT",project_name,str(pid_number))

    time.sleep(2)
    return getport(port_number)
    #检查 state DEFAULT 有没有 project_name
    #如果没有就添加
    #如果有就更新
    #state.add_a_data("DEFAULT",project_name,str(pid_number))
    #print(port_number)
    
    #return pid_number


#开机调用初始化 项目启动 PID 标记
def project_state_ini():
    all_project_list = project_list.get_all_sections()
    for project_name_vlue in all_project_list:
        print(project_name_vlue)
        state.del_option("DEFAULT",project_name_vlue)

#项目关机
def off_project(project_name):
    port_number = project_list.get_section_item_value(project_name,"port")
    pid_number = get_pid(port_number)
    time.sleep(1)
    if pid_number == 'timewait':
        return 'timewait'
    elif pid_number == 'notopen':
        return 'notopen'
    time.sleep(1)
    killok = kill(int(pid_number))
    state.del_option("DEFAULT",project_name)
    return killok
#off_project('test1')
#open_project("test1")
#get_pid(9001)


#获取当前所有项目的状态
def get_all_project_state():
    #time.sleep(1)
    state_dict = {}
    all_project_list = project_list.get_all_sections()
    for project_name_vlue in all_project_list:
        #getport(project_name_vlue)
        port_number = project_list.get_section_item_value(project_name_vlue,"port")
        state_dict.update({project_name_vlue:getport(port_number)})
    print(state_dict)
    return state_dict

#get_all_project_state()


def get_cmd_pid_re(strings):
    reg = r"cmd.exe (.+?) Console"
    reger = re.compile(reg)
    data = re.findall(reger, strings)
    return data


def new_cmd_pid(list1,list2):
    print("list1 = "+str(list1))
    print("list2 = "+str(list2))
    print(set(list1)^set(list2))
    new_list = set(list1)^set(list2)
    if new_list != []:
        for p in new_list:
            print(p)
            kill(p)


def set_cmd_pid():
    pass

#获取 cmd.exe 进程
def get_cmd_pid():
    #读取之前记录的所有cmd pid
    load_cmd_pid_data = cmd_temp_file.read_all_data()
    load_cmd_pid_list = load_cmd_pid_data[0].split(',')
    return_cmd_list = []
    cmd = 'tasklist | findstr "cmd.exe"'
    get_cmd_pid_p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE )
    line = get_cmd_pid_p.stdout.read()
    print("*********** ---- CMD.exe PID ---- ***********")
    cmd_return_data = line.decode('utf-8')
    cmd_pid_list = get_cmd_pid_re(cmd_return_data)
    #print(cmd_pid_list)
    for cmd_i in cmd_pid_list:
        return_cmd_list.append(cmd_i.strip())
    #print(return_cmd_list)
    time.sleep(2)
    #pid对比处理
    new_cmd_pid(load_cmd_pid_list,return_cmd_list)

    sve_cmd_pid = ','.join(return_cmd_list)
    print(sve_cmd_pid)
    #写入当前所有 cmd pid
    cmd_temp_file.write_file_all_data(sve_cmd_pid)
    print("*********** ---- ^^^^^^^^^^^ ---- ***********")
    time.sleep(1)
    get_cmd_pid_p.kill()





#开启 Redis
def start_redis():
    Redis_path = Man_API_Path+"\\Redis-x64-3.2.100\\"
    start_redis_cmd = Redis_path+"redis-server.exe "+Redis_path+"redis.windows.conf"
    print(start_redis_cmd)
    open_py(start_redis_cmd)


def start_man_api():
    print(" ______________________________________________________________________")
    print(" __  __                         _____ _____    _____  ________      __   ")
    print("|  \/  |                  /\   |  __ \_   _|  |  __ \|  ____\ \    / /   ")
    print("| \  / | __ _ _ ___      /  \  | |__) || |    | |  | | |__   \ \  / /    ")
    print("| |\/| |/ _` | '_  \    / /\ \ |  ___/ | |    | |  | |  __|   \ \/ /     ")
    print("| |  | | (_| | | | |   / ____ \| |    _| |_   | |__| | |____   \  /      ")
    print("|_|  |_|\__,_|_| |_|  /_/    \_\_|   |_____|  |_____/|______|   \/       ")
                                                                    
    print(" ______________________________________________________________________")
    print("     ************************ V1.0 **********************")
    print("     --> 启动Redis...")
    #time.sleep(1)
    start_redis()
    print("     --> 启动flask")
    #time.sleep(2)
#start_man_api()
