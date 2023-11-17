import threading

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class Player(QMediaPlayer):
    def __int__(self, video_screen):
        self.video_screen = video_screen
        self.audioOutput = QAudioOutput()

        self.audioOutput.setVolume(1.0)
        self.setAudioOutput(self.audioOutput)
        self.setVideoOutput(self.video_screen)

    def play_selected(self, file):
        thread = threading.Thread(target=self.setSource(file))
        thread.start()
        self.play()

