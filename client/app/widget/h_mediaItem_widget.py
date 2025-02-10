from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from app.ui.horizontal_mediaItem_widget import Ui_Form
from app.classes.image import Image

class HMediaItemWidget(QWidget):
    press_widget = pyqtSignal(int)
    def __init__(self, serial_index: int, id: int = 0, title: str = "Title", description: str = "", dop: str = "", parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__image = Image()

        self.id = int(id)
        self.ui.title.setText(title)
        self.serial_index = serial_index
        self.ui.number.setText(str(self.serial_index + 1))
        if description == '':
            self.ui.description.setText('Опис відсутній')
        else:    
            self.ui.description.setText(description)

        if dop == '':
            self.ui.widget.hide()
        else:
            self.ui.dop.setText(dop)

        image = QImage()
        image.loadFromData(self.__image.get_preview_mediaItem(id))
        pixmap_image = QPixmap(image)

        height_image = pixmap_image.height()
        width_image = pixmap_image.width()
        recommended_height = 94
        recommended_width = int((recommended_height * width_image) / height_image)
        self.scale_components_under_image(recommended_width, recommended_height)

        # if height_image == width_image:
        #     self.scale_components_under_image(94, 94)
        # elif width_image > height_image:
        #     # recommended_width = 168
        #     # recommended_height = int((height_image * recommended_width) / width_image)
        #     recommended_height = 94
        #     recommended_width = int((recommended_height * width_image) / height_image)
        #     self.scale_components_under_image(recommended_width, recommended_height)
        # else:
        #     recommended_height = 94
        #     recommended_width = int((recommended_height * width_image) / height_image)
        #     self.scale_components_under_image(recommended_width, recommended_height)
        
        self.ui.horizontalLayout_5.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ui.verticalLayout_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ui.preview.setPixmap(QPixmap(image))
        self.ui.preview.setScaledContents(True)

    def scale_components_under_image(self, width: int, height: int) -> None:
        self.ui.preview_widget.setMaximumSize(width, height)
        self.ui.preview_widget.setMinimumSize(width, height)
        self.ui.preview_widget.setBaseSize(width, height)

        self.ui.preview.setMaximumSize(width, height)
        self.ui.preview.setMinimumSize(width, height)
        self.ui.preview.setBaseSize(width, height)

    def get_id(self)->int:
        return self.id
    
    def mousePressEvent(self, a0):
        self.press_widget.emit(self.serial_index)
        return super().mousePressEvent(a0)