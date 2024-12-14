from machine import UART, Pin
import time

# Initialize UART0
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    if uart.any():
        data = uart.read()
        print("Received from Raspberry Pi:", data)
    uart.write(b'Hello from Pico!\n')
    time.sleep(1)
