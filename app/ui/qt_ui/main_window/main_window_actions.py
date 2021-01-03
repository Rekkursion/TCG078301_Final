import os

import cv2
import numpy as np
from PIL import ImageGrab, Image
from PyQt5.QtWidgets import QFileDialog

from app.enums.colors import Colors
from app.enums.dialog_status import DialogStatus
from app.enums.strings import Strs
from app.environment.env_helpers import load_pretrained_models
from app.loaded_image import get_ext_of_loaded_image, get_processed_image, get_size_of_processed_image
from app.preferences.pref_manager import PrefManager
from app.ui.qt_ui.url_input_dialog.url_input_dialog import URLInputDialog
from utils.configuration import configuration as cfg


# the triggered-event of the action-load-from-local
def action_load_from_local_triggered(self):
    def load_from_local_triggered():
        # open the file-dialog and get the image file(s)
        filename_list, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption=Strs.get_by_enum(Strs.Open_File_Dialog_Caption),
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
        # iterate the filenames to do the processes
        for filename in filename_list:
            name = filename[:cfg['MAX_LEN_OF_WIN_NAME']]
            if self.start_process(name, cv2.imread(filename, cv2.IMREAD_COLOR)):
                self.write_log('The image <u>{}</u> has been loaded <i>from local</i>.'.format(name), Colors.LOG_LOAD_IMAGE)
    return load_from_local_triggered


# the triggered-event of the action-load-from-url
def action_load_from_url_triggered(self):
    def load_from_url_triggered():
        # create a url-input-dialog to get the image-url
        dialog = URLInputDialog()
        # show and execute the created dialog
        dialog.show()
        dialog.exec()
        if dialog.get_status() == DialogStatus.ACCEPTED:
            name = dialog.get_url()[:cfg['MAX_LEN_OF_WIN_NAME']]
            if self.start_process(name, dialog.get_loaded_image()):
                self.write_log('The image <u>{}</u> has been loaded <i>from URL</i>.'.format(name), Colors.LOG_LOAD_IMAGE)
        elif dialog.get_status() == DialogStatus.ERROR:
            self.write_log(dialog.get_err_msg(), Colors.LOG_ERROR)
    return load_from_url_triggered


# the triggered-event of the action-load-from-clipboard
def action_load_from_clipboard_triggered(self):
    # start the process
    def start(win_name, img):
        if self.start_process(win_name, img):
            self.clipboard_counter += 1
            self.write_log('The image <u>{}</u> has been loaded <i>from the clipboard</i>.'.format(win_name), Colors.LOG_LOAD_IMAGE)

    # noinspection PyTypeChecker
    def load_from_clipboard_triggered():
        has_loaded = False
        # noinspection PyBroadException
        try:
            # grab data from the clipboard
            data = ImageGrab.grabclipboard()
            # if the grabbed data is an image
            if isinstance(data, Image.Image):
                # convert the pil-img into a cv2-img
                img = np.array(data.convert('RGB'))[:, :, ::-1]
                has_loaded = True
                start('From clipboard {}'.format(self.clipboard_counter), img)
            # if the grabbed data is a string, it could possibly be a filename, give it a try
            elif isinstance(data, str):
                has_loaded = True
                start('From clipboard {}'.format(self.clipboard_counter), cv2.imread(data, cv2.IMREAD_COLOR))
            # if the grabbed data is a list
            elif isinstance(data, list):
                # iterate the list to try getting the image(s)
                for item in data:
                    # if this item is an image
                    if isinstance(item, Image.Image):
                        # convert the pil-img into a cv2-img
                        img = np.array(item.convert('RGB'))[:, :, ::-1]
                        has_loaded = True
                        start('From clipboard {}'.format(self.clipboard_counter), img)
                    # if this item is a string, it could possibly be a filename, give it a try
                    elif isinstance(item, str):
                        has_loaded = True
                        start('From clipboard {}'.format(self.clipboard_counter), cv2.imread(item, cv2.IMREAD_COLOR))
        except BaseException:
            self.write_log('Failed to load the image from clipboard. Please make sure the copied object is an image.', Colors.LOG_ERROR)
        # if there's nothing loaded
        if not has_loaded:
            self.write_log('No images detected in the clipboard.', Colors.LOG_WARNING)
    return load_from_clipboard_triggered


# the triggered-event for saving all processed images to a directory
def action_save_all_triggered(self):
    def save_all_triggered():
        # open the dialog to let the user select an existing directory
        dir_name = QFileDialog.getExistingDirectory(parent=self, caption=Strs.get_by_enum(Strs.Open_Directory_Dialog_Caption))
        # iterate all loaded images
        if dir_name != '':
            cnt = 0
            for i in range(0, self.lis_imgs.count()):
                # get its window-name of a single image as the output filename
                win_name = self.lis_imgs.itemWidget(self.lis_imgs.item(i)).win_name
                # determine the extension of the output filename
                ext = get_ext_of_loaded_image(win_name)
                if ext == '':
                    ext = '.jpg'
                # write it out
                img = get_processed_image(win_name)
                if img is not None:
                    cnt += 1
                    cv2.imwrite(os.path.join(dir_name, 'processed_{}{}'.format(cnt, ext)), img)
            if cnt > 0:
                self.write_log('All processed images have been saved to the designated location.', Colors.LOG_IMAGE_SAVED)
            else:
                self.write_log('No any images which have been processed.', Colors.LOG_WARNING)
    return save_all_triggered


# the triggered-event for saving selected images to a directory
def action_save_selected_triggered(self):
    def save_selected_triggered():
        # open the dialog to let the user select an existing directory
        dir_name = QFileDialog.getExistingDirectory(parent=self, caption=Strs.get_by_enum(Strs.Open_Directory_Dialog_Caption))
        # iterate all loaded images
        if dir_name != '':
            cnt = 0
            for item in self.lis_imgs.selectedItems():
                # get its window-name of a single image as the output filename
                win_name = self.lis_imgs.itemWidget(item).win_name
                # determine the extension of the output filename
                ext = get_ext_of_loaded_image(win_name)
                if ext == '':
                    ext = '.jpg'
                # write it out
                img = get_processed_image(win_name)
                if img is not None:
                    cnt += 1
                    cv2.imwrite(os.path.join(dir_name, 'processed_{}{}'.format(cnt, ext)), img)
            if cnt > 0:
                self.write_log('All selected processed images have been saved to the designated location.', Colors.LOG_IMAGE_SAVED)
            else:
                self.write_log('No any images which have been processed in the selected set.', Colors.LOG_WARNING)
    return save_selected_triggered


# the triggered-event for switching the language into chinese
def action_lang_chi_triggered(self):
    def lang_chi_triggered():
        __change_lang_to(self, 0)
    return lang_chi_triggered


# the triggered-event for switching the language into english
def action_lang_eng_triggered(self):
    def lang_eng_triggered():
        __change_lang_to(self, 1)
    return lang_eng_triggered


# change the language to the designated one by its index (0 = chi, 1 = eng)
def __change_lang_to(self, lang_idx):
    # update at the global preferences file
    PrefManager.set_pref('lang', lang_idx)
    # notify all registered strings to be updated
    Strs.notify_all_registered()
    # change the checked item on the corresponding items
    if lang_idx == 0:
        self.action_lang_chi.setChecked(True)
        self.action_lang_eng.setChecked(False)
    else:
        self.action_lang_chi.setChecked(False)
        self.action_lang_eng.setChecked(True)
    # re-put the size of processed image on the button of saving on each item in the image-list
    for widget in self.lis_imgs.get_all_widgets():
        # get the size of this processed image
        img_size = get_size_of_processed_image(widget.win_name)
        # make sure the size exists, i.e., the process of this image has been done
        if img_size is not None:
            # re-put the size of this processed image on the corresponding widget
            widget.btn_save_processed.setText('{} [{} x {}]'.format(
                Strs.get_by_enum(Strs.Loaded_Img_Widget_Button_Save_Processed),
                *img_size
            ))


# the triggered-event for setting the pretrained rekk-model
def action_pretrained_rekk_model_triggered(self):
    def pretrained_rekk_model_triggered():
        # open the file-dialog and get the pretrained rekk-model
        rekk_model_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption=Strs.get_by_enum(Strs.Open_RekkModel_Dialog_Caption),
            filter='RekkModel (*.h5)'
        )
        if rekk_model_path != '':
            # set the path as a preference
            PrefManager.set_pref('rekkmodel', rekk_model_path)
            # then, re-load the weights of the pretrained rekk-model
            load_pretrained_models()
            self.write_log(f'Successfully set the path of the pretrained RekkModel to: <u>{rekk_model_path}</u>', Colors.LOG_REKKMODEL_SET)
        return rekk_model_path
    return pretrained_rekk_model_triggered
