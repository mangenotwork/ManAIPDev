var api_path = 'http://127.0.0.1:9888'
//var api_path = 'http://192.168.2.122:9888'

//获取表名的 ajax 函数
function get_table_info(){ 
      $.ajax({
            url : api_path+'/show_table',//需要提交的Url地址 默认get方式 //
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){//如果调用php成功  
                  //alert(status); 
                  //alert(data);
                  //json 字符串转换为json数据
                  var table_data = JSON.parse(data);
                  //alert(table_data);
                  //alert(table_data[0]);
                  /*
                  $('#respones_api_test').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
                  */
                  $('#table_all_list').empty();
                  for(var i = 0;i<table_data.length; i++){
                      $('#table_all_list').append('<li><a href="#">[Table Name]: '+table_data[i]+'</a></li>');
                  }       
            }
        });
    }

//获取对象的Value值
 function getValue(obj){
        try{
            console.log(JSON.stringify(obj));
            return JSON.stringify(obj);
        }catch(ex){
            console.log('输入数据的格式存在错误');
        }

    }

 //获取对象所有的key值
     function getKeys(obj){
         //es6新语法   Object.prototype.toString方法精准判断参数值 属于哪种类型
         if(Object.prototype.toString.call(obj) === '[object Object]'){
             var arr = [];
             (function getKeysFn(o, char) {
                 for(var key in o){
                     //判断 对象的属性是否需要拼接'.',如果是第一层对象属性不拼接，否则拼接'.'
                     var newChar = char == '' ? key : char + '.' + key;

                     if (Object.prototype.toString.call(o[key]) === '[object Object]') {
                         // 如果属性对应的属性值仍为可分解的对象，使用递归函数继续分解，直到最里层
                         getKeysFn(o[key],newChar);

                     }else{

                         arr.push(newChar);
                     }
                 }

             })(obj, '')
             return arr;
         }else{
             console.log('Not Obj');
         }

    }



//获取所有的json对象数据
function getAllJson(jsons) {
  var get_return = []
  var get_data = [];
    for(key in jsons) {
        var k = key;
        get_data = [];
        if(!(jsons[key] instanceof Object)){
            console.log(k + " : " + jsons[key]); //如果不是Object则打印键值
            get_data.push(k);
            get_data.push(jsons[key]);
            get_return.push(get_data);
        }else{
            getAllJson(jsons[key]); //如果是Object则递归
        } 
    }
    console.log(get_return);
    return get_return;

};

//获取第二层的 json数据 并返回字符串
function getAllJson_str(jsons) {
  var str_data = '';
    for(key in jsons) {
        var k = key;
        if(!(jsons[key] instanceof Object)){
            //console.log(k + " : " + jsons[key]); //如果不是Object则打印键值
            str_data+='<br>        "'+k+'" : "'+jsons[key]+'",'
        }else{
            getAllJson_str(jsons[key]); //如果是Object则递归
        } 
    }
    //console.log(str_data);
    return str_data;

};

// ajax get 通用方法
function get_api_ajax(obj){
  $.ajax({
            url : api_path+'/'+obj.id,//需要提交的Url地址 默认get方式 //
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){
                  var get_datas = JSON.parse(data);
                  //getAllJson(get_datas.return_data);
                  //var a = getValue(get_datas.return_data.api_test);
                  //var b = getKeys(get_datas.return_data)
                  //alert(a);
                  var jsons_data = getAllJson_str(get_datas.return_data);
                  jsons_data=jsons_data.substring(0,jsons_data.length-1);
                  var respones_info = '{<br>    "status" : "'+status+'",<br>    "API_type" : "GET",<br>    "href" : "'+get_datas.href+
                                      '",<br>    "code" : "'+get_datas.code+'",<br>    "msg" : "'+get_datas.msg+'",<br>    "data" : {'+
                                      jsons_data+'<br>    }<br>}';
                  var respones_id = '#respones_'+obj.id
                  $(respones_id).html(respones_info);
            }
        });
}


// ajax get 通用方法 2
function get_api_ajax2(api_url,Func){
  $.ajax({
            url : api_path+'/'+api_url,//需要提交的Url地址 默认get方式 //
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){
                  if(Func){
                    Func(data);
                  }
                  else{
                    alert(status);
                    alert(data);
                  }
            }
        });
}

// ajax post 通用方法
function post_api_ajax(obj,Func){
  //alert(obj.id);
  var from_data = '#'+obj.id+'_Form';
  //alert(from_data);
  console.log("from_data = "+from_data);
  console.log($(from_data).serialize());
  //alert($(from_data).serialize());
  $.ajax({  
            beforeSend: function(xhr) {
              xhr.setRequestHeader("Access-Toke");
             },
             headers: {
                 'Access-Token':$.cookie('man_token')
             },
            url : api_path+'/'+obj.id,//需要提交的Url地址 默认get方式 //
            type: "POST",
            data: $(from_data).serialize(),
            async : true,// true 设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            //dataType: "json",
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },

                 
            success: function(data,status){
                  //alert(status);
                  //alert(data);
                  if(Func){
                    Func(data);
                  }
                  else{
                    alert(data);
                  }
                  /*
                  
                  //getAllJson(get_datas.return_data);
                  //var a = getValue(get_datas.return_data.api_test);
                  //var b = getKeys(get_datas.return_data)
                  //alert(a);
                  var jsons_data = getAllJson_str(get_datas.return_data);
                  jsons_data=jsons_data.substring(0,jsons_data.length-1);
                  var respones_info = '{<br>    "status" : "'+status+'",<br>    "API_type" : "GET",<br>    "href" : "'+get_datas.href+
                                      '",<br>    "code" : "'+get_datas.code+'",<br>    "msg" : "'+get_datas.msg+'",<br>    "data" : {'+
                                      jsons_data+'<br>    }<br>}';
                  var respones_id = '#respones_'+obj.id
                  $(respones_id).html(respones_info);
                  */
            }
        });
}


// ajax post 通用方法2
function post_api_ajax2(obj,Func){
  var from_data = '#'+obj.id;
  console.log($(from_data).serialize());
  $.ajax({
            url : api_path+'/'+obj.id,//需要提交的Url地址 默认get方式 //
            type: "POST",
            data: $(from_data).serialize(),
            async : true,// true 设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            //dataType: "json",
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },   
            success: function(data,status){
                  if(Func){
                    Func(data);
                  }
                  else{
                    alert(data);
                  }
            }
        });
}



// ajax post 通用方法3
function post_api_ajax3(ids,url_data,Func){
  var from_data = '#'+ids;
  console.log($(from_data).serialize());
  $.ajax({
            url : api_path+'/'+url_data,//需要提交的Url地址 默认get方式 //
            type: "POST",
            data: $(from_data).serialize(),
            async : true,// true 设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            //dataType: "json",
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },   
            success: function(data,status){
                  if(Func){
                    Func(data);
                  }
                  else{
                    alert(data);
                  }
            }
        });
}

//添加 api ajax请求
function add_api_ajax(obj){
  //alert(obj.id);
  var from_data = '#'+obj.id+'_Form';
  //alert(from_data);
  console.log($(from_data).serialize());

  $.ajax({
            url : api_path+'/'+obj.id,//需要提交的Url地址 默认get方式 //
            type: "POST",
            data: $(from_data).serialize(),
            async : true,// true 设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            //dataType: "json",
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
                alert("add_api_ajax Error");
            },

                 
            success: function(data,status){
                  //alert(status);
                  //alert(data)
                  var get_datas = JSON.parse(data);
                  //alert(get_datas.return_data);
                  if(get_datas.return_data == 'success'){
                    alert('add api success.');
                    colse_Modal();
                    window.location.reload();
                  }
            }
        });
}

//删除 api 
function del_api_ajax(obj){
  //alert("Del : "+obj.id);
  var get_api_id = obj.id.split('_');
  get_api_id.splice(get_api_id.length-1,get_api_id.length);
  var api_id = get_api_id.join('_')
  var se=confirm("是否要删除 API : "+api_id);
  if (se==true)
    {
    //alert("/del_api?api_id="+api_id);
     $.ajax({
            url : api_path+"/del_api?api_id="+api_id,//需要提交的Url地址 默认get方式 //
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){
                  //alert(status);
                  //alert(data)
                  var get_datas = JSON.parse(data);
                  if(get_datas.return_data == 'success'){
                    alert('Del API ID = ['+get_datas.api_id+'] Success.');
                    colse_Modal();
                    window.location.reload();
                  }
            }
        });
    }
  else
    {
    //alert("你按下的是【取消】");
    }
}




$(function(){

  /*  
  //长轮询
    var getting = {

        url:api_path+'/get_db_conn_user',

        dataType:'json',

        success:function(res) {

         console.log(res);

         $.ajax(getting); //关键在这里，回调函数内再次请求Ajax

      }        
              //当请求时间过长（默认为60秒），就再次调用ajax长轮询
              error:function(res){
              $.ajax($getting);
              }

      };

      $.ajax(getting);
    */

    //短轮询
      var getting = {

        url : api_path+'/get_db_conn_user',

        dataType : 'json',

        success : function(res) {
          $("#db_state").empty();
         console.log(res);
         if(res){
            $("#db_state").css("color","#7FFF00");
            $("#db_state").append("user name: [ "+res+" ]");
         }
         else{
          $("#db_state").css("color","red");
          $("#db_state").append("连接失败");
         }
        }

      };


  
  window.onload=function (){

    $.ajax(getting);

}
  //关键在这里，Ajax定时访问服务端，不断获取数据 ，这里是60秒请求一次。
  window.setInterval(function(){$.ajax(getting)},60000);

    //connect_test ajax 请求  get
    $("#api_test_ajax").bind("click",function(){ 
      $.ajax({
            url : api_path+'/api_test',//需要提交的Url地址 默认get方式 //就是这行
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){//如果调用php成功  
                  //alert(status); 
                  //alert(data);
                  $('#respones_api_test').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
            }
        });
    });


    //db_connect_test 连接数据库
    $("#db_connect_test_ajax").click(function(){
      alert("db_connect_test_ajax");
        /*
          $.ajax({
               url: "api/api.php", 
               type: "POST",
               data:{
                //方式一  在标签加入 api字段来设置默认参数传递
                //api_id:$('#verify_adduser_data').attr("api"),
                //方式二 构造默认参数
                api_id:"verify_add_user",
                user_data:$("#verify_adduser_data").val()
                //数据加密方案  js 加密 php 解密
                },
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_verify_adduser').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_verify_adduser').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
          */
      });

    var wite_time = '<img id="wite_img" src="../static/man_api_img/wite.gif">'
   //connect_db 连接数据库
      $("#connect_db_ajax").click(function(){
        //alert("connect_db_ajax");
          $("#connect_db_return").empty();
          $("#connect_db_input").hide();
          $("#connect_db_input_wite").append(wite_time);
            $.ajax({
                 url: api_path+'/api_conn_db',
                 type: "POST",
                 data:{
                  //方式一  在标签加入 api字段来设置默认参数传递
                  //api_id:$('#verify_adduser_data').attr("api"),
                  //方式二 构造默认参数
                  host_data:$("#conn_host").val(),
                  port_data:$("#conn_port").val(),
                  db_name_data:$("#conn_db_name").val(),
                  acc_data:$("#conn_db_acc").val(),
                  password_data:$("#conn_db_password").val()
                  //数据加密方案  js 加密 php 解密
                  },
                 async : true,//默认设置下，所有请求均为异步请求
                 cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
                 dataType: "json",
                 
                 success: function(data,status){  
                    $("#connect_db_input").show();
                    $("#wite_img").remove();
                  /*
                    $('#respones_verify_adduser').html(
                    "请求状态 ： "+status+"<br>"+
                    "返回结果 ： "+data);
                    */
                    /*
                    alert(status);
                    alert(data);
                    */
                    console.log(status);
                    console.log(data);
                    //alert(data);
                    
                    if(data=='db connect succeed.'){
                      $("#connect_db_return").append('<span style="color: #7FFF00;">'+data+'</span>');
                      $.ajax(getting);
                    }
                    else{
                      $("#connect_db_return").append('<span style="color: red;">'+data+'</span>');
                    }
                    get_table_info();
                 },
                 /*
                 error:function(jqXHR,textStatus,errorThrown){
                    console.log(jqXHR);
                    console.log(textStatus);
                    console.log(errorThrown);
                  }
                  */
                  error:function(jqXHR){
                    $("#connect_db_input").show();
                    $("#wite_img").remove();
                    console.log(jqXHR);
                    alert(jqXHR);
                    alert("connect_db_input Error");
                  }
            }); 
            
        });


    

      

    //connect_test ajax 请求  get
    $("#connect_test").bind("click",function(){ 
      $.ajax({
            url : api_path+'/db_test',//需要提交的Url地址 默认get方式 //就是这行
            type: "GET",
            async : true,//默认设置下，所有请求均为异步请求
            cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
            dataType : 'text',//数据类型
            //错误回调函数
            error : function(xhr) {
                alert('请求状态： 错误:' + xhr.responseText);
            },
            success: function(data,status){//如果调用php成功  
                  //alert(status); 
                  //alert(data);
                  $('#respones_connect_test').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
            }
        });
    });

    
    //create_table_sys_user ajax 请求 get
    $("#create_table_sys_user").bind("click",function(){ 
      alert('create_table_sys_user ok');
      $.ajax({
            url : 'api/api.php?api=create_table_sys_user',
            type: "GET",
            async : true,
            cache : false,
            dataType : 'text',
            error : function(xhr) {
                alert('错误:' + xhr.responseText);
            },
            success: function(data,status){
                  $('#respones_create_table_sys_user').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
            }
        });
    });


    //get_user ajax 请求 get
      $("#get_user").click(function(){
          var seek_info = $("#user_seek").val();
          alert(seek_info);
          $.ajax({
               url: "api/api.php?api=get_user&seek="+seek_info, 
               type: "GET",
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "text",
               error: function(){   
                  $('#respones_get_user').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_get_user').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });

    //verification_add_user ajax 请求 post
    $("#verify_adduser").click(function(){
      alert("verify_adduser");
      
          $.ajax({
               url: "api/api.php", 
               type: "POST",
               data:{
                //方式一  在标签加入 api字段来设置默认参数传递
                //api_id:$('#verify_adduser_data').attr("api"),
                //方式二 构造默认参数
                api_id:"verify_add_user",
                user_data:$("#verify_adduser_data").val()
                //数据加密方案  js 加密 php 解密
                },
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_verify_adduser').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_verify_adduser').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


    //add_user ajax 请求 post
    $("#add_user").click(function(){
      alert("add_user");
      
          $.ajax({
               url: "api/api.php", 
               type: "POST",
               data:{
                api_id:"add_user",
                user_data:$("#adduser_data").val()
                },
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_add_user').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_add_user').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


    //sys_log ajax 请求 get
    $("#sys_log").click(function(){
      alert("sys_log");
      
          $.ajax({
               url: "api/api.php?api=sys_log", 
               type: "GET",
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_sys_log').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_sys_log').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


    //add_user ajax 请求 post
    $("#change_user_info").click(function(){
      alert("change_user_info");
      
          $.ajax({
               url: "api/api.php", 
               type: "POST",
               data:{
                api_id:"change_user_info",
                user_data:$("#update_user_data").val()
                },
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_change_user').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_change_user').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


    //delete_user ajax 请求 post
    $("#delete_user").click(function(){
      alert("delete_user");
      
          $.ajax({
               url: "api/api.php", 
               type: "POST",
               data:{
                api_id:"delete_user",
                user_data:$("#assign_user").val()
                },
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_delete_user').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_delete_user').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


     //sys_log ajax 请求 get
    $("#get_table_info").click(function(){
      var table_name = $("#table_name").val();
      alert(table_name);
      
          $.ajax({
               url: "api/api.php?api=get_table_info&table="+table_name, 
               type: "GET",
               async : true,//默认设置下，所有请求均为异步请求
               cache : false, //设置为 false 将不会从浏览器缓存中加载请求信息。
               dataType: "json",
               error: function(){   
                  $('#respones_get_table_info').html('Error loading XML document');   
               },
               success: function(data,status){  
                  $('#respones_get_table_info').html(
                  "请求状态 ： "+status+"<br>"+
                  "返回结果 ： "+data);
               }
          }); 
      });


});