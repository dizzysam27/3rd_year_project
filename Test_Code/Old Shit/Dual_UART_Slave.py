from machine import UART, Pin
import time

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    uart0.write("Hello from Pico!\n")
    time.sleep(1)
