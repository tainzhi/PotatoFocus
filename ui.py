from typing import Optional
import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Signal, QObject, QUrl, QEvent, Qt, qVersion, Slot, QTimer
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from pathlib import Path
import util
from image import Image
from threading import Thread
import random
import termcolor
from settings import Settings

QML_IMPORT_NAME = "MainModule"
QML_IMPORT_MAJOR_VERSION = 1


class Bridge(QObject):
    
    breakTimerColorSignal = Signal(str)
    fullScreenDesktopOverlayShowSignal = Signal(bool)
    settingsWindowShowSignal = Signal(bool)
    setBackgroundSignal = Signal(str)
    
    # signals for settings values
    workTimeInMinuteSignal = Signal(int)
    breakTimeInMinuteSignal = Signal(int)
    continuousWorkAfterBreakSignal = Signal(bool)
    continuousWorkCountSignal = Signal(int)
    longBreakTimeSignal = Signal(int)
    usePixabayImageSignal = Signal(bool)
    pixabayApiKeySignal = Signal(str)
    pixabayMostUsedPerImageSignal = Signal(int)

    def __init__(self, app: "MainApp", settings: Settings):
        super().__init__()
        self._app: MainApp = app
        self._settings: Settings = settings
    
    def load_settings(self):
        """Load settings and emit signals with current values"""
        # print(f"Bridge load settings: {self._settings.settings}")
        self.workTimeInMinuteSignal.emit(self._settings.getWorkTimeInMinue())
        self.breakTimeInMinuteSignal.emit(self._settings.getBreakTimeInMinue())
        self.continuousWorkAfterBreakSignal.emit(self._settings.getContinuousWorkAfterBreak())
        self.continuousWorkCountSignal.emit(self._settings.getContinuousWorkCount())
        self.longBreakTimeSignal.emit(self._settings.getLongBreakTimeInMinue())
        self.usePixabayImageSignal.emit(self._settings.getUseImageDownloadedFromPixabay())
        self.pixabayApiKeySignal.emit(self._settings.getPixabayApiKey())
        self.pixabayMostUsedPerImageSignal.emit(self._settings.getPixabayMostUsedPerImage())
        
    @Slot()
    def onBreakTimeout(self):
        if self._settings.getContinuousWorkAfterBreak():
            self._app.hide_full_screen_desktop_overlay()
            self._app.reset_work_timer()
    @Slot()
    def onSettingsWindowClosed(self):
        # termcolor.cprint("onSettingsWindowClosed", "green")
        self._settings.save()
        self._app.download_image()
    
    @Slot(int)
    def onWorkTimeInMinuteChanged(self, value: int):
        # termcolor.cprint(f"onWorkTimeInMinuteChanged: {value}", "green")    
        self._settings.setWorkTimeInMinue(value)
    
    @Slot(int)
    def onBreakTimeInMinuteChanged(self, value: int):
        self._settings.setBreakTimeInMinue(value)
    
    @Slot(bool)
    def onContinuousWorkAfterBreakChanged(self, value: bool):
        self._settings.setContinuousWorkAfterBreak(value)

    @Slot(int)
    def onContinuousWorkCountChanged(self, value: int):
        self._settings.setContinuousWorkCount(value)
    
    @Slot(int)
    def onLongBreakTimeInMinuteChanged(self, value: int):
        self._settings.setLongBreakTimeInMinue(value)

    @Slot(bool)
    def onUsePixabayImageChanged(self, value: bool):
        self._settings.setUseImageDownloadedFromPixabay(value)

    @Slot(str)
    def onPixabayApiKeyChanged(self, value: str):
        self._settings.setPixabayApiKey(value)

    @Slot(int)
    def onPixabayMostUsedPerImageChanged(self, value: int):
        self._settings.setPixabayMostUsedPerImage(value)

    
    def set_break_timer_color(self, color: str):
        self.breakTimerColorSignal.emit(color)
    
    def set_break_timer_value(self, value: int):
        self.breakTimeInMinuteSignal.emit(value)
    
    def set_background(self, file_path: str):
        self.setBackgroundSignal.emit( QUrl.fromLocalFile(file_path).toString())
    
    def show_full_screen_desktop_overlay(self):
        self.fullScreenDesktopOverlayShowSignal.emit(True)
    
    def hide_full_screen_desktop_overlay(self):
        self.fullScreenDesktopOverlayShowSignal.emit(False)
    
    def show_settings_window(self):
        self.settingsWindowShowSignal.emit(True)
        

class MainApp(QApplication):
    
    settings = Settings()

    def __init__(self, sys_argv: list[str]):
        super().__init__(sys_argv)
        self.setWindowIcon(QIcon(str(util.LOGO_ICON)))
        self.setApplicationName(util.APP_NAME)

        self.setApplicationVersion(qVersion())
        
        self.work_timer = QTimer(self)
        self.is_work_timer_set = False
        self.continues_work_count = 0
        self.work_timer_remain_time_str = ""
        self.reset_work_timer()
        self._image: Optional[Image] = None
        self.download_image()

        # 获取所有可用屏幕
        screens = self.screens()
        if len(screens) >= 2:
            self.main_screen = screens[0]
            self.second_screen = screens[1]
        else:
            self.main_screen = self.primaryScreen()
            self.second_screen = None

        self._bridge: Bridge = Bridge(self, self.settings)

        # 为主屏幕创建引擎
        self.main_engine = QQmlApplicationEngine()
        self.main_context = self.main_engine.rootContext()
        self.main_context.setContextProperty("bridge", self._bridge)

        main_qml_file = Path(__file__).parent / "Resource" / "qml" / "MainScreen.qml"
        self.main_engine.load(QUrl.fromLocalFile(main_qml_file))

        if not self.main_engine.rootObjects():
            sys.exit(-1)

        # 为副屏幕创建引擎
        if self.second_screen:
            self.second_engine = QQmlApplicationEngine()
            self.second_context = self.second_engine.rootContext()
            self.second_context.setContextProperty("mainApp", self)
            self.second_context.setContextProperty("bridge", self._bridge)

            second_qml_file = Path(__file__).parent / "Resource" / "qml" / "SecondScreen.qml"
            self.second_engine.load(QUrl.fromLocalFile(second_qml_file))

            if not self.second_engine.rootObjects():
                sys.exit(-1)

            # 设置副屏幕窗口的位置和大小
            second_window = self.second_engine.rootObjects()[0]
            second_window.setScreen(self.second_screen)
            second_window.setGeometry(self.second_screen.geometry())
            
        
        # 为设置窗口创建引擎
        self.set_engine = QQmlApplicationEngine()
        self.set_context = self.set_engine.rootContext()
        self.set_context.setContextProperty("bridge", self._bridge)

        set_qml_file = Path(__file__).parent / "Resource" / "qml" / "SettingsWindow.qml"
        self.set_engine.load(QUrl.fromLocalFile(set_qml_file))

        if not self.set_engine.rootObjects():
            sys.exit(-1)
        
        self.installEventFilter(self)
        
        # Set up the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(str(util.LOGO_ICON)))

        # Create a context menu for the tray icon
        self.tray_menu = QMenu()
        
        # Add an action to show the application
        settings_action = QAction("Settings", self)
        settings_action.setIcon(QIcon((str(util.SETTINGS_ICON))))
        settings_action.triggered.connect(self.show_settings_window)
        self.tray_menu.addAction(settings_action)

        # Add an action to show the application
        show_action = QAction("Break", self)
        show_action.setIcon(QIcon((str(util.FULLSCREEN_ICON))))
        show_action.triggered.connect(self.show_full_screen_desktop_overlay)
        self.tray_menu.addAction(show_action)

        # Add an action to quit the application
        quit_action = QAction("Quit", self)
        quit_action.setIcon(QIcon(str(util.QUIT_ICON)))
        quit_action.triggered.connect(self.on_quit)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
    
    def download_image(self):
        if self.settings.getUseImageDownloadedFromPixabay():
            if self._image:
                self._image.download()
            else:
                self._image: Image = Image(self.settings)
                self._image_thread = Thread(target=self._image.download, daemon=True)
                self._image_thread.start()
        else:
            termcolor.warn("[main] not set use pixal images as fullscreen overlays in Settings")
            self._image = None

    
    def reset_work_timer(self):
        # 断开之前的连接，避免重复连接
        if self.is_work_timer_set:
            try:
                self.work_timer.timeout.disconnect(self.update_countdown)
            except TypeError:
                pass
            self.is_work_timer_set = False
        self.remaining_time =  self.settings.getWorkTimeInMinue() * 60 * 1000  # in milliseconds
        self.work_timer.timeout.connect(self.update_countdown)
        self.work_timer.start(1000)  # Update every second
        self.is_work_timer_set = True
        self.continues_work_count += 1

    # catch esc key press event
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.hide_full_screen_desktop_overlay()
                self.reset_work_timer()
                return True
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                print("Enter key pressed.")
                return True
        return super().eventFilter(obj, event)

    def hide_full_screen_desktop_overlay(self):
        self._bridge.hide_full_screen_desktop_overlay()
    
    def show_settings_window(self) -> None:
        self._bridge.load_settings()
        self._bridge.show_settings_window()

    def show_full_screen_desktop_overlay(self):
        self._bridge.load_settings()
        self.work_timer.stop()
        # Show the main screen window
        # time_start = time.time()
        chosed_screen_photo_path = util.DEFAULT_SCREEN_PHOTO
        # random chose an image from CACHE_IMAGES_DIR
        if util.CACHE_IMAGES_DIR.exists():
            if self._image and self._image.usage.values():
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
        # 要计算出 Break Timer所在区域的图片的对比色
        # 便于突出显示 Break Timer
        main_color = util.get_image_main_color(str(chosed_screen_photo_path), util.BREAK_TIMER_SIZE_IN_MAIN_SCREEN)
        contrast_color = util.get_contrast_color(main_color)
        # print(f"Chosed image: {chosed_screen_photo_path}, main color: {main_color}, contrast color: {contrast_color}, costs {time.time() - time_start:.2f} seconds")
        # 把主屏幕的计时器颜色设置为对比色
        # rgb to hex color
        self._bridge.set_break_timer_color("#{:02x}{:02x}{:02x}".format(contrast_color[0], contrast_color[1], contrast_color[2]))   
        # 连续工作多个番茄钟后, 长时间休息
        if self.continues_work_count >= self.settings.getContinuousWorkCount():
            self._bridge.set_break_timer_value(self.settings.getLongBreakTimeInMinue())    
            self.continues_work_count = 0
        else:
            self._bridge.set_break_timer_value(self.settings.getBreakTimeInMinue())
        self._bridge.set_background(str(chosed_screen_photo_path))
        self._bridge.show_full_screen_desktop_overlay()
                
    def update_countdown(self):
        self.remaining_time -= 1000
        if self.remaining_time <= 0:
            self.work_timer.stop()
            self.show_full_screen_desktop_overlay()
            self.tray_icon.setToolTip(f"{util.APP_NAME} - work")
            print("Countdown finished, showing windows.")
        else:
            minutes = self.remaining_time // (60 * 1000)
            seconds = (self.remaining_time % (60 * 1000)) // 1000
            termcolor.cprint(f"{self.continues_work_count}th Work remaining time: {minutes:02d}:{seconds:02d}", color="green", end="\r")
            self.tray_icon.setToolTip(f"{util.APP_NAME} - work {minutes:02d}:{seconds:02d}")
    
    def on_quit(self):
        self.settings.save()
        self.quit()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_full_screen_desktop_overlay()

if __name__ == '__main__':
    app = MainApp(sys.argv)
    
    def clean_up():
        pass
    app.aboutToQuit.connect(clean_up)
    sys.exit(app.exec())