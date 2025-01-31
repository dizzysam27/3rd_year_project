from gpiozero import Button, LED
from signal import pause
# import time

#hello

"""
This class controls the physical buttons on the control panel. Initialising this class creates a callback for when each button is pressed.
The buttons are also illuminated to indicate the options available to the user. 
"""
class PHYSICAL_BUTTONS:
    
    def __init__(self, gui, led_control):
        from Controller import MODE_MANAGER

        self.gui = gui

        self.BUTTON_PIN_1 = Button(26, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_2 = Button(19, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_3 = Button(13, pull_up=True,bounce_time=0.1)

        self.mode_manager = MODE_MANAGER(self.gui, led_control)


        self.BUTTON_PIN_1.when_pressed = lambda: self.mode_manager.handle_input(1)
        self.BUTTON_PIN_2.when_pressed = lambda: self.mode_manager.handle_input(2)
        self.BUTTON_PIN_3.when_pressed = lambda: self.mode_manager.handle_input(3)


    def cleanup(self):
        # gpiozero does not require manual GPIO cleanup
        pass


class LED_CONTROL:

    def __init__(self):
        global GREEN_LED, RED_LED, BLUE_LED

        GREEN_LED = LED(21)
        RED_LED = LED(16)
        BLUE_LED = LED(20)


    def set_led(self, green, red, blue):

        if green == 1:
            GREEN_LED.on()
        else:
            GREEN_LED.off()

        if red == 1:
            RED_LED.on()
        else:
            RED_LED.off()
        
        if blue == 1:
            BLUE_LED.on()
        else:
            BLUE_LED.off()

# a = LED_CONTROL()
# while True:
#     a.set_led(1,1,1)
#     time.sleep(1)
#     a.set_led(0,0,0)
#     time.sleep(1)

