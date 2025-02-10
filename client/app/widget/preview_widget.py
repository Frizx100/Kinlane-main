from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLayout, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QPixmap, QPainter, QFont, QImage
from PyQt6.QtCore import Qt


class PreviewWidget(QWidget):
    def __init__(self, q_image_preview: QImage,  dop: str = '', parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.image_pixmap = QPixmap(q_image_preview)  # Load image
        
        if dop != '':
            # Create dop label
            self.dop_label = QLabel(dop, self)
            #self.dop_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
            self.dop_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
            self.dop_label.setStyleSheet("color: white; background: rgba(0, 0, 0, 100); padding: 5px;")
            self.dop_label.setFont(QFont("Arial", 12))

            self.h_layout = QHBoxLayout()
            spacerItem = QSpacerItem(5, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.h_layout.addItem(spacerItem)
            self.h_layout.addWidget(self.dop_label)

            # Layout for labels
            self.layout: QLayout = QVBoxLayout(self)
            self.layout.addStretch()  # Pushes title up
            self.layout.addLayout(self.h_layout)
            self.layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins for better spacing

    def paintEvent(self, event):
        """Custom paint event to draw the image as a background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if not self.image_pixmap.isNull():
            # Scale image proportionally to fit the widget
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x_offset = (self.width() - scaled_pixmap.width()) // 2
            y_offset = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)

    def set_minimum_size(self, min_w: int, min_h: int) -> None:
        self.setMinimumSize(min_w, min_h)