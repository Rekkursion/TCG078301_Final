from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTextBrowser
from PyQt5.QtGui import QFont
from threading import Thread
from app.environment.env_helpers import get_process_lock
from utils.help_func import do_process
from app.ui.pyqt5_ui.loaded_images_list.loaded_images_list_widget import LoadedImagesListWidget
from app.ui.pyqt5_ui.main_window.main_window_actions import *
from app.enums.strings import Strs


class MainWindow(QMainWindow):
    """
        action_load_from_local:     the action for loading the image from local
        action_load_from_url:       the action for loading the image from a certain url
        action_load_from_clipboard: the action for loading the image from the clipboard (only windows & macs supported)
        action_save_all:            the action for saving all the processed images to a directory
        action_save_selected:       the action for saving the selected images to a directory
        action_lang_chi:            the action for switching the language into chinese
        action_lang_eng:            the action for switching the language into english
        lis_imgs:                   the list-widget for showing all loaded/processed images
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # set the title of the main window
        self.setWindowTitle('TCG078301_Final - B10615031')
        # load the UI
        uic.loadUi('./ui/pyqt5_ui/main_window/main_window.ui', self)
        # the list-widget for showing all loaded images
        self.lis_imgs = LoadedImagesListWidget()
        self.main_layout.addWidget(self.lis_imgs)
        # the text-browser for showing logs
        self.log_area = QTextBrowser()
        self.log_area.setFont(QFont('Consolas', 9))
        self.log_area.setFixedHeight(160)
        self.main_layout.addWidget(self.log_area)
        # initialize the events
        self.init_events()
        # the counter for counting the number of opened images through the clipboard
        self.clipboard_counter = 0
        self.lis_imgs.setSelectionMode(QAbstractItemView.ExtendedSelection)
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
            (self.action_save_selected, Strs.Menubar_File_Save_Selected),
            (self.menu_preferences, Strs.Menubar_Pref),
            (self.menu_lang, Strs.Menubar_Pref_Lang)
        )

    # initialize the events
    def init_events(self):
        self.action_load_from_local.triggered.connect(action_load_from_local_triggered(self))
        self.action_load_from_url.triggered.connect(action_load_from_url_triggered(self))
        self.action_load_from_clipboard.triggered.connect(action_load_from_clipboard_triggered(self))
        self.action_save_all.triggered.connect(action_save_all_triggered(self))
        self.action_save_selected.triggered.connect(action_save_selected_triggered(self))
        self.action_lang_chi.triggered.connect(action_lang_chi_triggered(self))
        self.action_lang_eng.triggered.connect(action_lang_eng_triggered(self))

    # start the process of detection & judgement of a certain image
    def start_process(self, win_name, img):
        win_name = self.lis_imgs.deduplicate_win_name(win_name)
        widget = self.lis_imgs.push_back(win_name, img)
        Thread(target=do_process, name=win_name, daemon=True,
               args=(win_name, img, get_process_lock(), widget, self.write_log)).start()

    # write a single log and the text-color at the log-area (text-browser)
    def write_log(self, text, color, is_bold=False):
        log = '<span style="color: rgb{};">{}</span>'.format(str(color), '<strong>{}</strong>'.format(text) if is_bold else text)
        self.log_area.append(log)
