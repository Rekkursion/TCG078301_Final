from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
import sys
from app import pref_helpers as helper


# start the application
def start_app():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # load the pre-trained models (rekk-model & retinaface)
    helper.load_pretrained_models()
    # start the application
    start_app()
