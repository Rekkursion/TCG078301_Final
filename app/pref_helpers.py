import cv2
import insightface
from model_training.model import RekkModel
from utils.configuration import configuration as cfg
from app.pref import *


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
    # img = Image.open(pref[CUR_LOADED_IMG_FILE_PATH])
    # img = img.resize(cfg['SIZE_OF_IMGS'], Image.ANTIALIAS).convert(mode='RGB')
    img = cv2.imread(pref[CUR_LOADED_IMG_FILE_PATH], cv2.IMREAD_COLOR)
    # img = cv2.resize(img, cfg['SIZE_OF_IMGS'], interpolation=cv2.INTER_CUBIC)
    return img


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
