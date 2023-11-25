import os

from PySide6 import QtCore
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QPalette, Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QLabel, QStackedWidget, QSizePolicy

from modules.StackedWidget import SlidingStackedWidget


class VideoWidget(SlidingStackedWidget):
    def __init__(self, mediafile: str = None):
        super(VideoWidget, self).__init__()
        self.setWindowTitle("EMedia Player")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
        self.move(0, 0)
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.videoPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(1.0)
        self.current_volume = self.audioOutput.volume()
        self.videoPlayer.setAudioOutput(self.audioOutput)
        self.videoPlayer.setVideoOutput(self.videoWidget)

        self.stillViewer = QLabel()
        self.stillViewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stillViewer.setBackgroundRole(QPalette.Base)
        self.stillViewer.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.setStyleSheet('background-color:black;')
        self.addWidget(self.videoWidget)
        self.addWidget(self.stillViewer)
        self.addWidget(self.webView)

        self.setCurrentIndex(1)

        self.offset = None

        # EFFECTS
        # # Fade
        self.fade_out_anim = QPropertyAnimation(self.audioOutput, b"volume")
        self.fade_out_anim.setDuration(600)
        self.fade_out_anim.setStartValue(self.audioOutput.volume())
        self.fade_out_anim.setEndValue(0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.fade_out_anim.setKeyValueAt(0.01, self.audioOutput.volume())

        self.fade_in_anim = QPropertyAnimation(self.audioOutput, b"volume")
        self.fade_in_anim.setDuration(600)
        self.fade_in_anim.setStartValue(self.audioOutput.volume())
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.Linear)
        self.fade_in_anim.setKeyValueAt(0.01, 0.01)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.isFullScreen():
            return

        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)
