import serial
import time

# Initialize serial connection
ser = serial.Serial("/dev/serial0", 9600, timeout=1)

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
