
import numpy as np

from keras import *
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam


def make_model() :
    model = Sequential()
    
    model.add(Conv2D(32, (3, 3), input_shape=(150, 150 ,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
    
    return model


if __name__ == '__main__' :
    batch_size = 16
    model = make_model()

    image_data_generator = ImageDataGenerator(rescale=1./255)
    train_image_data = image_data_generator.flow_from_directory(
        'sample' ,
        target_size = (150,150) ,
        batch_size = batch_size ,
        class_mode = 'sparse' ,
        shuffle = True
    )
    test_image_data = image_data_generator.flow_from_directory(
        'test' ,
        target_size = (150,150) ,
        batch_size = batch_size ,
        class_mode = 'sparse' ,
        shuffle = True
    )

    model.fit_generator(
        train_image_data ,
        steps_per_epoch = train_image_data.samples // batch_size ,
        validation_data = test_image_data ,
        validation_steps = test_image_data.samples // batch_size ,
        epochs = train_image_data.samples
    )

    predict_result = model.predict_generator(
        test_image_data ,
        steps = test_image_data.samples // batch_size
    )
    classes_result = test_image_data.classes

    for index in zip(predict_result,classes_result) :
        print(index)


