import cv2
import numpy as np
import time
from simple_pid import PID
from Peripherals.Motor_Control import PCA9685
from Peripherals.Gyro_Control import LSM6DS3

gyro = LSM6DS3()
motors = PCA9685()

def get_flat_values():
    defaultx = 1860
    defaulty = 1920
    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))
    return defaultx, defaulty
x1,y1 = get_flat_values()

def gyro_flat_values():
    servo_start_x = 1800
    servo_start_y = 1800
    gyro.initialize_sensor()
    print("LSM6DS3 Initialized")
    
    motors.setServoPulse(0, int(servo_start_y))
    motors.setServoPulse(1, int(servo_start_x))
    
    
    
    
    data = gyro.get_sensor_data()
    x_data, y_data, z_data = (data['gyro_x']),(data['gyro_y']),(data['gyro_z'])
    
    print(f"Gyro (°/s): X={x_data}, Y={y_data}, Z={z_data}")
    
    
#def motor_pan()