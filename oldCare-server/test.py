# -*- coding: utf-8 -*-
import requests
import json
import time
import base64
host = "127.0.0.1:9656"
endpoint = r"/register"
url = ''.join([host, endpoint])
with open(r"C:\Users\seven\Desktop\12365.jpg", "rb") as r:
    photo = bytes.decode(base64.b64encode(r.read()))
headers = \
    {
        "applicationCode": "detection",
        "operationTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        "Content-Type": "application/json;charset=UTF-8"
    }
body = \
    {
        'username':'admin',
        'password':'admin'

    }
# r = requests.post("https://f557r67476.goho.co/login", headers=headers, json=body)
# r = requests.get("http://1.15.63.218/",headers=)
print(r.text)
# i=0
# for item in r.json()['data']:
#     print(i)
#     print(item)
#     i=i+1

# print(r.text)
