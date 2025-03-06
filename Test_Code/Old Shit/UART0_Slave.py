from machine import Pin, UART
import time

uart0 = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

def send_data_uart0(data):
    try:
        uart0.write(data)
        print("Sent: ", data)
    except Exception as e:
        print("Error sending data:", e)

def read_data_uart0():
    try:
        if uart0.any():
            data_uart0 = uart0.read().decode('utf-8')
            print("Received on UART0:", data_uart0)
            return data_uart0
    except Exception as e:
        print("Error reading data:", e)
    return None

while True:
    data_uart0 = read_data_uart0()
    
    if data_uart0:
        send_data_uart0("Hello from Pico\n")

    time.sleep(0.01)  # Delay before reading again
