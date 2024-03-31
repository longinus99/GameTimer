import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class NotificationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PATTERN_ALERT")

        alert_jpg = resource_path("alert.jpg") 

        self.setWindowIcon(QIcon(alert_jpg))
        self.setGeometry(100, 100, 300, 100)

        self.countdown_label = QLabel("", self)
        self.countdown_label.setStyleSheet("font-size: 20pt")
        self.countdown_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.countdown_label)
        self.setLayout(layout)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #가장앞으로 알림 올리게 함



    def set_countdown(self, countdown):
        self.countdown = countdown
        self.update_countdown()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        if self.countdown >= 0:
            if self.countdown == 0:
                self.countdown_label.setText("패턴 발동!")
                self.setStyleSheet("color:white; background-color: red")
            else:
                self.countdown_label.setText(f"{self.countdown}초 후 패턴.")
            self.countdown -= 1
            
        else:
            #다시 원해 색으로 돌리기 
            self.setStyleSheet("")
            self.timer.stop()
            self.close()


#기본 스탑워치 사용
class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()

        self.elapsed_time = QTime(0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.notification_window = NotificationWindow()  # 패턴 창 생성

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("GAMETIMER")

        stopwatch_jpg = resource_path("stopwatch.jpg") 
        self.setWindowIcon(QIcon(stopwatch_jpg))
        self.setGeometry(100, 100, 300, 150)

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setStyleSheet("font-size: 24pt")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.start_stop_button = QPushButton("시작", self)
        self.start_stop_button.clicked.connect(self.start_stop)

        self.reset_button = QPushButton("리셋", self)
        self.reset_button.clicked.connect(self.reset)

        self.exit_button = QPushButton("종료", self)
        self.exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_stop_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start_stop(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.start_stop_button.setText("정지")
        else:
            self.timer.stop()
            self.start_stop_button.setText("시작")

    def reset(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0)
        time_str = self.elapsed_time.toString("hh:mm:ss")
        self.time_label.setText(time_str)

    def update_time(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        time_str = self.elapsed_time.toString("hh:mm:ss")
        self.time_label.setText(time_str)
        #시간 초로 변환
        time_sec = int(self.elapsed_time.toString("ss")) + int(self.elapsed_time.toString("mm"))*60 + int(self.elapsed_time.toString("hh"))*60*60
    
        if (time_sec > 0):
            if (time_sec > 150):
                if (time_sec- 150) % 140 == 135:
                    self.show_notification()
            else:
                if (time_sec) % 145 == 0:
                    self.show_notification()

                    
    def show_notification(self):
        #몇초 보낼건지 전달 
        self.notification_window.set_countdown(5)
        self.notification_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())
