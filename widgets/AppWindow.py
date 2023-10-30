import datetime
import os
import random
import subprocess
import tempfile

import cv2
from PySide6 import QtWidgets, QtCore, QtMultimedia
from PySide6.QtCore import QUrl, QDir
from PySide6.QtGui import QColor, QImage, QPixmap, Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication, QListWidgetItem, QFileDialog

from widgets.Controls import ControlsWidget, Item
from widgets.VideoScreen import VideoWidget


VIDEO_FILTER = [
            '*.mp4',
            '*.mov',
            '*.mkv',
            '*.wmv',
            '*.avi',
            '*.webm',
            '*.flv',
            '*.f4v',
        ]

IMAGE_FILTER = [
            '*.png',
            '*.jpg'
        ]

AUDIO_FILTER = [
            '*.mp3',
            '*.wav',
            '*.ogg',
            '*.flac',
            '*.aac',
            '*.wma',
        ]


class EMediaPlayer(QtWidgets.QMainWindow):
    def __init__(self):
        super(EMediaPlayer, self).__init__()

        self.controls = ControlsWidget()
        self.setCentralWidget(self.controls)
        self.videoScreen = VideoWidget()
        self.videoScreen.show()

        self.setWindowTitle(self.controls.windowTitle())

        self.controls.playButton.clicked.connect(self.play)
        self.controls.pauseButton.clicked.connect(self.pause)
        self.controls.stopButton.clicked.connect(self.stop)
        self.controls.openButton.clicked.connect(self.openFile)
        self.controls.btnUpdateScreens.clicked.connect(self.getScreens)
        self.controls.fullScreenButton.clicked.connect(self.fullScreen)
        self.controls.btnHideVideoScreen.clicked.connect(self.hideShowVideoScreen)
        # self.controls.screenSelect.currentIndexChanged.connect(self.movePlayer)
        # self.controls.playlist.currentRowChanged.connect(self.selectMedia)
        self.controls.playlist.itemClicked.connect(self.showStats)
        self.controls.playlist.itemDoubleClicked.connect(self.loadSelected)
        self.controls.playlist.itemDoubleClicked.connect(self.selectedItem)
        self.controls.btnDeleteItem.clicked.connect(self.deleteItemFromPlaylist)

        self.videoScreen.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoScreen.videoPlayer.durationChanged.connect(self.durationChanged)
        self.controls.positionSlider.sliderMoved.connect(self.set_position)
        self.controls.btnMoveToScreen.clicked.connect(self.movePlayer)

        self.videoScreen.videoPlayer.mediaStatusChanged.connect(self.mediaLoaded)
        self.videoScreen.videoPlayer.playbackStateChanged.connect(self.loopMedia)

    def hideShowVideoScreen(self):
        if self.videoScreen.isHidden():
            self.showVideoScreen()
        else:
            self.hideVideoScreen()

    def hideVideoScreen(self):
        self.videoScreen.hide()

    def showVideoScreen(self):
        self.videoScreen.show()

    def showStats(self, item):
        text = "{type} | {length} | <a href=file://///{path}>{file}</a>".format(type=item.media_type, length=item.media_length, file=os.path.join(item.media_path, item.media_file), path=item.media_path)
        self.controls.statusbar.setText(text)

    def mediaLoaded(self, mediastatus: QMediaPlayer.MediaStatus):
        print('Media status', mediastatus)
        duration = datetime.timedelta(seconds=round(self.videoScreen.videoPlayer.duration() / 1000))
        self.controls.mediaDuration.setText(str(duration))

    def seekVideo(self, value):
        self.videoScreen.videoPlayer.setPosition(value)

    def closeEvent(self, event):
        if event.spontaneous():
            reply = QtWidgets.QMessageBox.question(
                self, 'QUIT',
                'Do you really want to quit?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                QApplication.quit()
            else:
                event.ignore()

    def deleteItemFromPlaylist(self):
        # if self.controls.playOnSelect.isChecked():
        #     self.videoScreen.videoPlayer.stop()

        item = self.controls.playlist.currentRow()
        self.controls.playlist.takeItem(item)

    def getScreens(self):
        self.controls.screenSelect.clear()
        count = len(QApplication.screens())
        for i in range(0, count):
            self.controls.screenSelect.addItem(QApplication.screens()[i].name())

        self.controls.screenSelect.setCurrentIndex(count - 1)
        self.fullScreen()

    def movePlayer(self):
        self.showNormal()
        screen = self.controls.screenSelect.currentIndex()
        screenGeometry = QApplication.screens()[screen].geometry()

        self.videoScreen.move(screenGeometry.left(), screenGeometry.top())

    def fullScreen(self):
        self.movePlayer()
        if self.videoScreen.isMaximized():
            self.videoScreen.showNormal()
        else:
            self.videoScreen.showMaximized()
            if self.controls.playOnFullscreen.isChecked():
                self.videoScreen.videoPlayer.play()

    def loopMedia(self, playbackstatus):
        # if self.videoScreen.videoPlayer.PlaybackState == QMediaPlayer.PlaybackState.StoppedState:
        # if QMediaPlayer.MediaStatus.EndOfMedia
        print('Playback Status', playbackstatus)
        if self.controls.loop.currentIndex() == 0:
            return
        elif self.controls.loop.currentIndex() == 1:
            # if self.videoScreen.videoPlayer.MediaStatus == QMediaPlayer.MediaStatus.
            print("loop current")
            self.videoScreen.videoPlayer.play()
        elif self.controls.loop.currentIndex() == 2:
            current = self.controls.playlist.currentIndex().row()
            print("loop all", current)
            if self.controls.playlist.count() <= current + 1:
                print("first item", self.controls.playlist.count(), current)
                self.controls.playlist.setCurrentRow(0)
            else:
                print("next item", self.controls.playlist.count(), current)
                self.controls.playlist.setCurrentRow(self.controls.playlist.currentRow() + 1)

            self.loadSelected()
            self.playPrev()
        else:
            return

    def loadMedia(self, file):
        self.videoScreen.videoPlayer.setSource(QUrl.fromLocalFile(file))

        if self.controls.playOnSelect.isChecked():
            self.play()

    def selectedItem(self, item: QListWidgetItem):
        back_background = item.background()
        back_foreground = item.foreground()

        if QColor('#70B471').toRgb() == item.background().color().toRgb():
            return

        for i in range(self.controls.playlist.count()):
            self.controls.playlist.item(i).setBackground(back_background)
            self.controls.playlist.item(i).setForeground(back_foreground)

        item.setBackground(QColor('#70B471'))
        item.setForeground(QColor('#000000'))

    def loadSelected(self, item: Item = None):
        if item:
            if item.media_type == "IMAGE":
                image = os.path.join(item.media_path, item.media_file)
                print(image)
                self.videoScreen.mainWidget.setCurrentIndex(1)
                self.videoScreen.stillViewer.setPixmap(QPixmap(image))
                self.stop()
            else:
                self.videoScreen.mainWidget.setCurrentIndex(0)
            # file = str(item.text()).split(' | ')[1]
            # if file:
            #     self.loadMedia(file)
            file = os.path.join(item.media_path, item.media_file)
            self.loadMedia(file)

        if item.media_type == "AUDIO":
            self.hideVideoScreen()
        else:
            self.showVideoScreen()

    def openFile_DELETE(self, videofile: None):
        joinfiletypes = ' '.join(VIDEO_FILTER + AUDIO_FILTER + IMAGE_FILTER)
        filetypes = f"Supportes files ({joinfiletypes});;Video files ({' '.join(VIDEO_FILTER)});;Images({' '.join(IMAGE_FILTER)});;Audio files ({' '.join(AUDIO_FILTER)});;All files(*)"
        fileNames = QFileDialog.getOpenFileNames(self, "Open Media", QDir.homePath(), filetypes)

        # if fileNames.count() > 0:

        i = self.controls.playlist.count()
        for file in fileNames[0]:
            if os.path.exists(file):
                if '*' + os.path.splitext(file)[-1].lower() in IMAGE_FILTER:
                    self.controls.playlist.addItem(f"[{i}] [IMAGE] {file}")
                else:
                    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                             "format=duration", "-of",
                                             "default=noprint_wrappers=1:nokey=1", file],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)

                    mediaduration = datetime.timedelta(seconds=round(float(result.stdout)))
                    # self.controls.playlistItems.append([i, mediaduration, file])
                    self.controls.playlist.addItem(f"[{i}] [{mediaduration}] {file}")
            i += 1

                        # self.videoPlayer.setMedia(
                        #     QMediaContent(QUrl.fromLocalFile(fileName)))
    def openFile(self):
        joinfiletypes = ' '.join(VIDEO_FILTER + AUDIO_FILTER + IMAGE_FILTER)
        filetypes = f"Supportes files ({joinfiletypes});;Video files ({' '.join(VIDEO_FILTER)});;Images({' '.join(IMAGE_FILTER)});;Audio files ({' '.join(AUDIO_FILTER)});;All files(*)"
        fileNames = QFileDialog.getOpenFileNames(self, "Open Media", QDir.homePath(), filetypes)

        for file in fileNames[0]:
            ifexist = [self.controls.playlist.item(i).media_file for i in range(self.controls.playlist.count())]

            if os.path.split(file)[-1] in ifexist:
                print("File already in playlist!")
            else:
                if os.path.exists(file):
                    item = Item()
                    filename, file_ext = os.path.splitext(file)

                    item.media_file = os.path.split(file)[-1]
                    item.media_path = os.path.split(file)[0]

                    if '*' + file_ext in VIDEO_FILTER:
                        item.media_type = 'VIDEO'
                        item.media_length = self.get_media_length(file)
                        item.setIcon(self.createThumbnail(file))

                    if '*' + file_ext in AUDIO_FILTER:
                        item.media_type = 'AUDIO'
                        item.media_length = self.get_media_length(file)
                        item.setIcon(QPixmap(os.path.join(os.getcwd(), 'images', 'speakers.png')))

                    if '*' + file_ext in IMAGE_FILTER:
                        item.media_type = 'IMAGE'
                        item.setIcon(QPixmap(file))

                    item.setText(item.media_file)
                    self.controls.playlist.addItem(item)

    def createThumbnail(self, file):
        cap = cv2.VideoCapture(file)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # frame = random.randrange(20, int(frame_count) - 20)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 50)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            thumbnail = pixmap.scaled(320, 240, Qt.AspectRatioMode.KeepAspectRatio)
        cap.release()
        return thumbnail

    def get_media_length(self, file):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        length = datetime.timedelta(seconds=round(float(result.stdout)))
        return length

    def playPause(self):
        if self.videoScreen.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.videoScreen.videoPlayer.pause()
        else:
            self.videoScreen.videoPlayer.play()

    def play(self):
        if self.videoScreen.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            return
        else:
            self.videoScreen.videoPlayer.play()

    def pause(self):
        if self.videoScreen.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PausedState:
            return
        else:
            self.videoScreen.videoPlayer.pause()

    def stop(self):
        if self.videoScreen.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            return
        else:
            self.videoScreen.videoPlayer.stop()

    def playNext(self):
        current = self.controls.playlist.currentRow()
        count = self.controls.playlist.count()
        prev = current - 1

        next = current + 1

        if next > count - 1:
            return
        else:
            self.controls.playlist.setCurrentRow(next)
            self.loadSelected()

    def playPrev(self):
        current = self.controls.playlist.currentRow()
        count = self.controls.playlist.count()
        prev = current - 1
        next = current + 1

        if prev < 0:
            return
        else:
            self.controls.playlist.setCurrentRow(prev)
            self.loadSelected()

    def positionChanged(self, position):
        # mediaduration = round((self.videoScreen.videoPlayer.duration() - position) / 1000)
        # mediaduration = round(position)
        # duration = self.videoScreen.videoPlayer.duration()
        counter = datetime.timedelta(seconds=round(position / 1000))
        # timeleft = datetime.timedelta(seconds=round((duration - position)/1000))
        self.controls.mediaTimeCounter.setText(str(counter))
        # self.controls.mediaTimeLeft.setText(str(timeleft))
        self.controls.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.controls.positionSlider.setRange(0, duration)

    def set_position(self, position):
        self.videoScreen.videoPlayer.setPosition(position)

    def keyPressEvent(self, event):

        print(event.text(), event.key())
        hotkeys = {
            QtCore.Qt.Key.Key_1: 1,
            QtCore.Qt.Key.Key_2: 2,
            QtCore.Qt.Key.Key_3: 3,
            QtCore.Qt.Key.Key_4: 4,
            QtCore.Qt.Key.Key_5: 5,
            QtCore.Qt.Key.Key_6: 6,
            QtCore.Qt.Key.Key_7: 7,
            QtCore.Qt.Key.Key_8: 8,
            QtCore.Qt.Key.Key_9: 9,
            QtCore.Qt.Key.Key_0: 0,
        }
        if event.key() in hotkeys:
            key = hotkeys[event.key()]
            print(key, self.controls.playlist.count())
            if self.controls.playlist.count() > key:
                self.controls.playlist.setCurrentRow(key)
                self.loadSelected(self.controls.playlist.item(key))
        if event.key() == QtCore.Qt.Key.Key_R:
            self.videoScreen.videoPlayer.setPosition(0)
        if event.key() == QtCore.Qt.Key.Key_Plus:
            self.playPause()
        if event.key() == QtCore.Qt.Key.Key_F:
            self.fullScreen()
        if event.key() == QtCore.Qt.Key.Key_Z:
            current = self.controls.screenSelect.currentIndex()
            print(current)
            if current == 0:
                return
            else:
                self.controls.screenSelect.setCurrentIndex(current - 1)

        if event.key() == QtCore.Qt.Key.Key_X:
            current = self.controls.screenSelect.currentIndex()
            maxcount = self.controls.screenSelect.count()
            print(current, maxcount)
            if maxcount <= current + 1:
                return
            else:
                self.controls.screenSelect.setCurrentIndex(current + 1)

        if event.key() == QtCore.Qt.Key.Key_P:
            self.playPrev()

        if event.key() == QtCore.Qt.Key.Key_N:
            self.playNext()
