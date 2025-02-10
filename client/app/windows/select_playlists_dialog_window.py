from PyQt6.QtWidgets import QDialog

from app.ui.select_playlists_dialog_window import Ui_Form
from app.widget.check_box_playlists_component import CheckBoxPlaylists

from typing import Callable

class SelectPlaylist(QDialog):
    def __init__(self, all_playlists: list, reserved_name: list, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.close)

        self.close_callback: Callable = None

        self.all_playlists_widget: list[CheckBoxPlaylists] = []
        self.selected_playlist = []
        for item in all_playlists:
            child_widget: CheckBoxPlaylists = CheckBoxPlaylists(item[0], item[1]) 
            if item[1] in reserved_name:
                child_widget.permanently_set(True)

            self.ui.vl_playlists.addWidget(child_widget)
            self.all_playlists_widget.append(child_widget)
        
    def get_selected_playlist_id(self)->list[str]:
        return self.selected_playlist
    
    def closeEvent(self, a0):
        for item in self.all_playlists_widget:
            if item.is_selected():
                self.selected_playlist.append(str(item.get_id()))

        if self.close_callback:
            self.close_callback(self)
        return super().closeEvent(a0)