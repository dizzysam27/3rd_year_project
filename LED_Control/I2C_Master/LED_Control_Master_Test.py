import smbus
import time

# Set up the I2C bus (1 is for Raspberry Pi 5)
bus = smbus.SMBus(1)
arduino_address = 0x08  # Address of Arduino

# Function to send color to Arduino
def send_color(color):
    bus.write_byte_data(arduino_address, 0, ord(color[0]))  # Send the first character of the color
    for char in color[1:]:
        bus.write_byte(arduino_address, ord(char))  # Send the rest of the characters
    print(f"Sent color: {color}")

# Example usage to send color data
send_color("Red")  # Send Red color to Arduino
time.sleep(1)

send_color("Green")  # Send Green color to Arduino
time.sleep(1)

send_color("Blue")  # Send Blue color to Arduino
time.sleep(1)

send_color("Chase")  # Start chase effect
time.sleep(1)

send_color("Red")  # Send Red again
