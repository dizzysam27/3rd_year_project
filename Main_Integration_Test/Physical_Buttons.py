from gpiozero import Button
from signal import pause
from Controller import MODE_MANAGER

class PHYSICAL_BUTTONS:
    
    def __init__(self, gui):
        self.gui = gui

        self.BUTTON_PIN_1 = Button(4, pull_up=True,bounce_time=1000)
        self.BUTTON_PIN_2 = Button(17, pull_up=True,bounce_time=1000)
        self.BUTTON_PIN_3 = Button(20, pull_up=True,bounce_time=1000)

        self.mode_manager = MODE_MANAGER(self.gui)


        self.BUTTON_PIN_1.when_pressed = lambda: self.mode_manager.handle_input(1)
        self.BUTTON_PIN_2.when_pressed = lambda: self.mode_manager.handle_input(2)
        self.BUTTON_PIN_3.when_pressed = lambda: self.mode_manager.handle_input(3)

    def cleanup(self):
        # gpiozero does not require manual GPIO cleanup
        pass
