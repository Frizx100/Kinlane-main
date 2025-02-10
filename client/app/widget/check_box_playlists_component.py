from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from app.ui.check_box_playlists_component import Ui_Form

class CheckBoxPlaylists(QWidget):
    def __init__(self, id: int = 0, title: str = "Title", parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.__id = id

        self.ui.playlists.setText(title)

    def get_id(self):
        return self.__id
    
    def is_selected(self):
        return self.ui.playlists.isChecked()
    
    def permanently_set(self, value: bool):
        self.ui.playlists.setChecked(value)
        self.ui.playlists.setDisabled(True)