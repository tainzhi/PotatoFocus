import enum
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import util
import Window
from TrayIcon import TrayIcon
import time
import random
import threading
from picture import Pictures


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
        self._left_seconds = util.TIMER_WORK
        # self._add_tray_icon()
        # 显示 system toolbar icon
        self._tray = TrayIcon()
        self._tray.show()
        # # start a qtthread to run pictures.Picutre.run()
        # self._pictures_thread = threading.Thread(target=Pictures().run, daemon=True)
        # self._pictures_thread.start()

    def run(self):
        while True:
            self._timer.start(util.TIMER_INTERVAL)
            self._app.exec_()

    def _show_full_screen(self):
        time_start = time.time()
        chosed_screen_photo_path = util.DEFAULT_SCREEN_PHOTO
        # random chose an image from CACHE_PICTURES_DIR
        if util.CACHE_PICTURES_DIR.exists():
            chosed_screen_photo_path = random.choice(list(util.CACHE_PICTURES_DIR.glob("*.jpg")))
        # get the image center postion 200x200 main color, then get the constrast color
        main_color = util.get_image_main_color(str(chosed_screen_photo_path), (1000, 1000))
        contrast_color = util.get_contrast_color(main_color)
        print(f"Chosed image: {chosed_screen_photo_path}, main color: {main_color}, contrast color: {contrast_color}, costs {time.time() - time_start:.2f} seconds")
        # 把主屏幕的计时器颜色设置为对比色
        self._main_window.set_background(str(chosed_screen_photo_path))
        self._second_window.set_background(str(chosed_screen_photo_path))
        self._main_window.show_full_screen(contrast_color)
        self._second_window.show_full_screen()

    def _add_tray_icon(self):
        app = self._app
        icon = QIcon(str(util.TRAY_ICON))
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
        # 必须要大于1s, 不能大于0s, 否则初始化会导致重复倒数两次
        print(f"Timer countdown: {self._left_seconds // 60:02d}:{self._left_seconds % 60:02d}")
        if self._left_seconds > 1:
            self._left_seconds -= 1
        else:
            self._timer.stop()
            self._show_full_screen()

    def _close_callback(self):
        """
        按 Esc 键退出全屏屏保的回调, 重新开始番茄钟工作计时
        :return:
        """
        self._main_window.close()
        self._second_window.close()
        self._left_seconds = util.TIMER_WORK
        self._timer.start()


if __name__ == '__main__':
    Main().run()