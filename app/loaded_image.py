# the dictionary of all loaded images
loaded_imgs = dict()


# update the processed image content of a certain image
def update_processed_image(name, new_img, orig_img=None):
    if orig_img is None:
        loaded_imgs[name][1] = new_img
    else:
        loaded_imgs[name] = [orig_img, new_img]


# get the processed image by its name
def get_processed_image(name):
    if name in loaded_imgs:
        return loaded_imgs[name][1]
    else:
        return None


# get the original image by its name
def get_original_image(name):
    if name in loaded_imgs:
        return loaded_imgs[name][0]
    else:
        return None
