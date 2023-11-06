import datetime
import os.path
import subprocess

import cv2
from PySide6.QtCore import QDir, Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QPalette, QColor
from PySide6.QtWidgets import QWidget, QMainWindow, QFileDialog, QApplication, QListView, QListWidget, QListWidgetItem

from UI.MainWindow import Ui_MainWindow
from qframelesswindow import FramelessWindow, StandardTitleBar
import qtawesome as qta

from modules.PlayListItem import Item
from modules.VideoScreen import VideoWidget

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


class AbstractMainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('EMedia')
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()

        qss = open(os.path.join(os.getcwd(), 'UI', 'Dark.qss')).read()
        self.setStyleSheet(qss)

        # Controls
        self.ui.btn_play.setIcon(qta.icon('mdi6.play', color='white'))
        self.ui.btn_pause.setIcon(qta.icon('mdi6.pause', color='white'))
        self.ui.btn_stop.setIcon(qta.icon('mdi6.stop', color='white'))

        self.ui.btn_reload_screens.setIcon(qta.icon('mdi6.reload', color='white'))
        self.ui.btn_reload_screens.setIconSize(QSize(20, 20))
        self.ui.btn_fullscreen.setIcon(qta.icon('mdi6.fullscreen', color='white'))
        self.ui.btn_fullscreen.setIconSize(QSize(20, 20))

        # Playlist
        self.ui.btn_view_mode.setIcon(qta.icon('mdi6.format-list-text', color='white'))
        self.ui.btn_view_mode.setIconSize(QSize(24, 24))

        self.ui.btn_playlist_add.setIcon(qta.icon('mdi6.file-plus', color='white'))
        self.ui.btn_playlist_del.setIcon(qta.icon('mdi6.file-remove-outline', color='white'))

        self.ui.list_loop.addItem("Loop None")
        self.ui.list_loop.addItem("Loop Current")
        self.ui.list_loop.addItem("Loop Playlist")

        # Video screen
        self.video_screen_get_screens()
        self.VIDEO_SCREEN = VideoWidget()
        self.video_screen_move(self.ui.list_screens.currentIndex())

    # Playlist
    def playlist_show_media_info(self, item: Item):
        text = (f'{item.media_type} | {item.media_length} | '
                f'<a href={os.path.split(item.media_path)[0]}><span style="color: #aecff7; ">{item.media_file}</span></a>')

        self.ui.lbl_media_info.setText(text)

    def playlist_icons_size(self, value):
        iWidth = value
        iHeight = value

        self.ui.playlist.setIconSize(QSize(iWidth, iHeight))
        # self.ui.playlist.setGridSize(QSize(iWidth + 5, iHeight + 5))

    def playlist_view_mode(self):
        if self.ui.btn_view_mode.isChecked():
            self.playlist_view_mode_list()
        else:
            self.playlist_view_mode_icons()

    def playlist_view_mode_list(self):
        self.ui.playlist.setViewMode(QListWidget.ViewMode.ListMode)
        # self.ui.playlist.setMovement(QListView.Movement.Snap)
        self.ui.playlist.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.ui.spin_playlist_icons_size.setValue(50)

    def playlist_view_mode_icons(self):
        self.ui.playlist.setViewMode(QListWidget.ViewMode.IconMode)
        self.ui.playlist.setMovement(QListView.Movement.Free)
        self.ui.playlist.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.ui.spin_playlist_icons_size.setValue(200)

    def playlist_item_delete(self):
        # IDEA: clear mediaplayer>media object on media delete

        item = self.ui.playlist.currentRow()
        self.ui.playlist.takeItem(item)

    def playlist_item_add(self):
        # TODO: put in thread
        jointypes = ' '.join(VIDEO_FILTER + AUDIO_FILTER + IMAGE_FILTER)
        filetypes = (f"Supported files ({jointypes});;Video files ({' '.join(VIDEO_FILTER)});;"
                     f"Images({' '.join(IMAGE_FILTER)});;Audio files ({' '.join(AUDIO_FILTER)});;All files(*)")

        file_dialog = QFileDialog(self)
        file_names = file_dialog.getOpenFileNames(self, "Open Media", QDir.homePath(), filetypes)

        for file in file_names[0]:
            if os.path.split(file)[-1] in [self.ui.playlist.item(i).media_file for i in range(self.ui.playlist.count())]:
                # check if name already in playlist
                print("File already in playlist!")
            else:
                if os.path.exists(file):
                    item = Item()
                    filename, file_ext = os.path.splitext(file)

                    item.media_file = os.path.split(file)[-1]
                    item.media_path = file

                    if '*' + file_ext in VIDEO_FILTER:
                        item.media_type = 'VIDEO'
                        item.media_length = self.playlist_get_media_length(file)
                        item.setIcon(self.playlist_create_thumbnail(file))

                    if '*' + file_ext in AUDIO_FILTER:
                        item.media_type = 'AUDIO'
                        item.media_length = self.playlist_get_media_length(file)
                        item.setIcon(QPixmap(os.path.join(os.getcwd(), 'images', 'speakers.png')))

                    if '*' + file_ext in IMAGE_FILTER:
                        item.media_type = 'IMAGE'
                        item.setIcon(QPixmap(file))

                    item.setText(item.media_file)
                    self.ui.playlist.addItem(item)

    def playlist_create_thumbnail(self, file):
        cap = cv2.VideoCapture(file)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # frame = random.randrange(20, int(frame_count) - 20)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 50)
        ret, frame = cap.read()
        thumbnail = None
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            thumbnail = pixmap.scaled(320, 240, Qt.AspectRatioMode.KeepAspectRatio)
        cap.release()
        return thumbnail

    def playlist_get_media_length(self, file):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        length = datetime.timedelta(seconds=round(float(result.stdout)))
        return length

    # Screen
    def video_screen_toggle_hide(self):
        if self.VIDEO_SCREEN.isHidden():
            self.VIDEO_SCREEN.show()
        else:
            self.VIDEO_SCREEN.hide()

    def video_screen_get_screens(self):
        self.ui.list_screens.clear()
        count = len(QApplication.screens())
        for i in range(0, count):
            self.ui.list_screens.addItem(QApplication.screens()[i].name())

        self.ui.list_screens.setCurrentIndex(count - 1)
        # self.video_screen_fullscreen()

    def video_screen_move(self, screen):
        self.VIDEO_SCREEN.showNormal()
        screenGeometry = QApplication.screens()[screen].geometry()

        self.VIDEO_SCREEN.move(screenGeometry.left(), screenGeometry.top())
        self.VIDEO_SCREEN.showFullScreen()

    def video_screen_fullscreen(self):
        self.video_screen_move(self.ui.list_screens.currentIndex())
        if self.VIDEO_SCREEN.isMaximized():
            self.VIDEO_SCREEN.showNormal()
        else:
            self.VIDEO_SCREEN.showMaximized()
            if self.ui.chk_play_on_fullscreen.isChecked():
                self.VIDEO_SCREEN.videoPlayer.play()


