from gpiozero import LED # type: ignore
import smbus # type: ignore
from PyQt5.QtCore import pyqtSignal, QThread

# i2c Bus Setup
bus = smbus.SMBus(1)

# LED Button Control Class
# Callable functions:
#        Red Button LED State (0 = Off, 1 = On)
#        |  Green Button LED State (0 = Off, 1 = On)
#        |  |  Blue Button LED State (0 = Off, 1 = On)
#        V  V  V
# setLED(r, g, b)
class LEDBUTTONCONTROL():
    def __init__(self):
        self.redLED = LED(21)
        self.greenLED = LED(20)
        self.blueLED = LED(16)

    def setLED(self, g=None, r=None, b=None):
        ledArray = [self.greenLED, self.redLED, self.blueLED]
        stateArray = [g, r, b]
        for i in range(3):
            if stateArray[i] == 0:
                ledArray[i].off()
            elif stateArray[i] == 1:
                ledArray[i].on()
            else:
                pass

# LED Strip Control Class
# Callable functions:
#              Colour Value (1 = Green, 2 = Red, 3 = Blue, 4 = White, 5 = Chase Effect)
#              V
# writeArduino(value)
ARDUINO_ADDRESS = 0x47 # Arduino Address
class LEDSTRIPCONTROL(QThread):
    printBuffer = pyqtSignal(str)

    def writeArduino(self,value):
        try:
            bus.write_byte(ARDUINO_ADDRESS, value)
            self.printBuffer.emit(f"Sent {value} to Arduino")
        except Exception as e:
            self.printBuffer.emit(f"Error: {e}")