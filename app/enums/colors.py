from enum import Enum


class Colors(Enum):
    # the color of the box for showing a 2d-face
    FACE_2D_BOX = (219, 34, 0)

    # the color of the box for showing a 3d-face
    FACE_3D_BOX = (97, 162, 14)

    # the color of the temporary box when the user is face-framing
    USER_FRAMING_BOX = (202, 91, 111)

    # the text-color of the log when an image is loaded successfully
    LOG_LOAD_IMAGE = (85, 79, 182)

    # the text-color of the log when the process of an image is done successfully
    LOG_PROCESS_DONE = (177, 91, 46)

    # the text-color of the log when the pretrained RekkModel is set
    LOG_REKKMODEL_SET = (143, 82, 204)

    # the text-color of the log when an image/a set of images has/have been saved
    LOG_IMAGE_SAVED = (107, 191, 146)

    # the text-color of the error-like log
    LOG_ERROR = (244, 61, 22)

    # the text-color of the warning-like log
    LOG_WARNING = (200, 155, 1)

    # for the convenience (no need to write Colors.XXX.value, only Colors.XXX is nice)
    def __get__(self, instance, owner):
        return self.value
