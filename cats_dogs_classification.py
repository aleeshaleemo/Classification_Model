# -*- coding: utf-8 -*-
"""Cats_Dogs_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F66FkkDr8xVy-yFO0HJqlz8IprN5nrFH
"""

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

"""**Batch normalization:** It serves to speed up training and use higher learning rates, making learning easier.
**Dense layers:** Dense layers are used **when association** can exist among any feature to any other feature in data point.
**Conv2D: **When neighborhoods matter to classify or detect
Maxpooling2D: ![maxpooling.jpg]
"""

train_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/drive/MyDrive/Train_Neural _Network/Train',
    labels='inferred',
    label_mode = 'int',
    batch_size=32,
    image_size=(256,256))
validation_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/drive/MyDrive/Train_Neural _Network/Test',
    labels='inferred',
    label_mode = 'int',
    batch_size=32,
    image_size=(256,256)
)

from google.colab import drive
drive.mount('/content/drive')

def process(image,label):
    image = tf.cast(image/255. ,tf.float32)
    return image,label

train_ds = train_ds.map(process)
validation_ds = validation_ds.map(process)

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

"""**To check file formats**"""

from pathlib import Path
import imghdr

data_dir = "/content/drive/MyDrive/Train_Neural _Network/Train"
image_extensions = [".png", ".jpg"]  # add there all your images file extensions

img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
for filepath in Path(data_dir).rglob("*"):
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")

history = model.fit(train_ds,epochs=20,validation_data=validation_ds)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

import cv2

test_img = cv2.imread('/content/drive/MyDrive/Train_Neural _Network/Test/CAT.png')

plt.imshow(test_img)

test_img.shape

test_img = cv2.resize(test_img,(256,256))

test_input = test_img.reshape((1,256,256,3))

model.predict(test_input)