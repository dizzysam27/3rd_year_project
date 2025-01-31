import utime
from i2c_slave import I2CSlave

# I2C setup
i2c = I2CSlave(0, scl=9, sda=8, addr=0x42)

while True:
    result = i2c.request()
    if result == I2CSlave.RECEIVE:
        received_data = i2c.read(16)  # Read up to 16 bytes
        if received_data:
            command = received_data.decode('utf-8').strip()
            print(f"Received: {command}")
            # Add your command handling logic here
    utime.sleep(0.1)
