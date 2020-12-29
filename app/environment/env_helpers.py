import cv2
import insightface
import numpy as np

from app.enums.colors import Colors
from app.environment.env import *
from app.loaded_image import get_processed_image
from app.preferences.pref_manager import PrefManager
from model_training.model import RekkModel
from utils.configuration import configuration as cfg
from utils.help_func import judge_avatars, draw_boxes


# get the pretrained rekk-model
def get_rekk_model():
    return env_dict[REKK_MODEL]


# get the pretrained retinaface model from insightface
def get_retinaface_model():
    return env_dict[RETINAFACE_MODEL]


# get the lock for processing of detection (and judgement)
def get_process_lock():
    return env_dict[PROCESS_LOCK]


# start the by-user face-framing
def start_framing_face_by_user(x, y):
    env_dict[FRAMING_FACE_BY_USER] = True
    env_dict[FRAMING_PT_1] = (x, y)


# finish the by-user face-framing
def finish_framing_face_by_user(win_name, x, y, widget):
    # make sure the order of two points is from small to big
    def make_sure_order_of_points(pt_1, pt_2):
        if pt_1[0] < pt_2[0]:
            if pt_1[1] < pt_2[1]:
                return pt_1[0], pt_1[1], pt_2[0], pt_2[1]
            else:
                return pt_1[0], pt_2[1], pt_2[0], pt_1[1]
        else:
            if pt_1[1] < pt_2[1]:
                return pt_2[0], pt_1[1], pt_1[0], pt_2[1]
            else:
                return pt_2[0], pt_2[1], pt_1[0], pt_1[1]

    img = get_processed_image(win_name)
    if img is None:
        return
    # if the new point & the original point are the different points
    if env_dict[FRAMING_PT_1][0] != x or env_dict[FRAMING_PT_1][1] != y:
        # resize the passed image into the possibly-adjusted (by wheeling) size
        img = cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
        # make sure the order of both points
        x1, y1, x2, y2 = make_sure_order_of_points((x, y), env_dict[FRAMING_PT_1])
        # frame out the user-framing face
        face = img[y1:y2, x1:x2]
        # judge it
        judged = judge_avatars([(face, (x1, y1), (x2, y2))])
        # draw it out
        draw_boxes(win_name, img, judged)
        # notify the number of detected faces has been updated
        widget.notify_new_detected()
    # dispel the status of framing face
    env_dict[FRAMING_FACE_BY_USER] = False
    env_dict[FRAMING_PT_1] = None
    # zero-fy the sampling counter
    env_dict[SAMPLING_COUNTER_OF_FRAMING] = 0


# frame the face by user
def frame_face_by_user(win_name, x, y):
    img = get_processed_image(win_name)
    if img is None:
        return
    # do the framing (draw the rectangle) only if the right button is down
    if env_dict[FRAMING_FACE_BY_USER]:
        # to avoid low efficiency, sample a certain frames to do the framing (draw the rectangle), e.g., draw it per 5 times when the mouse-move event is invoked
        env_dict[SAMPLING_COUNTER_OF_FRAMING] += 1
        if env_dict[SAMPLING_COUNTER_OF_FRAMING] == cfg['SAMPLING_RATE_OF_FRAMING_ON_CV_WIN']:
            # resize the passed image into the possibly-adjusted (by wheeling) size
            new_img = cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
            # copy a new image
            copied = cv2.copyMakeBorder(new_img, 0, 0, 0, 0, cv2.BORDER_REPLICATE)
            # draw the user-framing rectangle (semi-transparent filled)
            filled_rect = np.zeros(new_img.shape, np.uint8)
            cv2.rectangle(filled_rect, (x, y), env_dict[FRAMING_PT_1], Colors.USER_FRAMING_BOX, -1)
            copied = cv2.addWeighted(copied, 0.5, filled_rect, 0.5, 1)
            # draw the user-framing rectangle (border)
            cv2.rectangle(copied, (x, y), env_dict[FRAMING_PT_1], Colors.USER_FRAMING_BOX, 2)
            # show the boxes-drawn image
            cv2.imshow(win_name, copied)
            # re-zero the sampling counter
            env_dict[SAMPLING_COUNTER_OF_FRAMING] = 0


# check if the user is currently framing the face
def is_framing_face_by_user():
    return env_dict[FRAMING_FACE_BY_USER]


# load the pretrained models of both rekk-model and retinaface
# noinspection PyBroadException
def load_pretrained_models():
    # load the pretrained rekk-model which is used to judge the 2D/3D avatar (face)
    env_dict[REKK_MODEL] = RekkModel((cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3), 2)
    # try to load the pre-set (if any) path of the pretrained rekk-model
    try:
        env_dict[REKK_MODEL].load_weights(PrefManager.get_pref('rekkmodel'))
    except BaseException:
        pass
    # load the pretrained retinaface from insightface which is used to detect the faces from an image
    env_dict[RETINAFACE_MODEL] = insightface.model_zoo.get_model('retinaface_r50_v1')
    env_dict[RETINAFACE_MODEL].prepare(ctx_id=-1, nms=0.4)
