import cv2
from utils.configuration import configuration as cfg
from app.preferences import pref_helpers as helper


def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_MOUSEWHEEL:
        # get the scaling factor
        factor = cfg['SCALING_FACTOR_ON_CV_WIN']
        # if it's going to be decremented, let the factor be reversed
        if flags < 0:
            factor = 1.0 / factor
        # resize the designated opencv-window by the scaling factor
        helper.adjust_cv_window_size(params[0], params[1], scaling_factor=factor)
