from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import cv2
from utils.help_func import replace_file_ext, get_file_ext
from app.enums.process_status import ProcessStatus
from app.enums.strings import Strs
from app.loaded_image import get_processed_image, get_original_image, get_ext_of_loaded_image


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
        # set actions of the image-showing menu-button
        menu = QMenu()
        self.action_show_orig = QAction(Strs.get_by_enum(Strs.Loaded_Img_Widget_Action_Show_Original_Image), self)
        self.action_show_proc = QAction(Strs.get_by_enum(Strs.Loaded_Img_Widget_Action_Show_Processed_Image), self)
        menu.addAction(self.action_show_orig)
        menu.addAction(self.action_show_proc)
        self.btn_show_img.setMenu(menu)
        # disable all buttons from the beginning (they will be enabled until its process is done)
        self.btn_show_img.setDisabled(True)
        self.btn_save_processed.setDisabled(True)
        # register all text-related nodes to the str-enum class
        Strs.register_all(
            (self.lbl_status_title, Strs.Loaded_Img_Widget_Status_Title),
            (self.lbl_status, Strs.Status_Loading),
            (self.btn_save_processed, Strs.Loaded_Img_Widget_Button_Save_Processed),
            (self.action_show_orig, Strs.Loaded_Img_Widget_Action_Show_Original_Image),
            (self.action_show_proc, Strs.Loaded_Img_Widget_Action_Show_Processed_Image)
        )
        # initially change the text-color of the lbl-status
        self.lbl_status.setStyleSheet('color: rgb{};'.format(ProcessStatus.LOADING.get_text_color()[::-1]))
        # initialize events
        self.init_events()

    # initialize events
    def init_events(self):
        # show the original image
        self.action_show_orig.triggered.connect(lambda: cv2.imshow('|{}|'.format(self.win_name), get_original_image(self.win_name)))
        # show the processed image
        self.action_show_proc.triggered.connect(lambda: cv2.imshow(self.win_name, get_processed_image(self.win_name)))
        # save the processed image
        self.btn_save_processed.clicked.connect(self.action_save_processed_image)

    # notify the change of status of the image-process
    def notify_status_change(self, status):
        # replace the text by registering the status-showing label
        Strs.register(self.lbl_status, status.value)
        # change the text-color according to the status
        self.lbl_status.setStyleSheet('color: rgb{};'.format(status.get_text_color()[::-1]))
        # enable the buttons if and only if the process is done
        self.btn_show_img.setEnabled(status == ProcessStatus.DONE)
        self.btn_save_processed.setEnabled(status == ProcessStatus.DONE)

    # the action of saving the processed image
    def action_save_processed_image(self):
        # activate the save-file-dialog and get the filename and the file type selected by the user
        filename, file_type = QFileDialog.getSaveFileName(
            parent=self,
            caption=Strs.get_by_enum(Strs.Save_File_Dialog_Title),
            filter='All (*);;JPG (*.jpg *.jpeg);;PNG (*.png);;BMP (*.bmp)'
        )
        # make sure the filename is NOT empty (the user clicked the 'save' button in the file-dialog)
        if filename != '':
            # if the type is ALL, automatically determines the extension w/ the original one
            if file_type == 'All (*)' and get_file_ext(filename) == '':
                filename = replace_file_ext(filename, get_ext_of_loaded_image(self.win_name))
            # write the image into the file w/ the designated filename
            cv2.imwrite(filename, get_processed_image(self.win_name))
