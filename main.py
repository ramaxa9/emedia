import sys

from PySide6.QtWidgets import QApplication

from widgets.AppWindow import EMediaPlayer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = EMediaPlayer()
    videoplayer.resize(640, 480)
    videoplayer.show()
    videoplayer.showMaximized()
    videoplayer.getScreens()
    sys.exit(app.exec())
