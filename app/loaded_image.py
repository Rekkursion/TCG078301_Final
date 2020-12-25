import cv2

from utils.configuration import configuration as cfg

# the dictionary of all loaded images
# key, value: win_name, loaded-image-info
loaded_imgs = dict()


# the class for storing some information of a loaded image
class LoadedImageInfo:
    def __init__(self, processed_img, orig_img, ext):
        self.processed_img = processed_img
        self.orig_img = orig_img
        self.ext = ext
        # the list of detected faces (points & the predicted label)
        self.faces = []

    # add a new face w/ its points and its predicted label
    def add_face(self, pt_1, pt_2, pred_label):
        self.faces.append((pt_1, pt_2, pred_label))


# add a new processed image
def add_processed_image(win_name, new_img, orig_img, ext):
    info = LoadedImageInfo(new_img, orig_img, ext)
    loaded_imgs[win_name] = info


# add a new detected face
def add_detected_face(win_name, pt_1, pt_2, pred_label):
    loaded_imgs[win_name].add_face(pt_1, pt_2, pred_label)


# update the processed image
def update_processed_image(win_name, updated_img):
    loaded_imgs[win_name].processed_img = updated_img


# get the extension of the designated loaded image
def get_ext_of_loaded_image(win_name):
    if win_name in loaded_imgs:
        return loaded_imgs[win_name].ext
    else:
        return None


# get the processed image by its name
def get_processed_image(win_name):
    if win_name in loaded_imgs:
        return loaded_imgs[win_name].processed_img
    else:
        return None


# get the original image by its name
def get_original_image(win_name):
    if win_name in loaded_imgs:
        return cv2.copyMakeBorder(loaded_imgs[win_name].orig_img, 0, 0, 0, 0, cv2.BORDER_REPLICATE)
    else:
        return None


# get the current size of the processed image
def get_size_of_processed_image(win_name):
    img = get_processed_image(win_name)
    return img.shape[1], img.shape[0]


# get all detected faces
def get_detected_faces(win_name):
    return loaded_imgs[win_name].faces


# get the number of detected faces
def get_num_of_detected_faces(win_name):
    faces = get_detected_faces(win_name)
    return len(tuple(filter(lambda face: face[2] == cfg['CLS_NAMES'][0], faces))), len(tuple(filter(lambda face: face[2] == cfg['CLS_NAMES'][1], faces)))
