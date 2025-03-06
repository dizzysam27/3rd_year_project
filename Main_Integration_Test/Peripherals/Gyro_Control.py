import smbus
import time

# LSM6DS3 I2C address
LSM6DS3_ADDR = 0x6A  # Default address

# Register addresses
CTRL1_XL = 0x10  # Accelerometer control
CTRL2_G = 0x11   # Gyroscope control
OUTX_L_XL = 0x28  # Accelerometer data register
OUTX_L_G = 0x22   # Gyroscope data register

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use I2C bus 1

def initialize_sensor():
    # Set accelerometer to 2g range, 104 Hz output data rate
    bus.write_byte_data(LSM6DS3_ADDR, CTRL1_XL, 0x40)
    # Set gyroscope to 250 dps range, 104 Hz output data rate
    bus.write_byte_data(LSM6DS3_ADDR, CTRL2_G, 0x40)

def read_raw_data(addr):
    # Read two bytes of data from the specified address
    low = bus.read_byte_data(LSM6DS3_ADDR, addr)
    high = bus.read_byte_data(LSM6DS3_ADDR, addr + 1)
    
    # Combine high and low values
    value = (high << 8) | low
    
    # Convert to signed value
    if value > 32767:
        value -= 65536
    return value

def get_sensor_data():
    accel_x = read_raw_data(OUTX_L_XL) / 16384.0  # Convert to g
    accel_y = read_raw_data(OUTX_L_XL + 2) / 16384.0
    accel_z = read_raw_data(OUTX_L_XL + 4) / 16384.0
    
    gyro_x = read_raw_data(OUTX_L_G) / 131.0  # Convert to degrees/sec
    gyro_y = read_raw_data(OUTX_L_G + 2) / 131.0
    gyro_z = read_raw_data(OUTX_L_G + 4) / 131.0
    
    return {
        "accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z,
        "gyro_x": gyro_x, "gyro_y": gyro_y, "gyro_z": gyro_z
    }

if __name__ == "__main__":
    initialize_sensor()
    print("LSM6DS3 Initialized")
    
    try:
        while True:
            data = get_sensor_data()
            #print(f"Accel (g): X={data['accel_x']:.2f}, Y={data['accel_y']:.2f}, Z={data['accel_z']:.2f}")
            print(f"Gyro (°/s): X={data['gyro_x']:.2f}, Y={data['gyro_y']:.2f}, Z={data['gyro_z']:.2f}")
            #print("-----------------------")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Measurement stopped")

