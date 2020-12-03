import pickle


# save a certain image using pickle
def save_img_w_pickle(file_path, img):
    with open(file_path, 'wb') as f:
        pickle.dump(img, f)


# load a certain image using pickle
def load_img_w_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


# load all images from a certain directory
def load_imgs_under_dir_w_pickle(dir_path):
    # todo: load all images from a certain directory
    pass
