#-*-coding:gb2312#-*-
from distutils.errors import PreprocessError
from pickle import FALSE, NONE
from pickletools import optimize
from keras import models
from keras import layers
from keras.utils import to_categorical
import numpy as np
from keras import callbacks
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import ShuffleSplit
import pandas as pd
import matplotlib.pyplot as plt
import json
from keras.applications import VGG16 
from keras import optimizers
from keras import losses
import matplotlib.pyplot as plt
from keras.callbacks import ModelCheckpoint
import os
import cv2

testnow=0
train_dir = "D:\\data\\garbage_classify\\train_data"  
test_dir = "D:\\data\\garbage_classify_et\\train_data"    
height=200
lenth=200
input_shape=(height,lenth,3)
input_shape1=(-1,height,lenth,3)
resize_shape=(height,lenth)
conv_base = VGG16(weights='imagenet',      
                  include_top=False,        
                  input_shape=input_shape) 


model = models.Sequential()             
model.add(conv_base)             #VGG16ģ�ͣ���ʹ��ԭʼ�ķ�����
model.add(layers.Flatten())  #����ȫ���Ӳ�;����������ˣ����������չƽ����������֮���Dense��      
model.add(layers.Dense(units=512,activation='relu'))
#model.add(layers.Dense(units=512,activation='relu'))#����Ϊ512��ȫ���Ӳ�
#model.add(layers.Dropout(0.3)) 
model.add(layers.Dense(units=40, activation='softmax'))  
conv_base.trainable=False    #��VGG16����Ϊ����ѵ��״̬����С����Ĳ�����
model.summary()
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

if(testnow==1):
    model.load_weights('D:\\data\\garbage_classify_et\\model.h5')
    test_img=cv2.imread('D:\\data\\garbage_classify_et\\t.jpg')
    test_img=cv2.resize(test_img,resize_shape)
    test_img=test_img.reshape(input_shape1)
    result=model.predict(test_img)
    result=np.argmax(result,axis=1)
    dict={
    "0": "�ɻ�����/һ���Կ�ͺ�",
    "1": "������/��������",
    "2": "������/�̵�",
    "3": "������/��ǩ",
    "4": "������/���黨�輰����",
    "5": "������/���",
    "6": "ʪ����/ʣ��ʣ��",
    "7": "������/���ͷ",
    "8": "ʪ����/ˮ����Ƥ",
    "9": "ʪ����/ˮ������",
    "10": "ʪ����/��Ҷ��",
    "11": "ʪ����/��Ҷ�˸�",
    "12": "ʪ����/����",
    "13": "ʪ����/���",
    "14": "�ɻ�����/��籦",
    "15": "�ɻ�����/��",
    "16": "�ɻ�����/��ױƷƿ",
    "17": "�ɻ�����/�������",
    "18": "�ɻ�����/��������",
    "19": "�ɻ�����/�����¼�",
    "20": "�ɻ�����/���ֽ��",
    "21": "�ɻ�����/��ͷ����",
    "22": "�ɻ�����/���·�",
    "23": "�ɻ�����/������",
    "24": "�ɻ�����/��ͷ",
    "25": "�ɻ�����/ë�����",
    "26": "�ɻ�����/ϴ��ˮƿ",
    "27": "�ɻ�����/������",
    "28": "�ɻ�����/ƤЬ",
    "29": "�ɻ�����/���",
    "30": "�ɻ�����/ֽ����",
    "31": "�ɻ�����/����ƿ",
    "32": "�ɻ�����/��ƿ",
    "33": "�ɻ�����/����ʳƷ��",
    "34": "�ɻ�����/��",
    "35": "�ɻ�����/ʳ����Ͱ",
    "36": "�ɻ�����/����ƿ",
    "37": "�к�����/�ɵ��",
    "38": "�к�����/���",
    "39": "�к�����/����ҩ��"
}
    print (dict['%d'%result])
    exit(0)
'''
def data_preprocess_t(data):
    data=data.copy()
    print(data.columns)
    #y=data.pop('label')
    x=data.values
    print(x.shape)
    #y=np.array(y)
    x.reshape(-1,28,28,1)
    
    return x
'''
#train= pd.read_csv(train_dir)

label=[]
test_label=[]
train_data=[]
test_data=[]
for i in range(0,19735):
    #print(os.path.exists(train_dir+"\\fimg_%d.txt"%i))
    if(os.path.exists(train_dir+"\\img_%d.txt"%i)==False):
        continue
    f=open(train_dir+"\\img_%d.txt"%i,'r')
    fi=f.readlines()
    train_image=cv2.imread(train_dir+"\\img_%d.jpg"%i)
    #print(type(train_image)==np.ndarray)
    if(type(train_image)!=np.ndarray):
        continue
    #print(train_image.shape)
    train_image=cv2.resize(train_image,resize_shape)
    train_image=train_image.reshape(input_shape1)
    train_data.append(train_image)
    for j in fi:
        j=j.strip('\n').split(",")
        #print(j[1])
        label.append(int(j[-1]))
label=np.array(label)
train_images = np.concatenate(train_data, axis=0)
train_labels=to_categorical(label)

for i in range(0,5000):
    #print(os.path.exists(train_dir+"\\fimg_%d.txt"%i))
    if(os.path.exists(test_dir+"\\fimg_%d.txt"%i)==False):
        continue
    f=open(test_dir+"\\fimg_%d.txt"%i,'r')
    fi=f.readlines()
    test_image=cv2.imread(test_dir+"\\fimg_%d.jpg"%i)
    #print(type(train_image)==np.ndarray)
    if(type(test_image)!=np.ndarray):
        continue
    #print(train_image.shape)
    test_image=cv2.resize(test_image,resize_shape)
    test_image=test_image.reshape(input_shape1)
    test_data.append(test_image)
    for j in fi:
        j=j.strip('\n').split(",")
        #print(j[1])
        test_label.append(int(j[-1]))
test_label=np.array(test_label)
test_images = np.concatenate(test_data, axis=0)
test_labels=to_categorical(test_label)
#plt.imshow(train_images[0])
#plt.show()
#print (test_labels.shape)
#print (test_images.shape)

def group_split(X, y, train_size=0.8):
    splitter = ShuffleSplit(train_size=train_size)  
    train, test = next(splitter.split(X, y))  
    return (X.iloc[train], X.iloc[test], y.iloc[train], y.iloc[test])

#train_images,test_images,train_labels,test_labels=group_split(train_images, train_labels, train_size=0.8)

model.fit(train_images,train_labels,validation_split=0.15,batch_size=64,epochs=5,
       callbacks=None)
loss, acc = model.evaluate(test_images, test_labels)
print("train model, accuracy:{:5.2f}%".format(100 * acc))
model.save_weights('D:\\data\\garbage_classify_et\\model.h5')

