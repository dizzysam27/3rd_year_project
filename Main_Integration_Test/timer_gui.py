import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from Control_Panel import LCD1602_WRITE


class TimerThread(QObject):
    # Signal to update the timer display in the GUI
    update_time_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = False

    def start_timer(self):
        self.running = True
        start_time = time.time()
        while self.running:
            elapsed_time = time.time() - start_time
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.update_time_signal.emit(formatted_time)
            time.sleep(1)  # Update every second

    def stop_timer(self):
        self.running = False


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer_thread = TimerThread()
        self.timer_thread.update_time_signal.connect(self.update_timer_display)

        # Start the timer in a separate thread
        self.thread = threading.Thread(target=self.timer_thread.start_timer)
        self.thread.daemon = True
        self.thread.start()

    def init_ui(self):
        self.setWindowTitle('Timer Example')
        self.setGeometry(100, 100, 200, 100)

        self.timer_label = QLabel('00:00:00', self)
        self.timer_label.setStyleSheet('font-size: 24px;')

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        self.setLayout(layout)

    def update_timer_display(self, time_str):
        self.timer_label.setText(time_str)
        self.lcd = LCD1602_WRITE()
        self.lcd.update_messages(time_str,"")

    def closeEvent(self, event):
        # Stop the timer thread when the window is closed
        self.timer_thread.stop_timer()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec_())
