import cv2
import numpy as np
import time
from simple_pid import PID
from Peripherals.Motor_Control import PCA9685

motors = PCA9685()

def get_flat_values():
    defaultx = 1870
    defaulty = 1920


    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))

    return defaultx, defaulty


x1,y1 = get_flat_values()