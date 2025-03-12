from Peripherals.LCD_Control import LCD1602_WRITE
from Timer import TIMER
# from Peripherals.Gyro_Control import LSM6DS3
from Peripherals.Motor_Control import PCA9685
from Peripherals.Joystick_Control import JOYSTICK_READ_DATA
# from Peripherals.Physical_Button_Control import PHYSICAL_BUTTONS, LED_CONTROL
from Peripherals.LED_Strip_Control import ARDUINO


"""
This is the file which determines which mode of operation we are currently in
"""

# MODE MANAGER class
class MODE_MANAGER:
    # Init function
    # Required inputs: GUI class
    #                  |   LED_CONTROL class
    #                  V   V
    def __init__(self,gui,led):

        # Creates instances of the classes
        lcd = LCD1602_WRITE()
        timer = TIMER(gui)
        # gyro = LSM6DS3()
        gyro = 1
        motors = PCA9685()
        led_strip = ARDUINO()
        joystick = JOYSTICK_READ_DATA()

        # Collection of arguments required for each mode class
        mode_arguments = lcd,timer,gui,gyro,led,motors,led_strip

        # Dictionary of modes with required inputs
        self.modes = {
            "Menu": MENU_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "AI Solve": AI_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Manual": MANUAL_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Start": START_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Stop": STOP_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Calibrate": CALIBRATE_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Start Calibration":START_CALIBRATION(lcd,timer,gui,gyro,led,motors,led_strip,joystick),
            "Reset": RESET_MODE(lcd,timer,gui,gyro,led,motors,led_strip,joystick)
        }

        # Initialises the program to Menu Mode on start up
        self.current_mode = self.modes["Menu"]

    # Switch mode function called by handle_input
    # Required input:     New mode name (list in __init__.modes)
    #                     V
    def switch_mode(self, mode_name):
        self.current_mode = self.modes[mode_name]
        self.current_mode.display()

    # Handle input function, takes in GUI press or button press
    # Required input:      Button number pressed (1: Green, 2: Red, 3: Blue)
    #                      V
    def handle_input(self, button):
        # Find next mode name by running handle_input function specific to current_mode
        next_mode_name = self.current_mode.handle_input(button)
        # Check if next mode name is possible, call switch_mode function to change
        if next_mode_name in self.modes:
            self.switch_mode(next_mode_name)

# Parent class of each mode. Prevents repetition of code to define self.variables
class MODE:
    def __init__(self, lcd, timer, gui, gyro, led, motors, led_strip,joystick):
        self.lcd = lcd
        self.timer = timer
        self.gui = gui
        self.gyro = gyro
        self.led = led
        self.motors = motors
        self.led_strip = led_strip
        self.joystick = joystick

# Determines what we want to happen when system is in Menu Mode 
class MENU_MODE(MODE):

    def display(self):
        # Update LCD
        self.lcd.update_messages("The Maze Game", "AI    Man    Cal")
        self.gui.update_label("Welcome to the Maze Game")
        # Update GUI
        self.gui.update_button_text(1,"AI Solve")
        self.gui.update_button_text(2,"Manual Solve")
        self.gui.update_button_text(3,"Calibrate")
        # Update button LEDs
        self.led.set_led(1,1,1)
        # Update LED strip
        self.led_strip.write_to_arduino(4)
        self.lcd.setRGB(255,255,255)
        
    # current_mode specific handle_input function
    def handle_input(self, button):
        if button == 1:
            return "AI Solve"
        elif button == 2:
            return "Manual"
        elif button == 3:
            return "Calibrate"
        else:
            return "Menu"

# Determines what we want to happen when system is in AI Mode
class AI_MODE(MODE):

    def display(self):
        self.lcd.update_messages("AI Solver", "Start       Menu")
        self.gui.update_label("AI Solver")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(1)

    # Function determines which mode the program goes into after a button press interupt 
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

# Determines what we want to happen when system is in Manual Mode 
class MANUAL_MODE(MODE):

    def display(self):
        self.lcd.update_messages("Manual Solver", "Start       Menu")
        self.lcd.setRGB(255,255,255)
        self.gui.update_label("Manual Solver")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(2)

    # Function determines which mode the program goes into after a button press interupt 
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

# Determines what we want to happen when system is in Calibration Mode 
class CALIBRATE_MODE(MODE):
    
    def display(self):
        self.lcd.update_messages("Calibration Mode", "Start       Menu")
        self.gui.update_label("Calibration Mode")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(3)
        
    # Function determines which mode the program goes into after a button press interupt 
    def handle_input(self, button):
        if button == 1:
            return "Start Calibration"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

# Determines what we want to happen when system is in Start Mode 
class START_MODE(MODE):
    
    def display(self):
        self.gui.update_button_text(1,"")
        self.gui.update_button_text(2,"Stop")
        self.gui.update_button_text(3,"")
        self.led.set_led(0,1,0)
        # self.pca9685 = PCA9685()
        # self.pca9685.run()
        self.led_strip.write_to_arduino(5)
        self.timer.start_timer()  
        self.joystick.start_reading()
        

    # Function determines which mode the program goes into after a button press interupt 
    def handle_input(self, button):
        if button == 1:
            pass
        elif button == 2:
            return "Stop"
        elif button == 3:
            pass
        else:
            pass

# Determines what we want to happen when system is in Stop Mode 
class STOP_MODE(MODE):

    def display(self):
        self.gui.update_button_text(1,"")
        self.gui.update_button_text(2,"Reset")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(0,1,1)
        self.timer.stop_timer()
        self.joystick.stop_reading()
        self.led_strip.write_to_arduino(2)

    # Function determines which mode the program goes into after a button press interupt    
    def handle_input(self, button):
        if button == 1:
            pass
        elif button == 2:
            return "Reset"
        elif button == 3:
            return "Menu"
        else:
            pass

# Determines what we want to happen when system is in Reset Mode 
class RESET_MODE(MODE):

    def display(self):
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.timer.reset_timer()
        
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

# Calibration mode - unique mode
class START_CALIBRATION(MODE):

    def display(self):
        self.joystick = JOYSTICK_READ_DATA()

        # while True:
        #     try:
        #         self.joystick.read_data()
        #         x_gyro = self.gyro.read_gyroscope_x()
        #         y_gyro = self.gyro.read_gyroscope_y()
        #         z_gyro = self.gyro.read_gyroscope_z()
        #         self.lcd.update_messages(f"X:{x_gyro} Y:{y_gyro} Z:{z_gyro}", "            Menu")
        #         self.gui.update_label(f"X:{x_gyro} Y:{y_gyro} Z:{z_gyro}")
        #         self.gui.update_button_text(1,"Start")
        #         self.gui.update_button_text(2,"")
        #         self.gui.update_button_text(3,"Menu")
        #     except:
        #         pass
            
    def handle_input(self, button):
        if button == 1:
            return "Start Calibration"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass