import smbus
import time

# I2C bus (1 for Raspberry Pi 2 and later)
bus = smbus.SMBus(1)

# I2C address of the Arduino
SLAVE_ADDRESS1 = 0x08
SLAVE_ADDRESS2 = 0x47

def write_to_arduino1(value):
    try:
        bus.write_byte(SLAVE_ADDRESS1, value)
        print(f"Sent {value} to Arduino")
    except Exception as e:
        print(f"Error: {e}")

def read_from_arduino1():
    try:
        data = bus.read_i2c_block_data(SLAVE_ADDRESS1, 0, 20) # Read up to 16 bytes
        return ''.join(chr(byte) for byte in data)
    except Exception as e:
        print(f"Error: {e}")
        return ""

def write_to_arduino2(value):
    try:
        bus.write_byte(SLAVE_ADDRESS2, value)
        print(f"Sent {value} to Arduino")
    except Exception as e:
        print(f"Error: {e}")

def read_from_arduino2():
    try:
        data = bus.read_i2c_block_data(SLAVE_ADDRESS2, 0, 20) # Read up to 16 bytes
        return ''.join(chr(byte) for byte in data)
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
# Example usage
while True:
    write_to_arduino1(42)  # Send a value to Arduino
    write_to_arduino2(12)
    time.sleep(1)  # Wait for Arduino to respond
    response1 = read_from_arduino1()  # Read response from Arduino
    response2 = read_from_arduino2()
    print(f"Received Response 1: {response1}")
    print(f"Received Response 2: {response2}")
    time.sleep(1)
