import os

from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget


class VideoWidget(QtWidgets.QWidget):
    def __init__(self, mediafile: str = None):
        super(VideoWidget, self).__init__()
        self.setWindowTitle("EMedia Player")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
        # self.setMinimumSize(600, 400)
        # self.move(200, 200)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.move(0, 0)
        self.setMinimumSize(800, 600)

        self.videoPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(1.0)
        self.videoPlayer.setAudioOutput(self.audioOutput)
        self.videoPlayer.setVideoOutput(self.videoWidget)

        self.stillViewer = QLabel()
        # self.stillViewer.setStyleSheet('border:1 solid white;')
        # self.stillViewer.adjustSize()
        self.stillViewer.setScaledContents(True)

        self.mainWidget = QStackedWidget()
        self.mainWidget.setStyleSheet('background-color:black;')
        self.mainWidget.addWidget(self.videoWidget)
        self.mainWidget.addWidget(self.stillViewer)

        self.mainWidget.setCurrentIndex(1)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.mainWidget)
        # mainLayout.addWidget(self.controls)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        # centralWidget = QtWidgets.QWidget()
        # self.setCentralWidget(centralWidget)
        # centralWidget.setLayout(mainLayout)
        self.setLayout(mainLayout)

        self.offset = None
        self.showFullScreen()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)