from gpiozero import Button, LED
from signal import pause
from Controller import MODE_MANAGER

"""
This class controls the physical buttons on the control panel. Initialising this class creates a callback for when each button is pressed.
The buttons are also illuminated to indicate the options available to the user. 
"""
class PHYSICAL_BUTTONS:
    
    def __init__(self, gui):
        self.gui = gui

        self.BUTTON_PIN_1 = Button(26, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_2 = Button(19, pull_up=True,bounce_time=0.1)
        self.BUTTON_PIN_3 = Button(13, pull_up=True,bounce_time=0.1)

        self.GREEN_LED = LED(13)
        self.RED_LED = LED(19)
        self.BLUE_LED = LED(19)

        self.set_led(1,1,1) # Illuminates all leds

        self.mode_manager = MODE_MANAGER(self.gui)


        self.BUTTON_PIN_1.when_pressed = lambda: self.mode_manager.handle_input(1)
        self.BUTTON_PIN_2.when_pressed = lambda: self.mode_manager.handle_input(2)
        self.BUTTON_PIN_3.when_pressed = lambda: self.mode_manager.handle_input(3)

    def cleanup(self):
        # gpiozero does not require manual GPIO cleanup
        pass
    
    """
    This function within the PHYSICAL_BUTTONS class allows for the desired buttons to be illuminated
    """
    def set_led(self,green,red,blue):

        if green == 1:
            self.GREEN_LED.on()
        else:
            self.GREEN_LED.off()
        
        if red == 1:
            self.RED_LED.on()
        else:
            self.RED_LED.off()
        
        if blue == 1:
            self.BLUE_LED.on()
        else:
            self.BLUE_LED.off()

        