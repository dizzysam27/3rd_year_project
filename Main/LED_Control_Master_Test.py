import smbus
import time

class LED_CONTROL:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.arduino_address = 0x08  # Address of Arduino

    def send_color(self,color):
        self.bus.write_byte_data(self.arduino_address, 0, ord(color[0]))  # Send the first character of the color
        for char in color[1:]:
            self.bus.write_byte(self.arduino_address, ord(char))  # Send the rest of the characters
        print(f"Sent color: {color}")

# Example usage to send color data

LED_Control = LED_CONTROL()
LED_Control.send_color("Red")  # Send Red color to Arduino
time.sleep(1)

LED_Control.send_color("Green")  # Send Green color to Arduino
time.sleep(1)

LED_Control.send_color("Blue")  # Send Blue color to Arduino
time.sleep(1)

LED_Control.send_color("Chase")  # Start chase effect
time.sleep(1)

LED_Control.send_color("Red")  # Send Red again
