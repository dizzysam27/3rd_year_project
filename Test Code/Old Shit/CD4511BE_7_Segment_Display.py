from machine import Pin
from time import sleep

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
    sleep(1)
    # Set the values on the corresponding GPIO pins
    print(bcd)
    pins["A"].value(bcd[0])
    pins["B"].value(bcd[1])
    pins["C"].value(bcd[2])
    pins["D"].value(bcd[3])
    
    # Debug: Print the BCD value being set
    print(f"Setting BCD value: {value} -> A={bcd[0]} B={bcd[1]} C={bcd[2]} D={bcd[3]}")
    
def test_display():
    """Test each digit on the 7-segment display."""
    for i in range(10):
        set_bcd_value(i)


def clear():
    pins["A"].value(0)
    pins["B"].value(0)
    pins["C"].value(0)
    pins["D"].value(0)
    
    print("cleared")
    sleep(1)

def test():
    pins["A"].value(1)
    pins["B"].value(1)
    pins["C"].value(1)
    pins["D"].value(1)
    print("test")


clear()
test_display()
