# coding=utf-8


class BaseResponse(object):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def set_code(self, code):
        self.code = code

    def set_msg(self, msg):
        self.msg = msg


class DataResponse(BaseResponse):

    def __init__(self, code, data, msg):
        super(DataResponse, self).__init__(code, msg)
        self.data = data

    def set_data(self, data):
        self.data = data
