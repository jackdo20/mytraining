from __future__ import print_function
import shutil
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Activation,Flatten,BatchNormalization
from keras.layers.convolutional import Conv2D,MaxPooling2D
from keras.optimizers import SGD,Adam

def Makekdir(path="./dataset/"):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        os.makedirs(path+"train/")
        os.makedirs(path+"validation/")
        os.makedirs(path+"train/cat/")
        os.makedirs(path+"train/dog/")
        os.makedirs(path+"validation/cat/")
        os.makedirs(path+"validation/dog/")
        #print("Dataset folder created !")
    else:
        trainCatFolder=os.path.exists(path+"train/cat/")
        trainDogFolder=os.path.exists(path+"train/dog/")
        if not trainCatFolder:
            os.makedirs(path+"train/cat/")
        if not trainDogFolder:
            os.makedirs(path+"train/dog/")
        validationCatFolder=os.path.exists(path+"validation/cat/")
        validationDogFolder=os.path.exists(path+"validation/dog/")
        if not validationCatFolder:
            os.makedirs(path+"validation/cat/")
        if not validationDogFolder:
            os.makedirs(path+"validation/dog/")

    print("Dataset folder Created!")

def PicClassify():
    trainCatPath = "./dataset/train/cat/"
    trainDogPath = "./dataset/train/dog/"
    validationCatPath = "./dataset/validation/cat/"
    validationDogPath = "./dataset/validation/dog/"
    oriPath = "./train/"
    picFiles = os.listdir(oriPath)
    if os.listdir(trainCatPath) == [] or os.listdir(trainDogPath) ==[]:
        for pic in picFiles[:24000]:
            if pic.split(".")[0] == "cat":
                shutil.copy2(oriPath+pic,trainCatPath)
            if pic.split(".")[0] == "dog":
                shutil.copy2(oriPath+pic,trainDogPath)
        #print("pic Classified !")
    if os.listdir(validationCatPath) == [] or os.listdir(validationDogPath) ==[]:
        for pic in picFiles[24000:]:
            if pic.split(".")[0] == "cat":
                shutil.copy2(oriPath+pic,validationCatPath)
            if pic.split(".")[0] == "dog":
                shutil.copy2(oriPath+pic,validationDogPath)
    else:
        print("Already Classified !")

def DataPreprocess():
    trainDataGen = ImageDataGenerator(
        horizontal_flip = True,
        #vertical_flip = True,
        zoom_range = 0.2
    )
    validationDataGen = ImageDataGenerator(
        #horizontal_flip = True,
        #vertical_flip = True,
        zoom_range = 0.2
    )
    train_generator = trainDataGen.flow_from_directory(
        "./dataset/train",
        target_size = (240,240),
        batch_size = 16,
        #class_mode = "binary"
    )
    validation_generator= validationDataGen.flow_from_directory(
        "./dataset/validation",
        target_size = (240,240),
        batch_size = 16,
        #class_mode = "binary"
    )
    return train_generator,validation_generator

def NetworkCreate():
    model = Sequential()
    
    #model.add(Conv2D(4,(5,5),activation="relu",input_shape=(240,240,3)))
    model.add(Conv2D(16,(5,5),input_shape=(240,240,3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    #model.add(Conv2D(8,(3,3),activation="relu"))
    model.add(Conv2D(32,(3,3),activation="relu"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    #model.add(Conv2D(16,(3,3),activation="relu"))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation("softmax"))

    return model

def AlexNetCreate():
    # AlexNet
    model = Sequential()
    model.add(Conv2D(filters=96, kernel_size=(11,11),
                     strides=(4,4), padding='valid',
                     input_shape=(240,240,3),
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(3,3), 
                           strides=(2,2), 
                           padding='valid'))
    model.add(Conv2D(filters=256, kernel_size=(5,5), 
                     strides=(1,1), padding='same', 
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(3,3), 
                           strides=(2,2), 
                           padding='valid'))
    model.add(Conv2D(filters=384, kernel_size=(3,3), 
                     strides=(1,1), padding='same', 
                     activation='relu'))
    model.add(Conv2D(filters=384, kernel_size=(3,3), 
                     strides=(1,1), padding='same', 
                     activation='relu'))
    model.add(Conv2D(filters=256, kernel_size=(3,3), 
                     strides=(1,1), padding='same', 
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=(3,3), 
                           strides=(2,2), padding='valid'))
    
    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.5))
    
    # Output Layer
    model.add(Dense(2))
    model.add(Activation('softmax'))
    
    #model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])

    return model

def Training(model,train_gen,valid_gen):
    adam= Adam(lr=0.001)
    model.compile(
        loss = "categorical_crossentropy",
        optimizer = 'sgd',
        #optimizer = adam,
        metrics = ['accuracy']
    )
    model.fit_generator(
        train_gen,
        steps_per_epoch = 200,
        epochs = 40,
        validation_data = valid_gen,
        #shuffle = True
    )

if __name__ == "__main__":
    Makekdir()
    PicClassify()
    train_gen,valid_gen = DataPreprocess()
    #model = NetworkCreate() # No performance
    if os.path.exists("AlexNet_Model.h5"):
        model=load_model("AlexNet_Model.h5")
    else:
        model = AlexNetCreate()
    print("Model Classes:", valid_gen.class_indices)
    Training(model,train_gen,valid_gen)
    
    model.save("AlexNet_Model.h5")
    print("Done !")

 
