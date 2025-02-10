from PyQt6.QtWidgets import QSizePolicy, QWidget, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap, QBrush, QPainter
from PyQt6.QtCore import QRect
import requests
from random import randint
from typing import Callable

from app.ui.playlist_widget import Ui_Form
from app.classes.image import Image

class PlaylistWidget(QWidget):
    def __init__(self, logo: QPixmap, id: int = 0, title: str = "Title", description: str = "Description", dop: str = "50", parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__image = Image()

        self.id = int(id)
        self.ui.title.setText(title)
        self.ui.description.setText(description)
        self.ui.dop.setText(str(dop))
        self.click_callback: Callable = None

        # url_image ={
        #     '1': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgOD0abk6GHTIRcOLItB1UnxDP8NtyACkMCA&s',
        #     '2': 'https://apprendre-la-photo.fr/wp-content/uploads/2015/09/stockholm.jpg',
        #     '3': 'https://i.pinimg.com/originals/13/be/95/13be95147b920e7c4ee958ff30db7a11.jpg',
        # }
        image = QImage()
        #image.loadFromData(requests.get(url_image[str(randint(1, 3))]).content)
        image.loadFromData(self.__image.get_preview_playlist(id))
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
        self.ui.logo_type_label.setPixmap(logo)

    def scale_components_under_image(self, width: int, height: int) -> None:
        self.ui.preview_widget.setMaximumSize(width, height)
        self.ui.preview_widget.setMinimumSize(width, height)
        self.ui.preview_widget.setBaseSize(width, height)

        self.ui.preview_label.setMaximumSize(width, height)
        self.ui.preview_label.setMinimumSize(width, height)
        self.ui.preview_label.setBaseSize(width, height)

    def mousePressEvent(self, a0):
        if self.click_callback:
            self.click_callback(self.id)
        return super().mousePressEvent(a0)