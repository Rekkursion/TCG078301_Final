import os

import numpy as np
from PIL import Image

from utils.configuration import configuration as cfg


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
