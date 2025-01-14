import serial
import time

# Initialize UART on /dev/serial0
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    while True:
        ser.write(b'Hello from Raspberry Pi 4!\n')
        print("Sent: Hello from Raspberry Pi 4!")
        time.sleep(1)
        
        data = ser.readline().decode('utf-8').strip()
        print("Received:", data)
except KeyboardInterrupt:
    ser.close()
