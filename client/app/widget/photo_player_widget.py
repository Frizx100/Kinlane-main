from PyQt6.QtWidgets import QWidget, QLayoutItem
from PyQt6.QtGui import QImage, QKeySequence, QShortcut
from PyQt6.QtCore import pyqtSignal

from app.widget.preview_widget import PreviewWidget

from app.ui.photo_player_widget import Ui_Form
from app.classes.mediaItem import MediaItem

class PhotoPlayerWidget(QWidget):

    next_signal = pyqtSignal()
    previous_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.mediaItem = MediaItem() 
        #### binds ####
        self.shortcut = QShortcut(QKeySequence("n"), self)
        self.shortcut.activated.connect(self.next_signal.emit)
        self.shortcut = QShortcut(QKeySequence("p"), self)
        self.shortcut.activated.connect(self.previous_signal.emit)

    def set_id_mediaItem(self, id: int):
        self.id = id
        photo = QImage()
        photo.loadFromData(self.mediaItem.get_preview_mediaItem(self.id))

        while self.ui.box.count() > 0:
            child: QLayoutItem = self.ui.box.takeAt(0)
            child.widget().deleteLater()

        child = PreviewWidget(q_image_preview=photo)
        self.ui.box.addWidget(child)


    def stop_player(self):
        pass