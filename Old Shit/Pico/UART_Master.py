import serial
import time

# Initialize UART on /dev/serial0
ser = serial.Serial('/dev/ttyAMA2', baudrate=9600, timeout=1)

try:
    while True:
        ser.write(b'Hello from Raspberry Pi!\n')
        time.sleep(1)
        
        data = ser.readline().decode('utf-8').strip()
        print("Received:", data)
except KeyboardInterrupt:
    ser.close()

