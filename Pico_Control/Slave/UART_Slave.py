from machine import Pin, UART, ADC
import time

class JOYSTICK_PICO:

    def __init__(self):

        self.uart0 = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))
        self.xAxis = ADC(27)
        self.yAxis = ADC(26)
        self.JoyButton = Pin(2, Pin.IN, Pin.PULL_UP)

    def UARTtx(self,dataIn, uartName):
        try:
            uartName.write(dataIn + "\n")
            print("Sent:", dataIn)
        except Exception as e:
            print("Error sending data:", e)

    # Read Joystick Value
    def readJoy(self,axis):
        raw = axis.read_u16()
        return int((((200 * raw)) / 65535)-100)

    def run(self):
        
        joyx = self.readJoy(self.xAxis)
        joyy = self.readJoy(self.yAxis)
        buttonValue = int(not self.JoyButton.value())

        print(f"X: {joyx}, Y: {joyy}, Button: {buttonValue}",flush=True)
        
        dataTx = f"{joyx},{joyy},{buttonValue}"

        self.UARTtx(dataTx, self.uart0)

if __name__ == "__main__":

  joystick = JOYSTICK_PICO()

  while True:
      joystick.run()
      time.sleep(0.1)

