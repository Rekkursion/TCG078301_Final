from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import os
from app import pref_helpers as helper


class MainWindow(QMainWindow):
    """
        lbl_show_image:         the label for showing the loaded image
        action_load_image:      the action for loading the image
        action_start_detect:    the action for starting the detection after loading a certain image
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
        # connect the triggered-event on the action-start-detect
        self.action_start_detect.triggered.connect(self.action_start_detect_triggered)

    # load a certain image to the main window
    def load_image(self, file_path):
        # open the image by a certain file path
        img = QPixmap(file_path)
        # set the image on the main-label
        self.lbl_show_image.setPixmap(img)
        # resize both the label and the window
        self.lbl_show_image.resize(img.width(), img.height())
        self.resize(img.width(), img.height())
        # set the preference value of currently-loaded image
        helper.set_image_file_path(file_path)

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
            self.load_image(filename)

    # the triggered-event of the action-start-detect
    @staticmethod
    def action_start_detect_triggered():
        helper.get_model().do_prediction()
