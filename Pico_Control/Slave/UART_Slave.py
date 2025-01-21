from machine import Pin, UART, ADC
import time

class JOYSTICK_PICO:

    def __init__(self):
        
        self.segments = SEGMENT_DISPLAYS()
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

        # self.segments.display_number(1234)

class SEGMENT_DISPLAYS:

    def __init__(self):
        # Pin mapping for 4 CD4511BE ICs (each controls a 7-segment display)
        self.pins = {
            "A0": Pin(20, Pin.OUT),  # Segment A for display 0
            "B0": Pin(28, Pin.OUT),  # Segment B for display 0
            "C0": Pin(22, Pin.OUT),  # Segment C for display 0
            "D0": Pin(21, Pin.OUT),  # Segment D for display 0
            "A1": Pin(16, Pin.OUT),  # Segment A for display 1
            "B1": Pin(19, Pin.OUT),  # Segment B for display 1
            "C1": Pin(18, Pin.OUT),  # Segment C for display 1
            "D1": Pin(17, Pin.OUT),  # Segment D for display 1
            "A2": Pin(12, Pin.OUT),  # Segment A for display 2
            "B2": Pin(15, Pin.OUT),  # Segment B for display 2
            "C2": Pin(14, Pin.OUT),  # Segment C for display 2
            "D2": Pin(13, Pin.OUT),  # Segment D for display 2
            "A3": Pin(8, Pin.OUT),   # Segment A for display 3
            "B3": Pin(11, Pin.OUT),  # Segment B for display 3
            "C3": Pin(10, Pin.OUT),  # Segment C for display 3
            "D3": Pin(9, Pin.OUT),   # Segment D for display 3
        }

        self.decimals = {
            "DP1": Pin(3,Pin.OUT),
            "DP2": Pin(6,Pin.OUT),
            "DP3": Pin(7,Pin.OUT)
        }

        # BCD to 7-segment mapping for CD4511BE
        self.segment_map = {
            0: 0b1111,  # 0
            1: 0b0110,  # 1
            2: 0b1101,  # 2
            3: 0b1110,  # 3
            4: 0b0111,  # 4
            5: 0b1011,  # 5
            6: 0b1010,  # 6
            7: 0b1111,  # 7
            8: 0b1111,  # 8
            9: 0b1110,  # 9
        }

    def set_digit(self, display_index, digit):
        """
        Sets the digit on a specified display (0-3) by sending BCD to the corresponding CD4511BE.
        """
        # Ensure digit is between 0-9
        if digit < 0 or digit > 9:
            print("Invalid digit: must be between 0 and 9")
            return

        # Get the BCD representation of the digit (4-bit binary)
        bcd = self.segment_map[digit]

        # Map the BCD value to the corresponding segment pins for the selected display
        for i in range(4):
            pin = self.pins[f"A{display_index}"] if i == 0 else self.pins[f"B{display_index}"] if i == 1 else self.pins[f"C{display_index}"] if i == 2 else self.pins[f"D{display_index}"]
            pin.value((bcd >> (3 - i)) & 1)

    def clear_display(self):
        """Clear all segments (turn off all pins)"""
        for pin in self.pins.values():
            pin.value(0)

    def display_number(self, number):
        """Display a 4-digit number (0-9999) across the 4 displays"""
        if number < 0 or number > 9999:
            print("Invalid number: must be between 0 and 9999")
            return

        # Display each digit (thousands, hundreds, tens, ones) on the respective display
        digits = [int(digit) for digit in str(number).zfill(4)]
        for i, digit in enumerate(digits):
            self.set_digit(i, digit)


if __name__ == "__main__":

  joystick = JOYSTICK_PICO()

  while True:
      joystick.run()
      time.sleep(0.1)

