# -*- coding: utf-8 -*-
import requests
import json
import time
import base64
host = "127.0.0.1:9656"
endpoint = r"/register"
url = ''.join([host, endpoint])
headers = \
    {
        "applicationCode": "detection",
        "operationTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        "Content-Type": "application/json;charset=UTF-8"
    }
body = \
    {

        "username": "wju",
        "password": "4567"

    }

r = requests.post("http://127.0.0.1:9656/login", headers=headers, json=body)
print r.text
