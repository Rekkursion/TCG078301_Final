import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from random import randint
from utils.configuration import configuration as cfg
from app import pref_helpers as helper


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


# convert a numpy-array into a PIL-image
def nparray_to_image(arr, mode=None):
    return Image.fromarray(np.uint8(arr), mode)


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
    # if the model is loaded successfully
    if retinaface is not None:
        cv2.imshow(helper.get_image_file_path(), img)
        faces, landmarks = retinaface.detect(img, threshold=0.5, scale=1.0)
        if faces is not None:
            for k in range(faces.shape[0]):
                face, pt_1, pt_2 = get_face(img, faces[k])
                cv2.imshow('face ' + str(k), face)
