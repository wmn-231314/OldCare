import cv2
import imutils
import numpy
import time
import subprocess

#推流的地址
# 说明: 启动livego,用浏览器访问http://ip:8090/control/get?room=movie 得到channelkey
# rfBd56ti2SMtYvSgD5xAV0YU99zampta7Z7S575KLkIZ9PYk 就是channelkey
# rtmp地址格式 : rtmp://ip:1935/{appname}/{channelkey}
# 接收端访问rtmp视频流地址:
from falldetection import checkingfalldetection

rtmp = "rtmp://1.15.63.218:1935/live/rfBd56ti2SMtYvSgD5xAV0YU99zampta7Z7S575KLkIZ9PYk"

#IPCameraUrl = 'rtsp://admin:admin@192.168.3.20:8554/live'
#cap = cv2.VideoCapture(path) #path可以填本地的一个媒体文件路径 比如 E:\\1.flv
#cap = cv2.VideoCapture(IPCameraUrl)  # 也可以打开IP摄像头
cap = cv2.VideoCapture(0)  # 0代表本地摄像头

cv2.namedWindow('video',cv2.WINDOW_NORMAL)

#打开摄像头

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#画面尺寸  ffmpeg命令用
sizeStr = str(size[0]) + 'x' + str(size[1])

# windows 下要加 'cmd','/c', 不然会报错
command = ['cmd','/c',
    'ffmpeg',
    '-y', '-an',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', '20',  # 帧率  尽量与原视频流帧率一致,否则会出现各种问题  broken pipe,速度慢等
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    '-g','5',
    # '-b:v',' 700000',
    rtmp]

pipe = subprocess.Popen(command,stdin=subprocess.PIPE)
count = 0

fall_model = None
# 循环读取每一帧数据
while cap.isOpened():
    #返回标记和这一帧数据
    ret, frame = cap.read()
    (grabbed, frame) = cap.read()
    image = checkingfalldetection(grabbed, frame,fall_model)
    if image is None:
        pipe.stdin.write(frame.tobytes())
        continue
    image = imutils.resize(frame, width=640, height=480)

    # 显示数据,用窗口显示图像,可能会造成延迟卡顿,一般不显示
    cv2.imshow('video',image)
    key = cv2.waitKey(1)
    # 窗口处输入q结束程序
    if key == ord('q'):
        break
    pipe.stdin.write(frame.tobytes())

pipe.terminate()
cap.release()
cv2.destroyAllWindows()