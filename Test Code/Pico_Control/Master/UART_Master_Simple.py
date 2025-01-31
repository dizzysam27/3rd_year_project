import serial
import time

# Configure the UART
uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

while True:
    # Send a message
    uart.write(b"Hello from Raspberry Pi 5!\n")
    print("Message sent from Raspberry Pi 5")
    
    # Read incoming messages
    if uart.in_waiting > 0:
        received = uart.readline().decode('utf-8').strip()
        print(f"Received: {received}")
    
    time.sleep(1)

