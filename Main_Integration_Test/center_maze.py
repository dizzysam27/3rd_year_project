import cv2
import numpy as np
import time
from simple_pid import PID
from Peripherals.Motor_Control import PCA9685
from Peripherals.Gyro_Control import LSM6DS3

gyro = LSM6DS3()
motors = PCA9685()

def get_flat_values():
    defaultx = 1847
    defaulty = 1933
    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))
    return defaultx, defaulty
x1,y1 = get_flat_values()

def gyro_flat_values():
    servo_levels = np.arange(1800,2000,10).tolist()
    gyro_results = []
    servo_start_x = 1800
    servo_start_y = 1800
    gyro.initialize_sensor()
    print("LSM6DS3 Initialized")
    motors.setServoPulse(0, int(servo_start_y))
    motors.setServoPulse(1, int(servo_start_x))
    time.sleep(0.3)
    pos_y_x = []
    for servo in range(2):
        gyro_results = []
        for pos in servo_levels:
            motors.setServoPulse(servo, int(pos))
            time.sleep(0.1)
            gyro_data = gyro.get_sensor_data()
            print(f"Gyro (°/s): X={gyro_data['gyro_x']}, Y={gyro_data['gyro_y']}, Z={gyro_data['gyro_z']}")
            gyro_yx = [(gyro_data['gyro_y']),(gyro_data['gyro_x'])]
            gyro_results[(servo_levels.index(pos))] = gyro_xy(servo)
        gyro_results = np.array(gyro_results)
        pos_y_x(servo)= gyro_results.argmax()
    motors.setServoPulse(0,int(pos_y_x(0)))
    motors.setServoPulse(1,int(pos_y_x(1)))
    return pos_y_x
    #data = gyro.get_sensor_data()
    #x_data, y_data, z_data = (data['gyro_x']),(data['gyro_y']),(data['gyro_z'])
    
    print(f"Gyro (°/s): X={x_data}, Y={y_data}, Z={z_data}")
    
    
#def motor_pan()