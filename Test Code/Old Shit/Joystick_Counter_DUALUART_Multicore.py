from machine import Pin, UART, ADC
import time
import _thread

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

x_axis = ADC(27)  # Connect VRx to GP26 (ADC0)
y_axis = ADC(26)  # Connect VRy to GP27 (ADC1)

# Setup for joystick button
button = Pin(2, Pin.IN, Pin.PULL_UP)  # Connect SW to GP16 with pull-up

# Function to send data to Raspberry Pi
def send_data_uart1(data):
    uart1.write(data)
    print("CORE1 - Sent: " ,data)
    
def read_data_uart1():
    if uart1.any():
        data_uart1 = uart1.read().decode('utf-8')
        print("CORE1 - Received on UART1: ", data_uart1)
        return data_uart1
    return None

# Function to map analog values to a percentage (-100 to 100)
def map_value(value, in_min=0, in_max=65535, out_min=-100, out_max=100):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
def core1_joystick_uart1():
    
    while True:
        
        # Read raw ADC values
        x_raw = x_axis.read_u16()
        y_raw = y_axis.read_u16()
        
        # Map raw values to a percentage range (-100 to 100)
        x_percent = map_value(x_raw)
        y_percent = map_value(y_raw)
        
        button_state = not button.value()
        send_data_uart1(f"X: {x_percent}%, Y: {y_percent}%, Button Pressed: {button_state}\n")
        time.sleep(0.1)
        
def send_data_uart0(data):
    uart0.write(data)
    print("CORE0 - Sent: " ,data, "\n")
    
def read_data_uart0():
    if uart0.any():
        data_uart0 = uart0.read().decode('utf-8')
        print("CORE0 - Received on UART0: ", data_uart0)
        return data_uart0
    return None

def core0_timer_uart0():
        # Define GPIO pins for BCD inputs based on the new pin assignments
    pins = {
        "A": Pin(16, Pin.OUT),  # Connect to A on CD4511BE
        "B": Pin(19, Pin.OUT),  # Connect to B on CD4511BE
        "C": Pin(18, Pin.OUT),  # Connect to C on CD4511BE
        "D": Pin(17, Pin.OUT),  # Connect to D on CD4511BE
    }

    def set_bcd_value(value):
        """Set the BCD value on the CD4511BE."""
        # Map the BCD bits to the GPIO pins based on the pinout
        bcd = [
            (value >> 0) & 1,  # A (Least Significant Bit)
            (value >> 1) & 1,  # B
            (value >> 2) & 1,  # C
            (value >> 3) & 1   # D (Most Significant Bit)
        ]
     
        # Set the values on the corresponding GPIO pins
        pins["A"].value(bcd[0])
        pins["B"].value(bcd[1])
        pins["C"].value(bcd[2])
        pins["D"].value(bcd[3])
        
        # Debug: Print the BCD value being set
        print(f"CORE0 - Setting BCD value: {value} -> A={bcd[0]} B={bcd[1]} C={bcd[2]} D={bcd[3]}")
    
    def test_display():
        """Test each digit on the 7-segment display."""
        for i in range(10):
            clear()
            set_bcd_value(i)
            send_data_uart0(str(x_percent))
            time.sleep(0.1)  # Hold the number for 1 second
            
            

    def clear():
        pins["A"].value(0)
        pins["B"].value(0)
        pins["C"].value(0)
        pins["D"].value(0)
        print("CORE0 - digit cleared")


    clear()
    test_display()

_thread.start_new_thread(core1_joystick_uart1, ())
core0_timer_uart0()


