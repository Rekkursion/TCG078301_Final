from PyQt5.QtWidgets import QApplication
import sys
from app.environment import env_helpers as helper
from app.preferences.pref_manager import PrefManager
from app.ui.pyqt5_ui.main_window.main_window import MainWindow


# start the application
def start_app():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # load the pre-trained models (rekk-model & retinaface)
    helper.load_pretrained_models()
    # initially load the preferences from the json file
    PrefManager.init_pref()
    # start the application
    start_app()
