from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2


# noinspection PyUnresolvedReferences
class LoadedImagesWidget(QWidget):
    # the fixed size of showing the image (w, h)
    fixed_img_size = (80, 100)

    def __init__(self, parent=None):
        super(LoadedImagesWidget, self).__init__(parent)
        self.hbox_all = QHBoxLayout()
        self.vbox_right_side = QVBoxLayout()
        self.lbl_img = QLabel()
        self.lbl_status = QLabel()
        self.lbl_img_size = QLabel()
        self.btn_save = QPushButton(text='儲存處理後的圖片 Save the processed image')
        self.init_views()
        self.init_events()

    # initialize views
    def init_views(self):
        self.lbl_status.setAlignment(Qt.AlignLeft)
        self.lbl_img_size.setAlignment(Qt.AlignLeft)
        self.btn_save.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.vbox_right_side.addWidget(self.lbl_status, 0)
        self.vbox_right_side.addWidget(self.lbl_img_size, 0)
        self.vbox_right_side.addWidget(self.btn_save, 1)
        self.hbox_all.addWidget(self.lbl_img, 0)
        self.hbox_all.addLayout(self.vbox_right_side, 1)
        self.setLayout(self.hbox_all)

    # initialize events
    def init_events(self):
        # todo: save processed image
        self.btn_save.clicked.connect(lambda: print('rekk wtf'))

    def set_img_data(self, img):
        # resize the passed image
        resized = cv2.resize(img, LoadedImagesWidget.fixed_img_size)
        # convert it into the type of q-image
        q_img = QImage(resized.data, *LoadedImagesWidget.fixed_img_size, QImage.Format_RGB888).rgbSwapped()
        # show the image
        self.lbl_img.setPixmap(QPixmap.fromImage(q_img))
        # show its original size
        self.lbl_img_size.setText('[{} x {}]'.format(img.shape[1], img.shape[0]))
