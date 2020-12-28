import cv2

from app.environment import env_helpers as helper
from app.loaded_image import get_processed_image, get_original_image
from utils.configuration import configuration as cfg


# the callback function for the mouse-events
# params: [0] = win_name, [1] = widget
def mouse_callback(event, x, y, flags, params):
    win_name = params[0]
    widget = params[1]
    # a mouse-wheeling event -> scale the image as well as the window
    if event == cv2.EVENT_MOUSEWHEEL:
        resize_image(win_name, flags, widget)
    # a mouse-down event (right button) -> start the face-framing
    elif event == cv2.EVENT_RBUTTONDOWN:
        helper.start_framing_face_by_user(x, y)
    # a mouse-up event (right button) -> finish the face-framing
    elif event == cv2.EVENT_RBUTTONUP:
        try:
            helper.finish_framing_face_by_user(win_name, x, y, widget)
        except cv2.error:
            pass
    # a mouse-moving event -> frame the face
    elif event == cv2.EVENT_MOUSEMOVE:
        helper.frame_face_by_user(win_name, x, y)


# resize the image which is currently focused
def resize_image(win_name, flags, widget):
    # get the scaling factor
    scaling_factor = cfg['SCALING_FACTOR_ON_CV_WIN']
    # if it's going to be decremented, let the factor be reversed
    if flags < 0:
        scaling_factor = 1.0 / scaling_factor
    # the wheeling event could only be invoked when the user is NOT framing the face
    if helper.is_framing_face_by_user():
        return
    # get the processed image by the window name
    cur_img = get_processed_image(win_name)
    # get the original image by the window name
    orig_img = get_original_image(win_name)
    if cur_img is None or orig_img is None:
        return
    # calculate the new size
    new_size = (int(cur_img.shape[1] * scaling_factor), int(cur_img.shape[0] * scaling_factor))
    # if the new size is smaller than the minimum size, the resizing CANNOT be done
    if new_size[0] < cfg['MIN_SIZE_OF_IMG'] or new_size[1] < cfg['MIN_SIZE_OF_IMG']:
        return
    # actually re-size the opencv-window
    img = cv2.resize(orig_img, new_size, interpolation=cv2.INTER_CUBIC)
    # draw the boxes on the resized original image
    helper.draw_boxes(win_name, img)
    # notify the corresponding widget that the size of the processed image has been changed
    widget.notify_size_change()
