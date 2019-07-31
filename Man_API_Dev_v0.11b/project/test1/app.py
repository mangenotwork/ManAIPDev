#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man'

from flask import Flask
from flask import Flask,request,g,render_template,redirect,url_for,abort,session
from flask import make_response,Response  
import sys,os
import json
import time
from datetime import datetime,timedelta

Project_Name = "test1"
Project_Port = 9001

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

def Response_headers(content):
	resp = Response(content)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

# Project Man API 测试.
@app.route('/', methods=['POST','GET'])
def index():
	return "<h1>Man API.</h1><hr><h2>hello "+Project_Name+" Flask.</h2>"

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
    resp = Response_headers(content)
    return resp

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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=Project_Port,threaded=True)