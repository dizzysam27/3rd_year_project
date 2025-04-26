import serial
import threading
from motorControl import PCA9685
from PyQt5.QtCore import pyqtSignal, QThread


class JOYSTICK_READ_DATA(QThread):
    xRate = pyqtSignal(int)
    yRate = pyqtSignal(int)
    printBuffer = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.uart0 = serial.Serial("/dev/ttyAMA0",
                                   baudrate=9600,
                                   parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   timeout=0)
        self.running = False
        self.thread = None  # Initialize without a thread

    def read_data(self):
        while self.running:
            if self.uart0.in_waiting > 0:
                dataRx = self.uart0.readline().decode('utf-8').strip()
                try:
                    xValue, yValue = map(int, dataRx.split(','))
                    self.printBuffer.emit(f"x: {xValue}, y: {yValue}")
                    self.xRate.emit(int(xValue))
                    self.yRate.emit(int(yValue))
                except ValueError:
                    self.printBuffer.emit("Invalid data received")

    def start_reading(self):
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self.read_data, daemon=True)
            self.thread.start()
            self.printBuffer.emit("Joystick reading started.")
            
        else:
            self.printBuffer.emit("Thread is already running!")

    def stop_reading(self):
        if self.thread and self.thread.is_alive():
            self.running = False
            self.thread.join()
            self.printBuffer.emit("Joystick reading stopped.")