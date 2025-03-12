from gpiozero import LED

class LEDBUTTON():
    def __init__(self):
        self.redLED = LED(21)
        self.greenLED = LED(20)
        self.blueLED = LED(16)

    def setLED(self, r, g, b):
        ledArray = [self.redLED, self.greenLED, self.blueLED]
        stateArray = [r, g, b]
        for i in range(3):
            if stateArray[i] == 0:
                ledArray[i].off()
            elif stateArray[i] == 1:
                ledArray[i].on()
            else:
                pass