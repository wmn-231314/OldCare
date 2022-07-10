# coding:UTF-8

from flask import Flask, render_template, request, jsonify, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
import base64
import time
import json
import os
import urllib


from response import *
from models.models import *

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(__name__)
app.config['SECRET_KEY'] = 'old_care_flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/old_care_flask'
# 每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 设置跨域
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)


@app.route("/")
def root():
    """
    rootindex
    :return: Index.html
    """
    return render_template('Index.html')


# 系统管理员注册部分 即添加
@app.route('/register', methods=['POST'])
def add_sys_usr():
    body = request.json
    sys_usr = SysUser(UserName=body['username'], Password=body['password'])
    db.session.add(sys_usr)
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
            response = BaseResponse(code=200, msg="Succeed to login")
            response = json.dumps(response.__dict__)
            return response
        else:
            continue
    response = BaseResponse(code=400, msg="Fail to login")
    response = json.dumps(response.__dict__)
    return response



# 获取所有老人信息
@app.route('/table_oldPerson', methods=['GET'])
def get_old_person_info():
    result_list = []
    sql = 'SELECT username, profile_photo, id_card, gender, room_number, checkin_date FROM oldPerson_info'
    for result in db.session.execute(sql):
        with open(result[1], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data).encode('utf-8'))
            result_dict = {'userName': result[0], 'photo': encode_str, 'id_card': str(result[2]),
                           'gender': result[3], 'room_num': result[4], 'checkin_date': str(result[5])}
            result_list.append(result_dict)
    response = DataResponse(code=200, data=result_list, msg='Succeed to select all old persons')
    response = json.dumps(response.__dict__)
    return response


# 添加老人信息
@app.route('/addOldPersonInfo', methods=['POST'])
def add_old_person_info():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    old_person = OldPersonInfo(username=body['username'], gender=body['gender'], CREATED=current_time)
    db.session.add(old_person)
    response = BaseResponse(code=200, msg='Succeed to insert one old person')
    response = json.dumps(response.__dict__)
    return response


# 删除老人信息
@app.route('/deleteOldPerson', methods=['POST'])
def delete_old_person():
    body = request.json
    old_person = OldPersonInfo(ID=body['id'], username=body['username'])
    db.session.delete(old_person)
    db.session.commit()
    response = BaseResponse(code=200, msg="Succeed to delete one old person")
    response = json.dumps(response.__dict__)
    return response


# 修改老人信息
@app.route('/updateOldPerson', methods=['POST'])
def update_old_person():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    OldPersonInfo.query.filter_by(ID=body['id']).update({'username': body['userName'], 'UPDATED': current_time})
    db.session.commit()

    response = BaseResponse(code=200, msg="Succeed to update old person!")
    response = json.dumps(response.__dict__)

    return response


# 获取所有志愿者信息
@app.route('/table_volunteer', methods=['GET'])
def get_volunteer():
    result_list = []
    sql = "SELECT `name`, profile_photo, id_card, gender, phone, ISACTIVE FROM volunteer_info"
    for result in db.session.execute(sql):
        with open(result[1], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'userName': result[0], 'photo': encode_str, 'id_card': str(result[2]),
                           'gender': result[3], 'phone': result[4], 'is_active': str(result[5])}
        result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to select all old persons!')
    response = json.dumps(response.__dict__)

    return response


# 添加一个新的志愿者
@app.route('/addVolunteer', methods=['POST'])
def add_volunteer():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    volunteer = VolunteerInfo(name=body['name'], gender=['gender'], CREATED=current_time)
    db.session.add(volunteer)
    db.session.commit()

    response = BaseResponse(code=200, msg="Succeed to insert one volunteer!")
    response = json.dumps(response.__dict__)

    return response


# 获取某种类型事件发生的所有记录
@app.route('/table_events', methods=['GET'])
def get_events():
    body = request.json
    result_list = []
    for result in EventInfo.query.filter_by(event_type=body['eventType']).all():
        result_list.append(result.to_json())

    response = DataResponse(code=200, data=result_list, msg='Succeed to get specific events!')
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




# sys user login with face
@app.route('/loginWithFace', methods=['POST'])
def login_with_face():
    body = request.json
    photo_base64 = body['photo']
    # print(str(photo_base64))
    photo_base64 = str(photo_base64).split(',')[1]
    photo = base64.b64decode(photo_base64)
    checkingfaceimg = Checkingfaceimg(photo)
    is_login = checkingfaceimg.check()
    if len(is_login) == 0:
        response = BaseResponse(code=-1, msg="Fail to login with face!")
        response = json.dumps(response.__dict__)
        return response
    elif is_login[0] == 'Unknown':
        response = BaseResponse(code=-1, msg="Fail to login with face!")
        response = json.dumps(response.__dict__)
        return response
    else:
        response = BaseResponse(code=0, msg="Succeed to login with face!")
        response = json.dumps(response.__dict__)
        return response





if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9656')
