from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import os
import cv2
from app import pref_helpers as helper
from utils.help_func import get_face, detect_faces


class MainWindow(QMainWindow):
    """
        action_load_image:      the action for loading the image
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
            caption='選擇圖片 Choose an image',
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
        # if the selected file doesn't exist or it is not a proper file
        if not os.path.exists(filename) or not os.path.isfile(filename):
            pass
        # else, load the selected image on the main-label
        else:
            # set the preference value of currently-loaded image
            helper.set_image_file_path(filename)
            detect_faces(helper.get_current_image())
            # helper.get_model().do_prediction()
