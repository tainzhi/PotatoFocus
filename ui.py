import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtCore import Signal, QObject, QUrl, QEvent, Qt, qVersion, Slot, QTimer
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from pathlib import Path
import util
from image import Image
from threading import Thread
import time
import random

QML_IMPORT_NAME = "MainModule"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):
    
    breakTimeSignal = Signal(int)
    breakTimerColorSignal = Signal(str)

    def __init__(self, app):
        self._app = app
        super().__init__()
        
    @Slot()
    def onBreakTimeout(self):
        if util.CONTINUOUS_WORK_AFTER_BREAK:
            self._app.hide_windows()
            self._app.reset_work_timer()
    
    def set_break_timer_color(self, color: str):
        self.breakTimeSignal.emit(util.TIMER_BREAK)
        self.breakTimerColorSignal.emit(color)

        

class MainApp(QApplication):
    onClose = Signal()

    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.setWindowIcon(QIcon(str(util.LOGO_ICON)))
        self.setApplicationName(util.APP_NAME)

        self.setApplicationVersion(qVersion())
        
        self.work_timer = QTimer(self)
        self.reset_work_timer()
        
        self._image = Image()
        self._image_thread = Thread(target=self._image.download, daemon=True)
        self._image_thread.start()

        # 获取所有可用屏幕
        screens = self.screens()
        if len(screens) >= 2:
            self.main_screen = screens[0]
            self.second_screen = screens[1]
        else:
            self.main_screen = self.primaryScreen()
            self.second_screen = None

        # 为主屏幕创建引擎
        self.main_engine = QQmlApplicationEngine()
        self.main_context = self.main_engine.rootContext()

        main_qml_file = Path(__file__).parent / "Resource" / "qml" / "MainScreen.qml"
        self.main_engine.load(QUrl.fromLocalFile(main_qml_file))

        if not self.main_engine.rootObjects():
            sys.exit(-1)

        # 为副屏幕创建引擎
        if self.second_screen:
            self.second_engine = QQmlApplicationEngine()
            self.second_context = self.second_engine.rootContext()
            self.second_context.setContextProperty("mainApp", self)

            second_qml_file = Path(__file__).parent / "Resource" / "qml" / "SecondScreen.qml"
            self.second_engine.load(QUrl.fromLocalFile(second_qml_file))

            if not self.second_engine.rootObjects():
                sys.exit(-1)

            # 设置副屏幕窗口的位置和大小
            second_window = self.second_engine.rootObjects()[0]
            second_window.setScreen(self.second_screen)
            second_window.setGeometry(self.second_screen.geometry())
        
        self.installEventFilter(self)
        
        # Set up the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(str(util.LOGO_ICON)))
        self.tray_icon.setToolTip(util.APP_NAME)

        # Create a context menu for the tray icon
        self.tray_menu = QMenu()

        # Add an action to show the application
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_windows)
        self.tray_menu.addAction(show_action)

        # Add an action to quit the application
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
    
    def set_bridge(self, bridge):
        self.main_context.setContextProperty("bridge", bridge)
        self._bridge = bridge

    def set_background(self, file_path: str):
        # 为主屏幕设置背景
        self.main_root_objects = self.main_engine.rootObjects()
        if self.main_root_objects:
            main_window = self.main_root_objects[0]
            background_image = main_window.findChild(QObject, "backgroundImage")
            if background_image:
                background_image.setProperty("source", QUrl.fromLocalFile(file_path).toString())

        # 为副屏幕设置背景
        if self.second_screen:
            self.second_root_objects = self.second_engine.rootObjects()
            if self.second_root_objects:
                second_window = self.second_root_objects[0]
                background_image = second_window.findChild(QObject, "backgroundImage")
                if background_image:
                    background_image.setProperty("source", QUrl.fromLocalFile(file_path).toString())
    
    def reset_work_timer(self):
        # 断开之前的连接，避免重复连接
        try:
            self.work_timer.timeout.disconnect(self.update_countdown)
        except TypeError:
            pass
        self.remaining_time = util.TIMER_WORK * 1000  # 30 minutes in milliseconds
        self.work_timer.timeout.connect(self.update_countdown)
        self.work_timer.start(1000)  # Update every second

    # catch esc key press event
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.hide_windows()
                self.reset_work_timer()
                return True
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                print("Enter key pressed.")
                return True
        return super().eventFilter(obj, event)

    def hide_windows(self):
        # Hide the main screen window
        main_root_objects = self.main_engine.rootObjects()
        if main_root_objects:
            main_window = main_root_objects[0]
            main_window.setProperty('visible', False)

        # Hide the second screen window if it exists
        if self.second_screen:
            second_root_objects = self.second_engine.rootObjects()
            if second_root_objects:
                second_window = second_root_objects[0]
                second_window.setProperty('visible', False)

    def show_windows(self):
        # Show the main screen window
        time_start = time.time()
        chosed_screen_photo_path = util.DEFAULT_SCREEN_PHOTO
        # random chose an image from CACHE_IMAGES_DIR
        if util.CACHE_IMAGES_DIR.exists():
            if self._image.usage.values():
                # 从 self._image.image_usage()中使用次数较少的图片, 随机选取一个, 并且更新 image_usage, 然后报错
                min_usage = min(self._image.usage.values())
                least_used_images = [image for image, count in self._image.usage.items() if count == min_usage]
                # 随机选择一张使用次数最少的图片
                chosed_image = random.choice(least_used_images)
                # 更新该图片的使用次数
                self._image.usage[chosed_image] = self._image.usage[chosed_image] + 1
                self._image.save_usage()
                chosed_screen_photo_path = util.CACHE_IMAGES_DIR / chosed_image
            else:
                chosed_screen_photo_path = util.DEFAULT_SCREEN_PHOTO
        # get the image center postion 200x200 main color, then get the constrast color
        main_color = util.get_image_main_color(str(chosed_screen_photo_path), (1000, 1000))
        contrast_color = util.get_contrast_color(main_color)
        # print(f"Chosed image: {chosed_screen_photo_path}, main color: {main_color}, contrast color: {contrast_color}, costs {time.time() - time_start:.2f} seconds")
        self._bridge.set_break_timer_color(f"rgb({contrast_color[0]}, {contrast_color[1]}, {contrast_color[2]})")   
        self.set_background(str(chosed_screen_photo_path))
        # 把主屏幕的计时器颜色设置为对比色
        main_root_objects = self.main_engine.rootObjects()
        if main_root_objects:
            main_window = main_root_objects[0]
            main_window.setProperty('visible', True)
            if hasattr(main_window, 'showFullScreen'):
                main_window.showFullScreen()
                

        # Show the second screen window if it exists
        if self.second_screen:
            second_root_objects = self.second_engine.rootObjects()
            if second_root_objects:
                second_window = second_root_objects[0]
                second_window.setProperty('visible', True)
            if hasattr(second_window, 'showFullScreen'):
                second_window.showFullScreen()
                
    def update_countdown(self):
        self.remaining_time -= 1000
        if self.remaining_time <= 0:
            self.work_timer.stop()
            self.show_windows()
            print("Countdown finished, showing windows.")
        else:
            minutes = self.remaining_time // (60 * 1000)
            seconds = (self.remaining_time % (60 * 1000)) // 1000
            print(f"Work remaining time: {minutes:02d}:{seconds:02d}")

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_windows()

if __name__ == '__main__':
    app = MainApp(sys.argv)
    
    def clean_up():
        pass
    
    bridge = Bridge(app)
    app.set_bridge(bridge)
    app.aboutToQuit.connect(clean_up)
    sys.exit(app.exec())