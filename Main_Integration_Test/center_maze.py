import numpy as np
import time
from Peripherals.Motor_Control import PCA9685
from Peripherals.Gyro_Control import LSM6DS3

gyro = LSM6DS3()
motors = PCA9685()


def get_flat_values():
    # Manually set flat values to skip calibrating each time 
    
    defaultx = 1849
    defaulty = 1940
    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))
    return defaultx, defaulty

    # Tilt maze above and below assumes start values to find true flat values.
    # Return the servo pulse for determined flat level
    
def gyro_flat_values():
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
            
            # Initially move servo far from the test pulse location to reduce servo errors
            # This is as servos appear to respond less accurately to pulse changes > 10
            motors.setServoPulse(servo, int(pulse + 25))
            time.sleep(0.1)
            
            motors.setServoPulse(servo, int(pulse))
            time.sleep(0.3)
            
            # Read accelerometer values from gyroscope
            gyro_data = gyro.get_sensor_data()
            #print(f"Accel (g): X={gyro_data['accel_x']:.4f}, Y={gyro_data['accel_y']:.4f}, Z={gyro_data['accel_z']:.4f}")
            
            # X anb Y values swapped due to orientation of Gyroscope
            # on maze board 
            gyro_yx = [(gyro_data['accel_x']),(gyro_data['accel_y'])]
            gyro_results.append(gyro_yx[servo])

        gyro_results = np.array(gyro_results)
        print(gyro_results)
        
        # Return index and pulse of flattest reading
        flat_index = int(np.abs(gyro_results).argmin())
        pulse_y_x[servo] = int(servo_start_yx[servo] + servo_levels[flat_index])

        motors.setServoPulse(servo, pulse_y_x[int(servo)])

    # Set servos to flat pulse location and return values
    motors.setServoPulse(0,int(pulse_y_x[0]))
    motors.setServoPulse(1,int(pulse_y_x[1]))
    return pulse_y_x

get_flat_values()
# Values = gyro_flat_values()
# print(Values)
    