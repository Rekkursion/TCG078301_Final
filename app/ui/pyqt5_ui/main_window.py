from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PIL import ImageGrab, Image
from threading import Thread
import numpy as np
import cv2
from app.ui.pyqt5_ui.url_input_dialog import URLInputDialog
from app.preferences.pref_helpers import get_process_lock
from utils.help_func import do_process
from utils.configuration import configuration as cfg
from app.ui.pyqt5_ui.loaded_images_list.loaded_images_list_widget import LoadedImagesListWidget


class MainWindow(QMainWindow):
    """
        action_load_from_local:     the action for loading the image from local
        action_load_from_url:       the action for loading the image from a certain url
        action_load_from_clipboard: the action for loading the image from the clipboard (only windows & macs supported)
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

    # initialize the events
    def init_events(self):
        # connect the triggered-event on the action-load-from-local
        self.action_load_from_local.triggered.connect(self.action_load_from_local_triggered)
        # connect the triggered-event on the action-load-from-url
        self.action_load_from_url.triggered.connect(self.action_load_from_url_triggered)
        # connect the triggered-event on the action-load-from-clipboard
        self.action_load_from_clipboard.triggered.connect(self.action_load_from_clipboard_triggered)

    # start the process of detection & judgement of a certain image
    def start_process(self, win_name, img):
        self.lis_imgs.push_back(win_name, img)
        Thread(target=do_process, name=win_name, daemon=True, args=(win_name, img, get_process_lock(), self.lis_imgs,)).start()

    # the triggered-event of the action-load-from-local
    def action_load_from_local_triggered(self):
        # open the file-dialog and get the designated image file
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='選擇圖片 Select an image',
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
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
