import RPi.GPIO as GPIO
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
myFactory = PiGPIOFactory()
from gpiozero import Servo as LEDPWM
LED1 = LEDPWM(18,min_pulse_width = 0.01/1000,max_pulse_width=8/10,pin_factory=myFactory)
LED1.value = -1

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm=GPIO.PWM(18,1000)

pwm.start(0)

pwm.ChangeDutyCycle(7.5)
sleep(2)

pwm.ChangeDutyCycle(8.5)
sleep(2)
pwm.ChangeDutyCycle(6.5)
sleep(2)
pwm.ChangeDutyCycle(7.5)
sleep(2)
pwm.stop() 
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

