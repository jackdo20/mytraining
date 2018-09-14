from __future__ import print_function
from keras.models import load_model
from PIL import Image
import numpy as np
import os

PIC_W = 240
PIC_H = 240
MODEL_NAME = "AlexNet_Model.h5"
picPath = "./test1/27.jpg"


def ResizePic(picPath):
    if os.path.exists(picPath):
        pic=Image.open(picPath)
        pic=pic.resize((PIC_W,PIC_H))
        picArr=np.asarray(pic)
        picArr=np.expand_dims(picArr,axis=0)
    else:
        print("Not Found !")
    return picArr

def ClassPredict(picArr):
    model = load_model(MODEL_NAME)
    result = model.predict(picArr)
    print("Cat Possibility: ",result[0,0])
    print("Dog Possibility: ",result[0,1])
    if result[0,0] > result[0,1]:
        print("It is a Cat !")
    else:
        print("It is a Dog !")

if __name__=="__main__":
    picArr = ResizePic(picPath)
    ClassPredict(picArr)
