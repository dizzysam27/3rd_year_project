import serial
import time

# Initialize UART on /dev/serial0
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    ser.write(b'Stop')
    time.sleep(1)
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print("Received:", data)
except KeyboardInterrupt:
    ser.close()

