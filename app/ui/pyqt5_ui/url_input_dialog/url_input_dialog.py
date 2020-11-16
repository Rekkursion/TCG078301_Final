import socket
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PIL import Image, UnidentifiedImageError
from PIL.GifImagePlugin import GifImageFile
import urllib
import numpy as np
from app.enums.strings import Strs


# the dialog for the user to input the image-URL
class URLInputDialog(QDialog):
    """
        txt_url:    the line-edit for entering the text of url
        btn_apply:  the push-button for applying the entered text of url
        btn_reset:  the push-button for resetting (clearing) the line-edit for entering the text of url
        btn_cancel: the push-button for cancelling
    """
    def __init__(self):
        super(URLInputDialog, self).__init__()
        # load the UI
        uic.loadUi('./ui/pyqt5_ui/url_input_dialog/url_input_dialog.ui', self)
        # initialize the events
        self.init_events()
        # force this dialog being the top form
        self.setWindowModality(Qt.ApplicationModal)
        # the loaded image if any
        self.loaded_img = None
        # register all text-related nodes to the str-enum class
        Strs.register_all(
            (self, Strs.URL_Input_Dialog_Title),
            (self.txt_url, Strs.URL_Dialog_Line_Edit_Placeholder),
            (self.btn_apply, Strs.URL_Dialog_Apply_Button),
            (self.btn_reset, Strs.URL_Dialog_Reset_Button),
            (self.btn_cancel, Strs.URL_Dialog_Cancel_Button)
        )

    # initialize the events
    def init_events(self):
        # apply the entered url
        self.btn_apply.clicked.connect(lambda: {self.download_image_from_url(self.txt_url.text()), self.accept()})
        # reset the line-edit which is used to enter the url
        self.btn_reset.clicked.connect(lambda: {self.txt_url.setText(''), self.txt_url.setFocus()})
        # cancel the whole action
        self.btn_cancel.clicked.connect(lambda: self.close())
        pass

    # download the image from the designated url-text
    # noinspection PyUnresolvedReferences
    def download_image_from_url(self, url):
        try:
            # the pre-defined temporal filename
            filename = './res/dl_img/url-loaded'
            # download the file through the designated url
            urllib.request.urlretrieve(url, filename)
            # open the file as an image
            img = Image.open(filename).convert('RGB')
            # if the loaded image is a gif, raise the error because the gif format is NOT supported
            if isinstance(img, GifImageFile):
                raise UnidentifiedImageError
            # set the image as the loaded one
            self.loaded_img = np.asarray(img)
        # some possible errors due to the network-related things (url, socket, http, etc.)
        except (socket.error, urllib.error.URLError, urllib.error.HTTPError, urllib.error.ContentTooShortError):
            # todo
            print('Image downloading failed.')
        # some possible errors since the loaded image may be with an unknown or unsupported format/content
        except (ValueError, UnidentifiedImageError, OSError):
            # todo
            print('Unknown image file. Please aware that GIF files are NOT supported.')

    # get the user-entered url
    def get_url(self):
        return self.txt_url.text()

    # get the loaded image if any
    def get_loaded_image(self):
        return self.loaded_img
