from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten


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
