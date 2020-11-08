from threading import Lock

pref = {
    # the pre-trained rekk-model (used to judge a face image is a 2D or a 3D avatar)
    'REKK_MODEL': None,

    # the pre-trained retinaface model from insightface (used to detect the faces from an image)
    'RETINAFACE_MODEL': None,

    # the file path of currently-loaded image
    'CUR_LOADED_IMG_FILE_PATH': None,

    # the threading-lock for doing the process of detection (and judgement)
    'PROCESS_LOCK': Lock(),

    # the size-offsets of some opencv windows
    'CV_WIN_SIZES': dict()
}


REKK_MODEL = 'REKK_MODEL'
RETINAFACE_MODEL = 'RETINAFACE_MODEL'
CUR_LOADED_IMG_FILE_PATH = 'CUR_LOADED_IMG_FILE_PATH'
PROCESS_LOCK = 'PROCESS_LOCK'
CV_WIN_SIZES = 'CV_WIN_SIZES'
