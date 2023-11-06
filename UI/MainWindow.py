# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QListWidgetItem, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from modules.Playlist import Playlist
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 791)
        MainWindow.setMinimumSize(QSize(1200, 600))
        self.verticalLayout_5 = QVBoxLayout(MainWindow)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.w_titlebar = QWidget(MainWindow)
        self.w_titlebar.setObjectName(u"w_titlebar")
        self.w_titlebar.setMinimumSize(QSize(0, 30))
        self.w_titlebar.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_5.addWidget(self.w_titlebar)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(5, 5, 20, 20)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(MainWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignLeft)

        self.list_loop = QComboBox(self.groupBox)
        self.list_loop.setObjectName(u"list_loop")
        self.list_loop.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.list_loop)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.chk_doubleclick_play = QCheckBox(self.groupBox)
        self.chk_doubleclick_play.setObjectName(u"chk_doubleclick_play")
        self.chk_doubleclick_play.setChecked(True)

        self.verticalLayout.addWidget(self.chk_doubleclick_play)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(MainWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_show_hide_screen = QPushButton(self.groupBox_2)
        self.btn_show_hide_screen.setObjectName(u"btn_show_hide_screen")

        self.horizontalLayout_4.addWidget(self.btn_show_hide_screen)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_reload_screens = QPushButton(self.groupBox_2)
        self.btn_reload_screens.setObjectName(u"btn_reload_screens")
        self.btn_reload_screens.setMinimumSize(QSize(30, 0))
        self.btn_reload_screens.setMaximumSize(QSize(30, 16777215))
        icon = QIcon()
        icon.addFile(u":/icons/refresh-ccw.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_reload_screens.setIcon(icon)
        self.btn_reload_screens.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.btn_reload_screens)

        self.list_screens = QComboBox(self.groupBox_2)
        self.list_screens.setObjectName(u"list_screens")

        self.horizontalLayout_3.addWidget(self.list_screens)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_fullscreen = QPushButton(self.groupBox_2)
        self.btn_fullscreen.setObjectName(u"btn_fullscreen")
        icon1 = QIcon()
        icon1.addFile(u":/icons/move.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_fullscreen.setIcon(icon1)
        self.btn_fullscreen.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.btn_fullscreen)

        self.chk_play_on_fullscreen = QCheckBox(self.groupBox_2)
        self.chk_play_on_fullscreen.setObjectName(u"chk_play_on_fullscreen")

        self.horizontalLayout_5.addWidget(self.chk_play_on_fullscreen)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(MainWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.btn_view_mode = QPushButton(self.groupBox_3)
        self.btn_view_mode.setObjectName(u"btn_view_mode")
        self.btn_view_mode.setMinimumSize(QSize(0, 30))
        self.btn_view_mode.setCheckable(True)

        self.verticalLayout_6.addWidget(self.btn_view_mode, 0, Qt.AlignRight)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_10.addWidget(self.label_2)

        self.spin_playlist_icons_size = QSpinBox(self.groupBox_3)
        self.spin_playlist_icons_size.setObjectName(u"spin_playlist_icons_size")
        self.spin_playlist_icons_size.setMinimum(50)
        self.spin_playlist_icons_size.setMaximum(320)
        self.spin_playlist_icons_size.setSingleStep(5)
        self.spin_playlist_icons_size.setValue(50)

        self.horizontalLayout_10.addWidget(self.spin_playlist_icons_size)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_8.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_3 = QLabel(MainWindow)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_11.addWidget(self.label_3)

        self.lbl_current_media = QLabel(MainWindow)
        self.lbl_current_media.setObjectName(u"lbl_current_media")

        self.horizontalLayout_11.addWidget(self.lbl_current_media)

        self.horizontalLayout_11.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lbl_current_time = QLabel(MainWindow)
        self.lbl_current_time.setObjectName(u"lbl_current_time")

        self.horizontalLayout_7.addWidget(self.lbl_current_time)

        self.slider_progress = QSlider(MainWindow)
        self.slider_progress.setObjectName(u"slider_progress")
        self.slider_progress.setMinimumSize(QSize(600, 0))
        self.slider_progress.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.slider_progress)

        self.lbl_total_time = QLabel(MainWindow)
        self.lbl_total_time.setObjectName(u"lbl_total_time")

        self.horizontalLayout_7.addWidget(self.lbl_total_time)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.btn_play = QPushButton(MainWindow)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setMinimumSize(QSize(50, 50))
        icon2 = QIcon()
        icon2.addFile(u":/icons/play-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_play.setIcon(icon2)
        self.btn_play.setIconSize(QSize(36, 36))

        self.horizontalLayout.addWidget(self.btn_play)

        self.btn_pause = QPushButton(MainWindow)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setMinimumSize(QSize(50, 50))
        icon3 = QIcon()
        icon3.addFile(u":/icons/pause-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_pause.setIcon(icon3)
        self.btn_pause.setIconSize(QSize(36, 36))

        self.horizontalLayout.addWidget(self.btn_pause)

        self.btn_stop = QPushButton(MainWindow)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setMinimumSize(QSize(50, 50))
        icon4 = QIcon()
        icon4.addFile(u":/icons/stop-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_stop.setIcon(icon4)
        self.btn_stop.setIconSize(QSize(36, 36))

        self.horizontalLayout.addWidget(self.btn_stop)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.playlist = Playlist(MainWindow)
        self.playlist.setObjectName(u"playlist")
        self.playlist.setSortingEnabled(False)

        self.verticalLayout_4.addWidget(self.playlist)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.lbl_media_info = QLabel(MainWindow)
        self.lbl_media_info.setObjectName(u"lbl_media_info")
        self.lbl_media_info.setMinimumSize(QSize(100, 0))
        palette = QPalette()
        brush = QBrush(QColor(174, 207, 247, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Link, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush)
        self.lbl_media_info.setPalette(palette)
        self.lbl_media_info.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.lbl_media_info)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.btn_playlist_add = QPushButton(MainWindow)
        self.btn_playlist_add.setObjectName(u"btn_playlist_add")
        self.btn_playlist_add.setMinimumSize(QSize(0, 30))
        self.btn_playlist_add.setIconSize(QSize(24, 24))

        self.horizontalLayout_6.addWidget(self.btn_playlist_add)

        self.btn_playlist_del = QPushButton(MainWindow)
        self.btn_playlist_del.setObjectName(u"btn_playlist_del")
        self.btn_playlist_del.setMinimumSize(QSize(0, 30))
        self.btn_playlist_del.setIconSize(QSize(24, 24))

        self.horizontalLayout_6.addWidget(self.btn_playlist_del)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.horizontalLayout_8.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EMedia", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Player control", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.chk_doubleclick_play.setText(QCoreApplication.translate("MainWindow", u"Doubleclick to play", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Screen", None))
        self.btn_show_hide_screen.setText(QCoreApplication.translate("MainWindow", u"Show/Hide screen", None))
        self.btn_reload_screens.setText("")
        self.btn_fullscreen.setText(QCoreApplication.translate("MainWindow", u"Fullscreen", None))
        self.chk_play_on_fullscreen.setText(QCoreApplication.translate("MainWindow", u"Play on fullscreen", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Playlist", None))
        self.btn_view_mode.setText(QCoreApplication.translate("MainWindow", u"List", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Icons size", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Current media", None))
        self.lbl_current_media.setText("")
        self.lbl_current_time.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.lbl_total_time.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.btn_play.setText("")
        self.btn_pause.setText("")
        self.btn_stop.setText("")
        self.btn_playlist_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btn_playlist_del.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi
