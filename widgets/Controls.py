import os.path

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout, \
    QComboBox, QCheckBox, QListWidget, QListWidgetItem, QListView

from widgets.HelpDialog import HelpDialog


class Item(QListWidgetItem):
    def __init__(self):
        super().__init__()

        self.media_type = None
        self.media_length = None
        self.media_path = None
        self.media_file = None


class ControlsWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ControlsWidget, self).__init__()
        self.setWindowTitle("EMedia Controls")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'images', 'logo.png')))
        self.move(1, 1)
        self.setMinimumWidth(900)

        mainLayout = QVBoxLayout()

        self.btnHideVideoScreen = QPushButton('Show/Hide video screen')
        self.btnMoveToScreen = QPushButton('Move to')
        self.btnMoveToScreen.setIcon(qta.icon('fa5s.tv'))
        self.btnSaveList = QPushButton()
        self.btnSaveList.setIcon(qta.icon('fa5s.save'))
        self.btnHelp = QPushButton()
        self.btnHelp.setToolTip("Help")
        # self.btnHelp.setMinimumSize(40, 40)
        # self.btnHelp.setMaximumSize(40, 40)
        # self.btnHelp.setIconSize(QSize(30, 30))
        self.btnHelp.setIcon(qta.icon('fa5s.question'))
        self.playButton = QPushButton("Play")
        self.playButton.setIcon(qta.icon('fa5s.play'))
        # self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setIcon(qta.icon('fa5s.pause'))
        self.stopButton = QPushButton("Stop")
        self.stopButton.setIcon(qta.icon('fa5s.stop'))
        self.fullScreenButton = QPushButton("Fullscreen")
        self.fullScreenButton.setIcon(qta.icon('fa5s.expand-arrows-alt'))
        self.loop = QComboBox()
        self.loop.addItem("Loop None")
        self.loop.addItem("Loop Current")
        self.loop.addItem("Loop Playlist")
        self.loop.setCurrentIndex(0)
        self.allwaysOnTop = QCheckBox("Keep controls on top of other windows")
        self.playOnSelect = QCheckBox("Double click to load and play")
        # self.playOnSelect.setChecked(True)
        self.playOnFullscreen = QCheckBox("Play on Fullscreen pressed")
        self.playAll = QCheckBox("Play all")
        self.playlist = QListWidget()
        self.playlist.setIconSize(QSize(280, 150))
        self.playlist.setGridSize(QSize(290, 200))
        self.playlist.setSpacing(5)
        self.playlist.setMovement(QListView.Movement.Snap)
        # self.playlist.setSelectionMode(QListView.SelectionMode.NoSelection)
        self.playlist.setViewMode(QListWidget.ViewMode.IconMode)
        # self.playlist.setDragEnabled(True)
        # self.playlist.setAcceptDrops(True)
        # self.playlist.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.screenSelect = QComboBox()
        self.screenSelect.setToolTip("Select screen")
        self.btnUpdateScreens = QPushButton("Refresh")
        self.btnUpdateScreens.setIcon(qta.icon('fa5s.sync-alt'))
        self.openButton = QPushButton("Add Video")
        self.openButton.setIcon(qta.icon('fa5s.plus'))
        self.positionSlider = QSlider()
        self.positionSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        # stylesheet = "font-size: 20pt"
        self.mediaDuration = QLabel("0:00:00")
        self.mediaTimeLeft = QLabel("0:00:00")
        # self.mediaTimeLeft.setStyleSheet(stylesheet)
        self.mediaTimeCounter = QLabel("0:00:00")
        # self.mediaTimeCounter.setStyleSheet(stylesheet)

        self.btnDeleteItem = QPushButton('Delete')
        self.infoLabel = QLabel()
        self.infoLabel.setText("Double click on item to load media")
        self.infoLabel.setStyleSheet("color: blue;")

        self.helpDialog = HelpDialog()

        self.statusbar = QLabel()

        line0 = QHBoxLayout()
        line1 = QHBoxLayout()
        line2 = QHBoxLayout()
        line3 = QHBoxLayout()
        line4 = QHBoxLayout()
        line5 = QHBoxLayout()

        mainLayout.addLayout(line0)
        mainLayout.addLayout(line1)
        mainLayout.addLayout(line2)
        mainLayout.addLayout(line3)
        mainLayout.addWidget(self.statusbar)
        mainLayout.addLayout(line4, 1)
        mainLayout.addLayout(line5, 1)

        self.setLayout(mainLayout)

        line0.addWidget(self.openButton)
        line0.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # line0.addWidget(self.mediaTime, 1, QtCore.Qt.AlignCenter)
        line0.addWidget(self.btnSaveList)
        line0.addWidget(self.btnHelp)

        line1.addWidget(self.mediaTimeCounter)
        line1.addWidget(self.positionSlider, QtCore.Qt.AlignmentFlag.AlignCenter)
        line1.addWidget(self.mediaDuration)

        line2.addWidget(self.playButton)
        line2.addWidget(self.pauseButton)
        line2.addWidget(self.stopButton)
        line2.addWidget(self.loop)
        line2.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))
        line2.addWidget(self.btnHideVideoScreen)
        line2.addWidget(self.btnUpdateScreens)
        line2.addWidget(self.btnMoveToScreen)
        line2.addWidget(self.screenSelect)
        line2.addWidget(self.fullScreenButton)

        line3.addWidget(self.playOnSelect, 1)
        line3.addWidget(self.playOnFullscreen)

        line4.addWidget(self.playlist)

        line5.addWidget(self.btnDeleteItem)

        self.btnHelp.clicked.connect(self.helpDialog.show)
