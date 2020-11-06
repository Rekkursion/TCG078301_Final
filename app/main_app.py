from tensorflow import keras
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from model_training.model import RekkModel
from utils.configuration import configuration as cfg
from app.pref import *
import sys


# load the pretrained model
def load_pretrained_model():
    pref[MODEL] = RekkModel((cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3), 2)
    pref[MODEL].load_weights('../model_training/pretrained_model/rekk_model.h5')


if __name__ == '__main__':
    # load the pretrained model
    load_pretrained_model()
    # start the application
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
