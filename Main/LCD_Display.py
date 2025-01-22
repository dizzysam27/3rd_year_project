import time
from smbus import SMBus

b = SMBus(1)

# Device I2C Address
LCD_ADDRESS = (0x7c >> 1)

# LCD Command Set
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Entry Mode Flags
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Display Control Flags
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Cursor Shift Flags
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Function Set Flags
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x8DOTS = 0x00

class LCD1602:
    def __init__(self, col, row):
        self._row = row
        self._col = col
        self._showfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
        self.begin(self._row, self._col)

    def command(self, cmd):
        b.write_byte_data(LCD_ADDRESS, 0x80, cmd)

    def write(self, data):
        b.write_byte_data(LCD_ADDRESS, 0x40, data)

    def setCursor(self, col, row):
        if row == 0:
            col |= 0x80
        else:
            col |= 0xc0
        self.command(col)

    def clear(self):
        self.command(LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def printout(self, arg):
        if isinstance(arg, int):
            arg = str(arg)
        for x in bytearray(arg, 'utf-8'):
            self.write(x)

    def display(self):
        self._showcontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._showcontrol)

    def begin(self, cols, lines):
        if lines > 1:
            self._showfunction |= LCD_2LINE
        self._numlines = lines
        self._currline = 0

        time.sleep(0.05)

        # Send function set command sequence
        self.command(LCD_FUNCTIONSET | self._showfunction)
        time.sleep(0.005)
        self.command(LCD_FUNCTIONSET | self._showfunction)
        time.sleep(0.005)
        self.command(LCD_FUNCTIONSET | self._showfunction)
        self.command(LCD_FUNCTIONSET | self._showfunction)

        self._showcontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()
        self.clear()

        self._showmode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        self.command(LCD_ENTRYMODESET | self._showmode)

class LCD1602_WRITE(LCD1602): 
    def __init__(self):
        super().__init__(16, 2)
        self.message_line1 = "Welcome"
        self.message_line2 = "Group 12"
        self.flag = 0
        self.previous_hour = ""
        self.previous_minute = ""
        self.previous_second = ""

    def update_messages(self, new_message_line1, new_message_line2):
        self.flag = 1
        self.message_line1 = new_message_line1
        self.message_line2 = new_message_line2
        print(self.message_line1 + "    \r", end="", flush=True)  # Clear the rest of the line with spaces


        self.clear()
        self.display_lines(self.message_line1, self.message_line2)

    def display_lines(self, message_line1, message_line2):
        self.flag = 0
        self.setCursor(0, 0)
        self.printout(message_line1)
        self.setCursor(0, 1)
        self.printout(message_line2)
    
    # def display_timer(self):
    #     self.clear()
    #     self.setCursor(2, 0)
    #     self.printout(":")
    #     self.setCursor(5, 0)
    #     self.printout(":")

    #     while True:
    #         # Get the current time
    #         current_time = datetime.now().strftime('%H:%M:%S')
    #         current_hour, current_minute, current_second = current_time.split(':')
            
    #         # Update the hour if it has changed
    #         if current_hour != self.previous_hour:
    #             self.setCursor(0, 0)
    #             self.printout(current_hour)
    #             self.previous_hour = current_hour  # Update the previous hour

    #         # Update the minute if it has changed
    #         if current_minute != self.previous_minute:
    #             self.setCursor(3, 0)  # 3 is the starting position of minutes
    #             self.printout(current_minute)
    #             self.previous_minute = current_minute  # Update the previous minute

    #         # Update the second if it has changed
    #         if current_second != self.previous_second:
    #             self.setCursor(6, 0)  # 6 is the starting position of seconds
    #             self.printout(current_second)
    #             self.previous_second = current_second  # Update the previous second

    #         # Wait for 1 second
    #         time.sleep(1)

