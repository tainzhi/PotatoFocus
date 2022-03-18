from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QKeySequence, QFont
from PyQt5.QtWidgets import QMainWindow, QShortcut, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

import Util
from TimerWidget import TimerWidget


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(Util.logo_icon))
        self.setWindowTitle(Util.app_name)
        self._flags = self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Window | Qt.CustomizeWindowHint
        # add shortcut Esc to quit full window
        self.short_cut_close = QShortcut(QKeySequence('Esc'), self)
        self.short_cut_close.activated.connect(self.quit_full_screen)

    def set_background(self, url):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(url)))
        self.setPalette(palette)


class MainWindow(Window):
    def __init__(self, on_close=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Util.app_name)
        self._flags = Qt.WindowStaysOnTopHint & Qt.FramelessWindowHint
        self._geometry = ((self.screen().size().width() / 2) - (self.width() / 2),
                          (self.screen().size().height() / 2) - (self.height() / 2), 800, 600)
        self.setGeometry(*self._geometry)
        self._widget = TimerWidget()
        self.setCentralWidget(self._widget)
        self._on_close = on_close

    def quit_full_screen(self):
        if self._on_close and callable(self._on_close):
            self._on_close()

    def __quit_full_screen_2_normal__(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
        self.setGeometry(self._geometry)
        self.show()


class SecondMonitorWindow(Window):
    """
    多显示器，在主显示器之外的所有 window 默认全屏
    """
    def __init__(self, app, on_close=None):
        super(SecondMonitorWindow, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        desktop = app.desktop()
        sg = desktop.screenGeometry(1)
        self.setGeometry(sg)
        self._on_close = on_close

    def quit_full_screen(self):
        if self._on_close and callable(self._on_close):
            self._on_close()
