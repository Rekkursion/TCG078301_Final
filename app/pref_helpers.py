from PIL import Image
from utils.configuration import configuration as cfg
from app.pref import *


# get the pre-trained model
def get_model():
    return pref[MODEL]


# get the currently-loaded image as the type of pil-image
def get_current_image():
    if pref[CUR_LOADED_IMG_FILE_PATH] is None:
        return None
    img = Image.open(pref[CUR_LOADED_IMG_FILE_PATH])
    img = img.resize(cfg['SIZE_OF_IMGS'], Image.ANTIALIAS).convert(mode='RGB')
    return img


# set an image as the loaded image
def set_image_file_path(file_path):
    pref[CUR_LOADED_IMG_FILE_PATH] = file_path
