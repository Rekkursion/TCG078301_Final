from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from app.ui.pyqt5_ui.loaded_images_list.loaded_images_widget import LoadedImagesWidget


class LoadedImagesListWidget(QListWidget):
    def __init__(self):
        super(LoadedImagesListWidget, self).__init__()
        # set the margins
        self.setViewportMargins(12, 12, 12, 12)

    # push an item into this list
    def push_back(self, win_name, img):
        if img is not None:
            widget = LoadedImagesWidget(win_name, img, self.count() + 1)
            item = QListWidgetItem(self)
            item.setSizeHint(widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, widget)
            return widget

    # get the designated widget by the corresponding window name
    def get_widget_by_win_name(self, win_name):
        for widget in [self.itemWidget(self.item(i)) for i in range(0, self.count())]:
            if widget.win_name == win_name:
                return widget
        return None
