from PyQt6.QtWidgets import QSizePolicy, QWidget
from PyQt6.QtGui import QImage, QPixmap, QBrush
from PyQt6.QtCore import QRect

from app.ui.playlist import Ui_Form
from app.classes.image import Image

class PlaylistWidget(QWidget):
    def __init__(self, id: int = 0, title: str = "Title", description: str = "Description", dop: str = "", parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__image = Image()

        #self.setFixedWidth(300)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum, QSizePolicy.ControlType.DefaultType))

        self.pixmapImage = None
        self.backgroundPalette = self.previewWidget.palette()
        self.backgroundBrush = self.backgroundPalette.brush(self.previewWidget.backgroundRole())

        self.id = int(id)
        self.ui.title.setText(title)
        self.ui.description.setText(description)
        self.ui.dop.setText(str(dop))

        self.setImageBackground(int(id))

    @property
    def previewWidget(self):
        return self.ui.verticalWidget
    
    def showEvent(self, a0):
        if self.pixmapImage != None:
            self.setBackgroundPalette(self.pixmapImage)
        return super().showEvent(a0)

    def resizeEvent(self, a0):
        if self.pixmapImage != None:
            self.setBackgroundPalette(self.pixmapImage)
        return super().resizeEvent(a0)
    
    def setImageBackground(self, id: int):
        image = QImage()
        image.loadFromData(self.__image.get_preview_playlist(id))

        self.pixmapImage = QPixmap(image)
        self.setBackgroundPalette(self.pixmapImage)

    def setBackgroundPalette(self, pixmap: QPixmap):
        scaledPixmap = self.transformBackgroundImage(pixmap, self.backgroundBrush)
        self.backgroundBrush.setTexture(scaledPixmap)
        self.backgroundPalette.setBrush(self.previewWidget.backgroundRole(), self.backgroundBrush)
        self.previewWidget.setPalette(self.backgroundPalette)

    def transformBackgroundImage(self, pixmap: QPixmap, brush: QBrush) -> QPixmap:
        sizeA = self.previewWidget.size()
        sizeB = pixmap.size()
        result = pixmap.copy()
        transform = brush.transform()

        scaleFactor = max(sizeA.width() / sizeB.width(), sizeA.height() / sizeB.height())
        transform = transform.scale(scaleFactor, scaleFactor)
        
        result = result.transformed(transform)
        sizeB = result.size()

        offsetX = max((sizeB.width() - sizeA.width()) // 2, 0)
        offsetY = max((sizeB.height() - sizeA.height()) // 2, 0)

        result = result.copy(QRect(offsetX, offsetY, sizeB.width() - offsetX, sizeB.height() - offsetY))

        #print(f"{offsetX=}, {offsetY=}, {scaleFactor=}")

        return result