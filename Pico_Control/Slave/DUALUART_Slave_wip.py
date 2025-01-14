from machine import Pin, UART, ADC
import time
import _thread

uart1 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart0 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

x_axis = ADC(27)  # Connect VRx to GP26 (ADC0)
y_axis = ADC(26)  # Connect VRy to GP27 (ADC1)

# Setup for joystick button
button = Pin(2, Pin.IN, Pin.PULL_UP)  # Connect SW to GP16 with pull-up

# Function to send data to Raspberry Pi
def send_data_uart1(data):
    uart1.write(data)
    print("CORE1 Sent - " ,data)
    
def read_data_uart1():
    if uart1.any():
        data_uart1 = uart1.read().decode('utf-8')
        print("CORE0 - Received on UART1: ", data_uart1)
        return data_uart1
    return None

# Function to map analog values to a percentage (-100 to 100)
def map_value(value, in_min=0, in_max=65535, out_min=-100, out_max=100):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
def core1_joystick():
    
    while True:
        
        # Read raw ADC values
        x_raw = x_axis.read_u16()
        y_raw = y_axis.read_u16()
        
        # Map raw values to a percentage range (-100 to 100)
        x_percent = map_value(x_raw)
        y_percent = map_value(y_raw)
        
        button_state = not button.value()
        # send_data_uart1(f"X: {x_percent}%, Y: {y_percent}%, Button Pressed: {button_state}\n")
        send_data_uart1(f"X: {x_percent}\n")
        time.sleep(0.1)
        
def send_data_uart0(data):
    uart0.write(data)
    print("CORE0 - Sent: " ,data)
    
def read_data_uart0():
    if uart0.any():
        data_uart0 = uart0.read().decode('utf-8')
        print("CORE0 - Received on UART0: ", data_uart0)
        return data_uart0
    return None

def core2_uart_comms():
    while True:
        data_uart0 = read_data_uart0()
        if data_uart0:
            send_data_uart0("Hello from Pico on UART0\n")
        time.sleep(1)  # Delay before reading again

_thread.start_new_thread(core1_joystick, ())
core2_uart_comms()

