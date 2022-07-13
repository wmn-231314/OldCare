# -*-coding:UTF-8 -*-
import functools
import random
import sys
import urllib

import jwt
import datetime
from jwt import exceptions
from flask import Flask, render_template, request, jsonify, session, Response ,g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from pydantic import BaseModel, Field
from itsdangerous import TimedSerializer as Serializer

import base64
import time
import json
import os

from sqlalchemy.ext.serializer import Serializer
from werkzeug.utils import redirect
from models.models import *
from response import *





# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(__name__)
app.config['SECRET_KEY'] = 'old_care_flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:QSW129255956zyx@rm-uf6m16l5w58qx6lemho.mysql.rds.aliyuncs.com:3306/old_care_flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:63637072@localhost:3306/old_care_flask'
# 每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



# 设置跨域
# CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')

# 构造header
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

# 密钥
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='


@app.route("/")
def root():
    """
    rootindex
    :return: Index.html
    """
    return render_template('index.html')

# @app.before_request
# def is_login():
#     """
#         1.获取请求头Authorization中的token
#         2.判断是否以 Bearer开头
#         3.使用jwt模块进行校验
#         4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
#         """
#     token = request.headers.get('token')
#     print("token:%s" %token)
#     if token:
#         g.username = None
#         try:
#             "判断token的校验结果"
#             payload = jwt.decode(token, SALT, algorithms=['HS256'])
#             "获取载荷中的信息赋值给g对象"
#             g.username = payload.get('username')
#         except exceptions.ExpiredSignatureError:  # 'token已失效'
#             g.username = 1
#         except jwt.DecodeError:  # 'token认证失败'
#             g.username = 2
#         except jwt.InvalidTokenError:  # '非法的token'
#             g.username = 3
#         print("username:%s" %g.username)
#
# def verify_jwt(token, secret=None):
#     """
#     检验jwt
#     :param token: jwt
#     :param secret: 密钥
#     :return: dict: payload
#     """
#     if not secret:
#         secret = app.config['JWT_SECRET']
#
#     try:
#         payload = jwt.decode(token, secret, algorithms=['HS256'])
#         return payload
#     except exceptions.ExpiredSignatureError:  # 'token已失效'
#         return 1
#     except jwt.DecodeError:  # 'token认证失败'
#         return 2
#     except jwt.InvalidTokenError:  # '非法的token'
#         return 3
#
#
# def login_required(f):
#     '让装饰器装饰的函数属性不会变 -- name属性'
#     '第1种方法,使用functools模块的wraps装饰内部函数'
#
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         try:
#             print("wrapper username:%s" % g.username)
#             if g.username == 1:
#                 return {'code': 4001, 'message': 'token已失效'}, 401
#             elif g.username == 2:
#                 return {'code': 4001, 'message': 'token认证失败'}, 401
#             elif g.username == 2:
#                 return {'code': 4001, 'message': '非法的token'}, 401
#             else:
#                 print("这里")
#                 return f(*args, **kwargs)
#         except BaseException as e:
#             return {'code': 4001, 'message': '请先登录认证.'}, 401
#     return wrapper


@app.route("/homePage_data", methods=['GET'])
# @login_required
def get_homePage_Data():
    sql_number_oldPeople = "SELECT COUNT(*) FROM oldperson_info"
    sql_number_gender = "SELECT COUNT(case when oldperson_info.gender='male' then oldperson_info.gender end) as 'male', " \
                        "COUNT(case when oldperson_info.gender='female' then oldperson_info.gender end) as 'female' " \
                        "FROM oldperson_info"
    sql_numberOfNew_oldPeople = "SELECT COUNT(*) FROM oldperson_info WHERE DATE(oldperson_info.checkin_date)=CURDATE()"
    sql_number_volunteer = "SELECT COUNT(*) FROM volunteer_info"
    sql_numberOfActive_volunteer = "SELECT COUNT(*) FROM volunteer_info WHERE ISACTIVE='Yes'"
    sql_number_emotion = "SELECT COUNT(case when event_info.event_desc='anger' then event_info.event_desc end) as 'anger', " \
                         "COUNT(case when event_info.event_desc='disgust' then event_info.event_desc end) as 'disgust'," \
                         "COUNT(case when event_info.event_desc='fear' then event_info.event_desc end) as 'fear'," \
                         "COUNT(case when event_info.event_desc='happiness' then event_info.event_desc end) as 'happiness'," \
                         "COUNT(case when event_info.event_desc='neutral' then event_info.event_desc end) as 'neutral'," \
                         "COUNT(case when event_info.event_desc='sadness' then event_info.event_desc end) as 'anger'," \
                         "COUNT(case when event_info.event_desc='surprise' then event_info.event_desc end) as 'surprise' " \
                         "FROM event_info WHERE event_info.event_type=0 AND DATE(event_info.event_date)=CURDATE()"
    sql_number_fall = "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 DAY) AND CURDATE() then event_info.event_date end) as 'within_four_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 4 DAY) AND CURDATE() then event_info.event_date end) as 'within_five_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 5 DAY) AND CURDATE() then event_info.event_date end) as 'within_six_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 6 DAY) AND CURDATE() then event_info.event_date end) as 'within_seven_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND CURDATE() then event_info.event_date end) as 'within_eight_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 8 DAY) AND CURDATE() then event_info.event_date end) as 'within_nine_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 9 DAY) AND CURDATE() then event_info.event_date end) as 'within_ten_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 10 DAY) AND CURDATE() then event_info.event_date end) as 'within_eleven_days', "\
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 11 DAY) AND CURDATE() then event_info.event_date end) as 'within_twelve_days', " \
                      "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 12 DAY) AND CURDATE() then event_info.event_date end) as 'within_thirteen_days' " \
                      "FROM event_info WHERE event_info.event_type=3"
    sql_number_intrusion = "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 DAY) AND CURDATE() then event_info.event_date end) as 'within_four_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 4 DAY) AND CURDATE() then event_info.event_date end) as 'within_five_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 5 DAY) AND CURDATE() then event_info.event_date end) as 'within_six_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 6 DAY) AND CURDATE() then event_info.event_date end) as 'within_seven_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND CURDATE() then event_info.event_date end) as 'within_eight_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 8 DAY) AND CURDATE() then event_info.event_date end) as 'within_nine_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 9 DAY) AND CURDATE() then event_info.event_date end) as 'within_ten_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 10 DAY) AND CURDATE() then event_info.event_date end) as 'within_eleven_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 11 DAY) AND CURDATE() then event_info.event_date end) as 'within_twelve_days', " \
                           "COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 12 DAY) AND CURDATE() then event_info.event_date end) as 'within_thirteen_days' " \
                           "FROM event_info WHERE event_info.event_type=2 OR event_info.event_type=4"


    number_oldPeople = db.session.execute(sql_number_oldPeople).all()
    number_gender = db.session.execute(sql_number_gender).all()
    numberOfNew_oldPeople = db.session.execute(sql_numberOfNew_oldPeople).all()
    number_volunteer = db.session.execute(sql_number_volunteer).all()
    numberOfActive_volunteer = db.session.execute(sql_numberOfActive_volunteer).all()
    number_emotion = db.session.execute(sql_number_emotion).all()
    emotion_dic = {'anger':number_emotion[0][0], 'disgust':number_emotion[0][1], 'fear':number_emotion[0][2], 'happiness':number_emotion[0][3],
                 'neutral':number_emotion[0][4], 'sadness':number_emotion[0][5], 'surprise':number_emotion[0][6]}
    number_fall = db.session.execute(sql_number_fall).all()
    fall_dic = {'within_four_days':number_fall[0][0],'within_five_days':number_fall[0][1],'within_six_days':number_fall[0][2],
                'within_seven_days':number_fall[0][3],'within_eight_days':number_fall[0][4],'within_nine_days':number_fall[0][5],
                'within_ten_days':number_fall[0][6],'within_eleven_days':number_fall[0][7],'within_twelve_days':number_fall[0][8],
                'within_thirteen_days':number_fall[0][9]}
    number_intrusion = db.session.execute(sql_number_intrusion).all()
    intrusion_dic = {'within_four_days':number_intrusion[0][0],'within_five_days':number_intrusion[0][1],'within_six_days':number_intrusion[0][2],
                'within_seven_days':number_intrusion[0][3],'within_eight_days':number_intrusion[0][4],'within_nine_days':number_intrusion[0][5],
                'within_ten_days':number_intrusion[0][6],'within_eleven_days':number_intrusion[0][7],'within_twelve_days':number_intrusion[0][8],
                'within_thirteen_days':number_intrusion[0][9]}

    result = {"number_oldPeople": number_oldPeople[0][0], "male_OldPeople": number_gender[0][0],
              "female_OldPeople": number_gender[0][1],
              "numberOfNew_oldPeople": numberOfNew_oldPeople[0][0], "number_volunteer": number_volunteer[0][0],
              "numberOfActive_volunteer": numberOfActive_volunteer[0][0], 'emotion':emotion_dic,
              "fall":fall_dic, "intrusion":intrusion_dic}
    response = DataResponse(code=200, data=result, msg="Success get the data of home page!")
    response = json.dumps(response.__dict__)

    return response

# 系统管理员注册部分 即添加
@app.route('/register', methods=['POST'])
def add_sys_usr():
    body = request.json
    if SysUser.query.filter_by(UserName=body['username']).first():

        response = BaseResponse(code=412, msg='The administrator information already exists, cannot be entered repeatedly!')

    else:
        sys_usr = SysUser(UserName=body['username'], Password=body['password'], )
        db.session.add(sys_usr)
        print("add success")

        response = BaseResponse(code=200, msg="Succeed to register")
    response = json.dumps(response.__dict__)

    return response


# 系统管理员登录逻辑处理
@app.route('/login', methods=['POST'])
def login():
    body = request.json
    user_name = body['username']
    password = body['password']

    for result in SysUser.query.filter_by(UserName=user_name).all():
        if password == result.to_json()['password']:
            session['sys_user_id'] = result.to_json()['id']
            session['sys_user_name'] = result.to_json()['userName']
            token={'token':generate_token(user_name, password)}
            response = DataResponse(code=200, data=token, msg="Match and token has sent!")
            response = json.dumps(response.__dict__)
            return response
        else:
            continue

    response = BaseResponse(code=412, msg="Not match")
    response = json.dumps(response.__dict__)
    return response

# 获取所有老人信息
@app.route('/table_oldPerson', methods=['GET'])
# @login_required
def get_old_person_info():
    result_list = []
    sql = 'SELECT username, profile_photo, id_card, gender, room_number, checkin_date FROM oldPerson_info'
    for result in db.session.execute(sql):
        with open(result[1], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'username': result[0], 'photo': encode_str, 'id_card': str(result[2]),
                           'gender': result[3], 'room_num': result[4], 'checkin_date': str(result[5])}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to select all old persons!')
    response = json.dumps(response.__dict__)

    return response


# 添加老人信息
@app.route('/addOldPersonInfo', methods=['POST'])
# @login_required
def add_old_person_info():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    idCard_info = json.loads(identify_id_card(body['idCard_photo_base64']))['cards'][0]

    if OldPersonInfo.query.filter_by(id_card=idCard_info['id_card_number']).first():

        response = BaseResponse(code=412, msg='The elderly information already exists, cannot be entered repeatedly!')

    else:
        old_person = OldPersonInfo(username=idCard_info['name'], gender=idCard_info['gender'], phone=body['phone'],
                                   id_card=idCard_info['id_card_number'], birthday=idCard_info['birthday'],
                                   checkin_date=body['checkin_date'],checkout_date=body['checkout_date'], room_number=body['room_number'], CREATED=current_time)
        db.session.add(old_person)
        db.session.commit()

        response = BaseResponse(code=200, msg='Succeed to insert one old person!')

    response = json.dumps(response.__dict__)

    return response


# 删除老人信息
@app.route('/deleteOldPerson', methods=['POST'])
# @login_required
def delete_old_person():
    body = request.json
    old_person = OldPersonInfo(ID=body['id'], username=body['username'])
    db.session.delete(old_person)
    db.session.commit()

    response = BaseResponse(code=200, msg="Succeed to delete one old person!")
    response = json.dumps(response.__dict__)

    return response


# 修改老人信息
@app.route('/updateOldPerson', methods=['POST'])
# @login_required
def update_old_person():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    OldPersonInfo.query.filter_by(ID=body['id']).update({'username': body['userName'], 'UPDATED': current_time})
    db.session.commit()

    response = BaseResponse(code=200, msg="Succeed to update old person!")
    response = json.dumps(response.__dict__)

    return response


# 获取所有义工信息
@app.route('/table_volunteer', methods=['GET'])
# @login_required
def get_volunteer():
    result_list = []
    sql = "SELECT `name`, profile_photo, id_card, gender, phone, ISACTIVE FROM volunteer_info"
    for result in db.session.execute(sql):
        with open(result[1], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'username': result[0], 'photo': encode_str, 'id_card': str(result[2]),
                           'gender': result[3], 'phone': result[4], 'is_active': str(result[5])}
        result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to select all old persons!')
    response = json.dumps(response.__dict__)

    return response


# 添加一个新的义工
@app.route('/addVolunteer', methods=['POST'])
# @login_required
def add_volunteer():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    idCard_info = json.loads(identify_id_card(body['idCard_photo_base64']))['cards'][0]

    if VolunteerInfo.query.filter_by(id_card=idCard_info['id_card_number']).first():

        response = BaseResponse(code=412, msg='The volunteer information already exists, cannot be entered repeatedly!')

    else:
        volunteer = VolunteerInfo(name=idCard_info['name'], gender=idCard_info['gender'], phone=body['phone'],
                                  id_card=idCard_info['id_card_number'],birthday=idCard_info['birthday'], checkin_date=body['checkin_date'],
                                  checkout_date=body['checkout_date'], ISACTIVE=body['isActive'], CREATED=current_time)
        db.session.add(volunteer)
        db.session.commit()

        response = BaseResponse(code=200, msg="Succeed to insert one volunteer!")
    response = json.dumps(response.__dict__)

    return response


# 获取某种类型事件发生的所有记录
@app.route('/table_events', methods=['GET'])
# @login_required
def get_events():
    body = request.json
    result_list = []
    for result in EventInfo.query.filter_by(event_type=body['eventType']).all():
        result_list.append(result.to_json())

    response = DataResponse(code=200, data=result_list, msg='Succeed to get specific events!')
    response = json.dumps(response.__dict__)

    return response


# 老人情感检测数据
@app.route('/table_facial_expression', methods=['GET'])
# @login_required
def get_facial_expression():
    result_list = []

    sql = "SELECT oldperson_id,username, event_location, event_date, event_desc, event_image_dir FROM oldPerson_info, event_info WHERE event_info.oldperson_id = oldPerson_info.ID AND event_type=0"

    for result in db.session.execute(sql):
        with open(result[5], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'oldperson_id':result[0],'userName': result[1], 'eventLocation': result[2], 'eventDate': str(result[3]),
                           'eventDesc': result[4], 'eventPhoto': encode_str}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to get facial expression events!')
    response = json.dumps(response.__dict__)

    return response


# 获取区域入侵检测异常数据
@app.route('/table_instrusion', methods=['GET'])
# @login_required
def get_intrusion():
    result_list = []

    sql = "SELECT event_location, event_date, event_image_dir FROM event_info WHERE event_type=4"

    for result in db.session.execute(sql):
        with open(result[2], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'eventLocation': result[0], 'eventDate': str(result[1]), 'eventPhoto': encode_str}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to get intrusion events!')
    response = json.dumps(response.__dict__)

    return response


# 获取老人摔倒检测数据
@app.route('/table_fall', methods=['GET'])
# @login_required
def get_fall():
    result_list = []

    sql = "SELECT event_location, event_date, event_image_dir FROM event_info WHERE event_type=3"

    for result in db.session.execute(sql):
        with open(result[2], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'eventLocation': result[0], 'eventDate': str(result[1]), 'eventPhoto': encode_str}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to get fall events!')
    response = json.dumps(response.__dict__)

    return response


# 获取老人与护工交互检测异常数据
@app.route('/table_interaction', methods=['GET'])
# @login_required
def get_interaction():
    result_list = []

    sql = "SELECT oldperson_id, username, volunteer_id, `name`, event_location, event_date, event_image_dir FROM event_info, volunteer_info, oldPerson_info " \
          "WHERE event_type=1 AND event_info.oldperson_id = oldPerson_info.ID AND event_info.volunteer_id = volunteer_info.id"

    for result in db.session.execute(sql):
        with open(result[6], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'oldPersonId': result[0], 'oldPersonName': result[1], 'volunteerId': result[2],
                           'volunteerName': result[3],
                           'eventLocation': result[4], 'eventDate': str(result[5]), 'eventPhoto': encode_str}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to get interaction events!')
    response = json.dumps(response.__dict__)

    return response


# 添加一条事件记录
@app.route('/addEvent', methods=['POST'])
def add_event():
    body = request.json

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # event = EventInfo()

    # 陌生人检测或禁止区域入侵检测（事件类型，事件发生事件，事件发生地点，事件描述，捕捉到的图像）
    if body['eventType'] == 2 or body['eventType'] == 4:
        event = EventInfo(event_type=body['eventType'], event_date=current_time, event_location=body['eventLocation'],
                          event_desc=body['eventDesc'], event_image_dir=body['eventImageDir'])
    # 摔倒检测（事件类型，事件发生事件，事件发生地点，事件描述，捕捉到的图像）
    elif body['eventType'] == 3:
        event = EventInfo(event_type=body['eventType'], event_date=current_time,
                          event_location=body['eventLocation'], event_desc=body['eventDesc'],
                          event_image_dir=body['eventImageDir'])
    # 情感检测（事件类型，事件发生事件，事件发生地点，事件描述，老人的ID，捕捉到的图像）
    elif body['eventType'] == 0:
        event = EventInfo(event_type=body['eventType'], event_date=current_time, event_location=body['eventLocation'],
                          event_desc=body['eventDesc'], oldperson_id=body['oldPersonId'],
                          event_image_dir=body['eventImageDir'])
    # 老人与护工交互检测（事件类型，事件发生事件，事件发生地点，事件描述，老人的ID，志愿者的ID，捕捉到的图像）
    elif body['eventType'] == 1:
        event = EventInfo(event_type=body['eventType'], event_date=current_time, event_location=body['eventLocation'],
                          event_desc=body['eventDesc'], oldperson_id=body['oldPersonId'],
                          volunteer_id=body['volunteerId'], event_image_dir=body['eventImageDir'])

    db.session.add(event)
    db.session.commit()

    response = BaseResponse(code=200, msg='Succeed to add event')
    response = json.dumps(response.__dict__)

    return response





def generate_token(username, password):
    #构造payload
    payload = {
        'username': username,
        'password': password,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)  # 超时时间
    }
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).encode('utf-8').decode('utf-8')
    return token




# 识别身份证信息 （调用Face++旷视API完成）

# 图片要求 ：
# 图片格式：JPG(JPEG)，PNG
# 图片像素尺寸：最小48*48像素，最大4096*4096像素。 建议身份证在整张图片中面积占比大于1/10。
# 图片文件大小：2MB

# 图片数据采用base64编码的二进制图片数据
def identify_id_card(photo):
    http_url = 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard'
    key = "VfFq28mDLp1hLWXKGXVfNGO8LUKvpTBs"
    secret = "m1GTqEqGungSNT-J6YIn4MobFsAEOpkL"
    base64 = photo
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'image_base64')
    data.append(base64)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'legality')
    data.append('0')
    data.append('--%s--\r\n' % boundary)

    # print(data)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # 创建HTTP请求
    req = urllib.request.Request(url=http_url, data=http_body)

    # 设置HTTP请求头部
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # 访问目标url
        resp = urllib.request.urlopen(req, timeout=5)
        # 获取响应信息
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        return qrcont.decode('utf-8')
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000') #9656


    # with open(r"C:\Users\seven\Desktop\身份证.jpg","rb") as r:
    #     photo = base64.b64encode(r.read())
    #     print(photo)
        # result = json.loads(identify_id_card(photo))['cards'][0]
        # print(result['id_card_number'])

    # if OldPersonInfo.query.filter_by(phone=13321313711).first():
    #     print(OldPersonInfo.query.filter_by(phone=13321313711).first().ID)
    # else:
    #     print("no")
    # print(generate_token("admin","admin"))


    # sql_number_fall = "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 DAY) AND CURDATE() then event_info.event_date end) as 'within_four_days'" \
    #                   "FROM event_info WHERE event_info.event_type=3"
    # number_fall = db.session.execute(sql_number_fall).all()
    # print(number_fall[0])

    # old_person = OldPersonInfo(username="测试", gender="male", phone="1325636",
    #                            id_card="858585858", birthday="1966-09-09",
    #                            checkin_date="1966-09-09", checkout_date="1966-09-09",
    #                            room_number=302, CREATED="1966-09-09")
    # db.session.add(old_person)
    # db.session.commit()
