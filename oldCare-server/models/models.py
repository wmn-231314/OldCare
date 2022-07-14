# coding=utf-8

from app import db

# 老人信息表
class OldPersonInfo(db.Model):
    __tablename__ = 'oldPerson_info'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), info='用户名')
    gender = db.Column(db.String(5), info='性别')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    room_number = db.Column(db.String(50))
    firstguardian_name = db.Column(db.String(50))
    firstguardian_relationship = db.Column(db.String(50))
    firstguardian_phone = db.Column(db.String(50))
    firstguardian_wechat = db.Column(db.String(50))
    secondguardian_name = db.Column(db.String(50))
    secondguardian_relationship = db.Column(db.String(50))
    secondguardian_phone = db.Column(db.String(50))
    secondguardian_wechat = db.Column(db.String(50))
    health_state = db.Column(db.String(50))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))

    # 调试时输出4实例
    def __repr__(self):
        return {
            'id': self.ID,
            'userName': self.username,
            'gender': self.gender
        }

    def to_json(self):
        return {
            # 'id': self.ID,
            'userName': self.username,
            'photo': self.profile_photo,
            'id_card': self.id_card,
            'gender': self.gender,
            'room_num': self.room_number,
            'checkin_date': str(self.checkin_date)
        }

# 工作人员信息表
class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), info='用户名')
    gender = db.Column(db.String(5), info='密码')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    hire_date = db.Column(db.DateTime)
    resign_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))

# 义工信息表
class VolunteerInfo(db.Model):
    __tablename__ = 'volunteer_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), info='姓名')
    gender = db.Column(db.String(5), info='性别')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))

    def to_json(self):
        return {
            # 'id': self.ID,
            'userName': self.name,
            'photo': self.profile_photo,
            'id_card': self.id_card,
            'gender': self.gender,
            'phone': self.phone,
            'is_active': self.ISACTIVE
        }

# 事件表
class EventInfo(db.Model):
    __tablename__ = 'event_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type = db.Column(db.Integer, info='事件类型')
    event_date = db.Column(db.DateTime)
    event_location = db.Column(db.String(200))
    event_desc = db.Column(db.String(200))
    oldperson_id = db.Column(db.ForeignKey('oldPerson_info.ID'), index=True)
    event_image_dir = db.Column(db.String(255))
    volunteer_id = db.Column(db.ForeignKey('volunteer_info.id'), index=True)

    oldperson = db.relationship('OldPersonInfo', primaryjoin='EventInfo.oldperson_id == OldPersonInfo.ID',
                                backref='event_info_ibfk_1')

    oldperson = db.relationship('VolunteerInfo', primaryjoin='EventInfo.volunteer_id == VolunteerInfo.id',
        backref='event_info_ibfk_2')

    def to_json(self):
        return {
            # 'id': self.id,
            # 'event_type': self.event_type,
            'event_date': self.event_date,
            "event_location": self.event_location,
            "event_desc": self.event_desc,
            "oldperson_id": self.oldperson_id,
            "event_image_dir": self.event_image_dir
        }

# 系统管理员表
class SysUser(db.Model):
    __tablename__ = 'sys_user'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(50), nullable=False, info='用户名')
    Password = db.Column(db.String(50), info='密码')
    REAL_NAME = db.Column(db.String(50))
    SEX = db.Column(db.String(20))
    EMAIL = db.Column(db.String(50))
    PHONE = db.Column(db.String(50))
    MOBILE = db.Column(db.String(50))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))
    DATAFILTER = db.Column(db.String(200))
    theme = db.Column(db.String(45))
    defaultpage = db.Column(db.String(45), info='登录成功页面')
    logoimage = db.Column(db.String(45), info='显示不同logo')
    qqopenid = db.Column(db.String(100), info='第三方登录的凭证')
    appversion = db.Column(db.String(10), info='检测app的版本号')
    jsonauth = db.Column(db.String(1000), info=' app权限控制')

    def to_json(self):
        return {
            'id': self.ID,
            'userName': self.UserName,
            'password': self.Password
        }
