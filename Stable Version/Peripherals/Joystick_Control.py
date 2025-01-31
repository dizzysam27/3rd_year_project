import serial
from Peripherals.Motor_Control import PCA9685

"""
This class reads the data provided by the joystick over UART. The UART connection is initalised and the motors are calibrated to their starting point.
The data is read and the output is sent to the motors.
"""

class JOYSTICK_READ_DATA:

    def __init__(self):

        self.motors = PCA9685()
        self.motors.calibrate() # Motors are calibrated to their starting position
        # The UART communication protocol is now initalised
        self.uart0 = serial.Serial("/dev/ttyAMA0",
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=0)

    def read_data(self):

        if self.uart0.in_waiting > 0:
            dataRx = str(self.uart0.readline().decode('utf-8').strip()) # Reads the incoming data over the UART connection
            yValue,xValue = map(int, dataRx.split(',')) # Splits the data into x and y values
            xValue=(xValue)
            yValue=(yValue)
            self.motors.motorAngle(xValue,yValue) # Sends joystick data to the motors
            print(xValue,yValue)  
