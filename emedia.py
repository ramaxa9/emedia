import datetime
import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QColor, QPixmap, Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication, QListWidgetItem

from modules.AbstractMainWindow import AbstractMainWindow
from modules.PlayListItem import Item


class MainWindow(AbstractMainWindow):
    def __init__(self):
        super().__init__()

        self.playlist_current_media = None

        # [SIGNALS] Player
        self.ui.btn_play.clicked.connect(self.player_play)
        self.ui.btn_pause.clicked.connect(self.player_pause)
        self.ui.btn_stop.clicked.connect(self.player_stop)

        # [SIGNALS] PLAYLIST
        self.ui.btn_playlist_add.clicked.connect(self.playlist_item_add)
        self.ui.btn_view_mode.clicked.connect(self.playlist_view_mode)
        self.ui.btn_playlist_del.clicked.connect(self.playlist_item_delete)
        self.ui.playlist.itemClicked.connect(self.playlist_show_media_info)
        self.ui.spin_playlist_icons_size.valueChanged.connect(self.playlist_icons_size)
        self.ui.playlist.itemDoubleClicked.connect(self.media_load)

        self.playlist_view_mode_icons()

        # [SIGNALS] VIDEO SCREEN
        self.ui.btn_reload_screens.clicked.connect(self.video_screen_get_screens)
        self.ui.btn_fullscreen.clicked.connect(self.video_screen_fullscreen)
        self.ui.btn_show_hide_screen.clicked.connect(self.video_screen_toggle_hide)

        self.ui.list_screens.currentIndexChanged.connect(self.video_screen_move)

        self.VIDEO_SCREEN.videoPlayer.mediaStatusChanged.connect(self.media_status_handler)
        # self.VIDEO_SCREEN.videoPlayer.playbackStateChanged.connect(self.player_loop_media)

        # [SIGNALS] Application
        self.titleBar.closeBtn.clicked.connect(self.close)

    # PLAYER
    def player_toggle_play_pause(self):
        if self.VIDEO_SCREEN.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.VIDEO_SCREEN.videoPlayer.pause()
        else:
            self.VIDEO_SCREEN.videoPlayer.play()

    def player_play(self):
        if self.VIDEO_SCREEN.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            return
        else:
            self.VIDEO_SCREEN.videoPlayer.play()

    def player_pause(self):
        if self.VIDEO_SCREEN.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PausedState:
            return
        else:
            self.VIDEO_SCREEN.videoPlayer.pause()

    def player_stop(self):
        if self.VIDEO_SCREEN.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            return
        else:
            self.VIDEO_SCREEN.videoPlayer.stop()

    def player_next(self):
        # FIXME: rework
        current = self.ui.playlist.currentRow()
        count = self.ui.playlist.count()
        prev = current - 1

        next = current + 1

        if next > count - 1:
            return
        else:
            self.ui.playlist.setCurrentRow(next)
            self.loadSelected()

    def player_previous(self):
        # FIXME: rework
        current = self.ui.playlist.currentRow()
        count = self.ui.playlist.count()
        prev = current - 1
        next = current + 1

        if prev < 0:
            return
        else:
            self.ui.playlist.setCurrentRow(prev)
            self.loadSelected()

    def player_seek(self, value):
        self.VIDEO_SCREEN.videoPlayer.setPosition(value)

    # def player_loop_media(self, status):
    #     # FIXME: rework
    #     # if self.videoScreen.videoPlayer.PlaybackState == QMediaPlayer.PlaybackState.StoppedState:
    #     # if QMediaPlayer.MediaStatus.EndOfMedia
    #     print('Playback Status', status)
    #     if self.ui.list_loop.currentIndex() == 0:
    #         return
    #     elif self.ui.list_loop.currentIndex() == 1:
    #         # if self.videoScreen.videoPlayer.MediaStatus == QMediaPlayer.MediaStatus.
    #         print("loop current")
    #         self.VIDEO_SCREEN.videoPlayer.play()
    #     elif self.ui.list_loop.currentIndex() == 2:
    #         current = self.ui.playlist.currentIndex().row()
    #         print("loop all", current)
    #         if self.ui.playlist.count() <= current + 1:
    #             print("first item", self.ui.playlist.count(), current)
    #             self.ui.playlist.setCurrentRow(0)
    #         else:
    #             print("next item", self.ui.playlist.count(), current)
    #             self.ui.playlist.setCurrentRow(self.ui.playlist.currentRow() + 1)
    #
    #         item = self.ui.playlist.item(self.ui.playlist.currentIndex())
    #         self.media_load(item)
    #         self.player_next()
    #     else:
    #         return

    # MEDIA
    def media_status_handler(self, status):
        print('Media status', status)
        if status == QMediaPlayer.MediaStatus.NoMedia:
            pass

        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            duration = datetime.timedelta(seconds=round(self.VIDEO_SCREEN.videoPlayer.duration() / 1000))
            self.ui.lbl_total_time.setText(str(duration))

        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.VIDEO_SCREEN.hide()

    def media_mark_loaded(self, item: QListWidgetItem):
        back_background = item.background()
        back_foreground = item.foreground()

        if QColor('#70B471').toRgb() == item.background().color().toRgb():
            return

        for i in range(self.ui.playlist.count()):
            self.ui.playlist.item(i).setBackground(back_background)
            self.ui.playlist.item(i).setForeground(back_foreground)

        item.setBackground(QColor.fromString('#70B471'))
        item.setForeground(QColor.fromString('#000000'))

    def media_load(self, item: Item):
        if item.media_type == "IMAGE":
            self.VIDEO_SCREEN.showFullScreen()
            self.VIDEO_SCREEN.setCurrentIndex(1)

            image = QPixmap(item.media_path)
            screen = QApplication.screens()[self.ui.list_screens.currentIndex()].geometry()

            image = image.scaled(screen.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)

            self.VIDEO_SCREEN.stillViewer.setPixmap(image)
            # self.VIDEO_SCREEN.stillViewer.setScaledContents(True)
            self.VIDEO_SCREEN.stillViewer.adjustSize()
            self.player_stop()
        else:
            self.VIDEO_SCREEN.setCurrentIndex(0)
            self.VIDEO_SCREEN.videoPlayer.setSource(QUrl.fromLocalFile(item.media_path))

        if item.media_type == "AUDIO":
            self.VIDEO_SCREEN.hide()
        else:
            self.VIDEO_SCREEN.show()

        self.playlist_current_media = self.ui.playlist.row(item)
        self.ui.lbl_current_media.setText(f'{self.playlist_current_media} | {item.media_length} | {item.media_file}')
        self.media_mark_loaded(item)

        if self.ui.chk_doubleclick_play.isChecked():
            self.player_play()

    def media_loaded(self, status: QMediaPlayer.MediaStatus):
        print('Media status', status)
        duration = datetime.timedelta(seconds=round(self.VIDEO_SCREEN.videoPlayer.duration() / 1000))
        self.ui.lbl_total_time.setText(str(duration))

    def media_position_changed(self, position):
        counter = datetime.timedelta(seconds=round(position / 1000))
        self.ui.lbl_current_time.setText(str(counter))
        self.ui.slider_progress.positionSlider.setValue(position)

    def media_duration_changed(self, duration):
        self.ui.slider_progress.positionSlider.setRange(0, duration)

    def media_set_position(self, position):
        self.VIDEO_SCREEN.videoPlayer.setPosition(position)

    def closeEvent(self, event):
        # IDEA: save playlist on exit
        # FIXME: close dialog appears twice if press NO
        if event:
            reply = QtWidgets.QMessageBox.question(
                self, 'QUIT',
                'Do you really want to quit?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = MainWindow()
    videoplayer.resize(640, 480)
    videoplayer.show()
    # videoplayer.getScreens()
    videoplayer.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
    sys.exit(app.exec())
