import cv2
import insightface
import numpy as np
from model_training.model import RekkModel
from utils.configuration import configuration as cfg
from app.preferences.pref import *


# get the pre-trained rekk-model
def get_rekk_model():
    return pref[REKK_MODEL]


# get the pre-trained retinaface model from insightface
def get_retinaface_model():
    return pref[RETINAFACE_MODEL]


# get the currently-loaded image as the type of cv2-image
def get_current_image():
    if pref[CUR_LOADED_IMG_FILE_PATH] is None:
        return None
    img = cv2.imread(pref[CUR_LOADED_IMG_FILE_PATH], cv2.IMREAD_COLOR)
    return img


# get the lock for processing of detection (and judgement)
def get_process_lock():
    return pref[PROCESS_LOCK]


# get the file path of the loaded image
def get_image_file_path():
    return pref[CUR_LOADED_IMG_FILE_PATH]


# set an image as the loaded image
def set_image_file_path(file_path):
    pref[CUR_LOADED_IMG_FILE_PATH] = file_path


# load the pre-trained models of both rekk-model and retinaface
def load_pretrained_models():
    # load the pre-trained rekk-model which is used to judge the 2D/3D avatar (face)
    pref[REKK_MODEL] = RekkModel((cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3), 2)
    pref[REKK_MODEL].load_weights('../model_training/pretrained_model/rekk_model.h5')
    # load the pre-trained retinaface from insightface which is used to detect the faces from an image
    pref[RETINAFACE_MODEL] = insightface.model_zoo.get_model('retinaface_r50_v1')
    pref[RETINAFACE_MODEL].prepare(ctx_id=-1, nms=0.4)


# adjust the size of a certain opencv-window
def adjust_cv_window_size(win_name, img, scaling_factor=None, reset_size=None):
    new_size = None
    # resize the window by the scaling factor
    if scaling_factor is not None and win_name in pref[CV_WIN_SIZES]:
        new_size = [int(pref[CV_WIN_SIZES][win_name][0] * scaling_factor), int(pref[CV_WIN_SIZES][win_name][1] * scaling_factor)]
    # reset the window-size
    elif reset_size is not None:
        new_size = [reset_size[0], reset_size[1]]
    # if either resizing or resetting, apply the adjustment; do nothing if neither of them is chosen
    if new_size is not None:
        # set the new size on preference
        pref[CV_WIN_SIZES][win_name] = new_size
        # actually size the opencv-window
        resized = cv2.resize(img, tuple(pref[CV_WIN_SIZES][win_name]), interpolation=cv2.INTER_CUBIC)
        # re-show the resized/reset'd image
        cv2.imshow(win_name, resized)
