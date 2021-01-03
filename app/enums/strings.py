from enum import Enum

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QMenu, QAction, QLineEdit, QDialog

from app.preferences.pref_manager import PrefManager

# the dictionary to contain all registered nodes (components)
_registered_dict = dict()


# the current font-family which depends on the language using
_font_families = ['微軟正黑體', 'Consolas']


# the font size
_font_size = 9


class Strs(Enum):
    # titles of some windows/dialogs
    Main_Window_Title = ('TCG078301_Final - 真人或手繪人臉之辨識器 - B10615031', 'TCG078301_Final - Real/Fake Faces Detector - B10615031')
    URL_Input_Dialog_Title = ('地址輸入對話框', 'URL Input Dialog')

    # something related to the menubar in main-window
    Menubar_File = ('檔案', 'File')
    Menubar_File_Load = ('載入', 'Load')
    Menubar_File_Load_From_Local = ('從本機', 'From local')
    Menubar_File_Load_From_URL = ('從地址', 'From URL')
    Menubar_File_Load_From_Clipboard = ('從剪貼簿', 'From clipboard')
    Menubar_File_Save = ('儲存', 'Save')
    Menubar_File_Save_All = ('儲存所有處理後的圖片到目錄', 'Save all processed images to a directory')
    Menubar_File_Save_Selected = ('儲存目前有選定的圖片到目錄', 'Save the selected images to a directory')
    Menubar_Pref = ('設定', 'Preferences')
    Menubar_Pref_Lang = ('介面語言', 'Interface language')
    Menubar_Pref_Pretrained_Rekk_Model = ('設置預訓練的 RekkModel 的路徑（只需設置一次）', 'Set the path of the pretrained RekkModel (Only need to set once)')

    # something related to the url-input-dialog
    URL_Dialog_Line_Edit_Placeholder = ('在此鍵入圖片地址。', 'Enter the image URL here.')
    URL_Dialog_Apply_Button = ('套用', 'Apply')
    URL_Dialog_Reset_Button = ('重置', 'Reset')
    URL_Dialog_Cancel_Button = ('取消', 'Cancel')

    # something related to the widget of the list of loaded-images shown in the main-window
    Loaded_Img_Widget_Status_Title = ('狀態 :', 'Status:')
    Loaded_Img_Widget_Button_Save_Processed = ('儲存處理後的圖片', 'Save the processed image')
    Loaded_Img_Widget_Action_Show_Original_Image = ('顯示原始載入圖片', 'Show the original image')
    Loaded_Img_Widget_Action_Show_Processed_Image = ('顯示處理後的圖片', 'Show the processed image')

    # something related to the statuses of image-process
    Status_Loading = ('載入或等待中', 'Loading or waiting')
    Status_Processing = ('處理中', 'Processing')
    Status_Done = ('處理完畢', 'Done')
    Status_Error = ('有錯誤發生', 'ERROR happened')

    # the captions of file-dialogs
    Open_File_Dialog_Caption = ('選取圖片', 'Select an image')
    Save_File_Dialog_Caption = ('儲存處理後的圖片', 'Save the processed image')
    Open_Directory_Dialog_Caption = ('選取目錄', 'Select a directory')
    Open_RekkModel_Dialog_Caption = ('設置預訓練的 RekkModel 的路徑（只需設置一次）', 'Set the path of the pretrained RekkModel (Only need to set once)')

    # get the literal string by a certain enumeration type
    @staticmethod
    def get_by_enum(str_enum):
        if isinstance(str_enum, Strs):
            return str_enum.value[PrefManager.get_pref('lang')]
        return str_enum

    # register a single node
    @staticmethod
    def register(node, str_enum_or_literal_str):
        _registered_dict[node] = str_enum_or_literal_str
        Strs.notify_registered(node)

    # register multiple nodes
    @staticmethod
    def register_all(*nodes_and_str_enums):
        for (node, str_enum) in nodes_and_str_enums:
            Strs.register(node, str_enum)

    # unregister a node
    @staticmethod
    def unregister(node):
        _registered_dict.pop(node)

    # notify a node to be updated
    @staticmethod
    def notify_registered(node):
        Strs.update_registered(node)

    # notify all registered nodes to be updatedㄣ
    @staticmethod
    def notify_all_registered():
        for key, _ in _registered_dict.items():
            Strs.update_registered(key)

    # update a registered node w/ text-changing
    @staticmethod
    def update_registered(node):
        if node in _registered_dict:
            # get the literal string by the passed-in str-enum
            literal_str = Strs.get_by_enum(_registered_dict[node])
            # set the font-family according to the language chosen
            node.setFont(QFont(_font_families[PrefManager.get_pref('lang')], _font_size))

            # a q-label, q-push-button, q-action -> set its text
            if isinstance(node, (QLabel, QPushButton, QAction)):
                node.setText(literal_str)
            # q-line-edit -> set its placeholder
            elif isinstance(node, QLineEdit):
                node.setPlaceholderText(literal_str)
            # q-main-window, q-dialog -> set its window-title
            elif isinstance(node, (QMainWindow, QDialog)):
                node.setWindowTitle(literal_str)
            # q-menu -> set its title
            elif isinstance(node, QMenu):
                node.setTitle(literal_str)
