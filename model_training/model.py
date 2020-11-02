from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from PIL import Image
import numpy as np
from utils.configuration import configuration as cfg
from app.pref import *


# the model to be used in detecting the 2D and 3D images
class RekkModel(Sequential):
    def __init__(self, input_shape, num_classes):
        super(RekkModel, self).__init__()
        # create the model
        self.build_up(input_shape, num_classes)
        # set the optimizer and the loss function
        self.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    # build up the model
    def build_up(self, input_shape, num_classes):
        # create and add the layers
        # the convolutional layers
        self.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=input_shape))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(32, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(32, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(64, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        # the flatten layer
        self.add(Flatten())
        # the fully-connected layers
        self.add(Dense(128, activation='relu'))
        self.add(Dense(num_classes, activation='softmax'))

    # do the prediction from a designated model
    def do_prediction(self):
        img = Image.open(pref[CUR_LOADED_IMG])
        img = img.resize(cfg['SIZE_OF_IMGS'], Image.ANTIALIAS).convert(mode='RGB')
        # noinspection PyArgumentList
        arr = np.asarray(img).reshape(1, cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3)
        pred = self.predict_classes(arr)
        print('predicted:', cfg['CLS_NAMES'][pred[0]])
