import face_recognition
import cv2
import time
# 超参数
detection_method = 'hog' # either 'hog' or 'cnn'. default is hog.
# 初始化摄像头
cap = cv2.VideoCapture(0)
cap.set(0, 640)  # set Width (the first parameter is property_id)
cap.set(1, 480)  # set Height
time.sleep(2)

while True:  # 拍100张图片就结束
    ret, img = cap.read()
    # 人脸检测不依赖色彩，所以先把人脸图像转成灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_locations = face_recognition.face_locations(
        gray, number_of_times_to_upsample=1,
        model=detection_method)
    # 人脸位置
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(img, (left, top), (right, bottom),
                      (0, 0, 255), 2)
        cv2.rectangle(gray, (left, top), (right, bottom),
                      (0, 0, 255), 2)

    cv2.imshow('origin image', img)
    cv2.imshow('grayscale image', gray)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
