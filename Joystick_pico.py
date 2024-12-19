from machine import ADC, Pin
from time import sleep

# Setup for joystick axes
x_axis = ADC(26)  # Connect VRx to GP26 (ADC0)
y_axis = ADC(27)  # Connect VRy to GP27 (ADC1)

# Setup for joystick button
button = Pin(16, Pin.IN, Pin.PULL_UP)  # Connect SW to GP16 with pull-up

# Function to map analog values to a percentage (-100 to 100)
def map_value(value, in_min=0, in_max=65535, out_min=-100, out_max=100):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    # Read raw ADC values
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    
    # Map raw values to a percentage range (-100 to 100)
    x_percent = map_value(x_raw)
    y_percent = map_value(y_raw)
    
    # Read button state (0 = pressed, 1 = not pressed)
    button_state = not button.value()
    
    # Print joystick values
    print(f"X: {x_percent}%, Y: {y_percent}%, Button Pressed: {button_state}")
    
    # Add a short delay for stability
    sleep(0.1)
