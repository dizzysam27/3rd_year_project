from gpiozero import Button, LED # type: ignore
from signal import pause

# import time

# PHYSICAL BUTTONS class
class PHYSICAL_BUTTONS:
    
    # Init function
    # Required input:  GUI Class
    #                  |    LED Control Class
    #                  V    V
    def __init__(self, gui, led_control):

        self.gui = gui

        # Define LED button numbers according to config file
        self.BUTTON_PIN_1 = Button(26, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_2 = Button(19, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_3 = Button(13, pull_up=True,bounce_time=0.1)

        # Create instance of MODE_MANAGER
        from Controller import MODE_MANAGER
        self.mode_manager = MODE_MANAGER(self.gui, led_control)

        # gpiozero when_pressed triggers mode_handle.input to the relevant button
        self.BUTTON_PIN_1.when_pressed = lambda: self.mode_manager.handle_input(1)
        self.BUTTON_PIN_2.when_pressed = lambda: self.mode_manager.handle_input(2)
        self.BUTTON_PIN_3.when_pressed = lambda: self.mode_manager.handle_input(3)


    def cleanup(self):
        # gpiozero does not require manual GPIO cleanup
        pass

# LED CONTROL Class
class LED_CONTROL:

    # Init function - no dependencies
    def __init__(self):
        global GREEN_LED, RED_LED, BLUE_LED

        # Define LED pin numbers according to config file
        GREEN_LED = LED(20)
        RED_LED = LED(21)
        BLUE_LED = LED(16)

    # Set LED funnction
    # Required input: Green LED State (1 or 0)
    #                 |      Red LED State (1 or 0)
    #                 |      |    Blue LED State (1 or 0)
    #                 V      V    V
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
            
# leds = LED_CONTROL()
# while True:
#     leds.set_led(0,1,1)