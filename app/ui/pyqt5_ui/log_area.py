from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextBrowser


class LogArea(QTextBrowser):
    def __init__(self):
        super(LogArea, self).__init__()

    def append(self, p_str):
        super(LogArea, self).append(p_str)
        # to keep the text-browser always at the bottom
        self.moveCursor(self.textCursor().End)

    # def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
    #     cursor = self.cursorForPosition(ev.globalPos())
    #     position = cursor.position()
    #     self.textCursor().setPosition(position)
    #     self.setTextCursor(self.textCursor())
    #
    #     print(self.textCursor().select(QTextCursor.WordUnderCursor))
    #     print(self.textCursor().select(QTextCursor.BlockUnderCursor))
    #     print(self.textCursor().select(QTextCursor.LineUnderCursor), end='\n\n')
    #
    #     self.moveCursor(self.textCursor().End)
