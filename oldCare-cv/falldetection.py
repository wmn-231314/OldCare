# -*- coding: utf-8 -*-
'''
摔倒检测模型主程序

用法：
python checkingfalldetection.py
python checkingfalldetection.py --filename ../images/tests/videos/3.mp4
'''

# import the necessary packages
import base64
import threading

import imutils
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import os
import argparse

import insertingcontrol
from campusher import stream_pusher
from api import SmileApi
import math
import cv2
import time
import multiprocessing

from inserting import insert

image_api = ''
result = ''
f = ""

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=False, default='',help="")
args = vars(ap.parse_args())
input_video = args['filename']

# 控制陌生人检测
fall_timing = 0  # 计时开始
fall_start_time = 0  # 开始时间
fall_limit_time = 2  # if >= 1 seconds, then he/she falls.

# 全局变量
model_path = './models_saving/fall_detection.hdf5'
output_fall_path = '/home/reed/Desktop/code/oldcare/supervision'
# your python path
# python_path = '/home/reed/anaconda3/envs/tensorflow/bin/python3.6'

# 全局常量
TARGET_WIDTH = 64
TARGET_HEIGHT = 64

def run1():
    global image_api
    global result
    biaoqing = SmileApi()
    while True:
        if image_api != '':
            print("has image")
            result = biaoqing.detect_fall(image_api)
        else:
            print("no_image")
            time.sleep(2)

result = {"skeletons": []}

# speed
speeda = 0
acceleration = -1
the_buttocks_x = 0
the_buttocks_y = 0
the_time = time.time()
fall = 0
normal = 0

print('[INFO] 开始检测是否有人摔倒...')
counter = 0

# 连接骨架函数
def connect_skeleton(image, skeleton1, skeleton2, left, top, color):
    cv2.line(image, (int(skeleton1.get('x')) + int(left), int(skeleton1.get('y')) + int(top)),
             (int(skeleton2.get('x')) + int(left), int(skeleton2.get('y')) + int(top)), color, 2)
    # 计算角度

def calc_angle(x1, y1, x2, y2):

    x = abs(x1 - x2)

    y = abs(y1 - y2)

    z = math.sqrt(x * x + y * y)
    if z == 0:
        angle = round(0)
        return angle
    angle = round(math.asin(y / z) / math.pi * 180)
    return angle



# 传入参数
def checkingfalldetection(grabbed,image,model=None):
    global speeda,acceleration,the_buttocks_x,the_buttocks_y,the_time
    global result
    global fall_timing,fall_start_time,counter,fall,normal

    if not grabbed:
        return

    biaoqing = SmileApi()
    img = cv2.imencode(".jpg", image)[1].tobytes()
    counter += 1
    if counter % 25 == 0:
        result = biaoqing.detect_fall(img)
        roi = cv2.resize(image, (TARGET_WIDTH, TARGET_HEIGHT))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
    # print(result)
    if result.get("skeletons"):
        for b in result.get("skeletons"):
            landmark = b.get("landmark")
            left = b.get("body_rectangle").get("left")
            top = b.get("body_rectangle").get("top")
            width = b.get("body_rectangle").get("width")
            height = b.get("body_rectangle").get("height")
            # print(b)
            cv2.rectangle(image, (int(left), int(top)), (int(left) + int(width), int(top) + int(height)), (0, 0, 255),
                          2)
            head = landmark.get("head")
            neck = landmark.get("neck")
            left_shoulder = landmark.get("left_shoulder")
            right_shoulder = landmark.get("right_shoulder")
            left_hand = landmark.get("left_hand")
            right_hand = landmark.get("right_hand")
            left_buttocks = landmark.get("left_buttocks")
            right_buttocks = landmark.get("right_buttocks")
            left_knee = landmark.get("left_knee")
            right_knee = landmark.get("right_knee")
            left_foot = landmark.get("left_foot")
            right_foot = landmark.get("right_foot")

            connect_skeleton(image, head, neck, left, top, (0, 255, 0))
            connect_skeleton(image, neck, left_shoulder, left, top, (0, 255, 0))
            connect_skeleton(image, neck, right_shoulder, left, top, (0, 255, 0))
            connect_skeleton(image, right_hand, right_shoulder, left, top, (255, 20, 147))
            connect_skeleton(image, left_hand, left_shoulder, left, top, (255, 20, 147))
            connect_skeleton(image, neck, left_buttocks, left, top, (0, 255, 0))
            connect_skeleton(image, neck, right_buttocks, left, top, (0, 255, 0))
            connect_skeleton(image, right_buttocks, right_knee, left, top, (255, 255, 0))
            connect_skeleton(image, left_buttocks, left_knee, left, top, (255, 255, 0))
            connect_skeleton(image, left_knee, left_foot, left, top, (255, 255, 0))
            connect_skeleton(image, right_knee, right_foot, left, top, (255, 255, 0))

            # cv2.imshow("123",image)
    # time.sleep(100)
    # exit()
    # determine facial expression

    if result.get("skeletons") and counter % 30 == 0:

        for b in result.get("skeletons"):
            landmark = b.get("landmark")
            width = b.get("body_rectangle").get("width")
            height = b.get("body_rectangle").get("height")
            head = landmark.get("head")
            left_buttocks = landmark.get("left_buttocks")
            right_buttocks = landmark.get("right_buttocks")
            mid_buttocks_x = int(left_buttocks.get('x')) + int(right_buttocks.get('x'))
            mid_buttocks_x = mid_buttocks_x / 2
            mid_buttocks_y = int(left_buttocks.get('y')) + int(right_buttocks.get('y'))
            mid_buttocks_y = mid_buttocks_y / 2

            right_foot = landmark.get("right_foot")
            left_foot = landmark.get("left_foot")
            mid_foot_x = int(right_foot.get('x')) + int(left_foot.get('x'))
            mid_foot_x = mid_foot_x / 2
            mid_foot_y = int(right_foot.get('y')) + int(left_foot.get('y'))
            mid_foot_y = mid_foot_y / 2

            right_knee = landmark.get("right_knee")
            left_knee = landmark.get("left_knee")
            mid_knee_x = int(right_knee.get('x')) + int(left_knee.get('x'))
            mid_knee_x = mid_knee_x / 2
            mid_knee_y = int(right_knee.get('y')) + int(left_knee.get('y'))
            mid_knee_y = mid_knee_y / 2

            # check speed
            if counter % 15 == 0:
                if the_buttocks_x == 0 and the_buttocks_y == 0:
                    the_buttocks_x = mid_buttocks_x
                    the_buttocks_y = mid_buttocks_y
                else:
                    dtime = time.time() - the_time
                    the_time = time.time()
                    sq1 = (mid_buttocks_x - the_buttocks_x) * (mid_buttocks_x - the_buttocks_x)
                    sq2 = (mid_buttocks_y - the_buttocks_y) * (mid_buttocks_y - the_buttocks_y)
                    dis = math.sqrt(sq1 + sq2)
                    speedb = dis / dtime
                    if acceleration != -1:
                        if acceleration != 0 and abs((speeda - speedb) / dtime) > 7 * acceleration:
                            print("加速度变化较大，存在摔倒风险")
                        acceleration = abs((speeda - speedb) / dtime)
                        speeda = speedb
                        # print(acceleration)
                    else:
                        speeda = speedb
                        acceleration = abs((speeda - speedb) / dtime)
                        # print(-1)
                    the_buttocks_x = mid_buttocks_x
                    the_buttocks_y = mid_buttocks_y

            # tocheck torso line
            check = 0
            # print(calc_angle(mid_buttocks_x,mid_buttocks_y,int(head.get('x')),int(head.get('y'))))
            # print(calc_angle(mid_foot_x,mid_foot_y,mid_buttocks_x,mid_buttocks_y))
            if abs(calc_angle(mid_buttocks_x, mid_buttocks_y, int(head.get('x')),
                                   int(head.get('y')))) < 60 and abs(
                    calc_angle(mid_foot_x, mid_foot_y, mid_buttocks_x, mid_buttocks_y)) < 60:
                print("check method1:")
                print("Upper body torso line:" + str(
                    calc_angle(mid_buttocks_x, mid_buttocks_y, int(head.get('x')), int(head.get('y')))))
                print("Lower body torso line:" + str(
                    calc_angle(mid_foot_x, mid_foot_y, mid_buttocks_x, mid_buttocks_y)))
                check = 1                # break
            if abs(calc_angle(mid_knee_x, mid_knee_y, int(head.get('x')), int(head.get('y')))) < 70 and abs(
                    calc_angle(mid_foot_x, mid_foot_y, mid_knee_x, mid_knee_y)) < 45:
                print("check method2:")
                print("all torso line:" + str(
                    calc_angle(mid_buttocks_x, mid_buttocks_y, int(head.get('x')), int(head.get('y')))))
                print("Calf line:" + str(calc_angle(mid_foot_x, mid_foot_y, mid_buttocks_x, mid_buttocks_y)))
                check = 1
                # break
            if check == 0:
                index = 0
            else:
                index = 1

        if index == 1:
            fall = calc_angle(mid_buttocks_x, mid_buttocks_y, int(head.get('x')), int(head.get('y')))
            normal = 0
        else:
            fall = 0
            normal = calc_angle(mid_buttocks_x, mid_buttocks_y, int(head.get('x')), int(head.get('y')))

        if fall > normal:
            if fall_timing == 0:  # just start timing
                fall_timing = 1
                fall_start_time = time.time()
            else:  # alredy started timing
                fall_end_time = time.time()
                difference = fall_end_time - fall_start_time

                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                if difference < fall_limit_time:
                    print('[INFO] %s, 走廊, 摔倒仅出现 %.1f 秒. 忽略.' % (current_time, difference))
                else:  # strangers appear
                    event_desc = '走廊, 有人摔倒!!!'
                    event_location = '走廊'
                    print('[EVENT] %s, 走廊, 有人摔倒!!!' % (current_time))
                    # path = os.path.join(output_fall_path, 'fall_%s.jpg' % current_time)
                    # cv2.imwrite(path, image)
                    # insert into database
                    # command = '%s inserting.py --event_desc %s--event_type3 - -event_location % s'% (python_path, event_desc, event_location)
                    # p = subprocess.Popen(command, shell=True)
                    # image_base = base64.b64encode(image)
                    ret, jpeg = cv2.imencode('.jpg', image)
                    image_base = bytes.decode(base64.b64encode(jpeg))
                    insert(3,event_location,event_desc,image_base,'fall_%s.jpg'% current_time)
    # else:
    #     print("waiting")
    #     # if model is not None:
    #     #     (fall, normal) = model.predict(roi)[0]
    #     # else:
    #     fall = 0
    #     normal = 1

    # determine facial expression
    if fall > normal:
        label = "Fall (%.2f)" % fall
    else:
        label = "Normal (%.2f)" % normal

    # display the label and bounding box rectangle on the output frame
    cv2.putText(image, label, (image.shape[1] - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    return image

if __name__ == '__main__':
    # input_video="/home/reed/Desktop/code/oldcare/tests/testfall1.mp4"
    # 初始化摄像头
    rtmpSrc = "rtmp://1.15.63.218:1935/live/rawvideo"
    if not input_video:
        vs = cv2.VideoCapture(rtmpSrc)
        time.sleep(2)
    else:
        vs = cv2.VideoCapture(input_video)
    #
    # print('[INFO] 开始检测是否有人摔倒...')
    # fall_model = load_model(model_path)
    fall_model = None
    t5 = threading.Thread(target=insertingcontrol.control)
    t5.start()
    # 开启线程
    # t1 = threading.Thread(target=run1())
    # t1.start()
    # 不断循环
    rtmpUrl = "rtmp://1.15.63.218:1935/live/rfBd56ti2SMtYvSgD5xAV0YU99zampta7Z7S575KLkIZ9PYk"
    raw_q = multiprocessing.Queue(100)

    my_pusher = stream_pusher(rtmp_url=rtmpUrl, raw_frame_q=raw_q)
    my_pusher.run()
    while True:
        (grabbed, frame) = vs.read()
        image = checkingfalldetection(grabbed, frame,fall_model)
        # if image is None:
        #     continue
        image = imutils.resize(frame, width=640, height=480)
        info = (image, '2', '3', '4')
        if not raw_q.full():  # 如果队列没满
            raw_q.put(info)  # 送入队列
        cv2.imshow("oldcare_system", image)
        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    vs.release()
    cv2.destroyAllWindows()
