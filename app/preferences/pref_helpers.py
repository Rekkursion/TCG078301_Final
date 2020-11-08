import cv2
import insightface
import numpy as np
from model_training.model import RekkModel
from utils.configuration import configuration as cfg
from utils.help_func import judge_avatars, draw_boxes, make_sure_order_of_points
from app.preferences.pref import *


# get the pre-trained rekk-model
def get_rekk_model():
    return pref[REKK_MODEL]


# get the pre-trained retinaface model from insightface
def get_retinaface_model():
    return pref[RETINAFACE_MODEL]


# get the lock for processing of detection (and judgement)
def get_process_lock():
    return pref[PROCESS_LOCK]


# start the by-user face-framing
def start_framing_face_by_user(x, y):
    pref[FRAMING_FACE_BY_USER] = True
    pref[FRAMING_PT_1] = (x, y)


# finish the by-user face-framing
def finish_framing_face_by_user(win_name, img, x, y):
    if pref[FRAMING_PT_1][0] != x or pref[FRAMING_PT_1][1] != y:
        x1, y1, x2, y2 = make_sure_order_of_points((x, y), pref[FRAMING_PT_1])
        # frame out the user-framing face
        face = img[y1:y2, x1:x2]
        # judge it
        judged = judge_avatars([(face, (x1, y1), (x2, y2))])
        # draw it out
        draw_boxes(win_name, img, judged)
    # dispel the status of framing face
    pref[FRAMING_FACE_BY_USER] = False
    pref[FRAMING_PT_1] = None
    # zero-fy the sampling counter
    pref[SAMPLING_COUNTER_OF_FRAMING] = 0


# frame the face by user
def frame_face_by_user(win_name, img, x, y):
    # do the framing (draw the rectangle) only if the right button is down
    if pref[FRAMING_FACE_BY_USER]:
        # to avoid low efficiency, sample a certain frames to do the framing (draw the rectangle), e.g., draw it per 5 times when the mouse-move event is invoked
        pref[SAMPLING_COUNTER_OF_FRAMING] += 1
        if pref[SAMPLING_COUNTER_OF_FRAMING] == cfg['SAMPLING_RATE_OF_FRAMING_ON_CV_WIN']:
            # copy a new image
            copied = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_REPLICATE)
            # draw the user-framing rectangle (semi-transparent filled)
            filled_rect = np.zeros(img.shape, np.uint8)
            cv2.rectangle(filled_rect, (x, y), pref[FRAMING_PT_1], (202, 91, 111), -1)
            copied = cv2.addWeighted(copied, 0.5, filled_rect, 0.5, 1)
            # draw the user-framing rectangle (border)
            cv2.rectangle(copied, (x, y), pref[FRAMING_PT_1], (202, 91, 111), 2)
            # show the boxes-drawn image
            cv2.imshow(win_name, copied)
            # re-zero the sampling counter
            pref[SAMPLING_COUNTER_OF_FRAMING] = 0


# load the pre-trained models of both rekk-model and retinaface
def load_pretrained_models():
    # load the pre-trained rekk-model which is used to judge the 2D/3D avatar (face)
    pref[REKK_MODEL] = RekkModel((cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3), 2)
    pref[REKK_MODEL].load_weights('../model_training/pretrained_model/rekk_model.h5')
    # load the pre-trained retinaface from insightface which is used to detect the faces from an image
    pref[RETINAFACE_MODEL] = insightface.model_zoo.get_model('retinaface_r50_v1')
    pref[RETINAFACE_MODEL].prepare(ctx_id=-1, nms=0.4)


# adjust the size of a certain opencv-window
def resize_cv_window(win_name, img, scaling_factor=None, reset_size=None):
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
