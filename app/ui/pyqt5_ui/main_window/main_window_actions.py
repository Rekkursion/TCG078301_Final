from PIL import ImageGrab, Image
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import cv2
import os
from app.enums.strings import Strs
from app.loaded_image import get_ext_of_loaded_image, get_processed_image
from app.preferences.pref_manager import PrefManager
from app.ui.pyqt5_ui.url_input_dialog.url_input_dialog import URLInputDialog
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
            self.start_process(filename[:cfg['MAX_LEN_OF_WIN_NAME']], cv2.imread(filename, cv2.IMREAD_COLOR))
    return load_from_local_triggered


# the triggered-event of the action-load-from-url
def action_load_from_url_triggered(self):
    def load_from_url_triggered():
        # create a url-input-dialog to get the image-url
        dialog = URLInputDialog()
        # show and execute the created dialog
        dialog.show()
        dialog.exec()
        self.start_process(dialog.get_url()[:cfg['MAX_LEN_OF_WIN_NAME']], dialog.get_loaded_image())
    return load_from_url_triggered


# the triggered-event of the action-load-from-clipboard
def action_load_from_clipboard_triggered(self):
    # noinspection PyTypeChecker
    def load_from_clipboard_triggered():
        # grab data from the clipboard
        data = ImageGrab.grabclipboard()
        # if the grabbed data is an image
        if isinstance(data, Image.Image):
            self.start_process('From clipboard {}'.format(self.clipboard_counter), np.asarray(data.convert('RGB')))
            self.clipboard_counter += 1
        # if the grabbed data is a string, it could possibly be a filename, give it a try
        elif isinstance(data, str):
            self.start_process('From clipboard {}'.format(self.clipboard_counter), cv2.imread(data, cv2.IMREAD_COLOR))
            self.clipboard_counter += 1
        # if the grabbed data is a list
        elif isinstance(data, list):
            # iterate the list to try getting the image(s)
            for item in data:
                # if this item is an image
                if isinstance(item, Image.Image):
                    self.start_process('From clipboard {}'.format(self.clipboard_counter), np.asarray(item.convert('RGB')))
                    self.clipboard_counter += 1
                # if this item is a string, it could possibly be a filename, give it a try
                elif isinstance(item, str):
                    self.start_process('From clipboard {}'.format(self.clipboard_counter), cv2.imread(item, cv2.IMREAD_COLOR))
                    self.clipboard_counter += 1
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
    return save_selected_triggered


# the triggered-event for switching the language into chinese
def action_lang_chi_triggered(self):
    def lang_chi_triggered():
        PrefManager.set_pref('lang', 0)
        Strs.notify_all_registered()
        self.action_lang_chi.setChecked(True)
        self.action_lang_eng.setChecked(False)
    return lang_chi_triggered


# the triggered-event for switching the language into english
def action_lang_eng_triggered(self):
    def lang_eng_triggered():
        PrefManager.set_pref('lang', 1)
        Strs.notify_all_registered()
        self.action_lang_chi.setChecked(False)
        self.action_lang_eng.setChecked(True)
    return lang_eng_triggered
