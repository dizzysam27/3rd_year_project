import serial
import threading
from motorControl import PCA9685

class JOYSTICK_READ_DATA:
    def __init__(self):
        self.uart0 = serial.Serial("/dev/ttyAMA0",
                                   baudrate=9600,
                                   parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   timeout=0)
        self.running = False
        self.thread = None  # Initialize without a thread
        self.motors = PCA9685()

    def read_data(self):
        while self.running:
            if self.uart0.in_waiting > 0:
                dataRx = self.uart0.readline().decode('utf-8').strip()
                try:
                    yValue, xValue = map(int, dataRx.split(','))
                    print(f"x: {xValue}, y: {yValue}")
                    self.motors.setServoPulse(1,1850+yValue/2) # Sends joystick data to the motors
                    self.motors.setServoPulse(0,1915+xValue/2)
                except ValueError:
                    print("Invalid data received")

    def start_reading(self):
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self.read_data, daemon=True)
            self.thread.start()
            print("Joystick reading started.")
            
        else:
            print("Thread is already running!")

    def stop_reading(self):
        if self.thread and self.thread.is_alive():
            self.running = False
            self.thread.join()
            print("Joystick reading stopped.")