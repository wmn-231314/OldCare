from sys import platform

import cv2
import time
import subprocess as sp
import multiprocessing
import psutil


class stream_pusher(object):
    def __init__(self, rtmp_url=None, raw_frame_q=None):
        self.rtmp_url = rtmp_url
        self.raw_frame_q = raw_frame_q
        width = 640
        height = 480
        fps=15

        # self.command = ['cmd', '/c',
        #            'ffmpeg',
        #            '-y', '-an',
        #            '-f', 'rawvideo',
        #            '-vcodec', 'rawvideo',
        #            '-pix_fmt', 'bgr24',
        #            '-s', "{}x{}".format(width, height),
        #            '-r', '30',  # 帧率  尽量与原视频流帧率一致,否则会出现各种问题  broken pipe,速度慢等
        #            '-i', '-',
        #            '-c:v', 'libx264',
        #            '-pix_fmt', 'yuv420p',
        #            '-preset', 'ultrafast',
        #            '-f', 'flv',
        #            '-g', '5',
        #            '-b:v', ' 700000',
        #            self.rtmp_url]

        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        '-g', '5',
                        '-b:v', ' 700000',
                        self.rtmp_url]

    def __frame_handle__(self, raw_frame, text, shape1, shape2):
        return (raw_frame)

    def push_frame(self):
        p = psutil.Process()
        p.cpu_affinity([0, 1, 2, 3])
        p = sp.Popen(self.command, stdin=sp.PIPE)

        while True:
            if not self.raw_frame_q.empty():
                raw_frame, text, shape1, shape2 = self.raw_frame_q.get()
                frame = self.__frame_handle__(raw_frame, text, shape1, shape2)

                p.stdin.write(frame.tobytes())
            else:
                time.sleep(0.001)

    def run(self):
        push_frame_p = multiprocessing.Process(target=self.push_frame, args=())
        push_frame_p.daemon = True
        push_frame_p.start()


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    rtmpUrl = "rtmp://1.15.63.218:1935/live/L17LTlsVqMNTZyLKMIFSD2x28MlgPJ0SDZVHnHJPxMKi0tWx"
    raw_q = multiprocessing.Queue(100)

    my_pusher = stream_pusher(rtmp_url=rtmpUrl, raw_frame_q=raw_q)
    my_pusher.run()
    while True:
        grabbed, image = cap.read()
        info = (image, '2', '3', '4')  # 把需要送入队列的内容进行封装
        if not raw_q.full():  # 如果队列没满
            raw_q.put(info)  # 送入队列
        # cv2.waitKey(1)
    cap.release()
    print('finish')
