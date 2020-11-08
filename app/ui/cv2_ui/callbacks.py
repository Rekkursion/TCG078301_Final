import cv2
from utils.configuration import configuration as cfg
from app.preferences import pref_helpers as helper


def mouse_callback(event, x, y, flags, params):
    # a mouse-wheeling event
    if event == cv2.EVENT_MOUSEWHEEL:
        # get the scaling factor
        factor = cfg['SCALING_FACTOR_ON_CV_WIN']
        # if it's going to be decremented, let the factor be reversed
        if flags < 0:
            factor = 1.0 / factor
        # resize the designated opencv-window by the scaling factor
        helper.resize_cv_window(params[0], params[1], scaling_factor=factor)
    # a mouse-down event (right button)
    elif event == cv2.EVENT_RBUTTONDOWN:
        helper.start_framing_face_by_user(x, y)
    # a mouse-up event (right button)
    elif event == cv2.EVENT_RBUTTONUP:
        helper.finish_framing_face_by_user(params[0], params[1], x, y)
    # a mouse-moving event
    elif event == cv2.EVENT_MOUSEMOVE:
        helper.frame_face_by_user(params[0], params[1], x, y)
        pass
