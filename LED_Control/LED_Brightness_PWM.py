import pigpio 
import math
import time

LED_drive = pigpio.pi()
Max_Duty = 70
LED_drive.set_mode(18, pigpio.OUTPUT)	#Is this line needed? The line below should automatically take care of it, no?
LED_drive.hardware_PWM(18,1000,Max_Duty*1000)


# testing
for x in range (0,Max_Duty,1):
   LED_drive.hardware_PWM(18,1000,x*1000)
   time.sleep(0.1)

# while True:
#     for y in range (0,np.pi,0.01):
#         test_duty = Max_Duty * np.sin(y)
#         LED_drive.change_duty_cycle(test_duty)
#         time.sleep(0.05)

# def LED_control (Duty, Stop):
#     if Stop == 1:
#         LED_drive.stop()
#     else:
#         LED_drive.start(1)
#         if Duty >= Max_Duty:
#             LED_drive.change_duty_cycle(Max_Duty)
#         else:
#             LED_drive.change_duty_cycle(Duty)
            
# LED_control(10,0)

