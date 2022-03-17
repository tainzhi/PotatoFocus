from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        font = QFont('Arial', 120, QFont.Bold)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self._left_seconds = 300
        self.timer = QTimer()
        self.timer.timeout.connect(self._countdown_and_show)
        interval = 1000
        self.timer.start(1000)
        self.show_time()

    def _countdown_and_show(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
            self.show_time()
        else:
            # todo callback
            self.timer.stop()
            pass

    def show_time(self):
        total_seconds = self._left_seconds
        minutes = total_seconds // 60
        seconds = total_seconds - (minutes * 60)
        self.label.setText("{:02}:{:02}".format(int(minutes), int(seconds)))
