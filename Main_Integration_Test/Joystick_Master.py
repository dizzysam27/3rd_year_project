import serial
import time
from PCA9685 import PCA9685

class JOYSTICK_READ_DATA:

    def __init__(self):

        self.motors = PCA9685()
        self.motors.calibrate()
        self.uart0 = serial.Serial("/dev/ttyAMA0",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=0)

    def read_data(self):

        if self.uart0.in_waiting > 0:
            dataRx = str(self.uart0.readline().decode('utf-8').strip())
            yValue,xValue = map(int, dataRx.split(','))
            xValue=(xValue)
            yValue=(yValue)
            self.motors.motorAngle(xValue,yValue)
            print(xValue,yValue)  


# joystick = JOYSTICK_READ_DATA()


# while True:
#     joystick.read_data()
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