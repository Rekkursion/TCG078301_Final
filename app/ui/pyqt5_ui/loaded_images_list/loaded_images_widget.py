from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import cv2
from utils.configuration import configuration as cfg
from utils.help_func import replace_file_ext, get_file_ext
from app.enums.colors import Colors
from app.enums.process_status import ProcessStatus
from app.enums.strings import Strs
from app.loaded_image import get_processed_image, get_original_image, get_ext_of_loaded_image, get_size_of_processed_image, get_num_of_detected_faces


# noinspection PyUnresolvedReferences
class LoadedImagesWidget(QWidget):
    """
        lbl_order:              the label for displaying the opening order among all have-been-loaded images
        lbl_win_name:           the label for displaying the (window) name of this loaded image
        lbl_size:               the label for displaying the size of the original image
        lbl_status_title:       the label for displaying the title of the status
        lbl_status:             the label for displaying the current status of image-processing
        lbl_num_of_detected:    the label for displaying the number of detected (2d/3d) faces
        btn_show_img:           the menu-like button for showing both original & processed images
        btn_save_processed:     the button for saving the processed image
    """
    def __init__(self, win_name, img, order, log_writer=None, parent=None):
        super(LoadedImagesWidget, self).__init__(parent)
        # the window name
        self.win_name = win_name
        # the log writer
        self.log_writer = log_writer
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
        self.lbl_num_of_detected = QLabel()
        self.btn_show_img = QPushButton(QIcon(QPixmap('./res/img_search.png')), '')
        self.btn_show_img.setStyleSheet("""
            QPushButton {background-color: transparent;}
            QPushButton:pressed {background-color: rgb(226, 230, 234);}
            QPushButton:hover:!pressed {background-color: rgb(226, 230, 234);}
        """)
        self.btn_save_processed = QPushButton()
        self.hbox_sec.addWidget(self.lbl_status_title, 0)
        self.hbox_sec.addWidget(self.lbl_status, 0)
        self.hbox_sec.addWidget(self.lbl_num_of_detected, 0)
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

    # notify the status of the image-process has been changed
    def notify_status_change(self, status):
        # replace the text by registering the status-showing label
        Strs.register(self.lbl_status, status.value)
        # change the text-color according to the status
        self.lbl_status.setStyleSheet('color: rgb{};'.format(status.get_text_color()[::-1]))
        # enable the buttons if and only if the process is done
        self.btn_show_img.setEnabled(status == ProcessStatus.DONE)
        self.btn_save_processed.setEnabled(status == ProcessStatus.DONE)
        # if the process is done
        if status == ProcessStatus.DONE:
            # initially show the size of the processed image (although it's still the same as the original one)
            self.notify_size_change()
            # show the number of detected faces, splitted into 2d & 3d
            self.notify_new_detected()

    # notify the size of the processed image has been changed
    def notify_size_change(self):
        # get the new size of the processed image
        new_size = get_size_of_processed_image(self.win_name)
        # re-write the text of the saving button
        Strs.register(self.btn_save_processed, Strs.Loaded_Img_Widget_Button_Save_Processed)
        self.btn_save_processed.setText('{} [{} x {}]'.format(self.btn_save_processed.text(), *new_size))

    # notify the number of detected faces has been updated
    def notify_new_detected(self):
        num_of_2d, num_of_3d = get_num_of_detected_faces(self.win_name)
        self.lbl_num_of_detected.setText('{}{}: {}, {}: {}{}'.format('{', cfg['CLS_NAMES'][0], num_of_2d, cfg['CLS_NAMES'][1], num_of_3d, '}'))

    # the action of saving the processed image
    def action_save_processed_image(self):
        # activate the save-file-dialog and get the filename and the file type selected by the user
        filename, file_type = QFileDialog.getSaveFileName(
            parent=self,
            caption=Strs.get_by_enum(Strs.Save_File_Dialog_Caption),
            filter='All (*);;JPG (*.jpg *.jpeg);;PNG (*.png);;BMP (*.bmp)'
        )
        # make sure the filename is NOT empty (the user clicked the 'save' button in the file-dialog)
        if filename != '':
            # if the type is ALL, automatically determines the extension w/ the original one
            if file_type == 'All (*)' and get_file_ext(filename) == '':
                filename = replace_file_ext(filename, get_ext_of_loaded_image(self.win_name))
            # write the image into the file w/ the designated filename
            cv2.imwrite(filename, get_processed_image(self.win_name))
            # write a log
            if self.log_writer is not None:
                self.log_writer(f'The processed image \"{self.win_name}\" has been saved to the designated location.', Colors.LOG_IMAGE_SAVED)
