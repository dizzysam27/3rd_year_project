import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm=GPIO.PWM(18,50)

pwm.start(0)

pwm.ChangeDutyCycle(7.5)
sleep(10)

pwm.ChangeDutyCycle(10)
sleep(10)
pwm.ChangeDutyCycle(7.5)
sleep(10)
pwm.ChangeDutyCycle(4)
sleep(10)

# pwm.ChangeDutyCycle(4.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(1.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(7.5)
# sleep(0.1)
# pwm.ChangeDutyCycle(0)

