import os

import cv2
import numpy as np

from app.enums.colors import Colors
from app.enums.process_status import ProcessStatus
from app.environment import env_helpers as helper
from app.loaded_image import add_detected_face, add_processed_image, update_processed_image, get_original_image, \
    get_detected_faces, get_num_of_detected_faces
from app.ui.cv2_ui.callbacks import mouse_callback
from utils.configuration import configuration as cfg


# get the face through an original image and a detected face-box on it
def get_face(img, box):
    x1, y1, x2, y2, _ = box.astype(np.int)
    x1, y1 = abs(x1), abs(y1)
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


# detect the faces of an image by retinaface
def detect_faces(img):
    # if there's no image, return directly
    if img is None:
        return
    # get the retinaface model
    retinaface = helper.get_retinaface_model()
    # the result-list of all detected faces and their boxes
    ret = []
    # if the model is loaded successfully
    if retinaface is not None:
        threshold = cfg['RETINAFACE_THRESHOLD']
        scale = cfg['RETINAFACE_SCALE']
        faces, landmarks = retinaface.detect(img, threshold=threshold, scale=scale)
        if faces is not None:
            for k in range(faces.shape[0]):
                face, pt_1, pt_2 = get_face(img, faces[k])
                ret.append((face, pt_1, pt_2))
                # cv2.imshow('face ' + str(k), face)
    return ret


# judge if the passed faces are 2d or 3d avatars respectively
def judge_avatars(detected_faces):
    # the result-list
    ret = []
    # loaded the pretrained rekk-model
    rekk = helper.get_rekk_model()
    if rekk is not None:
        # iterate all the detected faces
        for (face, pt_1, pt_2) in detected_faces:
            # do the prediction on a single detected face
            pred = rekk.do_prediction(face)
            # add the prediction into the result-list and loaded-image-dict
            ret.append((face, pt_1, pt_2, pred))
    # return the list of results
    return ret


# draw the boxes of the detected-and-judged faces (avatars) on the originally-loaded image
def draw_boxes(win_name, img, judged_faces=(), orig_img=None):
    # store the original image and the processed image if it's the first time
    if orig_img is not None:
        add_processed_image(win_name, img, orig_img, get_file_ext(win_name))
    # copy an original image out to be modified
    orig_img = cv2.copyMakeBorder(get_original_image(win_name), 0, 0, 0, 0, cv2.BORDER_REPLICATE)
    # resize the copied original image into the shape of the passed image
    new_img = cv2.resize(orig_img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
    # add the detected face into the loaded-image-dictionary
    for (_, pt_1, pt_2, judged_label) in judged_faces:
        reversed_factor = orig_img.shape[0] / new_img.shape[0]
        add_detected_face(win_name, (int(pt_1[0] * reversed_factor), int(pt_1[1] * reversed_factor)),
                          (int(pt_2[0] * reversed_factor), int(pt_2[1] * reversed_factor)), judged_label)
    # calculate the scaling-factor
    scaling_factor = new_img.shape[0] / orig_img.shape[0]
    # iterate all detected-and-judged faces (avatars)
    for (pt_1, pt_2, judged_label) in get_detected_faces(win_name):
        clr = Colors.FACE_2D_BOX if judged_label == cfg['CLS_NAMES'][0] else Colors.FACE_3D_BOX
        # draw the rectangle on a single face
        cv2.rectangle(new_img, (int(pt_1[0] * scaling_factor), int(pt_1[1] * scaling_factor)),
                      (int(pt_2[0] * scaling_factor), int(pt_2[1] * scaling_factor)), clr, 2)
        # put the judged label on the corresponding face
        cv2.putText(new_img, judged_label, (int(pt_1[0] * scaling_factor), int((pt_1[1] - 4) * scaling_factor)),
                    cv2.FONT_HERSHEY_PLAIN, 1, clr, 2)
    # show the boxes-drawn image
    cv2.imshow(win_name, new_img)
    # update the processed image
    update_processed_image(win_name, new_img)


# do the process of judging the faces on an image are 2D or 3D respectively
def do_process(win_name, img, lock, widget, log_writer):
    if img is None:
        return
    # acquire the lock to avoid race-condition and release it after finishing the task (before the key-waiting)
    with lock:
        # noinspection PyBroadException
        try:
            # detect faces and face-boxes of the original image by retinaface
            widget.notify_status_change(ProcessStatus.PROCESSING)
            detected_faces = detect_faces(img)
            # judge the detected faces into 2d or 3d avatars
            judged_faces = judge_avatars(detected_faces)
            # draw the boxes of detected-and-judged faces w/ the corresponding colors
            draw_boxes(win_name, img, judged_faces, orig_img=cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_REPLICATE))
            widget.notify_status_change(ProcessStatus.DONE)
            log_writer('The process of the loaded image <u>{}</u> has been done: {} 2D & {} 3D faces detected.'
                       .format(win_name, *get_num_of_detected_faces(win_name)), Colors.LOG_PROCESS_DONE)
            # set the mouse callback to activate by-user events
            cv2.setMouseCallback(win_name, mouse_callback, (win_name, widget,))
        except BaseException:
            widget.notify_status_change(ProcessStatus.ERROR)
            log_writer('Error happened when the program processes the loaded image <u>{}</u>.'.format(win_name), Colors.LOG_ERROR)
    # wait for user's action to avoid sudden window-vanishing
    cv2.waitKey(0)


# get the extension of a file through its filename
def get_file_ext(filename):
    _, ext = os.path.splitext(filename)
    return ext


# replace the extension of a file w/ the designated one
def replace_file_ext(filename, replacer_ext):
    # the original extension which is about to be replaced
    replacee_ext = get_file_ext(filename)
    # if the original filename does NOT have any extension sticked to it, directly add the replacer to it
    if replacee_ext == '':
        return '{}.{}'.format(filename, replacer_ext)
    # else, replace the extension
    else:
        return '{}{}'.format(filename[:len(filename) - len(replacee_ext)], replacer_ext)


# to support utf-8 characters in the file path when loading the image through open-cv,
# since the original 'cv2.imread' does NOT support the path that has non-ascii characters in it
def imread_utf8_supported(file_path):
    im_stream = open(file_path, 'rb')
    im_bytes = bytearray(im_stream.read())
    return cv2.imdecode(np.asarray(im_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
