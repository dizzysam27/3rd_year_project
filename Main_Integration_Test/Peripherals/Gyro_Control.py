# Reference software: https://github.com/worldsensing/grove-pi-LSM6DS3-python/blob/main/src/LSM6DS3.py , https://github.com/wrh2/LSM6DS3
# License: https://choosealicense.com/licenses/mit/

import smbus
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

## Gyro as a class test START

class LSM6DS3:
    # LSM6DS3 I2C address
    LSM6DS3_ADDR = 0x6A  # Default address

    # Register addresses
    CTRL1_XL = 0x10  # Accelerometer control
    CTRL2_G = 0x11   # Gyroscope control
    OUTX_L_XL = 0x28  # Accelerometer data register
    OUTX_L_G = 0x22   # Gyroscope data register
    def __init__(self):
        # Initialize I2C bus
        self.bus = smbus.SMBus(1)  # Use I2C bus 1

    def initialize_sensor(self):
        # Set accelerometer to 2g range, 104 Hz output data rate
        self.bus.write_byte_data(self.LSM6DS3_ADDR, self.CTRL1_XL, 0x40)
        # Set gyroscope to 250 dps range, 104 Hz output data rate
        self.bus.write_byte_data(self.LSM6DS3_ADDR, self.CTRL2_G, 0x40)

    def read_raw_data(self, addr):
        # Read two bytes of data from the specified address
        low = self.bus.read_byte_data(self.LSM6DS3_ADDR, addr)
        high = self.bus.read_byte_data(self.LSM6DS3_ADDR, addr + 1)
        
        # Combine high and low values
        value = (high << 8) | low
    
        # Convert to signed value
        if value > 32767:
            value -= 65536
        return value

    def get_sensor_data(self):
        accel_x = self.read_raw_data(self.OUTX_L_XL) / 16384.0  # Convert to g
        accel_y = self.read_raw_data(self.OUTX_L_XL + 2) / 16384.0
        accel_z = self.read_raw_data(self.OUTX_L_XL + 4) / 16384.0
    
        gyro_x = self.read_raw_data(self.OUTX_L_G) / 131.0  # Convert to degrees/sec
        gyro_y = self.read_raw_data(self.OUTX_L_G + 2) / 131.0
        gyro_z = self.read_raw_data(self.OUTX_L_G + 4) / 131.0
    
        return {
            "accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z,
            "gyro_x": gyro_x, "gyro_y": gyro_y, "gyro_z": gyro_z
        }

