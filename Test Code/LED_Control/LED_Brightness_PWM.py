from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)

while True:
    led.value = 0 
    sleep(2)
    led.value = 0.009
    sleep(2)
    led.value = 0.01  
    sleep(2)
    led.value = 1  
    sleep(2)
# from gpiozero.pins.pigpio import PiGPIOFactory
# myFactory = PiGPIOFactory()
# from gpiozero import LED
# LED1 = LED(18,pin_factory=myFactory)
# LED1.value = -1
# LED=18 
# GPIO.setmode( GPIO.BCM )
# GPIO.setup(LED, GPIO.OUT )
# pwm=GPIO.PWM(LED,1000)

# pwm.start(5)

# pwm.ChangeDutyCycle(7.5)
# sleep(2)

# pwm.ChangeDutyCycle(8.5)
# sleep(2)
# pwm.ChangeDutyCycle(6.5)
# sleep(2)
# pwm.ChangeDutyCycle(7.5)
# sleep(2)
# pwm.stop() 
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

