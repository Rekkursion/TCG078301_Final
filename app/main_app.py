import sys

from PyQt5.QtWidgets import QApplication

from app.environment import env_helpers as helper
from app.preferences.pref_manager import PrefManager
from app.ui.qt_ui.main_window.main_window import MainWindow


# start the application
def start_app():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # initially load the preferences from the json file
    PrefManager.init_pref()
    # load the pretrained models (rekk-model & retinaface)
    helper.load_pretrained_models()
    # start the application
    start_app()
