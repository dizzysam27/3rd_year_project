from gpiozero import PWMLED
from time import sleep
import numpy as np
class main_LED:

    def __init__(self):
        # Initialise the LED 
        self.LED = PWMLED(18, frequency = 2000)
        self.SetMax_value(1.0)
        self.LED_level(0.1)

    def LED_level(self,LED_value):
        # LED_value must be a float between 0 and 1, this code ensures no overvalue
        if LED_value >= 1.0:
            LED_value = 1.0
        elif LED_value <= 0.0:
            LED_value = 0.0
        else:
            pass
        
        self.LED_value = (LED_value * self.Max_value)
        self.LED.value = (self.LED_value)
        print(f"New LED Value : {self.LED_value}")


    def SetMax_value(self,Max_value):
        # Change these values to the desired maximum value
        # This is used to keep LED brightness a linear function 
        # in the event that 100% duty-cycle draws too much current  
        # from the power hat. 

        if Max_value >= 1.0:
            self.Max_value = 1.0
        elif Max_value <= 0.0:
            self.Max_value = 0.0
        else:
            self.Max_value = Max_value
        

    def sinewave_test(self):
        test = 0
        while test < 3:
            for x in range(1,179,1):
                y = np.sin(np.deg2rad(x))
                self.LED_level(y)
                sleep(0.01)
                test =+1

led1 = main_LED()

led1.sinewave_test()