# -*- coding: utf-8 -*-
'''
训练情感分析模型，判断笑没笑
用法：
python /home/reed/Desktop/code/oldcare/trainingfacialexpression.py
'''

# import the necessary packages
from datasets import SimpleDatasetLoader
from preprocessing import AspectAwarePreprocessor
from preprocessing import ImageToArrayPreprocessor
from conv import MiniVGGNet
from callback import TrainingMonitor
from imutils import paths
from sklearn.model_selection import train_test_split
from keras.optimizers import SGD
from keras.optimizers import *
from sklearn.metrics import classification_report
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder


# 全局变量
dataset_path = '/home/reed/Desktop/code/oldcare/images/emotion'# 图片数据
output_model_path = '/home/reed/Desktop/code/oldcare/models/mini/expression_mini_6400140sgd.hdf5'
output_plot_path = '/home/reed/Desktop/code/oldcare/plots/mini/expression_mini_6400140sgd.png'


# 全局常量
TARGET_WIDTH = 28
TARGET_HEIGHT = 28
BATCH_SIZE = 64
# BATCH_SIZE = 128
# EPOCHS = 15
EPOCHS = 40
LR_INIT = 0.01
# LR = 0.01
DECAY = LR_INIT/EPOCHS
MOMENTUM = 0.9


# 加载图片
aap = AspectAwarePreprocessor(TARGET_WIDTH, TARGET_HEIGHT)
iap = ImageToArrayPreprocessor()

print("[INFO] loading images...")
imagePaths = list(paths.list_images(dataset_path))

sdl = SimpleDatasetLoader(preprocessors=[aap, iap])
(data, labels) = sdl.load(imagePaths, 500, True)
data = data.astype("float") / 255.0

# convert the labels from integers to vectors
le = LabelEncoder().fit(labels)
labels = to_categorical(le.transform(labels), 2)# 分2类，笑和不笑

# account for skew in the labeled data
classTotals = labels.sum(axis=0)
classWeight = classTotals.max() / classTotals

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.20, stratify=labels, random_state=42)

# initialize the model
print("[INFO] compiling model...")
model = MiniVGGNet.build(width=TARGET_WIDTH,height=TARGET_HEIGHT, depth=1, classes=2)# 分两类，笑和不笑
opt = SGD(lr=LR_INIT, decay=DECAY, momentum = MOMENTUM, nesterov=True)# 优化器选的是SGD
# opt = Adam(lr=LR)# 优化器选的是adam
model.compile(loss="binary_crossentropy", optimizer=opt,metrics=["accuracy"])# 使用交叉熵损失函数

# construct the set of callbacks
callbacks = [TrainingMonitor(output_plot_path)]# 监控准确度和损失率

# train the network
print("[INFO] training network...")
H = model.fit(trainX, trainY, validation_data=(testX, testY),
	class_weight=classWeight, batch_size=BATCH_SIZE, epochs=EPOCHS,
    callbacks = callbacks, verbose=1)

# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=64)
print(classification_report(testY.argmax(axis=1),predictions.argmax(axis=1), target_names=le.classes_))

# save the model to disk
print("[INFO] serializing network...")
model.save(output_model_path)