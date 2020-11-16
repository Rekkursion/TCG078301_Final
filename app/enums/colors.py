from enum import Enum


class Colors(Enum):
    # the color of the box for showing a 2d-face
    FACE_2D_BOX = (219, 34, 0)

    # the color of the box for showing a 3d-face
    FACE_3D_BOX = (97, 162, 14)

    # the color of the temporary box when the user is face-framing
    USER_FRAMING_BOX = (202, 91, 111)

    # the color of the general log
    LOG_GENERAL = (85, 79, 182)

    # the color of the error-like log
    LOG_ERROR = (244, 61, 22)

    # for the convenience (no need to write Colors.XXX.value, only Colors.XXX is nice)
    def __get__(self, instance, owner):
        return self.value
