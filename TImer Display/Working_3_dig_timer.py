from machine import Pin
import time


segments = {
    "digit1": [22, 17, 6, 27, 5, 21, 18, 28],  # 8-segment with dp
    "digit2": [19, 16, 10, 8, 7, 20, 9, 11],  # 8-segment with dp
    "digit3": [13, 12, 4, 3, 2, 15, 14],  # 7-segment
}

# Create a dictionary to hold the initialized Pin objects
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
    if digit_name not in pins:
        raise ValueError(f"Invalid digit name: {digit_name}")
    if number not in number_to_segments:
        raise ValueError(f"Invalid number: {number}")

    if len(pins[digit_name]) == 8:
        segment_states = number_to_segments_with_dp[number]
        segment_states[-1] = 1 if dp else 0
    elif len(pins[digit_name]) == 7:
        segment_states = number_to_segments[number]
    else:
        raise ValueError(f"Unsupported number of segments for {digit_name}")

    clear_digit(digit_name)

    for i, state in enumerate(segment_states):
        pins[digit_name][i].value(state)

# Display floating-point number
def display_float(value):
    int_part = int(value)
    frac_part = int((value - int_part) * 10)
    clear_digit("digit2")
    clear_digit("digit1")
    clear_digit("digit3")

    digit1 = int_part // 10
    digit2 = int_part % 10
    digit3 = frac_part
    
    display_number("digit1", digit1)
    display_number("digit2", digit2, dp=True)
    display_number("digit3", digit3)
    

# Counter loop
counter = 0.0
while True:
    try:
        display_float(counter)
        counter += 0.1
        if counter >= 100:
            counter = 0.0
        time.sleep(0.1)  # 0.1s precision
    except Exception as e:
        print(f"Error: {e}")
        break
