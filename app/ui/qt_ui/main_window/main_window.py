from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from app.enums.strings import Strs
from app.environment.env_helpers import get_process_lock
from app.preferences.pref_manager import PrefManager
from app.ui.qt_ui.loaded_images_list.loaded_images_list_widget import LoadedImagesListWidget
from app.ui.qt_ui.log_area.log_area import LogArea
from app.ui.qt_ui.main_window.main_window_actions import *
from utils.configuration import configuration as cfg
from utils.help_func import do_process


class MainWindow(QMainWindow):
    """
        action_load_from_local:         the action for loading the image from local
        action_load_from_url:           the action for loading the image from a certain url
        action_load_from_clipboard:     the action for loading the image from the clipboard (only windows & macs supported)
        action_save_all:                the action for saving all the processed images to a directory
        action_save_selected:           the action for saving the selected images to a directory
        action_lang_chi:                the action for switching the language into chinese
        action_lang_eng:                the action for switching the language into english
        action_pretrained_rekk_model:   the action for setting the pretrained rekk-model
        lis_imgs:                       the list-widget for showing all loaded/processed images
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # load the UI
        uic.loadUi('./app/ui/qt_ui/main_window/main_window.ui', self)
        # the list-widget for showing all loaded images
        self.lis_imgs = LoadedImagesListWidget(self.write_log)
        self.main_layout.addWidget(self.lis_imgs)
        # the text-browser for showing logs
        self.log_area = LogArea()
        self.main_layout.addWidget(self.log_area)
        # initialize the events
        self.init_events()
        # the counter for counting the number of opened images through the clipboard
        self.clipboard_counter = 0
        # initially set the currently-used language
        if PrefManager.get_pref('lang') == 0:
            self.action_lang_chi.setChecked(True)
        else:
            self.action_lang_eng.setChecked(True)
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
            (self.menu_lang, Strs.Menubar_Pref_Lang),
            (self.action_pretrained_rekk_model, Strs.Menubar_Pref_Pretrained_Rekk_Model)
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
        self.action_pretrained_rekk_model.triggered.connect(action_pretrained_rekk_model_triggered(self))

    # start the process of detection & judgement of a certain image
    def start_process(self, win_name, img):
        # if the size of the loaded image is too small (either of the width & height must be bigger than 30)
        if img.shape[0] < cfg['MIN_SIZE_OF_IMG'] or img.shape[1] < cfg['MIN_SIZE_OF_IMG']:
            self.write_log('Failed at loading. \
                           The size of the image <u>{}</u> is too small ({} x {}), \
                           both of the width & the height must be bigger than {} pixels.'.format(
                win_name,
                img.shape[1],
                img.shape[0],
                cfg['MIN_SIZE_OF_IMG']
            ), Colors.LOG_ERROR)
            return False
        # check if the path of the pretrained rekk-model is set or not
        rekk_model_path = PrefManager.get_pref('rekkmodel')
        # if no, trigger the dialog to let the user set the path
        if rekk_model_path is None or rekk_model_path == '':
            # open the file-dialog
            rekk_model_path = action_pretrained_rekk_model_triggered(self)()
            # if the user still no select the pretrained rekk-model, return directly
            if rekk_model_path is None or rekk_model_path == '':
                self.write_log('A pretrained <b>RekkModel</b> is a must for judging faces. \
                               Please set the path of the pretrained <b>RekkModel</b>.', Colors.LOG_ERROR)
                return False
        win_name = self.lis_imgs.deduplicate_win_name(win_name)
        widget = self.lis_imgs.push_back(win_name, img)
        Thread(target=do_process, name=win_name, daemon=True,
               args=(win_name, img, get_process_lock(), widget, self.write_log)).start()
        return True

    # write a single log and the text-color at the log-area (text-browser)
    def write_log(self, text, color):
        log = '<span style="color: rgb{};"> &gt; {}</span>'.format(str(color), '<strong>{}</strong>'.format(text))
        self.log_area.append(log)
