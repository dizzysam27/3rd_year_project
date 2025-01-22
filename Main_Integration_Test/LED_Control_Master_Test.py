import smbus
import time

class LEDControl:

    def __init__(self, bus_number=1, arduino_address=0x08):
        self.bus = smbus.SMBus(bus_number)  # Initialize the I2C bus
        self.arduino_address = arduino_address

    def send_color(self, color):
        # Prepare data as a list of ASCII values, appending a newline
        data = [ord(char) for char in color] + [ord('\n')]
        try:
            # Send the data block
            self.bus.write_i2c_block_data(self.arduino_address, 0, data)
            print(f"Sent color: {color}")
        except OSError as e:
            print(f"Error sending color {color}: {e}")


# Example usage
if __name__ == "__main__":
    led_control = LEDControl()

    colors = ["Red"]
    for color in colors:
        led_control.send_color(color)
        time.sleep(1)  # Delay to observe the effect
