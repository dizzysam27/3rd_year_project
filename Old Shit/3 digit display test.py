from machine import Pin
import time

# Dictionary which stores the pins for each segment
segments = {
    "digit1": [4,5,21,22,26,2,3],
    "digit2": [7,8,17,19,20,6,18],
    "digit3": [11,12,13,14,15,9,10],
}

global seconds, minutes
seconds = 0
minutes = 0

# Dictionary which stores the pins for the decimal points
dp1 = Pin(28,Pin.OUT)
dp2 = Pin(11,Pin.OUT)

# Dictionary which holds the initialised pins
pins = {
    digit: [Pin(pin_num, Pin.OUT) for pin_num in pin_list]
    for digit, pin_list in segments.items()
}

# Segment mappings
number_to_segments = {
    0: [1, 1, 1, 1, 1, 1, 0],  # abcdef
    1: [0, 1, 1, 0, 0, 0, 0],  # bc
    2: [1, 1, 0, 1, 1, 0, 1],  # abdeg
    3: [1, 1, 1, 1, 0, 0, 1],  # abcdg
    4: [0, 1, 1, 0, 0, 1, 1],  # bcfg
    5: [1, 0, 1, 1, 0, 1, 1],  # acdfg
    6: [1, 0, 1, 1, 1, 1, 1],  # acdefg
    7: [1, 1, 1, 0, 0, 0, 0],  # abc
    8: [1, 1, 1, 1, 1, 1, 1],  # abcdefg
    9: [1, 1, 1, 1, 0, 1, 1],  # abcdfg
    "G": [1, 0, 1, 1, 1, 1, 0] # acdef
}

number_to_segments_with_dp = {
    key: value + [0] for key, value in number_to_segments.items()
}

# Clear digit
def clear_digit(digit_name):
    for pin in pins[digit_name]:
        pin.value(0)

# Display number
def display_number(digit_name, number, dp=False):

# This elif statement removes the decimal place from the 

    clear_digit(digit_name)

    for i, state in enumerate(number_to_segments[number]):
        pins[digit_name][i].value(state)

# Display floating-point number
def display_float(value):
    int_part = int(value)
    frac_part = int((value - int_part) * 10)
    clear_digit("digit1")
    clear_digit("digit2")
    clear_digit("digit3")
    
    if minutes == 0:
        dp1.value(0)
        dp2.value(1)
        digit1 = int_part // 10
        digit2 = int_part % 10
        digit3 = frac_part
    else:
        dp1.value(1)
        dp2.value(0)
        digit1 = 8
        digit2 = 8
        digit3 = 8
    
    display_number("digit1", digit1)
    display_number("digit2", digit2, dp=True)
    display_number("digit3", digit3)

def display_go():
    display_number("digit1", "G")
    display_number("digit2", 0)


# Counter loop
clear_digit("digit1")
clear_digit("digit2")
clear_digit("digit3")
dp1.value(0)
dp2.value(0)

display_go()
time.sleep(1)
seconds += 1

display_number("digit1", 8)
display_number("digit2", 8, dp=True)
display_number("digit3", 8)
            


