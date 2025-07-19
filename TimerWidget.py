from ast import Tuple
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from typing import Optional, Tuple
import util


class TimerWidget(QWidget):
    def __init__(self, on_finish=None):
        super().__init__()
        self._color = [255, 255, 255]  # Default color
        self._on_finish = on_finish
        font = QFont('Arial', 120, QFont.Bold)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self._left_seconds = util.timer_break
        self.timer = QTimer()
        self.timer.timeout.connect(self._countdown_and_show)
        self.timer.start(util.timer_interval)
        self._show_time()

    def _countdown_and_show(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
            self._show_time()
        else:
            self._on_finish()
            self.timer.stop()

    def reset(self, color: Optional[Tuple[int, int, int]] = None):
        self._left_seconds = util.timer_break
        self.timer.start(util.timer_interval)
        if color:
            self._color = color
        self._show_time()

    def _show_time(self):
        total_seconds = self._left_seconds
        minutes = total_seconds // 60
        seconds = total_seconds - (minutes * 60)
        self.label.setText("{:02}:{:02}".format(int(minutes), int(seconds)))
        self.label.setStyleSheet(f"color: rgb({self._color[0]}, {self._color[1]}, {self._color[2]})")