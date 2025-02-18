import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685
import time

motors = PCA9685()

motors.setServoPulse(1,1870)
motors.setServoPulse(0,1925)

