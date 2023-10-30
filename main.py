import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from widgets.AppWindow import EMediaPlayer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = EMediaPlayer()
    videoplayer.resize(640, 480)
    videoplayer.show()
    videoplayer.showMaximized()
    videoplayer.getScreens()
    videoplayer.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
    sys.exit(app.exec())
