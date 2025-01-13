from machine import Pin, UART
import time

# uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# # Function to send data to Raspberry Pi
# def send_data_uart0(data):
#     uart0.write(data)
#     print("Sent: " ,data)
#     
def send_data_uart1(data):
    uart1.write(data)
    print("Sent: " ,data)

# # Function to read data from Raspberry Pi
# def read_data_uart0():
#     if uart0.any():
#         data_uart0 = uart0.read().decode('utf-8')
#         print("Received on UART0: ", data_uart0)
#         return data_uart0
#     return None

def read_data_uart1():
    if uart1.any():
        data_uart1 = uart1.read().decode('utf-8')
        print("Received on UART1: ", data_uart1)
        return data_uart1
    return None

# Example usage
while True:
    # Read data from Raspberry Pi
#     data_uart0 = read_data_uart0()
    data_uart1 = read_data_uart1()
#     
#     if data_uart0:
#         send_data_uart0("Hello from Pico on UART0\n")
#         
    if data_uart1:
        send_data_uart1("Hello from Pico on UART1\n")
    
    time.sleep(1)  # Delay before reading again
