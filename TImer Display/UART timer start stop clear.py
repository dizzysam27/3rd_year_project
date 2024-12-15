from machine import UART, Pin

import time

# Dictionary which stores the pins for each segment
segments = {
    "digit1": [22, 17, 6, 27, 5, 21, 18],
    "digit2": [19, 16, 10, 8, 7, 20, 9],
    "digit3": [13, 12, 4, 3, 2, 15, 14],
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
        digit1 = minutes
        digit2 = int_part // 10
        digit3 = int_part % 10
    
    display_number("digit1", digit1)
    display_number("digit2", digit2, dp=True)
    display_number("digit3", digit3)

def display_go():
    display_number("digit1", "G")
    display_number("digit2", 0)

def waiting():
    while True:
        if uart.any():
            data = uart.read()
            print("Received:", data)
            value = data.decode()
            print(value)
            if value == "Start":
                clear_digit("digit1")
                clear_digit("digit2")
                clear_digit("digit3")
                dp1.value(0)
                dp2.value(0)
                counter()
            if value == "Clear":
                clear_digit("digit1")
                clear_digit("digit2")
                clear_digit("digit3")
                dp1.value(0)
                dp2.value(0)
                seconds = 0
                minutes = 0
                
        time.sleep(1)
        
def counter():

    global seconds, minutes
    seconds = 0
    minutes = 0
    display_go()
    time.sleep(1)
    seconds += 1
    counting = True
    while counting == True:
        
        if uart.any():
            data = uart.read()
            value = data.decode()
            print(value)
            if value == "Stop":
                counting == False
                waiting()
            else:
                pass
        else:
            seconds += 0.1

            if seconds >= 60:
                seconds = 0
                time.sleep(0.1)  # 0.1s precision
                minutes += 1
            elif minutes == 10:
                minutes = 0
                seconds = 0
                time.sleep(0.1)
            else:
                time.sleep(0.1)
                display_float(seconds)

# Initialize UART0
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

waiting()




        



