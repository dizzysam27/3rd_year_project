import serial
import time
import tkinter as tk
from PCA9685 import PCA9685

class JOYSTICK_READ_DATA:

    def __init__(self):

        self.motors = PCA9685()
        self.uart0 = serial.Serial("/dev/ttyAMA0",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=0)

        self.xValue = 0
        self.yValue = 0
        self.bValue = 0

    def read_data(self):

        while True:

            if self.uart0.in_waiting > 0:
                    dataRx = str(self.uart0.readline().decode('utf-8').strip())
                    self.yValue,self.xValue,self.bValue = map(int, dataRx.split(','))
                    self.xValue=self.xValue-100
                    self.yValue=self.yValue-100
                    self.motors.motorAngle(-self.xValue,-self.yValue)
                    print(self.xValue,self.yValue,self.bValue)  
            else:
                 pass      
            
            time.sleep(0.001)



        # uart0.close()

        # while True:
        #     try:
        #         if ser.in_waiting > 0:
        #             data = ser.readline().decode('utf-8').strip()
        #             print("Received:", data)
        #         time.sleep(1)
        #     except KeyboardInterrupt:
        #         print("Exiting...")
        #         break
        #     except Exception as e:
        #         print("Error:", e)

        # ser.close()

            #  testData += 1
            # uart0.write(b'2')