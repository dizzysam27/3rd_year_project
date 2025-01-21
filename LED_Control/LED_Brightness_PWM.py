from rpi_hardware_pwm import HardwarePWM
import math
import time
import numpy as np

Max_Duty = 70

LED_drive = HardwarePWM(pwm_channel=0, hz=1000, chip=2)
LED_drive.start(1) # Start at 10% Duty Cycle


# testing
for x in range (0,Max_Duty,1):
   LED_drive.change_duty_cycle(x) 
   time.sleep(0.1)

while True:
    for y in range (0,np.pi,0.01):
        test_duty = Max_Duty * np.sin(y)
        LED_drive.change_duty_cycle(test_duty)
        time.sleep(0.05)

def LED_control (Duty, Stop):
    if Stop == 1:
        LED_drive.stop()
    else:
        LED_drive.start(1)
        if Duty >= Max_Duty:
            LED_drive.change_duty_cycle(Max_Duty)
        else:
            LED_drive.change_duty_cycle(Duty)
            
LED_control(10,0)

