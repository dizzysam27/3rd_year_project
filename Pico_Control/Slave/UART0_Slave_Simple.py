from machine import UART, Pin
import time

# Initialize UART1 (TX: GP4, RX: GP5)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    # Send a message
    uart.write("Hello from Pico!\n")
    print("Message sent from Pico")
    
    # Check for incoming messages
    if uart.any():
        received = uart.read().decode('utf-8').strip()
        print(f"Received: {received}")
    
    time.sleep(1)
