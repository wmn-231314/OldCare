# -*-coding:UTF-8 -*-
from flask import Flask, render_template, request, jsonify, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_siwadoc import SiwaDoc
from pydantic import BaseModel, Field

import base64
import time
import json
import os

from response import *
from models.models import *

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(__name__)
app.config['SECRET_KEY'] = 'old_care_flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:63637072@localhost:3306/old_care_flask'
# 每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# 将Flask实例传入SiwaDoc的构造方法初始化SiwaDoc
siwa = SiwaDoc(app)


@app.route("/")
def root():
    """
    rootindex
    :return: Index.html
    """
    return render_template('Index.html')


@app.route("/homePage_data", methods=['Get'])
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
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 4 DAY) AND CURDATE() then event_info.event_date end) as 'within_five_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 5 DAY) AND CURDATE() then event_info.event_date end) as 'within_six_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 6 DAY) AND CURDATE() then event_info.event_date end) as 'within_seven_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND CURDATE() then event_info.event_date end) as 'within_eight_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 8 DAY) AND CURDATE() then event_info.event_date end) as 'within_nine_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 9 DAY) AND CURDATE() then event_info.event_date end) as 'within_ten_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 10 DAY) AND CURDATE() then event_info.event_date end) as 'within_eleven_days', "\
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 11 DAY) AND CURDATE() then event_info.event_date end) as 'within_twelve_days', " \
                      "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 12 DAY) AND CURDATE() then event_info.event_date end) as 'within_thirteen_days', " \
                      "FROM event_info WHERE event_info.event_type=3"
    sql_number_intrusion = "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 3 DAY) AND CURDATE() then event_info.event_date end) as 'within_four_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 4 DAY) AND CURDATE() then event_info.event_date end) as 'within_five_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 5 DAY) AND CURDATE() then event_info.event_date end) as 'within_six_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 6 DAY) AND CURDATE() then event_info.event_date end) as 'within_seven_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 7 DAY) AND CURDATE() then event_info.event_date end) as 'within_eight_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 8 DAY) AND CURDATE() then event_info.event_date end) as 'within_nine_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 9 DAY) AND CURDATE() then event_info.event_date end) as 'within_ten_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 10 DAY) AND CURDATE() then event_info.event_date end) as 'within_eleven_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 11 DAY) AND CURDATE() then event_info.event_date end) as 'within_twelve_days', " \
                           "SELECT COUNT(case when DATE(event_info.event_date) BETWEEN DATE_SUB(CURDATE(),INTERVAL 12 DAY) AND CURDATE() then event_info.event_date end) as 'within_thirteen_days', " \
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


# 添加系统管理员请求体
class AddSystemUserModel(BaseModel):
    username: str
    password: str


# 系统管理员注册部分 即添加
@app.route('/register', methods=['POST'])
@siwa.doc(body=AddSystemUserModel, group="Test", tags="a")
def add_sys_usr():
    body = request.json
    sys_usr = SysUser(UserName=body['username'], Password=body['password'], )
    db.session.add(sys_usr)
    print("add success")

    response = BaseResponse(code=200, msg="Succeed to register")
    response = json.dumps(response.__dict__)

    return response


# 系统管理员登录逻辑处理
@app.route('/login', methods=['POST'])
@siwa.doc(group="Test", tags="b")
def login():
    body = request.json
    user_name = body['username']
    password = body['password']

    for result in SysUser.query.filter_by(UserName=user_name).all():
        if password == result.to_json()['password']:
            session['sys_user_id'] = result.to_json()['id']
            session['sys_user_name'] = result.to_json()['userName']
            response = BaseResponse(code=0, msg="Match")
            response = json.dumps(response.__dict__)
            return response
        else:
            continue
    response = BaseResponse(code=-1, msg="Not match")
    response = json.dumps(response.__dict__)
    return response


class tableOfOlderPersonModel(BaseModel):
    result_dict: dict
    result_list: list


# 获取所有老人信息
@app.route('/table_oldPerson', methods=['GET'])
@siwa.doc(resp=tableOfOlderPersonModel)
def get_old_person_info():
    result_list = []
    sql = 'SELECT username, profile_photo, id_card, gender, room_number, checkin_date FROM oldPerson_info'
    for result in db.session.execute(sql):
        with open(result[1], 'rb') as f:
            data = f.read()
            encode_str = "data:image/jpg;base64," + str(base64.b64encode(data), 'utf-8')
            result_dict = {'userName': result[0], 'photo': encode_str, 'id_card': str(result[2]),
                           'gender': result[3], 'room_num': result[4], 'checkin_date': str(result[5])}
            result_list.append(result_dict)

    response = DataResponse(code=200, data=result_list, msg='Succeed to select all old persons!')
    response = json.dumps(response.__dict__)

    return response


# 添加老人信息
@app.route('/addOldPersonInfo', methods=['POST'])
@siwa.doc()
def add_old_person_info():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    old_person = OldPersonInfo(username=body['username'], gender=body['gender'], phone=body['phone'],
                               checkin_date=body['checkin_date'], checkout_date=body['checkout_date'],
                               CREATED=current_time)
    db.session.add(old_person)
    db.session.commit()

    response = BaseResponse(code=200, msg='Succeed to insert one old person!')
    response = json.dumps(response.__dict__)

    return response


# 删除老人信息
@app.route('/deleteOldPerson', methods=['POST'])
@siwa.doc()
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
@siwa.doc()
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
@siwa.doc()
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


# 添加一个新的义工
@app.route('/addVolunteer', methods=['POST'])
@siwa.doc()
def add_volunteer():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    volunteer = VolunteerInfo(name=body['name'], gender=['gender'], phone=body['phone'],
                              checkin_date=body['checkin_date'], checkout_date=body['checkout_date'],
                              ISACTIVE=body['isActive'], CREATED=current_time)
    db.session.add(volunteer)
    db.session.commit()

    response = BaseResponse(code=200, msg="Succeed to insert one volunteer!")
    response = json.dumps(response.__dict__)

    return response


# 获取某种类型事件发生的所有记录
@app.route('/table_events', methods=['GET'])
@siwa.doc()
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
@siwa.doc()
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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9656')
    # get_homePage_Data()
