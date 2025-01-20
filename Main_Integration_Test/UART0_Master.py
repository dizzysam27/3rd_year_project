import serial # type: ignore
import time
import tkinter as tk
from PCA9685 import PCA9685
# Define UART Protocol

motors = PCA9685()
uart0 = serial.Serial("/dev/ttyAMA0",
                      baudrate=9600,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=0)

xValue = 0
yValue = 0

# Main Loop
testData = 0
while True:

    # Update Joystick Values
    if uart0.in_waiting > 0:
            dataRx = str(uart0.readline().decode('utf-8').strip())
            y,x,button = map(int, dataRx.split(','))
            x=x-100
            y=y-100
            motors.motorAngle(-x,-y)
            print(x,y,button)        
    
    testData += 1
    # uart0.write(b'2')

    time.sleep(0.001)

uart0.close()

while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print("Received:", data)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error:", e)

ser.close()