from machine import I2C, Pin

# Initialize I2C bus 0 (SDA on GPIO 2, SCL on GPIO 3)
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)  # 100kHz speed
slave_address = 0x61

print("Pico I2C slave initialized and listening at address", hex(slave_address))

while True:
    try:
        # Wait for data from the master
        data = i2c.readfrom(slave_address, 16)  # Read up to 16 bytes
        if data:
            print("Data received:", data)
        # Optionally, write a response to the master
        i2c.writeto(slave_address, b"Hello from Pico")
    except OSError as e:
        pass  # Ignore errors if no communication happens yet
