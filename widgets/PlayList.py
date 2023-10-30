import sys

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QMainWindow, QPushButton, QFileDialog, QWidget
from PySide6.QtCore import Qt
import cv2

class VideoThumbnailApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Создание Thumbnail")
        self.setGeometry(100, 100, 400, 200)

        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Выбрать видео", self)
        self.select_button.clicked.connect(self.selectVideo)

        self.create_button = QPushButton("Создать Thumbnail", self)
        self.create_button.clicked.connect(self.createThumbnail)

        layout = QVBoxLayout()
        layout.addWidget(self.thumbnail_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.create_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def selectVideo(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi *.mkv);;All Files (*)", options=options)

        if file_path:
            self.video_path = file_path

    def createThumbnail(self):
        if hasattr(self, 'video_path'):
            cap = cv2.VideoCapture(self.video_path)
            ret, frame = cap.read()
            if ret:
                # Преобразуем кадр в RGB и масштабируем
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                # Уменьшаем изображение до размера миниатюры
                thumbnail = pixmap.scaled(320, 240, Qt.AspectRatioMode.KeepAspectRatio)

                # Отображаем миниатюру
                self.thumbnail_label.setPixmap(thumbnail)

            cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoThumbnailApp()
    ex.show()
    sys.exit(app.exec())
