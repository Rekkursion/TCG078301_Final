from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PIL import ImageGrab
from threading import Thread
import cv2
from app.preferences.pref_helpers import get_process_lock
from utils.help_func import do_process


class MainWindow(QMainWindow):
    """
        action_load_from_local:     the action for loading the image from local
        action_load_from_clipboard: the action for loading the image from the windows clipboard
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # set the title of the main window
        self.setWindowTitle('TCG078301_Final - B10615031')
        # load the UI
        uic.loadUi('./ui/pyqt5_ui/main_window.ui', self)
        # initialize the events
        self.init_events()

    # initialize the events
    def init_events(self):
        # connect the triggered-event on the action-load-from-local
        self.action_load_from_local.triggered.connect(self.action_load_from_local_triggered)
        # connect the triggered-event on the action-load-from-clipboard
        self.action_load_from_clipboard.triggered.connect(self.action_load_from_clipboard_triggered)

    # start the process of detection & judgement of a certain image
    @staticmethod
    def start_process(win_name, img):
        Thread(target=do_process, daemon=True, args=(win_name, img, get_process_lock(),)).start()

    # the triggered-event of the action-load-from-local
    def action_load_from_local_triggered(self):
        # open the file-dialog and get the designated image file
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='選擇圖片 Select an image',
            filter='Image Files (*.jpg *.jpeg *.png *bmp)'
        )
        MainWindow.start_process(filename, cv2.imread(filename, cv2.IMREAD_COLOR))

    # the triggered-event of the action-load-from-clipboard
    def action_load_from_clipboard_triggered(self):
        # MainWindow.start_process('')
        pass
