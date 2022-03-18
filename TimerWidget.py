from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

import Util


class TimerWidget(QWidget):
    def __init__(self, on_finish=None):
        super().__init__()
        self._on_finish = on_finish
        font = QFont('Arial', 120, QFont.Bold)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self._left_seconds = Util.timer_break
        self.timer = QTimer()
        self.timer.timeout.connect(self._countdown_and_show)
        self.timer.start(Util.timer_interval)
        self._show_time()

    def _countdown_and_show(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
            self._show_time()
        else:
            self._on_finish()
            self.timer.stop()

    def reset(self):
        self._left_seconds = Util.timer_break
        self.timer.start(Util.timer_interval)
        self._show_time()

    def _show_time(self):
        total_seconds = self._left_seconds
        minutes = total_seconds // 60
        seconds = total_seconds - (minutes * 60)
        self.label.setText("{:02}:{:02}".format(int(minutes), int(seconds)))
