import smbus
import time

# Grove 6-axis accelerometer and gyroscope I2C address
I2C_ADDRESS = 0x6a

# Register addresses for the MPU6050 (Grove 6-Axis)
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize I2C bus
bus = smbus.SMBus(1)  # Bus 1 for Raspberry Pi

# Wake up the MPU6050 (by default, it is in sleep mode)
bus.write_byte_data(I2C_ADDRESS, PWR_MGMT_1, 0)

# Function to read data from a specific register (2 bytes)
def read_word(register):
    high = bus.read_byte_data(I2C_ADDRESS, register)
    low = bus.read_byte_data(I2C_ADDRESS, register + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value -= 0x10000
    return value

# Function to convert the raw accelerometer data to 'g'
def read_accel_data():
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)
    
    return accel_x, accel_y, accel_z

# Function to convert the raw gyroscope data to degrees per second
def read_gyro_data():
    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_XOUT_H + 2)
    gyro_z = read_word(GYRO_XOUT_H + 4)
    
    return gyro_x, gyro_y, gyro_z

try:
    while True:
        # Read and print accelerometer and gyroscope data
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        
        print(f"Accelerometer (g): X={accel_x}, Y={accel_y}, Z={accel_z}")
        print(f"Gyroscope (°/s): X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

