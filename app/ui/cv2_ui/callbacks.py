import cv2
from utils.configuration import configuration as cfg
from app.preferences import pref_helpers as helper


def mouse_callback(event, x, y, flags, params):
    win_name = params[0]
    # a mouse-wheeling event -> scale the image as well as the window
    if event == cv2.EVENT_MOUSEWHEEL:
        # get the scaling factor
        factor = cfg['SCALING_FACTOR_ON_CV_WIN']
        # if it's going to be decremented, let the factor be reversed
        if flags < 0:
            factor = 1.0 / factor
        # resize the designated opencv-window by the scaling factor
        helper.resize_cv_window(win_name, scaling_factor=factor)
    # a mouse-down event (right button) -> start the face-framing
    elif event == cv2.EVENT_RBUTTONDOWN:
        helper.start_framing_face_by_user(x, y)
    # a mouse-up event (right button) -> finish the face-framing
    elif event == cv2.EVENT_RBUTTONUP:
        helper.finish_framing_face_by_user(win_name, x, y)
    # a mouse-moving event -> frame the face
    elif event == cv2.EVENT_MOUSEMOVE:
        helper.frame_face_by_user(win_name, x, y)
        pass
