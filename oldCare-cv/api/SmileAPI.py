import urllib3
import requests
from json import JSONDecoder
import base64


class SmileApi:
    def detect_smile(self, filepath1):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        # 你要调用API的URL

        key = "IQ2q4ni5yiHG_yJTu27bvB72pr6kZGbJ"
        secret = "l20s66oVPzga3YorSkxEnbO8wjRADQSr"
        # face++提供的一对密钥
        # 图片文件的绝对路径
        data = {"api_key": key, "api_secret": secret, "return_attributes": "gender,age,smiling,beauty,emotion"}
        # 必需的参数，注意key、secret、"gender,age,smiling,beauty"均为字符串，与官网要求一致
        files = {"image_file": filepath1}
        '''以二进制读入图像，这个字典中open(filepath1, "rb")返回的是二进制的图像文件，所以"image_file"是二进制文件，符合官网要求'''
        response = requests.post(http_url, data=data, files=files)
        # POTS上传
        req_con = response.content.decode('utf-8')
        # response的内容是JSON格式
        req_dict = JSONDecoder().decode(req_con)
        # 对其解码成字典格式
        # print(req_dict)
        # 输出
        return req_dict

    def detect_fall(self, filepath1):
        http_url = "https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton"
        # 你要调用API的URL

        key = "IQ2q4ni5yiHG_yJTu27bvB72pr6kZGbJ"
        secret = "l20s66oVPzga3YorSkxEnbO8wjRADQSr"
        # face++提供的一对密钥
        # 图片文件的绝对路径
        data = {"api_key": key, "api_secret": secret}
        # 必需的参数，注意key、secret、"gender,age,smiling,beauty"均为字符串，与官网要求一致
        # files = {"image_file": open(filepath1, "rb")}
        files = {"image_file": filepath1}
        '''以二进制读入图像，这个字典中open(filepath1, "rb")返回的是二进制的图像文件，所以"image_file"是二进制文件，符合官网要求'''
        response = requests.post(http_url, data=data, files=files)
        # POTS上传
        req_con = response.content.decode('utf-8')
        # response的内容是JSON格式
        req_dict = JSONDecoder().decode(req_con)

        # 输出
        return req_dict
