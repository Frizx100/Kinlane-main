import os
from PyQt6.QtWidgets import QDialog, QFileDialog

from app.ui.add_new_mediaItem_dialog_window import Ui_Form
from app.windows.select_playlists_dialog_window import SelectPlaylist
from app.classes.mediaItem import MediaItem
from app.classes.user import User

class AddNewMediaItemWidget(QDialog):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setModal(True)
        self.mediaItem = MediaItem()
        self.user: User = user
        self.select_playlist_user = []
        self.is_disable_element(True)
        self.hide_error()

        callBacks = (
            (self.ui.select_file, self.select_file),
            (self.ui.save, self.save),
            (self.ui.cancel, self.close),
            (self.ui.select_playlist, self.select_playlist)
        )
        for callback in callBacks:
            callback[0].clicked.connect(callback[1])
    
    def select_file(self):
        supported_formats = ''
        supported_formats_list = self.mediaItem.get_supported_formats()
        all_supported_formats = ''
        for format in supported_formats_list:
            buf = ''
            for item in format[3].split():
                buf += '*.' + item + ' '
            all_supported_formats += buf
            supported_formats += format[1] + ' (' + buf + ');;'
        supported_formats = 'All (' + all_supported_formats + ');;' + supported_formats[:-2]

        #self.file = QFileDialog.getOpenFileName(self, "Виберіть файл", '',"All(*.png *.jpg *.jpeg *.mp4 *.flv *.ts *.mts *.avi *.ape *.mp3);;Images (*.png *.jpg *.jpeg);;Video (*.mp4 *.flv *.ts *.mts *.avi);;Music (*.ape *.mp3)")
        self.file = QFileDialog.getOpenFileName(self, "Виберіть файл", '',supported_formats)
        if self.file[0] != '':
            file_name = os.path.basename(self.file[0])
            self.ui.file_name.setText(file_name)
            self.ui.title.setPlaceholderText(file_name)
            self.is_disable_element(False)
        else:
            self.error('Виберіть файл!')
            self.is_disable_element(True)

    def is_disable_element(self, status: bool)->None:
        for item in (self.ui.save, self.ui.label_2, self.ui.title, self.ui.label_3, self.ui.description, self.ui.select_playlist):
            item.setDisabled(status)
    
    def error(self, message: str)->None:
        self.ui.error_label.setText(message)
        self.ui.error_label.show()

    def hide_error(self)->None:
        self.ui.error_label.hide()

    def save(self):
        file_path = self.file[0]
        file_type = self.mediaItem.check_type(file_path)
        if file_type['status']:
            title = self.get_title()
            description = self.ui.description.toPlainText()
            #print(f'file: {file_path}\ntitle: {title}\ndescription: {description}\nfile_type: {file_type['slug_format']}')
            self.user.upload_mediaItem(file_path, self.select_playlist_user, file_type['slug_format'], title, description)
            self.close()
        else:
            self.error(file_type['description'])

    def get_title(self)->str:
        if self.ui.title.text() == '':
            return os.path.basename(self.file[0])
        else:
            return self.ui.title.text()

    def select_playlist(self):
        file_path = self.file[0]
        file_type = self.mediaItem.check_type(file_path)
        if file_type['status']:
                all_playlists: list = self.user.get_all_playlists_type(file_type['slug_format'])

                supported_formats = self.mediaItem.get_supported_formats()
                reserved_name = []
                for format in supported_formats:
                    reserved_name.append(format[1])

                select_playlist_window: SelectPlaylist = SelectPlaylist(all_playlists, reserved_name)
                select_playlist_window.show()
                select_playlist_window.close_callback = self.get_selected_playlists
        else:
            self.error(file_type['description'])

    def get_selected_playlists(self, window: SelectPlaylist):
        self.select_playlist_user = window.get_selected_playlist_id()