from PySide6.QtCore import Signal, QObject, QUrl, Slot
from settings import Settings


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

    def __init__(self, app: "MainApp", settings: Settings): # type: ignore
        super().__init__()
        self._app: MainApp = app # type: ignore
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
        
