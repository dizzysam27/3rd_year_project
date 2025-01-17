import time
import RPi.GPIO as GPIO
from smbus import SMBus
b = SMBus(1)

#Device I2C Arress
LCD_ADDRESS   =  (0x7c>>1)

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
    b.write_byte_data(LCD_ADDRESS,0x80,cmd)

  def write(self,data):
    b.write_byte_data(LCD_ADDRESS,0x40,data)
    
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

class LCD1602_WRITE:
   
    def __init__(self):
        self.lcd = LCD1602(16,2)
        self.message_line1 = "Welcome"
        self.message_line2 = "Group 12"
        self.flag=0

    def update_messages(self,new_message_line1, new_message_line2):
        self.flag=1
        self.message_line1 = new_message_line1
        self.message_line2 = new_message_line2
        print(self.message_line1)
        print(self.message_line2)
        self.lcd.clear()
        self.display_lines(self.message_line1,self.message_line2)

    def display_lines(self,message_line1,message_line2):
        self.flag=0
        self.lcd.setCursor(0, 0)
        self.lcd.printout(message_line1)
        self.lcd.setCursor(0, 1)
        self.lcd.printout(message_line2)

class MODE_SELECTION:

    def __init__(self):
        self.BUTTON_PIN_1 = 4
        self.BUTTON_PIN_2 = 17
        self.BUTTON_PIN_3 = 20
        global mode
        mode = "Manual"
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.BUTTON_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.BUTTON_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.lcd = LCD1602_WRITE()
        # self.current_mode = "Menu"  # Initial mode is "Menu"

        # Dictionary to map button presses to actions in each mode
        # self.mode_actions = {
        #     "Menu": {1: self.AI_Solve, 2: self.Manual, 3: self.Menu},
        #     "AI Solve": {1: self.Start, 2: self.Stop, 3: self.Menu},
        #     "Manual": {1: self.Start, 2: self.Stop, 3: self.Menu},
        #     "Start": {2: self.Stop, 3: self.Menu},
        #     "Stop": {1: self.Start, 3: self.Menu}
        # }


    def button1_released_callback(self, channel):
        # print("Button 1 pressed")
        self.mode_switcher(1,mode)

    def button2_released_callback(self, channel):
        # print("Button 2 pressed")
        self.mode_switcher(2,mode)

    def button3_released_callback(self, channel):
        # print("Button 3 pressed")
        self.mode_switcher(3,mode)
        

    def event_detect(self):
        GPIO.add_event_detect(self.BUTTON_PIN_1, GPIO.RISING, callback=self.button1_released_callback, bouncetime=500)
        GPIO.add_event_detect(self.BUTTON_PIN_2, GPIO.RISING, callback=self.button2_released_callback, bouncetime=500)
        GPIO.add_event_detect(self.BUTTON_PIN_3, GPIO.RISING, callback=self.button3_released_callback, bouncetime=500)
    
    def cleanup(self):
        GPIO.cleanup()
    



    def mode_switcher(self,button,mode):
        print(mode)
        if mode == "Menu":
            print("Menu")
            if button == 1:
               self.AI_Solve()
            if button == 2:
               self.Manual()
            if button == 3:
               self.Calibrate()

        if mode == "AI Solve":
            
            if button == 1:
               self.Start()
            if button == 2:
               self.Stop()
            if button == 3:
               self.Menu()

        if mode == "Manual":

            print("Manual")
            if button == 1:
               self.Start()
            if button == 2:
               self.Stop()
            if button == 3:
               self.Menu()
        
        if mode == "Calibrate":

            print("Stop")
            if button == 1:
               pass
            if button == 2:
               pass
            if button == 3:
               self.Menu()
        
        if mode == "Start":

            print("Start")
            if button == 1:
               pass
            if button == 2:
               self.Stop()
            if button == 3:
               self.Menu()
        
        if mode == "Stop":

            print("Stop")
            if button == 1:
               pass
            if button == 2:
               pass
            if button == 3:
               self.Menu()
        
           
    def Menu(self):
        global mode
        mode = "Menu"
        self.lcd.update_messages("The Maze Game","AI    Man    Cal")

    
    def AI_Solve(self):
        global mode
        mode = "AI Solve"
        self.lcd.update_messages("AI Solver","Start Stop Menu")
    

    def Manual(self):
        global mode
        mode = "Manual"
        self.lcd.update_messages("Manual Solver","Start Stop Menu")
    
    def Start(self):
        global mode
        mode = "Start"
        self.lcd.update_messages("Running","      Stop Menu")
    
    def Stop(self):
        global mode
        mode = "Stop"
        self.lcd.update_messages("Stopped","      Stop Menu")
    
    def Calibrate(self):
        global mode
        mode = "Calibrate"
        self.lcd.update_messages("Calibration Mode","Start Stop Menu")




        




