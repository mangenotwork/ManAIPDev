# -*- coding:utf8 -*-
#encoding = utf-8


from flask import Flask,request,g,render_template,redirect,url_for,abort
from flask import Blueprint , render_template
import sys,os

img = Blueprint('img',__name__)

#函数不能命名 test

# API 主界面	
@img.route('/img', methods=['POST','GET'])
def img_show():
	return "This is a Blueprint : img."