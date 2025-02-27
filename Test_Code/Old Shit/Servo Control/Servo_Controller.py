import RPi.GPIO as GPIO
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
myFactory = PiGPIOFactory()
from gpiozero import Servo
myServo = Servo(18,min_pulse_width = 0.05/1000,max_pulse_width=2.5/1000,pin_factory=myFactory)
myServo.value = -0.2

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm=GPIO.PWM(18,50)

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
# pwm.ChangeDutyCycle(4.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(1.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(7.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(0)

