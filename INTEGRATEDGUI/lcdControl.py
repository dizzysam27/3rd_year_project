import time
import smbus # type: ignore

bus = smbus.SMBus(1)

#Device I2C Arress
LCD_ADDRESS   =  (0x7c>>1)
RGB_ADDRESS   =  (0xc0>>1)

#color define

REG_RED    =     0x04
REG_GREEN  =     0x03
REG_BLUE   =     0x02
REG_MODE1  =     0x00
REG_MODE2  =     0x01
REG_OUTPUT =     0x08
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

#flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

#flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

#flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

#flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x8DOTS = 0x00


class LCD1602:
  def __init__(self, col, row):
    self._row = row
    self._col = col
    self._showfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS;
    self.begin(self._row,self._col)

        
  def command(self,cmd):
    bus.write_byte_data(LCD_ADDRESS,0x80,cmd)

  def write(self,data):
    bus.write_byte_data(LCD_ADDRESS,0x40,data)
    
  def setReg(self,reg,data):
    bus.write_byte_data(RGB_ADDRESS,reg,data)


  def setRGB(self,r,g,b):
    self.setReg(REG_RED,r)
    self.setReg(REG_GREEN,g)
    self.setReg(REG_BLUE,b)

  def setCursor(self,col,row):
    if(row == 0):
      col|=0x80
    else:
      col|=0xc0;
    self.command(col)

  def clear(self):
    self.command(LCD_CLEARDISPLAY)
    time.sleep(0.002)
  def printout(self,arg):
    if(isinstance(arg,int)):
      arg=str(arg)

    for x in bytearray(arg,'utf-8'):
      self.write(x)


  def display(self):
    self._showcontrol |= LCD_DISPLAYON 
    self.command(LCD_DISPLAYCONTROL | self._showcontrol)

 
  def begin(self,cols,lines):
    if (lines > 1):
        self._showfunction |= LCD_2LINE 
     
    self._numlines = lines 
    self._currline = 0 
     
    time.sleep(0.05)

    
    # Send function set command sequence
    self.command(LCD_FUNCTIONSET | self._showfunction)
    #delayMicroseconds(4500);  # wait more than 4.1ms
    time.sleep(0.005)
    # second try
    self.command(LCD_FUNCTIONSET | self._showfunction);
    #delayMicroseconds(150);
    time.sleep(0.005)
    # third go
    self.command(LCD_FUNCTIONSET | self._showfunction)
    # finally, set # lines, font size, etc.
    self.command(LCD_FUNCTIONSET | self._showfunction)
    # turn the display on with no cursor or blinking default
    self._showcontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF 
    self.display()
    # clear it off
    self.clear()
    # Initialize to default text direction (for romance languages)
    self._showmode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT 
    # set the entry mode
    self.command(LCD_ENTRYMODESET | self._showmode);

    # backlight init
    self.setReg(REG_MODE1, 0)
    # set LEDs controllable by both PWM and GRPPWM registers
    self.setReg(REG_OUTPUT, 0xFF)
    # set MODE2 values
    # 0010 0000 -> 0x20  (DMBLNK to 1, ie blinky mode)
    self.setReg(REG_MODE2, 0x20)

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
        if new_message_line1 == "":
          pass
        else:
          self.message_line1 = new_message_line1
        if new_message_line2 == "":
          pass
        else:
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
