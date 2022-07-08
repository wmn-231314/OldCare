# -*- coding: utf-8 -*-
'''
图像采集程序-人脸检测
由于外部程序需要调用它，所以不能使用相对路径

用法：
python collectingfaces.py --id 106 --imagedir ../images

'''
import argparse
from util.facialutil import FaceUtil
from util import audioplayer
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import shutil
import time
import threading

f = ""
image = ""
inf1 = ""


class Collectingfaces():

    def __init__(self, imagedir, id):
        self.imagedir = imagedir
        self.id = id

    # 线程处理
    def run1(self):
        while True:
            time.sleep(1)
            global image
            global inf1

    def run(self):
        global f
        global image
        global inf1
        # 全局参数
        audio_dir = 'audios'
        # 控制参数
        error = 0
        start_time = None
        limit_time = 2  # 2 秒
        image = ''
        inf1 = ""
        # 开启线程
        t1 = threading.Thread(target=self.run1)
        t1.start()
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height
        # # 传入参数
        # ap = argparse.ArgumentParser()
        # ap.add_argument("-ic", "--id", required=True,
        #     help="")
        # ap.add_argument("-id", "--imagedir", required=True,
        #     help="")
        # args = vars(ap.parse_args())
        # args=
        action_list = ['blink', 'open_mouth', 'smile', 'rise_head', 'bow_head',
                       'look_left', 'look_right']
        action_map = {'blink': '请眨眼', 'open_mouth': '请张嘴',
                      'smile': '请笑一笑', 'rise_head': '请抬头',
                      'bow_head': '请低头', 'look_left': '请看左边',
                      'look_right': '请看右边'}

        faceutil = FaceUtil()

        counter = 0
        while True:
            counter += 1
            _, image = cam.read()
            if counter <= 10:  # 放弃前10帧
                continue
            image = cv2.flip(image, 1)

            if error == 1:
                end_time = time.time()
                difference = end_time - start_time
                print(difference)
                if difference >= limit_time:
                    error = 0

            face_location_list = faceutil.get_face_location(image)
            for (left, top, right, bottom) in face_location_list:
                cv2.rectangle(image, (left, top), (right, bottom),
                              (0, 0, 255), 2)

            f = image
            cv2.imshow('Collecting Faces', image)  # show the image
            # Press 'ESC' for exiting video
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break

            face_count = len(face_location_list)
            if error == 0 and face_count == 0:  # 没有检测到人脸
                print('[WARNING] 没有检测到人脸')
                audioplayer.play_audio(os.path.join(audio_dir,
                                                    'no_face_detected.mp3'))
                error = 1
                start_time = time.time()
            elif error == 0 and face_count == 1:  # 可以开始采集图像了
                print('[INFO] 可以开始采集图像了')
                audioplayer.play_audio(os.path.join(audio_dir,
                                                    'start_image_capturing.mp3'))
                time.sleep(3)
                break
            elif error == 0 and face_count > 1:  # 检测到多张人脸
                print('[WARNING] 检测到多张人脸')
                audioplayer.play_audio(os.path.join(audio_dir,
                                                    'multi_faces_detected.mp3'))
                error = 1
                start_time = time.time()
            else:
                pass

        # 新建目录
        if os.path.exists(os.path.join(self.imagedir, self.id)):
            shutil.rmtree(os.path.join(self.imagedir, self.id), True)
        os.mkdir(os.path.join(self.imagedir, self.id))

        type = 1
        # 开始采集人脸
        error = 0
        for action in action_list:
            audioplayer.play_audio(os.path.join(audio_dir, action + '.mp3'))
            time.sleep(3)
            action_name = action_map[action]
            counter = 1
            for i in range(15):

                if error == 1:
                    end_time = time.time()
                    difference = end_time - start_time
                    print(difference)
                    if difference >= 3:
                        error = 0
                        type = 0
                        break

                print('%s-%d' % (action_name, i))
                _, img_OpenCV = cam.read()
                img_OpenCV = cv2.flip(img_OpenCV, 1)
                origin_img = img_OpenCV.copy()  # 保存时使用

                face_location_list = faceutil.get_face_location(img_OpenCV)
                for (left, top, right, bottom) in face_location_list:
                    cv2.rectangle(img_OpenCV, (left, top),
                                  (right, bottom), (0, 0, 255), 2)

                # if face_location_list:
                #     # print(face_location_list)
                #     sp = img_OpenCV.shape
                #     img_OpenCV = cameramove.cameramove(img_OpenCV, sp[1], sp[0],
                #                                        face_location_list[0][1], face_location_list[0][3],
                #                                        face_location_list[0][0], face_location_list[0][2])

                face_count = len(face_location_list)
                print(face_count)
                if error == 0 and face_count == 0:  # 中途退出，采集失败
                    start_time = time.time()
                    error = 1

                elif face_count > 1:  # 中途有别人，采集失败
                    type = 0
                    break
                elif face_count == 1 and error == 1:

                    error = 0
                else:
                    pass

                img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV,
                                                       cv2.COLOR_BGR2RGB))

                draw = ImageDraw.Draw(img_PIL)
                draw.text((int(image.shape[1] / 2), 30), action_name + "\n" + inf1,
                          font=ImageFont.truetype('resource/NotoSansCJK-Black.otf', 40),
                          fill=(255, 0, 0))  # linux

                # 转换回OpenCV格式
                img_OpenCV = cv2.cvtColor(np.asarray(img_PIL),
                                          cv2.COLOR_RGB2BGR)

                f = img_OpenCV
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                cv2.imshow('Collecting Faces', img_OpenCV)  # show the image

                image_name = os.path.join(self.imagedir, self.id,
                                          action + '_' + str(counter) + '.jpg')
                cv2.imwrite(image_name, origin_img)
                # Press 'ESC' for exiting video
                k = cv2.waitKey(100) & 0xff
                if k == 27:
                    break
                counter += 1
            if type == 0:
                break
        # 结束
        if type == 1:
            print('[INFO] 采集完毕')
            audioplayer.play_audio(os.path.join(audio_dir, 'end_capturing.mp3'))
            time.sleep(5)
        else:
            print('[INFO] 采集失败')
            audioplayer.play_audio(os.path.join(audio_dir, 'out_and_restart.mp3'))
            time.sleep(5)

        # 释放全部资源
        cam.release()
        cv2.destroyAllWindows()

    def startCollect(self):
        # 开启线程
        t = threading.Thread(target=self.run)
        t.start()

    def get_frame(self):
        global f
        if f != "":
            ret, jpeg = cv2.imencode('.jpg', f)
            # ret, jpeg = cv2.imencode('.jpg', )
            return jpeg.tobytes()
        else:
            return None
