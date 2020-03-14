import keras
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.datasets import cifar10
from keras import regularizers
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler
import numpy as np


(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

def cifar10_extract(x_train, y_train, target_label):
  target_instance = y_train==target_label
  target_instance = target_instance.reshape(target_instance.size)
  
  x_target = x_train[target_instance]
  y_target = np.full((5000, 1), target_label)
  
  return (x_target[:1000], y_target[:1000])

def cifar10_merge_and_shuffle(x_train, y_train):
  (real_x_train, real_y_train) = cifar10_extract(x_train, y_train, 0)
  for i in range(1, 10):
    real_x_train = np.concatenate((real_x_train, (cifar10_extract(x_train, y_train, i))[0]), axis=0)
    real_y_train = np.concatenate((real_y_train, (cifar10_extract(x_train, y_train, i))[1]), axis=0)
    
  s = np.arange(real_x_train.shape[0])
  np.random.shuffle(s)
  real_x_train = real_x_train[s]
  real_y_train = real_y_train[s]
  
  return (real_x_train, real_y_train)

(x_train, y_train) = cifar10_merge_and_shuffle(x_train, y_train)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

mean = np.mean(x_train,axis=(0,1,2,3))
std = np.std(x_train,axis=(0,1,2,3))
x_train = (x_train-mean)/(std+1e-7)
x_test = (x_test-mean)/(std+1e-7)

num_classes = 10
y_train = np_utils.to_categorical(y_train,num_classes)
y_test = np_utils.to_categorical(y_test,num_classes)

def lr_schedule(epoch):
    lrate = 0.01
    if epoch > 50:
        lrate = 0.001
    if epoch > 75:
        lrate = 0.0005
    if epoch > 95:
        lrate = 0.0001
    return lrate

weight_decay = 1e-4
model = Sequential()
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay), input_shape=x_train.shape[1:]))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))
 
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.3))
 
model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))
 
model.add(Flatten())
model.add(Dense(512, activation='elu',kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
 
model.summary()
 
# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    )
datagen.fit(x_train)
 
# Training
batch_size = 128 
opt_adam = Adam(lr=0.001,decay=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(loss='categorical_crossentropy', optimizer=opt_adam, metrics=['accuracy'])
model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),\
                    steps_per_epoch=x_train.shape[0] // batch_size,epochs=120,
                    verbose=1,validation_data=(x_test,y_test),callbacks=[LearningRateScheduler(lr_schedule)])

 # Testing
scores = model.evaluate(x_test, y_test, batch_size=100, verbose=1)
print('Accuracy: %.3f loss: %.3f' % (scores[1]*100,scores[0]))
