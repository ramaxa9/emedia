from PySide6.QtWidgets import QListWidgetItem


class Item(QListWidgetItem):
    def __init__(self):
        super().__init__()

        self.media_type = None
        self.media_length = None
        self.media_path = None
        self.media_file = None
