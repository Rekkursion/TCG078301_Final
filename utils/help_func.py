import tensorflow as tf
import numpy as np
import os
import cv2
import threading
import matplotlib.pyplot as plt
from PIL import Image
from random import randint
from utils.configuration import configuration as cfg
from app.preferences import pref_helpers as helper
from app.ui.cv2_ui.callbacks import mouse_callback


# randomly get an index in a certain range starts from zero
def get_idx(max_idx):
    return randint(0, max_idx - 1)


# load images which are under a certain directory
def load_imgs_from_dir(dir_name):
    # the result-list
    ret = []
    # iterate all the files under the designated directory
    print('Loading images from the directory: \"{}\" ...'.format(dir_name))
    for filename in os.listdir(dir_name):
        # open an image
        img = Image.open(os.path.join(dir_name, filename))
        # resize it to the designated size
        img = img.resize(cfg['SIZE_OF_IMGS'], Image.ANTIALIAS)
        # append it to the result-list
        ret.append(np.asarray(img))
    # return the result-list as a numpy-array
    return np.asarray(ret)


# show some images by matplotlib
def show_imgs(cols, rows, img_list):
    # the total number of to-be-shown images
    n = cols * rows
    # the randomly-chosen indices of to-be-shown images
    indices = np.random.choice(img_list.shape[0], n, replace=False)
    # build up the figure
    fig = plt.figure(figsize=(cols * 2, rows * 2))
    # iteratively add the sub-plot to the figure
    for k in range(0, n):
        img = img_list[indices[k]]
        fig.add_subplot(rows, cols, k + 1)
        plt.imshow(img)
    # show the figure
    plt.show()


# split both classes of data into training & testing sets
def split_data(animes, reals, ratio):
    # shuffle both of lists
    np.random.shuffle(animes)
    np.random.shuffle(reals)
    # calc the total numbers of images of training sets
    a_train_num = int(animes.shape[0] * ratio)
    r_train_num = int(reals.shape[0] * ratio)
    # split anime-avatars into training & testing sets
    a_x_train = np.empty_like(animes[:a_train_num])
    a_x_train[:] = animes[:a_train_num]
    a_x_test = np.empty_like(animes[a_train_num:])
    a_x_test[:] = animes[a_train_num:]
    # split real-avatars into training & testing sets
    r_x_train = np.empty_like(reals[:r_train_num])
    r_x_train[:] = reals[:r_train_num]
    r_x_test = np.empty_like(reals[r_train_num:])
    r_x_test[:] = reals[r_train_num:]
    # combine the training-data list
    x_train = np.concatenate((a_x_train, r_x_train))
    # combine the testing-data list
    x_test = np.concatenate((a_x_test, r_x_test))
    # create the label-list ('anime' = 0, 'real' = 1)
    y_train = np.concatenate((
        np.full((a_x_train.shape[0]), 0),
        np.full((r_x_train.shape[0]), 1)
    ))
    y_test = np.concatenate((
        np.full((a_x_test.shape[0]), 0),
        np.full((r_x_test.shape[0]), 1)
    ))
    # shuffle the training data
    indices = np.arange(x_train.shape[0])
    np.random.shuffle(indices)
    x_train = x_train[indices]
    y_train = y_train[indices]
    # shuffle the testing data
    indices = np.arange(x_test.shape[0])
    np.random.shuffle(indices)
    x_test = x_test[indices]
    y_test = y_test[indices]
    # return all o them
    return x_train, y_train, x_test, y_test


# show the detail of a predicted testing-image
def show_detail_of_predicted(x_test_origin, y_test_origin, prediction, idx=-1):
    if idx < 0:
        idx = get_idx(x_test_origin.shape[0])
    print('   predicted:', cfg['CLS_NAMES'][prediction[idx]])
    print('ground truth:', cfg['CLS_NAMES'][y_test_origin[idx]])


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
    # loaded the pre-trained rekk-model
    rekk = helper.get_rekk_model()
    if rekk is not None:
        # iterate all the detected faces
        for (face, pt_1, pt_2) in detected_faces:
            # do the prediction on a single detected face
            pred = rekk.do_prediction(face)
            # add the prediction into the result-list
            ret.append((face, pt_1, pt_2, pred))
            # print(pred)
    else:
        # todo: exception handling
        print('wtf')
    # return the list of results
    return ret


# draw the boxes of the detected-and-judged faces (avatars) on the originally-loaded image
def draw_boxes(orig_img, judged_faces):
    # iterate all detected-and-judged faces (avatars)
    for (_, pt_1, pt_2, judged_label) in judged_faces:
        # draw the rectangle on a single face
        cv2.rectangle(orig_img, pt_1, pt_2, cfg['BOX_CLRS'][judged_label], 2)
        # put the judged label on the corresponding face
        cv2.putText(orig_img, judged_label, (pt_1[0], pt_1[1] - 4), cv2.FONT_HERSHEY_PLAIN, 1, cfg['BOX_CLRS'][judged_label], 2)
    # show the boxes-drawn image
    cv2.imshow(helper.get_image_file_path(), orig_img)
    # set the size of the designated opencv-window
    helper.adjust_cv_window_size(helper.get_image_file_path(), orig_img, reset_size=(orig_img.shape[1], orig_img.shape[0]))
    # set the mouse callback to activate by-user events
    cv2.setMouseCallback(helper.get_image_file_path(), mouse_callback, (helper.get_image_file_path(), orig_img,))


# do the process of judging the faces on an image are 2D or 3D respectively
def do_process(filename, lock):
    # acquire the lock to avoid race-condition and release it after finishing the task (before the key-waiting)
    with lock:
        # set the preference value of the currently-loaded image
        helper.set_image_file_path(filename)
        # detect faces and face-boxes of the original image by retinaface
        detected_faces = detect_faces(helper.get_current_image())
        # judge the detected faces into 2d or 3d avatars
        judged_faces = judge_avatars(detected_faces)
        # draw the boxes of detected-and-judged faces w/ the corresponding colors
        draw_boxes(helper.get_current_image(), judged_faces)
    # if the current thread is not the main thread, wait for user's action to avoid window-flashing
    if threading.current_thread() is not threading.main_thread():
        cv2.waitKey(0)


# initialize gpus
def init_gpus():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)
