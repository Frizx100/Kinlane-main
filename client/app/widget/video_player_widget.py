from PyQt6.QtGui import QKeySequence, QIcon, QShortcut, QImage, QPixmap, QCursor
from PyQt6.QtCore import Qt, QUrl, QTime, QTimer, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QWidget, QApplication


from app.ui.video_player_widget import Ui_Form
from app.classes.image import Image
from app.classes.mediaItem import MediaItem


class VideoPlayerWidget(QWidget):

    next_signal = pyqtSignal()
    previous_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(VideoPlayerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.image_class = Image()
        self.mediaItem = MediaItem()
        self.ui.video_widget.children()[0].setMouseTracking(True)

        self.media_player = QMediaPlayer()
        #self.media_player.mediaStatusChanged.connect(self.printMediaData)
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.4)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.ui.video_widget)
        self.is_fullscreen = False

        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        constant_values: tuple = (
            (self.ui.btn_play_pause, 'play'),
            (self.ui.btn_full_screen, 'full_screen'),
            (self.ui.btn_previous, 'previous'),
            (self.ui.btn_next, 'next')
        )
        icons = QImage()
        for items in constant_values:
            icons.loadFromData(self.image_class.get_icon_by_slug(items[1]))
            items[0].setIcon(QIcon(QPixmap(icons)))

        self.ui.position_slider.sliderMoved.connect(self.set_position)
        self.ui.position_slider.sliderPressed.connect(self.change_position)
        self.ui.volume_slider.setValue(40)
        self.ui.volume_slider.valueChanged.connect(self.set_volume)

        self.ui.btn_play_pause.clicked.connect(self.play)
        self.ui.btn_full_screen.clicked.connect(self.handle_fullscreen)
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_previous.clicked.connect(self.previous)

        #### binds ####
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.handle_fullscreen)
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

        self.last_mouse_position = QCursor.pos()
        self.visibility_cursor = True
        self.mouse_inside = False  # Track if the mouse is inside the custom widget

        # Create a QTimer to track mouse inactivity
        self.cursor_timer = QTimer(self)
        self.cursor_timer.setInterval(5000) # 5 seconds
        self.cursor_timer.timeout.connect(self.hide_cursor)

        self.timer = QTimer(self)
        self.timer.setInterval(50)  
        self.timer.timeout.connect(self.checkMouse)
        self.timer.start()

    def set_id_mediaItem(self, id: int):
        self.id = id
        url_video = self.mediaItem.get_url_video()
        icons = self.get_icon('play')
        self.ui.btn_play_pause.setIcon(QIcon(QPixmap(icons)))
        self.media_player.setSource(QUrl(f'{url_video}{id}'))

    def stop_player(self):
        self.media_player.stop()

    def next(self):
        self.next_signal.emit()

    def previous(self):
        self.previous_signal.emit()

    def get_icon(self, slug: str)->QImage:
        icons = QImage()
        icons.loadFromData(self.image_class.get_icon_by_slug(slug))
        return icons
    
    def mouseDoubleClickEvent(self, event):
        self.handle_fullscreen()

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

    def handle_fullscreen(self):
        # self.ui.video_widget.setFullScreen(not self.ui.video_widget.isFullScreen())
        if self.ui.verticalWidget.isFullScreen():
            self.ui.verticalWidget.setWindowFlags(Qt.WindowType.WindowTitleHint|Qt.WindowType.WindowSystemMenuHint|Qt.WindowType.WindowMinimizeButtonHint|Qt.WindowType.WindowMaximizeButtonHint|Qt.WindowType.WindowCloseButtonHint|Qt.WindowType.WindowFullscreenButtonHint)
            self.ui.verticalWidget.setWindowState(Qt.WindowState.WindowNoState)
            self.ui.verticalWidget.showNormal()
            icons = self.get_icon('full_screen')
        else:
            print(f"{Qt.WindowType(self.ui.verticalWidget.windowFlags()).name}, {self.ui.verticalWidget.windowState()}")
            self.ui.verticalWidget.setWindowFlag(Qt.WindowType.CoverWindow)
            self.ui.verticalWidget.show()
            self.ui.verticalWidget.setWindowState(Qt.WindowState.WindowFullScreen)
            icons = self.get_icon('minimize')
        self.ui.btn_full_screen.setIcon(QIcon(QPixmap(icons)))

    def show_controls(self, switch: bool):    
        if switch and self.visibility_cursor and self.mouse_inside:
            self.ui.position_slider.show()
            self.ui.control_widget.show()
        else:
            self.ui.position_slider.hide()
            self.ui.control_widget.hide()
    
    def forward_slider(self):
        self.media_player.setPosition(self.media_player.position() + 1000 * 10) #1000*60)

    def back_slider(self):
        self.media_player.setPosition(self.media_player.position() - 1000 * 10)
        
    def volume_up(self):
        self.ui.volume_slider.setValue(self.ui.volume_slider.value() + 5)
    
    def volume_down(self):
        self.ui.volume_slider.setValue(self.ui.volume_slider.value() - 5)

    def checkMouse(self):
        widgetPosition = self.mapToGlobal(self.ui.verticalWidget.pos()) 
        mousePosition = QCursor.pos()

        x = widgetPosition.x()
        y = widgetPosition.y()
        width = x + self.ui.verticalWidget.size().width()
        height = y + self.ui.verticalWidget.size().height()

        if (mousePosition.x() > x and mousePosition.y() > y and mousePosition.x() < width and mousePosition.y() < height):
            self.mouse_inside = True
            self.show_controls(True)
            # print(f"Mouse is inside! {mousePosition}")
        else:
            self.mouse_inside = False
            self.show_controls(False)
            # print(f"Mouse is outside! {mousePosition}")

        if mousePosition != self.last_mouse_position:
            self.restore_cursor()

        self.last_mouse_position = mousePosition
        self.timer.start()

    def hide_cursor(self):
        # Hide the cursor after 5 seconds of inactivity
        if self.mouse_inside:
            self.visibility_cursor = False
            self.show_controls(False)
            QApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)

    def restore_cursor(self):
        # Restore the cursor when the mouse moves
        self.visibility_cursor = True
        self.show_controls(True)
        QApplication.restoreOverrideCursor()
        self.cursor_timer.start()  # Restart the timer

    def getParentRecursive(self, widget: QWidget):
        if widget.parent() is not None:
            return self.getParentRecursive(widget.parent())        
        return widget

    def mousePressEvent(self, a0):
        self.play()
        return super().mousePressEvent(a0)