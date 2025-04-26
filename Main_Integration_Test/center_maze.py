import numpy as np
import time
from Peripherals.Motor_Control import PCA9685
from Peripherals.Gyro_Control import LSM6DS3

gyro = LSM6DS3()
motors = PCA9685()

def get_flat_values():
    defaultx = 1849
    defaulty = 1939
    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))
    return defaultx, defaulty
x1,y1 = get_flat_values()

def gyro_flat_values():
    # Pan over assumes start values to find true flat values.
    # Return the servo pulse values for flat level

    # Set servo pulse range and approximate centre
    servo_levels = np.arange(-50,50,5).tolist()
    servo_start_yx = [1930,1850]

    gyro.initialize_sensor()
    print("LSM6DS3 Initialized")

    # Set servo motors to assumed default value
    motors.setServoPulse(0, int(servo_start_yx[0]))
    motors.setServoPulse(1, int(servo_start_yx[1]))
    time.sleep(0.3)
    pulse_y_x = [0,0]
    for servo in range(2):
        gyro_results = []
        for offset in servo_levels:
            pulse = servo_start_yx[servo] + offset
            motors.setServoPulse(servo, int(pulse + 25))
            time.sleep(0.1)
            motors.setServoPulse(servo, int(pulse))
            time.sleep(0.3)
            gyro_data = gyro.get_sensor_data()
            print(f"Accel (g): X={gyro_data['accel_x']:.4f}, Y={gyro_data['accel_y']:.4f}, Z={gyro_data['accel_z']:.4f}")
            # X adb Y values swapped due to orientation of Gyroscope
            # on maze board 
            gyro_yx = [(gyro_data['accel_x']),(gyro_data['accel_y'])]
            gyro_results.append(gyro_yx[servo])

        gyro_results = np.array(gyro_results)
        print(gyro_results)
        flat_index = int(np.abs(gyro_results).argmin())
        pulse_y_x[servo] = int(servo_start_yx[servo] + servo_levels[flat_index])

        motors.setServoPulse(servo, pulse_y_x[int(servo)])

    motors.setServoPulse(0,int(pulse_y_x[0]))
    motors.setServoPulse(1,int(pulse_y_x[1]))
    return pulse_y_x
    #data = gyro.get_sensor_data()
    #x_data, y_data, z_data = (data['gyro_x']),(data['gyro_y']),(data['gyro_z'])
    #print(f"Gyro (°/s): X={x_data}, Y={y_data}, Z={z_data}")

# get_flat_values()
# Values = gyro_flat_values()
# print(Values)
    
#def motor_pan()