import os
from PyQt6.QtWidgets import QDialog, QFileDialog
from typing import Callable

from app.ui.add_new_playlist_dialog_window import Ui_Form
from app.classes.user import User
from app.classes.image import Image

class AddNewPlaylistWidget(QDialog):
    def __init__(self, user: User, type: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setModal(True)
        self.user: User = user
        self.image: Image = Image()
        self.type = type
        self.file = None
        self.create_callback: Callable = None
        self.ui.title.textEdited.connect(self.create_disabled)
        self.ui.create.setDisabled(True)
        self.hide_error()

        callBacks = (
            (self.ui.select_file, self.select_file),
            (self.ui.cancel, self.close),
            (self.ui.create, self.save),
        )
        for callback in callBacks:
            callback[0].clicked.connect(callback[1])
    
    def select_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Виберіть файл", '',"Images (*.png *.jpg *.jpeg)")
        if self.file[0] != '':
            self.ui.file_name.setText(os.path.basename(self.file[0]))
        else:
            self.error('Виберіть файл!')
    
    def error(self, message: str)->None:
        self.ui.error_label.setText(message)
        self.ui.error_label.show()

    def hide_error(self)->None:
        self.ui.error_label.hide()

    def create_disabled(self):
        if len(self.ui.title.text()) > 0:
            self.ui.create.setDisabled(False)
        else:
            self.ui.create.setDisabled(True)

    def save(self):
        if len(self.ui.title.text()) == 0:
            self.error('Дайте назву плейлисту.')
        else:
            title = self.ui.title.text()
            description = self.ui.description.toPlainText()
            if (self.file != None) and os.path.isfile(self.file[0]):
                file_path = self.file[0]
                self.user.create_playlist(title, description, self.type, file_path)
            else:
                self.user.create_playlist(title, description, self.type, '')

        if self.create_callback:
            self.create_callback(self.type)
        self.close()

    