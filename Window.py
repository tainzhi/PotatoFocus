from PyQt5 import QtGui, QtCore
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
        # self._flags = self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Window | Qt.CustomizeWindowHint
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
        # add shortcut Esc to quit full window
        self.short_cut_close = QShortcut(QKeySequence('Esc'), self)
        self.short_cut_close.activated.connect(self._quit_full_screen)

    def set_background(self, url):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(url)))
        self.setPalette(palette)

    def _show_full_screen(self):
        pass


class MainWindow(Window):
    def __init__(self, on_close=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Util.app_name)
        self._flags = Qt.WindowStaysOnTopHint & Qt.FramelessWindowHint
        self._geometry = ((self.screen().size().width() / 2) - (self.width() / 2),
                          (self.screen().size().height() / 2) - (self.height() / 2), 800, 600)
        self.setGeometry(*self._geometry)
        """ 主屏屏保图片添加倒计时 """
        self._widget = TimerWidget(self._on_timer_finish)
        self.setCentralWidget(self._widget)
        self._on_close = on_close

    def _on_timer_finish(self):
        """TimerWidget的计时完成后的回调"""
        self._quit_full_screen()

    def show_full_screen(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 设置全屏大小
        self._geometry = (0, 0, self.screen().size().width(), self.screen().size().height())
        self.setGeometry(*self._geometry)
        self._widget.reset()
        self.show()

    def _quit_full_screen(self):
        if self._on_close and callable(self._on_close):
            self._on_close()


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

    def show_full_screen(self):
        # 默认是全屏覆盖属性,直接显示
        self.show()

    def _quit_full_screen(self):
        if self._on_close and callable(self._on_close):
            self._on_close()
