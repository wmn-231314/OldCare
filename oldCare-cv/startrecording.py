# -*- coding: utf-8 -*-

'''
录像
按 Ctrl+C 结束录像

用法：
python startingrecording.py
python startingrecording.py --location room
'''

# 导入包

import time
import subprocess
import argparse
import cv2
import threading


class Startingrecording():
    def __init__(self, location):
        self.location = location

    def run(self):

        # # 传入参数
        # ap = argparse.ArgumentParser()
        # ap.add_argument("-f", "--location", required=False,
        #                 default = 'room', help="")
        # args = vars(ap.parse_args())
        location = self.location

        if location not in ['room', 'yard', 'corridor', 'desk']:
            raise ValueError('location must be one of room, yard, corridor or desk')

        # 全局变量
        camera_host_ip = '192.168.239.133'
        camera_host_port = 5001
        save_video_path = '../supervision/records/' + location + '_datetime.avi'.replace('datetime',
                                                                                         time.strftime('%Y%m%d-%H%M%S',
                                                                                                       time.localtime(
                                                                                                           time.time())))
        jug = 0
        try:
            while True:
                k = input()
                print(k)
                if k == '32':
                    if jug == 1:

                        # 主程序彻底结束之前，停止录像
                        stop_record_video_command = 'curl -X POST http://%s:%d/record_status -d "status=false"' % (
                        camera_host_ip, camera_host_port)
                        p = subprocess.Popen(stop_record_video_command, shell=True,
                                             stdout=subprocess.PIPE)
                        out, err = p.communicate()
                        out = str(out, encoding="utf8")

                        if err is None and out == 'stop record':
                            current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(time.time()))
                            print('[INFO] %s 停止录像程序启动了.' % (current_time))
                        else:
                            raise ValueError('[ERROR] 停止录像程序出现问题.')
                        jug = 0
                    else:
                        # 启动画面监控程序
                        save_video_path = 'records\\' + location + '_datetime.avi'.replace('datetime',
                                                                                                         time.strftime(
                                                                                                             '%Y%m%d-%H%M%S',
                                                                                                             time.localtime(
                                                                                                                 time.time())))
                        record_video_command = 'curl -X POST http://%s:%d/record_status -d "status=true&save_video_path=%s"' % (
                        camera_host_ip, camera_host_port,
                        save_video_path)
                        p = subprocess.Popen(record_video_command, shell=True,
                                             stdout=subprocess.PIPE)
                        out, err = p.communicate()
                        out = str(out, encoding="utf8")

                        if err is None and out == 'start record':
                            current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(time.time()))
                            print('[INFO] %s 录像程序启动了.' % (current_time))
                        else:
                            raise ValueError('[ERROR] 录像程序出现问题.')
                        jug = 1
        except KeyboardInterrupt:
            pass
        finally:
            pass

    def startStartrecord(self):
        # 开启线程
        t = threading.Thread(target=self.run)
        t.start()