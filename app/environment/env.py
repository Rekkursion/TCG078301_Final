from threading import Lock

env_dict = {
    # the pretrained rekk-model (used to judge a face image is a 2D or a 3D avatar)
    'REKK_MODEL': None,

    # the pretrained retinaface model from insightface (used to detect the faces from an image)
    'RETINAFACE_MODEL': None,

    # the threading-lock for doing the process of detection (and judgement)
    'PROCESS_LOCK': Lock(),

    # the boolean value to check if the user is currently framing the face
    'FRAMING_FACE_BY_USER': False,

    # the start point of face-framing
    'FRAMING_PT_1': None,

    # the sampling counter of by-user face-framing
    'SAMPLING_COUNTER_OF_FRAMING': 0
}


REKK_MODEL = 'REKK_MODEL'
RETINAFACE_MODEL = 'RETINAFACE_MODEL'
PROCESS_LOCK = 'PROCESS_LOCK'
FRAMING_FACE_BY_USER = 'FRAMING_FACE_BY_USER'
FRAMING_PT_1 = 'FRAMING_PT_1'
SAMPLING_COUNTER_OF_FRAMING = 'SAMPLING_COUNTER_OF_FRAMING'
