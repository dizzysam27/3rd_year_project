import RPi.GPIO as GPIO
import time

BUTTON_PIN_1 = 4
BUTTON_PIN_2 = 17
BUTTON_PIN_3 = 20
BUTTON_PIN_4 = 7
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.wait_for_edge(BUTTON_PIN_1,GPIO.BOTH)
# print("Button has been pressed")

def button1_released_callback(channel):
    print("Button1 has just been released")
def button2_released_callback(channel):
    print("Button2 has just been released")
def button3_released_callback(channel):
    print("Button3 has just been released")
def button4_released_callback(channel):
    print("Button4 has just been released")

GPIO.add_event_detect(BUTTON_PIN_1,GPIO.RISING,callback=button1_released_callback,bouncetime=500)
GPIO.add_event_detect(BUTTON_PIN_2,GPIO.RISING,callback=button2_released_callback,bouncetime=500)
GPIO.add_event_detect(BUTTON_PIN_3,GPIO.RISING,callback=button3_released_callback,bouncetime=500)
GPIO.add_event_detect(BUTTON_PIN_4,GPIO.RISING,callback=button4_released_callback,bouncetime=50)

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()