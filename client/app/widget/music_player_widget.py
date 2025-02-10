from PyQt6.QtWidgets import QWidget, QLayoutItem
from PyQt6.QtGui import QImage, QPixmap, QIcon, QKeySequence, QShortcut
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl, QTime, pyqtSignal

from app.widget.preview_widget import PreviewWidget

from app.ui.music_player_widget import Ui_Form
from app.classes.image import Image
from app.classes.mediaItem import MediaItem

class MusicPlayerWidget(QWidget):

    next_signal = pyqtSignal()
    previous_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.image_class = Image()
        self.mediaItem = MediaItem()

        self.media_player = QMediaPlayer()
        #self.media_player.mediaStatusChanged.connect(self.printMediaData)
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.25)
        self.media_player.setAudioOutput(self.audio_output)
        self.fullscreen = False
        self.in_widget = True

        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        constant_values: tuple = (
            (self.ui.btn_play_pause, 'play'),
            (self.ui.btn_previous, 'previous'),
            (self.ui.btn_next, 'next')
        )
        icons = QImage()
        for items in constant_values:
            icons.loadFromData(self.image_class.get_icon_by_slug(items[1]))
            items[0].setIcon(QIcon(QPixmap(icons)))
        icons.loadFromData(self.image_class.get_icon_by_slug('volume'))
        self.ui.lbl_volume.setPixmap(QPixmap(icons))

        self.ui.position_slider.sliderMoved.connect(self.set_position)
        self.ui.position_slider.sliderPressed.connect(self.change_position)
        self.ui.volume_slider.setValue(25)
        self.ui.volume_slider.valueChanged.connect(self.set_volume)

        self.ui.btn_play_pause.clicked.connect(self.play)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_previous.clicked.connect(self.previous)

        #### binds ####
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence("n"), self)
        self.shortcut.activated.connect(self.next)
        self.shortcut = QShortcut(QKeySequence("p"), self)
        self.shortcut.activated.connect(self.previous)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcut.activated.connect(self.forward_slider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.shortcut.activated.connect(self.back_slider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        self.shortcut.activated.connect(self.volume_up)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        self.shortcut.activated.connect(self.volume_down)

    def set_id_mediaItem(self, id: int):
        self.id = id
        url_video = self.mediaItem.get_url_video()
        self.media_player.setSource(QUrl(f'{url_video}{id}'))
        self.set_preview()

    def stop_player(self):
        self.media_player.pause()

    def next(self):
        self.next_signal.emit()

    def previous(self):
        self.previous_signal.emit()

    def set_preview(self):
        preview = QImage()
        preview.loadFromData(self.mediaItem.get_preview_mediaItem(self.id))
        
        while self.ui.box.count() > 0:
            child: QLayoutItem = self.ui.box.takeAt(0)
            child.widget().deleteLater()

        child = PreviewWidget(q_image_preview=preview)
        self.ui.box.addWidget(child)

    def get_icon(self, slug: str)->QImage:
        icons = QImage()
        icons.loadFromData(self.image_class.get_icon_by_slug(slug))
        return icons

    def play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            icons = self.get_icon('play')
            self.media_player.pause()
        else:
            icons = self.get_icon('pause')
            self.media_player.play()
        self.ui.btn_play_pause.setIcon(QIcon(QPixmap(icons)))
    
    def position_changed(self, position):
        self.ui.position_slider.setValue(position)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.media_player.position())
        self.ui.current_position.setText(mtime.toString())
        
    def duration_changed(self, duration):
        self.ui.position_slider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.media_player.duration())
        self.ui.total_time.setText(mtime.toString())

    def set_position(self, position):
        self.change_position()

    def change_position(self):
        self.media_player.setPosition(self.ui.position_slider.value())

    def set_volume(self, value):
        self.audio_output.setVolume(value/100)
    
    def forward_slider(self):
        self.media_player.setPosition(self.media_player.position() + 1000 * 10) #1000*60)

    def back_slider(self):
        self.media_player.setPosition(self.media_player.position() - 1000 * 10)
        
    def volume_up(self):
        self.ui.volume_slider.setValue(self.ui.volume_slider.value() + 5)
    
    def volume_down(self):
        self.ui.volume_slider.setValue(self.ui.volume_slider.value() - 5)