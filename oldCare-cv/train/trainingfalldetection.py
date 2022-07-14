# -*- coding: utf-8 -*-
'''
训练摔倒检测模型,mini模型
用法：
python /home/reed/Desktop/code/oldcare/trainingfalldetection.py
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
from sklearn.metrics import classification_report
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.image import ImageDataGenerator


# 全局变量
dataset_path = 'D:/Codes/oldCare/oldCare-cv/data/falldetection'
output_model_path = 'D:/Codes/oldCare/oldCare-cv/models_saving/fall_detection_1.hdf5'
output_plot_path = 'D:/Codes/oldCare/oldCare-cv/plots/fall_detection.png'


# 全局常量
TARGET_WIDTH = 64
TARGET_HEIGHT = 64
BATCH_SIZE = 32
EPOCHS = 10
LR_INIT = 0.01
DECAY = LR_INIT/EPOCHS
MOMENTUM = 0.9


# 加载图片
aap = AspectAwarePreprocessor(TARGET_WIDTH, TARGET_HEIGHT)
iap = ImageToArrayPreprocessor()

print("[INFO] loading images...")
imagePaths = list(paths.list_images(dataset_path))

sdl = SimpleDatasetLoader(preprocessors=[aap, iap])
(data, labels) = sdl.load(imagePaths, 500, False)
data = data.astype("float") / 255.0

# convert the labels from integers to vectors
le = LabelEncoder().fit(labels)
labels = to_categorical(le.transform(labels), 2)

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data,labels, test_size=0.20, stratify=labels, random_state=42)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2,
                         zoom_range=0.2, horizontal_flip=True,
                         fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = MiniVGGNet.build(width=TARGET_WIDTH, height=TARGET_HEIGHT,depth=3, classes=2)
opt = SGD(lr=LR_INIT, decay=DECAY, momentum = MOMENTUM, nesterov=True)
model.compile(loss="binary_crossentropy", optimizer=opt,metrics=["accuracy"])

# construct the set of callbacks
callbacks = [TrainingMonitor(output_plot_path)]

# train the network
print("[INFO] training network...")
H=model.fit_generator(aug.flow(trainX, trainY,batch_size=BATCH_SIZE),
                      validation_data=(testX, testY),
                      steps_per_epoch=len(trainX) // BATCH_SIZE,
                      epochs=EPOCHS,
                      callbacks = callbacks, verbose=1)

# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=BATCH_SIZE)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=le.classes_))

# save the model to disk
print("[INFO] serializing network...")
model.save(output_model_path)