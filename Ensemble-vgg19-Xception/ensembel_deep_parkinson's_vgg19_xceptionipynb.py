# -*- coding: utf-8 -*-
"""Ensembel_Deep_parkinson's_vgg19-xceptionipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-OffcJFVTjcYg3FpEm9Uzp0FgFnit1We

# Ensembling VGG19-Xception
"""

from google.colab import drive
drive.mount('/content/drive')

"""**Load Images**"""

import os
import numpy as np
import matplotlib.pyplot as plt

images = "/content/drive/MyDrive/parkinsons t2/train"

folders = os.listdir(images)
print(folders)

image_data = []
labels = []

label_dict = {
    'control':0,
    'pd':1
}

from keras.preprocessing import image

for ix in folders:
    path = os.path.join(images,ix)
    for im in os.listdir(path):
        img = image.load_img(os.path.join(path,im),target_size = ((512,512)))
        img_array = image.img_to_array(img)
        image_data.append(img_array)
        labels.append(label_dict[ix])

print(len(image_data),len(labels))

combined = list(zip(image_data,labels))
image_data[:],labels[:] = zip(*combined)

print(labels)

x_train = np.array(image_data)
y_train = np.array(labels)

print(x_train.shape,y_train.shape)

from keras.utils import np_utils

y_train = np_utils.to_categorical(y_train)
print(x_train.shape,y_train.shape)

from keras.preprocessing.image import ImageDataGenerator

"""**Data Augmentation**

"""

augment = ImageDataGenerator( 
                             rotation_range=20,
                              width_shift_range=0.01, 
                              height_shift_range=0.01, 
                              horizontal_flip=False, 
                              vertical_flip=False,
                            )
augment.fit(x_train)

from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2

"""**Load VGG19 Model**"""

model = VGG19(include_top = False,weights = 'imagenet',input_shape = (512,512,3))

model.summary()

for ix in range(len(model.layers)):
    print(ix,model.layers[ix])

"""**Fine Tuning**"""

for layer in model.layers[:19]:
    layer.trainable = False
for i, layer in enumerate(model.layers):
    print(i, layer.name, layer.trainable)

av1 = Flatten()(model.output)
fc1 = Dense(256,activation='relu',kernel_regularizer= l2(0.01),input_dim=256)(av1)
d1 = Dropout(0.5)(fc1)
fc2 = Dense(128,activation='relu',kernel_regularizer= l2(0.01),input_dim=128)(d1)
d2 = Dropout(0.5)(fc2)
fc3 = Dense(2,activation = 'sigmoid')(d2)


model_vgg = Model(model.input,fc3)
model_vgg.summary()

from tensorflow.keras.applications import Xception

"""**Loading Xception Model**"""

model1 = Xception(include_top=False, input_shape=(512,512,3), weights='imagenet')

model1.summary()

for ix in range(len(model1.layers)):
    print(ix,model1.layers[ix])

"""**Fine Tuning**"""

for layer in model1.layers[:127]:
    layer.trainable = False
for i, layer in enumerate(model1.layers):
    print(i, layer.name, layer.trainable)

av1 = Flatten()(model1.output)
fc1 = Dense(256,activation='relu',kernel_regularizer= l2(0.01),input_dim=256)(av1)
d1 = Dropout(0.5)(fc1)
fc2 = Dense(128,activation='relu',kernel_regularizer= l2(0.01),input_dim=128)(d1)
d2 = Dropout(0.5)(fc2)
fc3 = Dense(2,activation = 'sigmoid')(d2)


model_x = Model(model1.input,fc3)
model_x.summary()

"""**VGG19-Xcpetion-Average**"""

import tensorflow as tf
models = [model_x,model_vgg]
model_input = tf.keras.Input(shape=(512, 512, 3))
model_outputs = [model(model_input) for model in models]
ensemble_output = tf.keras.layers.Average()(model_outputs)
ensemble_model = tf.keras.models.Model(inputs=model_input, outputs=ensemble_output, name='ensemble')

ensemble_model.summary()

adam = Adam(learning_rate=0.0001)
ensemble_model.compile(loss='categorical_crossentropy',optimizer = adam,metrics=['accuracy'])

tf.keras.utils.plot_model(ensemble_model, 'model.png', show_shapes= True)

from tensorflow.keras.callbacks import ModelCheckpoint

filepath="parkinsons_detection_ensemble.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=2, save_best_only=True, mode='min',patience=5)
callbacks_list = [checkpoint]

"""**Model-Training**"""

hist = ensemble_model.fit(x_train,y_train,
                    shuffle = True,
                    batch_size=32,
                    epochs = 25,
                    validation_split = 0.10,callbacks=callbacks_list)

plt.figure(1, figsize = (15, 5))
plt.subplot(1,2,1)
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.plot( hist.history["loss"], label = "Training Loss")
plt.plot( hist.history["val_loss"], label = "Validation Loss")
plt.grid(True)
plt.legend()

plt.subplot(1,2,2)
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.plot( hist.history["accuracy"], label = "Training Accuracy")
plt.plot( hist.history["val_accuracy"], label = "Validation Accuracy")
plt.grid(True)
plt.legend()

test_images = "/content/drive/MyDrive/parkinsons t2/test"

test_image_data = []
test_labels = []

test_folders = os.listdir(test_images)
print(test_folders)

label_dict = {
    'control':0,
    'pd':1
}

from keras.preprocessing import image

for ix in test_folders:
    path = os.path.join(test_images,ix)
    for im in os.listdir(path):
        img = image.load_img(os.path.join(path,im),target_size = ((512,512)))
        img_array = image.img_to_array(img)
        test_image_data.append(img_array)
        test_labels.append(label_dict[ix])
        

combined = list(zip(test_image_data,test_labels))
test_image_data[:],test_labels[:] = zip(*combined)

x_test = np.array(test_image_data)
y_test = np.array(test_labels)

from keras.utils import np_utils

y_test = np_utils.to_categorical(y_test)
print(x_test.shape,y_test.shape)

ensemble_model.evaluate(x_test,y_test)

from sklearn.metrics import classification_report,confusion_matrix

predictions = ensemble_model.predict(x_test, batch_size = 32)
pred = np.argmax(predictions, axis=1)

print(classification_report(test_labels, pred))

print(confusion_matrix(test_labels, pred))

