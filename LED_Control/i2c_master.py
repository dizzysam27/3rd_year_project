import smbus
import time

SLAVE_ADDRESS = 0x47  # I2C address of Arduino

# Create an SMBus instance
bus = smbus.SMBus(1)  # Use 1 for Raspberry Pi 3/4/5

def communicate_with_arduino():
    try:
        # Send a test byte (100) to the Arduino
        bus.write_byte(SLAVE_ADDRESS, 100)
        print("Sent to Arduino: 100")
        
        time.sleep(0.1)  # Delay to allow Arduino to process the data

        # Read a byte from the Arduino
        received_byte = bus.read_byte(SLAVE_ADDRESS)
        print(f"Received from Arduino: {received_byte}")
    except Exception as e:
        print(f"Error: {e}")

while True:
    communicate_with_arduino()
    time.sleep(1)  # Repeat every second
