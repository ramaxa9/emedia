from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QListWidget


class Playlist(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        self.item_positions = {}

    def dropEvent(self, event):
        super().dropEvent(event)
        self.save_positions()

    def save_positions(self):
        for i in range(self.count()):
            item = self.item(i)
            self.item_positions[item.text()] = self.visualItemRect(item).topLeft()

    def restore_positions(self):
        for text, position in self.item_positions.items():
            items = self.findItems(text, QtCore.Qt.MatchFlag.MatchExactly)
            if items:
                item = items[0]
                rect = item.rect()
                rect.moveTopLeft(position)
                item.setViewModeRect(rect)
