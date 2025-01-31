from machine import Pin, I2C, Timer
import utime

# Setup I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)

# Define GPIO for 7-segment display
segments = [Pin(i, Pin.OUT) for i in range()]  # Change GPIO pins as needed
common_pins = [Pin(16, Pin.OUT), Pin(17, Pin.OUT)]  # Pins for two digits

# Digit to 7-segment mapping
digit_map = [
    [1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 1, 1, 0, 0, 1, 1],  # 4
    [1, 0, 1, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1],  # 6
    [1, 1, 1, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 1, 0, 1, 1],  # 9
]

# Initialize variables
timer_running = False
time_elapsed = 0  # Time in tenths of a second

def display_number(num):
    tens = num // 10
    ones = num % 10

    # Display tens
    common_pins[0].on()
    common_pins[1].off()
    for seg, state in zip(segments, digit_map[tens]):
        seg.value(state)
    utime.sleep_ms(5)

    # Display ones
    common_pins[0].off()
    common_pins[1].on()
    for seg, state in zip(segments, digit_map[ones]):
        seg.value(state)
    utime.sleep_ms(5)

def timer_callback(timer):
    global time_elapsed, timer_running
    if timer_running:
        time_elapsed += 1
        if time_elapsed >= 100:  # Reset after 10 seconds
            time_elapsed = 0

# Timer for 0.1s increments
tim = Timer()
tim.init(period=100, mode=Timer.PERIODIC, callback=timer_callback)

def read_i2c_commands():
    global timer_running
    try:
        if i2c.any():
            data = i2c.readfrom(0x10, 1)  # Replace 0x10 with your Pico's I2C address
            command = data[0]
            if command == 1:  # Start command
                timer_running = True
            elif command == 0:  # Stop command
                timer_running = False
    except:
        pass

while True:
    read_i2c_commands()
    display_number(time_elapsed)
