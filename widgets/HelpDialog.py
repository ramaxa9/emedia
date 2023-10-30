from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QVBoxLayout


class HelpDialog(QtWidgets.QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("Help")
        self.setMinimumSize(400, 800)
        textarea = QtWidgets.QTextBrowser()
        self.setModal(True)
        author = QLabel("Created by Roman Malashevych")
        layout = QVBoxLayout()
        layout.addWidget(textarea)
        layout.addWidget(author)
        self.setLayout(layout)

        helpText = """
Mouse:
    * Double click - load selected media
    * mouse right click - toggle full-screen (video area only)

Keyboard:
    * F - toggle full-screen
    * +(plus) - play/pause
    * R - set video slider to 0
    * N - select next
    * P - select previous
    * 0 to 9 - select and load item in playlist
    * X - put video output to the next screen
    * Z - put video output to the previous screen
        """

        textarea.setText(helpText)