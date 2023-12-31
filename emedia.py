import datetime
import os
import sys
import threading

import requests as requests
from pytube import extract, YouTube

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QColor, QPixmap, Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication, QListWidgetItem

from modules.MainWindow import AbstractMainWindow
from modules.PlayListItem import Item


class MainWindow(AbstractMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
        screen = QApplication.screens()[0].geometry()
        window = self.geometry()
        self.move(int(screen.width() / 2 - window.width() / 2), int(screen.height() / 2 - window.height() / 2))

        self.playlist_current_media = None
        self.item_current_media = None

        self.video_screen_move(self.ui.list_screens.currentIndex())

        self.ui.slider_progress.setRange(0, 0)

        self.disable_fade_buttons(100)

        # [SIGNALS] Player
        self.ui.btn_play.clicked.connect(self.player_play)
        self.ui.btn_pause.clicked.connect(self.player_pause)
        self.ui.btn_stop.clicked.connect(self.player_stop)
        self.ui.btn_next.clicked.connect(self.player_next)
        self.ui.btn_previous.clicked.connect(self.player_previous)
        self.ui.btn_fadeout.clicked.connect(self.volume_fadeout)
        self.ui.btn_fadein.clicked.connect(self.volume_fadein)

        self.VIDEO_SCREEN.fade_out_anim.finished.connect(self.volume_fadeout_pause)

        # [SIGNALS] PLAYLIST
        self.ui.link_youtbe.returnPressed.connect(self.add_youtube_video)
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
        self.VIDEO_SCREEN.videoPlayer.playbackStateChanged.connect(self.playback_state_handler)

        self.VIDEO_SCREEN.videoPlayer.positionChanged.connect(self.on_media_position_changed)
        self.VIDEO_SCREEN.videoPlayer.durationChanged.connect(self.media_slider_set_range)

        self.ui.slider_progress.sliderMoved.connect(self.on_slider_position_changed)

        self.ui.slider_volume.sliderMoved.connect(self.change_volume_output)
        self.ui.slider_volume.valueChanged.connect(self.disable_fade_buttons)

        self.VIDEO_SCREEN.fade_out_anim.valueChanged.connect(self.change_volume_slider)
        self.VIDEO_SCREEN.fade_in_anim.valueChanged.connect(self.change_volume_slider)

        # [SIGNALS] Application

    def add_youtube_video(self):
        # 'https://www.youtube.com/watch?v=_WJq0cfNvtg'

        url = str(self.ui.link_youtbe.text())
        yid = extract.video_id(url)
        metadata = YouTube(url)

        item = Item()
        item.setText(metadata.title)
        item.media_path = f'https://www.youtube.com/embed/{yid}?autoplay=1&start=1&rel=0s'
        item.media_length = datetime.timedelta(seconds=round(float(metadata.length)))
        item.media_type = 'YOUTUBE'
        item.media_file = metadata.title
        item.setIcon(self.getImageFromURL(metadata.thumbnail_url))
        self.ui.playlist.addItem(item)
        self.ui.link_youtbe.clear()

    def getImageFromURL(self, url):
        request = requests.get(url)
        thumbnail = QPixmap()
        thumbnail.loadFromData(request.content)
        thumbnail.scaledToHeight(150)
        return thumbnail

    # PLAYER
    def disable_fade_buttons(self, value):
        if int(value) == 0:
            self.ui.btn_fadeout.setDisabled(True)
            self.ui.btn_fadein.setEnabled(True)
        elif int(value) > 0:
            self.ui.btn_fadeout.setDisabled(False)
            self.ui.btn_fadein.setEnabled(False)

    def change_volume_output(self, value):
        self.ui.lbl_volume.setText(f'{value}%')
        value = value / 100
        print(f'change_volume_output: {value}')
        self.VIDEO_SCREEN.audioOutput.setVolume(value)

    def change_volume_slider(self, value):
        value = round(value * 100)
        self.ui.lbl_volume.setText(f'{value}%')
        print(f'change_volume_slider: {value}')
        self.ui.slider_volume.setSliderPosition(value)

    def volume_fadeout(self):
        self.VIDEO_SCREEN.fade_out_anim.setStartValue(self.VIDEO_SCREEN.audioOutput.volume())
        self.VIDEO_SCREEN.fade_out_anim.start()

    def volume_fadeout_pause(self):
        if self.ui.chk_fadeout_pause.isChecked():
            self.player_pause()

    def volume_fadein(self):
        self.VIDEO_SCREEN.fade_in_anim.setStartValue(self.VIDEO_SCREEN.audioOutput.volume())
        self.VIDEO_SCREEN.fade_in_anim.start()

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
        if self.ui.playlist.count() <= 0:
            return

        if self.playlist_current_media < self.ui.playlist.count() - 1:
            self.media_load(self.ui.playlist.item(self.playlist_current_media + 1))
        elif self.playlist_current_media == self.ui.playlist.count() - 1:
            self.media_load(self.ui.playlist.item(0))
        else:
            return

    def player_previous(self):
        if self.ui.playlist.count() <= 0:
            return

        if self.playlist_current_media > 0:
            self.media_load(self.ui.playlist.item(self.playlist_current_media - 1))
        else:
            return

    def player_loop_media(self):
        if self.ui.list_loop.currentIndex() == 1:
            self.player_play()
        elif self.ui.list_loop.currentIndex() == 2:
            self.player_next()
        else:
            return

    # MEDIA
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
        # print(f'{self.VIDEO_SCREEN.videoPlayer.source().path().lower()[1:]} {item.media_path.lower()}')
        if self.VIDEO_SCREEN.videoPlayer.source().path().lower()[1:] == item.media_path.lower():
            self.player_play()
            return

        self.VIDEO_SCREEN.webView.reload()
        if self.VIDEO_SCREEN.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player_stop()

        # if not os.path.exists(item.media_path):
        #     print(f'{item.media_path} not exists')
        #     return
        self.item_current_media = item
        self.playlist_current_media = self.ui.playlist.row(item)
        self.ui.lbl_current_media.setText(item.media_file)
        item_icon = item.icon()
        self.ui.lbl_current_media_thumbnail.setPixmap(item_icon.pixmap(QSize(130, 60)))
        self.VIDEO_SCREEN.videoPlayer.setSource(QUrl())

        if item.media_type == "IMAGE":
            self.player_stop()

            self.VIDEO_SCREEN.showFullScreen()
            self.VIDEO_SCREEN.setCurrentIndex(1)

            image = QPixmap(item.media_path)
            screen = QApplication.screens()[self.ui.list_screens.currentIndex()].geometry()
            image = image.scaled(screen.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.FastTransformation)

            self.VIDEO_SCREEN.stillViewer.setPixmap(image)
            self.VIDEO_SCREEN.stillViewer.adjustSize()
        # elif item.media_type == "DOCUMENT":
        #     self.player_stop()
        #     self.VIDEO_SCREEN.showFullScreen()
        #     self.VIDEO_SCREEN.setCurrentIndex(2)
        #
        #     self.VIDEO_SCREEN.webView.setUrl(item.media_path)
        elif item.media_type == "YOUTUBE" or item.media_type == "DOCUMENT":
            self.player_stop()
            self.VIDEO_SCREEN.showFullScreen()
            self.VIDEO_SCREEN.setCurrentIndex(2)

            self.VIDEO_SCREEN.webView.setUrl(item.media_path)
            # self.VIDEO_SCREEN.webView.reload()

        elif item.media_type == "DOCUMENT":
            self.player_stop()
            self.VIDEO_SCREEN.showFullScreen()
            self.VIDEO_SCREEN.setCurrentIndex(2)

            self.VIDEO_SCREEN.webView.setUrl(item.media_path)
            self.VIDEO_SCREEN.webView.settings().WebAttribute.FullScreenSupportEnabled()
            self.VIDEO_SCREEN.webView.settings().WebAttribute.AllowWindowActivationFromJavaScript()
            self.VIDEO_SCREEN.webView.settings().WebAttribute.JavascriptEnabled()
            self.VIDEO_SCREEN.webView.settings().WebAttribute.JavascriptCanOpenWindows()
            self.VIDEO_SCREEN.webView.settings().WebAttribute.ReadingFromCanvasEnabled()
            # self.VIDEO_SCREEN.webView.reload()

        else:
            self.VIDEO_SCREEN.setCurrentIndex(0)
            thread = threading.Thread(target=self.VIDEO_SCREEN.videoPlayer.setSource(QUrl.fromLocalFile(item.media_path)))
            thread.start()

            if self.ui.chk_doubleclick_play.isChecked() and self.item_current_media.media_type != "IMAGE":
                self.player_play()

    def media_status_handler(self, status: QMediaPlayer.MediaStatus):
        print(status)
        if status == QMediaPlayer.MediaStatus.NoMedia:
            pass

        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            pass

        if status == QMediaPlayer.MediaStatus.LoadingMedia:
            pass

        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            pass

        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.VIDEO_SCREEN.videoPlayer.setPosition(0)
            self.ui.slider_progress.setValue(0)
            self.player_loop_media()
            # TODO: show custom image on playback end

    def playback_state_handler(self, status: QMediaPlayer.PlaybackState):
        print(status)

        if status == QMediaPlayer.PlaybackState.PlayingState:
            pass

        if status == QMediaPlayer.PlaybackState.StoppedState:
            pass

    def media_slider_set_range(self, duration):
        counter = datetime.timedelta(seconds=round(duration / 1000))
        self.ui.lbl_total_time.setText(str(counter))
        self.ui.slider_progress.setRange(0, duration)

    def on_media_position_changed(self, position):
        self.ui.slider_progress.setValue(position)
        counter = datetime.timedelta(seconds=round(position / 1000))
        self.ui.lbl_current_time.setText(str(counter))

    def on_slider_position_changed(self, position):
        self.VIDEO_SCREEN.videoPlayer.setPosition(position)

    def closeEvent(self, event):
        # IDEA: save playlist on exit
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

    sys.exit(app.exec())
