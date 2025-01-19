import RPi.GPIO as GPIO
from Controller import MODE_MANAGER

class PHYSICAL_BUTTONS:
    
    def __init__(self):

        self.BUTTON_PIN_1 = 4
        self.BUTTON_PIN_2 = 17
        self.BUTTON_PIN_3 = 20

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.BUTTON_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.mode_manager = MODE_MANAGER()

    def button1_callback(self, channel):
        self.mode_manager.handle_input(1)

    def button2_callback(self, channel):
        self.mode_manager.handle_input(2)

    def button3_callback(self, channel):
        self.mode_manager.handle_input(3)
        
    def event_detect(self):
        GPIO.add_event_detect(self.BUTTON_PIN_1, GPIO.RISING, callback=self.button1_callback, bouncetime=500)
        GPIO.add_event_detect(self.BUTTON_PIN_2, GPIO.RISING, callback=self.button2_callback, bouncetime=500)
        GPIO.add_event_detect(self.BUTTON_PIN_3, GPIO.RISING, callback=self.button3_callback, bouncetime=500)
    
    def cleanup(self):
        GPIO.cleanup()