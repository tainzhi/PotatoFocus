import enum
import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import Util
import Window
from TrayIcon import TrayIcon


class TimerStatus(enum.Enum):
    init, counting, paused = 1, 2, 3


class Main:
    def __init__(self):
        self._app = QApplication(sys.argv)
        # 多屏显示器的主屏
        self._main_window = Window.MainWindow(self._close_callback)
        # 多屏显示器的副屏
        self._second_window = Window.SecondMonitorWindow(self._app, self._close_callback)
        self._timer = QTimer()
        # todo how to use status
        self._timer_status = TimerStatus.init
        self._timer.timeout.connect(self._timer_countdown_callback)
        self._left_seconds = Util.timer_work
        # self._add_tray_icon()
        # 显示 system toolbar icon
        self._tray = TrayIcon()
        self._tray.show()

    def run(self):
        while True:
            self._timer.start(Util.timer_interval)
            self._app.exec_()

    def _show_full_screen(self):
        self._main_window.show_full_screen()
        # self._second_window.show_full_screen()

    def _set_background(self):
        self._main_window.set_background(Util.screen_photo)
        self._second_window.set_background(Util.screen_photo)

    def _add_tray_icon(self):
        app = self._app
        icon = QIcon(Util.tray_icon)
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()
        quit_app = QAction("Quit")
        quit_app.triggered.connect(app.quit)
        menu.addAction(quit_app)
        # todo: add settings menu
        # settings = QAction("Settings")
        # settings.triggered.connect(app.quit)
        # menu.addAction(settings)
        tray.setContextMenu(menu)

    def _timer_countdown_callback(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
        else:
            self._timer.stop()
            self._set_background()
            self._show_full_screen()
        print("left time: {:02}:{:02}".format(self._left_seconds // 60, (self._left_seconds % 60) ))

    def _close_callback(self):
        """
        按 Esc 键退出全屏屏保的回调, 重新开始番茄钟工作计时
        :return:
        """
        self._main_window.close()
        self._second_window.close()
        self._left_seconds = Util.timer_work
        self._timer.start()


if __name__ == '__main__':
    Main().run()
