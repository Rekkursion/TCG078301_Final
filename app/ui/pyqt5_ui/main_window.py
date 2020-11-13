from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAbstractItemView
from PIL import ImageGrab, Image
from threading import Thread
import numpy as np
import os
import cv2
from app.loaded_image import get_processed_image, get_ext_of_loaded_image
from app.ui.pyqt5_ui.url_input_dialog import URLInputDialog
from app.environment.env_helpers import get_process_lock
from utils.help_func import do_process
from utils.configuration import configuration as cfg
from app.ui.pyqt5_ui.loaded_images_list.loaded_images_list_widget import LoadedImagesListWidget
from app.enums.strings import Strs


class MainWindow(QMainWindow):
    """
        action_load_from_local:     the action for loading the image from local
        action_load_from_url:       the action for loading the image from a certain url
        action_load_from_clipboard: the action for loading the image from the clipboard (only windows & macs supported)
        action_save_all:            the action for saving all the processed images to a directory
        action_save_selected:       the action for saving the selected images to a directory
        lis_imgs:                   the list-widget for showing all loaded/processed images
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # set the title of the main window
        self.setWindowTitle('TCG078301_Final - B10615031')
        # load the UI
        uic.loadUi('./ui/pyqt5_ui/main_window.ui', self)
        # the list-widget for showing all loaded images
        self.lis_imgs = LoadedImagesListWidget()
        self.setCentralWidget(self.lis_imgs)
        # initialize the events
        self.init_events()
        # the counter for counting the number of opened images through the clipboard
        self.clipboard_counter = 0
        self.lis_imgs.setSelectionMode(QAbstractItemView.MultiSelection)
        # register all text-related nodes to the str-enum class
        Strs.register_all(
            (self, Strs.Main_Window_Title),
            (self.menu_File, Strs.Menubar_File),
            (self.menu_Load, Strs.Menubar_File_Load),
            (self.action_load_from_local, Strs.Menubar_File_Load_From_Local),
            (self.action_load_from_url, Strs.Menubar_File_Load_From_URL),
            (self.action_load_from_clipboard, Strs.Menubar_File_Load_From_Clipboard),
            (self.menu_Save, Strs.Menubar_File_Save),
            (self.action_save_all, Strs.Menubar_File_Save_All),
            (self.action_save_selected, Strs.Menubar_File_Save_Selected)
        )

    # initialize the events
    def init_events(self):
        self.action_load_from_local.triggered.connect(self.action_load_from_local_triggered)
        self.action_load_from_url.triggered.connect(self.action_load_from_url_triggered)
        self.action_load_from_clipboard.triggered.connect(self.action_load_from_clipboard_triggered)
        self.action_save_all.triggered.connect(self.action_save_all_triggered)
        self.action_save_selected.triggered.connect(self.action_save_selected_triggered)

    # start the process of detection & judgement of a certain image
    def start_process(self, win_name, img):
        win_name = self.lis_imgs.deduplicate_win_name(win_name)
        widget = self.lis_imgs.push_back(win_name, img)
        Thread(target=do_process, name=win_name, daemon=True, args=(win_name, img, get_process_lock(), widget,)).start()

    # the triggered-event of the action-load-from-local
    def action_load_from_local_triggered(self):
        # open the file-dialog and get the image file(s)
        filename_list, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption=Strs.get_by_enum(Strs.Open_File_Dialog_Caption),
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
        # iterate the filenames to do the processes
        for filename in filename_list:
            self.start_process(filename[:cfg['MAX_LEN_OF_WIN_NAME']], cv2.imread(filename, cv2.IMREAD_COLOR))

    # the triggered-event of the action-load-from-url
    def action_load_from_url_triggered(self):
        # create a url-input-dialog to get the image-url
        dialog = URLInputDialog()
        # show and execute the created dialog
        dialog.show()
        dialog.exec()
        self.start_process(dialog.get_url()[:cfg['MAX_LEN_OF_WIN_NAME']], dialog.get_loaded_image())

    # the triggered-event of the action-load-from-clipboard
    # noinspection PyTypeChecker
    def action_load_from_clipboard_triggered(self):
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

    # the triggered-event for saving all processed images to a directory
    def action_save_all_triggered(self):
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

    # the triggered-event for saving selected images to a directory
    def action_save_selected_triggered(self):
        # print('selected:', *)
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
