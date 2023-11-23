import datetime
import os.path
import subprocess
import threading
from collections import OrderedDict

import cv2
import qtawesome as qta
from PySide6.QtCore import QDir, Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtWidgets import QWidget, QFileDialog, QApplication, QListView, QListWidget, QTreeWidgetItem

from modules.UI_MainWindow import Ui_MainWindow
from modules.PlayListItem import Item
from modules.VideoScreen import VideoWidget

VIDEO_FILTER = [
    '*.mp4',
    '*.mov',
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
    '*.ogg',
    '*.aac',
]

DOCUMENT_FILTER = [
    '*.pdf',
]


class AbstractMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.oldPos = None

        self.setWindowTitle('EMedia')
        self.setWindowIcon(QPixmap(os.path.join(os.getcwd(), 'images', 'logo.png')))

        qss = open('Dark.qss').read()
        self.setStyleSheet(qss)

        # Controls
        self.ui.btn_play.setIcon(qta.icon('mdi6.play', color='white'))
        self.ui.btn_pause.setIcon(qta.icon('mdi6.pause', color='white'))
        self.ui.btn_stop.setIcon(qta.icon('mdi6.stop', color='white'))
        self.ui.btn_previous.setIcon(qta.icon('mdi6.skip-previous', color='white'))
        self.ui.btn_next.setIcon(qta.icon('mdi6.skip-next', color='white'))

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

    # Playlist
    def playlist_show_media_info(self, item: Item):
        self.ui.media_info.clear()

        media_info = OrderedDict({
            'media_type': item.media_type,
            'media_file': item.media_file,
            'media_path': item.media_path,
            'media_length': item.media_length,
        })

        self.ui.media_info.setColumnCount(2)
        self.ui.media_info.setHeaderHidden(False)
        self.ui.media_info.setHeaderLabels(['Key', 'Value'])

        for key, value in media_info.items():
            list_item = QTreeWidgetItem(self.ui.media_info)
            list_item.setText(0, str(key))
            list_item.setText(1, str(value))
            list_item.setToolTip(1, str(value))
            self.ui.media_info.setCurrentItem(list_item)
        #
        # text = (f'{item.media_type} | {item.media_length} | '
        #         f'<a href={os.path.split(item.media_path)[0]}><span style="color: #aecff7; ">{item.media_file}</span></a>')
        #
        # self.ui.lbl_media_info.setText(text)

    def playlist_icons_size(self, value):
        self.ui.playlist.setIconSize(QSize(value, value))

    def playlist_view_mode(self):
        if self.ui.btn_view_mode.isChecked():
            self.playlist_view_mode_list()
        else:
            self.playlist_view_mode_icons()

    def playlist_view_mode_list(self):
        self.ui.playlist.setViewMode(QListWidget.ViewMode.ListMode)
        self.ui.playlist.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.ui.playlist.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.ui.playlist.setWrapping(True)
        self.ui.spin_playlist_icons_size.setValue(50)

    def playlist_view_mode_icons(self):
        self.ui.playlist.setViewMode(QListWidget.ViewMode.IconMode)
        self.ui.playlist.setMovement(QListView.Movement.Free)
        self.ui.playlist.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.ui.playlist.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.ui.playlist.setWrapping(True)
        self.ui.spin_playlist_icons_size.setValue(200)

    def playlist_item_delete(self):
        item = self.ui.playlist.currentRow()
        self.ui.playlist.takeItem(item)

    def playlist_item_add(self):
        # TODO: put in thread

        jointypes = ' '.join(VIDEO_FILTER + AUDIO_FILTER + IMAGE_FILTER + DOCUMENT_FILTER)
        filetypes = (f"Supported files ({jointypes});;Video files ({' '.join(VIDEO_FILTER)});;"
                     f"Images({' '.join(IMAGE_FILTER)});;Audio files ({' '.join(AUDIO_FILTER)});;Document files ({' '.join(DOCUMENT_FILTER)});;All files(*)")

        file_dialog = QFileDialog(self)
        file_names = file_dialog.getOpenFileNames(self, "Open Media", QDir.homePath(), filetypes)

        def worker():
            for file in file_names[0]:
                if os.path.split(file)[-1] in [self.ui.playlist.item(i).media_file for i in
                                               range(self.ui.playlist.count())]:
                    # check if name already in playlist
                    print("File already in playlist!")
                else:
                    if os.path.exists(file):
                        item = Item()
                        filename, file_ext = os.path.splitext(file)

                        item.media_file = os.path.split(file)[-1]
                        item.media_path = file

                        file_supported = True

                        if '*' + file_ext.lower() in VIDEO_FILTER:
                            item.media_type = 'VIDEO'
                            item.media_length = self.playlist_get_media_length(file)
                            item.setIcon(self.playlist_create_thumbnail(file))

                        elif '*' + file_ext.lower() in AUDIO_FILTER:
                            item.media_type = 'AUDIO'
                            item.media_length = self.playlist_get_media_length(file)
                            item.setIcon(QPixmap(os.path.join(os.getcwd(), 'images', 'speakers.png')))

                        elif '*' + file_ext.lower() in IMAGE_FILTER:
                            item.media_type = 'IMAGE'
                            item.setIcon(QPixmap(file).scaledToHeight(200))

                        elif '*' + file_ext.lower() in DOCUMENT_FILTER:
                            item.media_type = 'DOCUMENT'
                            item.setIcon(QPixmap(file).scaledToHeight(200))

                        else:
                            item.media_type = 'NOT SUPPORTED'
                            try:
                                item.media_length = self.playlist_get_media_length(file)
                                item.setIcon(self.playlist_create_thumbnail(file))
                            except:
                                file_supported = False

                        if file_supported:
                            item.setText(item.media_file)
                            item.setFont(QFont("Tahoma", 12))
                            self.ui.playlist.addItem(item)
                        else:
                            print(f'{file} file not supported!')

        threading.Thread(target=worker()).run()

    def playlist_create_thumbnail(self, file):
        cap = cv2.VideoCapture(file)
        # frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
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
            self.video_screen_move(self.ui.list_screens.currentIndex())
        else:
            self.VIDEO_SCREEN.hide()

    def video_screen_get_screens(self):
        self.ui.list_screens.clear()
        count = len(QApplication.screens())
        for i in range(0, count):
            self.ui.list_screens.addItem(QApplication.screens()[i].name())

        self.ui.list_screens.setCurrentIndex(count - 1)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None
