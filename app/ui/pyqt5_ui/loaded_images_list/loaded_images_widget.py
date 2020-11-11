from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from app.enums.process_status import ProcessStatus
from app.enums.strings import Strs


# noinspection PyUnresolvedReferences
class LoadedImagesWidget(QWidget):
    """
        lbl_order
        lbl_win_name
        lbl_size
        lbl_status_title
        lbl_status
        btn_show_img
        btn_save_processed
    """
    def __init__(self, win_name, img, order, parent=None):
        super(LoadedImagesWidget, self).__init__(parent)
        # the window name
        self.win_name = win_name
        # some nodes of a single widget
        self.vbox_all = QVBoxLayout()
        # nodes of the first row
        self.hbox_fir = QHBoxLayout()
        self.lbl_order = QLabel('{} |'.format(order))
        self.lbl_win_name = QLabel(self.win_name)
        self.lbl_size = QLabel('[{} x {}]'.format(img.shape[1], img.shape[0]))
        self.hbox_fir.addWidget(self.lbl_order, 0)
        self.hbox_fir.addWidget(self.lbl_win_name, 1)
        self.hbox_fir.addWidget(self.lbl_size, 0)
        # nodes of the second row
        self.hbox_sec = QHBoxLayout()
        self.lbl_status_title = QLabel()
        self.lbl_status = QLabel()
        self.btn_show_img = QPushButton(QIcon(QPixmap('./res/img_search.png')), '')
        self.btn_show_img.setStyleSheet("""
            QPushButton {background-color: transparent;}
            QPushButton:pressed {background-color: rgb(226, 230, 234);}
            QPushButton:hover:!pressed {background-color: rgb(226, 230, 234);}
        """)
        self.btn_save_processed = QPushButton()
        self.hbox_sec.addWidget(self.lbl_status_title, 0)
        self.hbox_sec.addWidget(self.lbl_status, 0)
        self.hbox_sec.addWidget(self.btn_show_img, 0)
        self.hbox_sec.addWidget(self.btn_save_processed, 1)
        # push both the first & the second rows into the all-hbox
        self.vbox_all.addLayout(self.hbox_fir, 0)
        self.vbox_all.addLayout(self.hbox_sec, 0)
        self.setLayout(self.vbox_all)
        # initialize events
        self.init_events()
        # register all text-related nodes to the str-enum class
        Strs.register_all(
            (self.lbl_status_title, Strs.Loaded_Img_Widget_Status_Title),
            (self.lbl_status, Strs.Status_Loading),
            (self.btn_save_processed, Strs.Loaded_Img_Widget_Button_Save_Processed)
        )
        # initially change the text-color of the lbl-status
        self.lbl_status.setStyleSheet('color: rgb{};'.format(ProcessStatus.LOADING.get_text_color()[::-1]))

    # initialize events
    def init_events(self):
        pass
        # todo: save processed image
        # self.btn_save.clicked.connect(lambda: print('rekk wtf'))

    # notify the change of status of the image-process
    def notify_status_change(self, status):
        Strs.register(self.lbl_status, status.value)
        self.lbl_status.setStyleSheet('color: rgb{};'.format(status.get_text_color()[::-1]))
