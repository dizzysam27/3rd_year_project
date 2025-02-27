from machine import Pin, UART
import time

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def send_data_uart0(data):
    uart0.write(data)
    print("Sent: " ,data)

# Function to read data from Raspberry Pi
def read_data_uart0():
    if uart0.any():
        data_uart0 = uart0.read().decode('utf-8')
        print("Received on UART0: ", data_uart0)
        return data_uart0
    return None

# Example usage
while True:
    # Read data from Raspberry Pi
    print("waiting")
    data_uart0 = read_data_uart0()
    
    send_data_uart0("Hello from Pico on UART0\n")
            
    
    time.sleep(1)  # Delay before reading again

