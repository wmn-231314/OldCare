# -*- coding: utf-8 -*-

'''
禁止区域检测主程序
摄像头对准围墙那一侧

用法：
python checkingfence.py
python checkingfence.py --filename ../images/tests/videos/yard_01.mp4
'''

from cv.sourcecode.oldcare.track import CentroidTracker
from cv.sourcecode.oldcare.track import TrackableObject
from imutils.video import FPS
import numpy as np
import imutils
import argparse
import time
import dlib
import cv2
import os
import subprocess
import json
import requests
import threading

f = ""


class Checkingfence():

    def __init__(self, filename):
        self.filename = filename

    # 线程处理
    def run(self):
        global f
        # 得到当前时间
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(time.time()))
        print('[INFO] %s 禁止区域检测程序启动了.' % (current_time))

        # 全局变量
        prototxt_file_path = 'D:/SoftwareEngineering/PythonProjects/homework/OldCare/OldCare/oldCare-server/cv/models/mobilenet_ssd/MobileNetSSD_deploy.prototxt'
        model_file_path = 'D:/SoftwareEngineering/PythonProjects/homework/OldCare/OldCare/oldCare-server/cv/models/mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
        output_fence_path = 'D:/SoftwareEngineering/PythonProjects/homework/OldCare/OldCare/oldCare-server/cv/supervision/fence'
        input_video = self.filename
        skip_frames = 30
        # your python path
        python_path = 'D:/SoftwareEngineering/python/python2.7.18/2.7.18'

        # 超参数
        minimum_confidence = 0.80

        # 物体识别模型能识别的物体（21种）
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair",
                   "cow", "diningtable", "dog", "horse", "motorbike",
                   "person", "pottedplant", "sheep", "sofa", "train",
                   "tvmonitor"]

        # 摄像头或视频文件
        if not input_video:
            print("[INFO] starting video stream...")
            vs = cv2.VideoCapture(0)
            time.sleep(2)
        else:
            print("[INFO] opening video file...")
            vs = cv2.VideoCapture(input_video)

        # 加载物体识别模型
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(prototxt_file_path, model_file_path)

        W = None
        H = None
        weight = 300
        # 横线左上起点
        x1 = 0
        y1 = 100
        # 右上（横线终点）
        x2 = x1 + 300
        y2 = 100
        # 左竖线终点
        x3 = x1
        y3 = y1 + 500
        # 右竖线终点
        x4 = x2
        y4 = y3

        # 初始化质心追踪
        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        trackers = []
        trackableObjects = {}

        totalFrames = 0
        totalDown = 0
        totalUp = 0

        # 启动每秒帧数吞吐量估计器
        fps = FPS().start()

        while True:
            ret, frame = vs.read()

            if input_video and not ret:
                break

            if not input_video:
                frame = cv2.flip(frame, 1)

            frame = imutils.resize(frame, width=500)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # 未检测到目标时状态为waiting
            status = "Waiting"
            rects = []

            if totalFrames % skip_frames == 0:
                status = "Detecting"
                trackers = []

                # 图像预处理
                blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
                # 网络发送 得到Numpy ndarray
                net.setInput(blob)
                # 返回四维数据 在最后一维，第二个开始依次是：标签、置信度、目标位置的4个坐标信息[xmin ymin xmax ymax]
                # 倒数第二维是检测到结果的索引
                detections = net.forward()

                # detections.shape[2] 可以得到检测结果的数量
                for i in np.arange(0, detections.shape[2]):
                    # 提取与预测相关的置信度（即概率）
                    confidence = detections[0, 0, i, 2]

                    # 通过要求最小置信度来过滤弱检测
                    if confidence > minimum_confidence:
                        # 从检测列表中提取类标签的索引
                        idx = int(detections[0, 0, i, 1])
                        if CLASSES[idx] != "person":
                            continue

                        # 计算边界框值
                        box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        (startX, startY, endX, endY) = box.astype("int")

                        # 构建dlib矩形对象，然后启动dlib相关跟踪器
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(startX, startY, endX, endY)
                        tracker.start_track(rgb, rect)
                        trackers.append(tracker)

            # 否则，进行目标追踪
            else:
                for tracker in trackers:
                    status = "Tracking"

                    tracker.update(rgb)
                    pos = tracker.get_position()

                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  (0, 255, 0), 2)

                    rects.append((startX, startY, endX, endY))

            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.line(frame, (x1, y1), (x3, y3), (0, 255, 255), 2)
            cv2.line(frame, (x2, y2), (x4, y4), (0, 255, 255), 2)

            # 质心追踪更新物体位置（消失、新增）
            objects = ct.update(rects)

            for (objectID, centroid) in objects.items():
                to = trackableObjects.get(objectID, None)
                # 如果当前目标未加入到可追踪列表则加入
                if to is None:
                    to = TrackableObject(objectID, centroid)
                else:
                    y = [c[1] for c in to.centroids]
                    # 当前质心位置减去之前位置平均值
                    direction = centroid[1] - np.mean(y)
                    to.centroids.append(centroid)

                    if not to.counted:
                        # 小于0上移 在横线外
                        if direction < 0 and centroid[1] < y2:
                            totalUp += 1
                            to.counted = True
                        # 大于0下移 在区域内
                        elif direction > 0 and centroid[1] >= y2 and x1 < centroid[0] < x2:
                            totalDown += 1
                            to.counted = True

                            current_time = time.strftime('%Y%m%d_%H%M%S',
                                                         time.localtime(time.time()))
                            event_desc = '有人闯入禁止区域!!!'
                            event_location = 'yard'
                            print('[EVENT] %s, 院子, 有人闯入禁止区域!!!' % (current_time))
                            snapshot_dir = os.path.join(output_fence_path, 'snapshot_%s.jpg' % (current_time))
                            cv2.imwrite(snapshot_dir, frame)  # snapshot
                            #
                            # # insert into mysql
                            # url = "http://127.0.0.1:5000/addEvent"
                            # headers = {"Access-Control-Allow-Origin": "*",
                            #            "Content-Type": "application/json;charset=utf-8"
                            #            }
                            # data = json.dumps(
                            #     {"eventType": 4, "eventLocation": event_location, "eventDesc": "intrusion",
                            #      "eventImageDir": snapshot_dir})
                            # response = requests.post(url=url, data=data, headers=headers).text
                            #
                            # # insert into database
                            # command = '%s inserting.py --event_desc %s --event_type 4 --event_location %s' % (
                            # python_path, event_desc, event_location)
                            # p = subprocess.Popen(command, shell=True)

                trackableObjects[objectID] = to

                # 显示目标id和质心
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4,
                           (0, 255, 0), -1)

            # 界面展示信息
            info = [
                 ("Up", totalUp),
                ("Down", totalDown),
                ("Status", status),
            ]

            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # show the output frame
            f = frame
            cv2.imshow("Frame", frame)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            elif k == ord('y'):
                print("右移")
                x1 = x1 + 10
                x3 = x1
                x2 = x2 + 10
                x4 = x2
            elif k == ord('z'):
                print("左移")
                x1 = x1 - 10
                x3 = x1
                x2 = x2 - 10
                x4 = x2
            elif k == ord('s'):
                print("上移")
                y1 = y1 - 10
                y2 = y1

            elif k == ord('x'):
                print("下移")
                y1 = y1 + 10
                y2 = y1
            elif k == ord('t'):
                print("暂停")
                cv2.waitKey(0)
            elif k == ord('k'):
                print("增加宽度")
                x2 = x2 + 10
                x4 = x2
            elif k == ord('j'):
                print("减少宽度")
                x2 = x2 - 10
                x4 = x2

            # 增加到目前为止处理的总帧数，然后更新FPS计数器
            totalFrames += 1
            fps.update()

        # 停止并展示信息
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))  # 14.19
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))  # 90.43

        vs.release()
        cv2.destroyAllWindows()

    def startfence(self):
        # 开启线程
        t = threading.Thread(target=self.run)
        t.start()

    def get_frame(self):
        global f
        if f != "":
            ret, jpeg = cv2.imencode('.jpg', f)
            return jpeg.tobytes()
        else:
            return None



