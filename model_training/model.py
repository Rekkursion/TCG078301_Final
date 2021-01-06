import cv2
import numpy as np
import tensorflow
from PIL import Image
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Sequential

from utils.configuration import configuration as cfg


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
        self.add(Conv2D(128, kernel_size=3, activation='relu', input_shape=input_shape))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(128, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(64, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(64, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        self.add(Conv2D(64, kernel_size=3, activation='relu'))
        self.add(MaxPooling2D(pool_size=(2, 2)))
        # the flatten layer
        self.add(Flatten())
        # the fully-connected layers
        self.add(Dense(128, activation='relu'))
        self.add(Dense(128, activation='relu'))
        self.add(Dense(128, activation='relu'))
        self.add(Dense(num_classes, activation='softmax'))

    # do the prediction from the model and return the prediction ('2D' or '3D')
    def do_prediction(self, img):
        if not (img is None):
            # convert the opencv-image into a pil-image
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))\
                .resize(cfg['SIZE_OF_IMGS'], Image.ANTIALIAS)\
                .convert(mode='RGB')
            # then convert the converted image into a numpy-array
            arr = np.asarray(pil_img)
            # reshape it to a rank-4 tensor
            arr = np.reshape(arr, (1, arr.shape[0], arr.shape[1], 3))
            # use cpu instead of gpu
            with tensorflow.device('/cpu:0'):
                # pred = self.predict_classes(arr)
                # do the prediction
                pred = np.argmax(self.predict(arr), axis=-1)
                # return the label of the prediction ('2D' or '3D')
                return cfg['CLS_NAMES'][pred[0]]
            # print('predicted:', cfg['CLS_NAMES'][pred[0]])
        else:
            return 'NONE'
