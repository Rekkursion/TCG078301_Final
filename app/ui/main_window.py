from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from threading import Thread
import os
from app.preferences.pref_helpers import get_process_lock
from app.supported_file_types import SupportedFileType
from utils.help_func import do_process


class MainWindow(QMainWindow):
    """
        action_load_image: the action for loading the image
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # set the title of the main window
        self.setWindowTitle('TCG078301_Final - B10615031')
        # load the UI
        uic.loadUi('./ui/main_window.ui', self)
        # initialize the events
        self.init_events()

    # initialize the events
    def init_events(self):
        # connect the triggered-event on the action-load-image
        self.action_load_image.triggered.connect(self.action_load_image_triggered)

    # the triggered-event of the action-load-image
    def action_load_image_triggered(self):
        # open the file-dialog and get the designated image file
        filename, f_type = QFileDialog.getOpenFileName(
            parent=self,
            # caption='選擇圖片或影片 Select an image or a video',
            caption='選擇圖片 Select an image',
            # filter='Both (*.jpg *.jpeg *.png *bmp *.mp4 *.avi);;Image Files (*.jpg *.jpeg *.png *bmp);;Video Files (*.mp4 *.avi)'
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
        # if the selected file doesn't exist or it is not a proper file
        if not os.path.exists(filename) or not os.path.isfile(filename):
            pass
        # else, load the selected image on the main-label and start doing the process
        else:
            # check if file type (image or video)
            file_type = SupportedFileType.is_supported(filename)
            Thread(target=do_process, daemon=True, args=(filename, file_type, get_process_lock(),)).start()
