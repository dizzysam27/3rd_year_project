import serial # type: ignore
import time
import tkinter as tk

# Define UART Protocol
uart0 = serial.Serial("/dev/serial0",
                      baudrate=9600,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=0)

# Main Loop
while True:

    # Update Joystick Values
    if uart0.in_waiting > 0:
            dataRx = str(uart0.readline().decode('utf-8').strip())
            buttonValue = int(dataRx[-1])
            xValue = int(dataRx[-4:-2]) - 100
            yValue = int(dataRx) - (xValue*10 + buttonValue) - 100        
    
    testData = str(xValue)[-2:-1] + str(yValue)[-2:-1]
    ser.write(b''+testData+'\n')

    time.sleep(0.1)


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
