import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm=GPIO.PWM(18,50)

pwm.start(0)  # Start PWM with 0% duty cycle

def set_angle(angle):

    duty_cycle = 7.5 + (angle / 180.0) * 10# Map angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to move to the position


def servo_sweep():


    while True:
        for angle in range(0, 180, 1):  # Sweep from 0 to 180 degrees
            set_angle(angle)
        for angle in range(180, -1, -1):  # Sweep from 180 to 0 degrees
            set_angle(angle)


try:
    servo_sweep()
except KeyboardInterrupt:
    print("\nExiting program...")
finally:
    pwm.stop()
    GPIO.cleanup()

