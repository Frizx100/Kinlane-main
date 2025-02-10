from PyQt6.QtWidgets import QSizePolicy, QWidget, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap, QBrush, QPainter
from PyQt6.QtCore import QRect
from typing import Callable

from app.ui.create_new_playlist_widget import Ui_Form
from app.classes.image import Image

class CreateNewPlaylistWidget(QWidget):
    def __init__(self, type: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__image = Image()

        self.ui.title.setText(type)
        self.type = type
        self.click_callback: Callable = None

        image = QImage()
        image.loadFromData(self.__image.get_icon_by_slug('add'))
        pixmap_image = QPixmap(image)

        height_image = pixmap_image.height()
        width_image = pixmap_image.width()
        recommended_height = 94
        recommended_width = int((recommended_height * width_image) / height_image)
        self.scale_components_under_image(recommended_width, recommended_height)

        # if height_image == width_image:
        #     self.scale_components_under_image(144, 144)
        # elif width_image > height_image:
        #     recommended_width = 256
        #     recommended_height = int((height_image * recommended_width) / width_image)
        #     self.scale_components_under_image(recommended_width, recommended_height)
        # else:
        #     recommended_height = 144
        #     recommended_width = int((recommended_height * width_image) / height_image)
        #     self.scale_components_under_image(recommended_width, recommended_height)

        self.ui.preview_label.setPixmap(QPixmap(image))
        self.ui.preview_label.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    def scale_components_under_image(self, width: int, height: int) -> None:
        self.ui.preview_label.setMaximumSize(width, height)
        self.ui.preview_label.setMinimumSize(width, height)
        self.ui.preview_label.setBaseSize(width, height)

    def mousePressEvent(self, a0):
        if self.click_callback:
            self.click_callback(self.type)
        return super().mousePressEvent(a0)