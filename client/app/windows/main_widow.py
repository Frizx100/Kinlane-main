from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QLayoutItem, QLayout
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtCore import Qt


from app.ui.main_widow import Ui_MainWindow

from app.widget.playlist_widget import PlaylistWidget
from app.widget.create_new_playlist_widget import CreateNewPlaylistWidget
from app.widget.flow_layout import FlowLayout
from app.widget.h_mediaItem_widget import HMediaItemWidget

from app.widget.photo_player_widget import PhotoPlayerWidget
from app.widget.video_player_widget import VideoPlayerWidget
from app.widget.music_player_widget import MusicPlayerWidget

from app.windows.add_new_mediaItem_dialog_window import AddNewMediaItemWidget
from app.windows.add_new_playlist_dialog_window import AddNewPlaylistWidget

from app.classes.user import User
from app.classes.image import Image
from app.classes.mediaItem import MediaItem

class MainApplicationGUI(QMainWindow):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.__mediaItem = MediaItem()
        self.__image = Image()
        self.__user: User = user
        self.player = None

        callBacks = (
            (self.ui.add_new_mediaItem, self.add_new_mediaItem),
            (self.ui.m_pb_history, lambda: self.tab_all_playlist_type('history')),
            (self.ui.m_pb_photo, lambda: self.tab_all_playlist_type('photo')),
            (self.ui.m_pb_video, lambda: self.tab_all_playlist_type('video')),
            (self.ui.m_pb_music, lambda: self.tab_all_playlist_type('music')),
        )
        for callback in callBacks:
            callback[0].clicked.connect(callback[1])

        self.ui.tabWidget.currentChanged.connect(self.tab_changed)

        icons = QImage()
        icon_pixmap = QPixmap()
        icons_from_btn =(
            ('photo', self.ui.m_pb_photo),
            ('video', self.ui.m_pb_video),
            ('music', self.ui.m_pb_music),
            ('history', self.ui.m_pb_history),
            ('add', self.ui.add_new_mediaItem)
        )
        for item in icons_from_btn:
            icons.loadFromData(self.__image.get_icon_by_slug(item[0]))
            icon_pixmap.convertFromImage(icons)
            item[1].setIcon(QIcon(icon_pixmap))

        self.ui.verticalLayout_9.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.main_window()

    def main_window(self):
        self.ui.tabWidget.setCurrentIndex(0)

        icons = QImage()
        icons.loadFromData(self.__image.get_icon_by_slug('history'))
        icon_pixmap = QPixmap(icons)
        self.ui.th_history_icon.setPixmap(icon_pixmap)
        self.ui.m_pb_history.setIcon(QIcon(icon_pixmap))

        constant_values: tuple[tuple[str, QLabel, QHBoxLayout]] = (
            ('photo', self.ui.th_photo_icon, self.ui.hl_photo),
            ('video', self.ui.th_video_icon, self.ui.hl_video),
            ('music', self.ui.th_music_icon, self.ui.hl_music)
        )
        for constant_item in constant_values:
            icons.loadFromData(self.__image.get_icon_by_slug(constant_item[0]))
            icon_pixmap.convertFromImage(icons)
            constant_item[1].setPixmap(icon_pixmap)
            for item in self.__user.get_all_playlists_type(constant_item[0]):
                playlists_widget = PlaylistWidget(logo=icon_pixmap, 
                                                  id=item[0], 
                                                  title=item[1], 
                                                  description=item[2], 
                                                  dop=item[3])
                constant_item[2].addWidget(playlists_widget)
                playlists_widget.click_callback = self.show_playlist_content
            constant_item[2].addStretch()

    def remove_all_widgets(self, layout: QLayout):
        while layout.count() > 0:
            child: QLayoutItem = layout.takeAt(0)
            child.widget().deleteLater()

    def tab_all_playlist_type(self, slug: str):
        if self.ui.vl_all_playlist_type.itemAt(0) != None and isinstance(self.ui.vl_all_playlist_type.itemAt(0), FlowLayout):
            flow_layout: FlowLayout = self.ui.vl_all_playlist_type.itemAt(0)
            self.remove_all_widgets(flow_layout)
        else:
            flow_layout = FlowLayout()
            self.ui.vl_all_playlist_type.addLayout(flow_layout)
        self.ui.tabWidget.setCurrentIndex(1)

        create_new_playlist = CreateNewPlaylistWidget(type=slug)
        flow_layout.addWidget(create_new_playlist)
        # connecting click callback for widget, which will create new
        # playlist. Connect is not implemented and we using callbacks instead
        create_new_playlist.click_callback = self.add_new_playlist
        icons = QImage()
        icons.loadFromData(self.__image.get_icon_by_slug(slug))
        icon_pixmap = QPixmap(icons)

        playlists = self.__user.get_all_playlists_type(slug)
        for item in playlists:
            playlists_widget = PlaylistWidget(logo=icon_pixmap, 
                                              id=item[0], 
                                              title=item[1], 
                                              description=item[2], 
                                              dop=item[3])
            flow_layout.layout().addWidget(playlists_widget)
            playlists_widget.click_callback = self.show_playlist_content

    def add_new_mediaItem(self):
        self.add_new_mediaItem_window = AddNewMediaItemWidget(self.__user)
        self.add_new_mediaItem_window.show()

    def add_new_playlist(self, type: str):
        self.add_new_playlist_window = AddNewPlaylistWidget(self.__user, type)
        self.add_new_playlist_window.create_callback = self.tab_all_playlist_type
        self.add_new_playlist_window.show()

    def set_active_mediaItem_by_index(self, index: int):
        id = self.ui.vl_view_container.itemAt(index).widget().get_id()
        self.player.set_id_mediaItem(id)
        self.active_index_mediaItem = index
        info_mediaItem = self.__mediaItem.get_info_mediaItem(id)
        self.ui.view_title_mediaItem.setText(info_mediaItem['title'])
        self.ui.view_description_mediaItem.setText(info_mediaItem['description'])
        time = info_mediaItem['date']
        self.ui.view_data_mediaItem.setText(f'{time[3:5]}.{time[0:2]}.{time[6:10]} {time[11:13]}:{time[14:16]}:{time[17:]}')

    def next_mediaItem(self):
        promising_active_mediaItem = self.active_index_mediaItem + 1
        if promising_active_mediaItem >= self.ui.vl_view_container.count():
            self.set_active_mediaItem_by_index(0)
        else:
            self.set_active_mediaItem_by_index(promising_active_mediaItem)

    def previous_mediaItem(self):
        promising_active_mediaItem = self.active_index_mediaItem - 1
        if promising_active_mediaItem < 0:
            self.set_active_mediaItem_by_index(self.ui.vl_view_container.count() - 1)
        else:
            self.set_active_mediaItem_by_index(promising_active_mediaItem)

    def show_playlist_content(self, id_play_list: int):
        self.remove_all_widgets(self.ui.view_player_mediaItem_gl)
        self.remove_all_widgets(self.ui.vl_view_container)

        info_playlist = self.__user.get_info_playlist_by_id(id_play_list)
        content_playlist = self.__user.get_content_playlist_by_id(id_play_list)
        
        self.ui.view_title.setText(info_playlist['title'])
        serial_index = 0
        for mediaItem in content_playlist:
            child_widget = HMediaItemWidget(serial_index=serial_index, id=mediaItem[0], title=mediaItem[1], description=mediaItem[2])
            self.ui.vl_view_container.addWidget(child_widget)
            child_widget.press_widget.connect(self.set_active_mediaItem_by_index)
            serial_index += 1

        player_types = {
            'photo': PhotoPlayerWidget,
            'video': VideoPlayerWidget,
            'music': MusicPlayerWidget
        }
        self.player = player_types[info_playlist['slug_format']]()
        self.player.next_signal.connect(self.next_mediaItem)
        self.player.previous_signal.connect(self.previous_mediaItem)
        self.ui.view_player_mediaItem_gl.addWidget(self.player, 0, 0)
        self.set_active_mediaItem_by_index(0)

        self.ui.tabWidget.setCurrentIndex(2)

    def tab_changed(self, index: int):
        if self.player != None and index != 2:
            self.player.stop_player()