import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import Util
import Window


def add_tray_icon(app):
    icon = QIcon(Util.tray_icon)
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()
    quit_app = QAction("Quit")
    quit_app.triggered.connect(app.quit)
    menu.addAction(quit_app)
    # todo: add settings menu
    settings = QAction("Settings")
    settings.triggered.connect(app.quit)
    menu.addAction(settings)
    tray.setContextMenu(menu)


def close_callback():
    print("close callback")


def main():
    app = QApplication(sys.argv)
    main_window = Window.MainWindow(close_callback)
    second_window = Window.SecondMonitorWindow(app, close_callback)
    second_window.set_background(Util.screen_photo)
    main_window.show()
    # secondwindow.show()
    add_tray_icon(app)
    app.exec_()

if __name__ == '__main__':
    main()
