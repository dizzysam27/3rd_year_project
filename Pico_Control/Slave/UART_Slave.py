from machine import Pin, UART, ADC  # type: ignore
import time

class JOYSTICK:
    
    def __init__(self):
        # UART Protocol
        self.uart0 = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

        # Joystick and Button
        self.xAxis = ADC(27)
        self.yAxis = ADC(26)
        self.JoyButton = Pin(2, Pin.IN, Pin.PULL_UP)

    # UART Transmit Function
    def UARTtx(self,dataIn, uartName):
        try:
            uartName.write(dataIn + "\n")
            print("Sent:", dataIn)
        except Exception as e:
            print("Error sending data:", e)

    # Read Joystick Value
    def readJoy(self,axis):
        raw = axis.read_u16()
        return int(((200 * raw)) / 65535)

    def run(self):
    
        joyx = -(self.readJoy(self.xAxis))+100
        joyy = -(self.readJoy(self.yAxis))+100
        # Read Joystick and Button
        
        if (joyx < 100):
            xValue = joyx
        elif (joyx > 100):
            xValue = joyx
        
        
        if (joyy < 100):
            yValue = joyy 
        elif (joyy > 100):
            yValue = joyy 
        
        
        buttonValue = int(not self.JoyButton.value())

        # Pack Data
        dataTx = f"{joyx},{joyy},{buttonValue}"

        # Transmit Data
        self.UARTtx(dataTx, self.uart0)
        time.sleep(0.1)

while True:
    JOYSTICK().run()
   
    