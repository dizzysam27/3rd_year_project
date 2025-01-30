from LCD_Display import LCD1602_WRITE
from Timer import TIMER
from Gyro import LSM6DS3
from PCA9685 import PCA9685
from Joystick_Master import JOYSTICK_READ_DATA
from Physical_Buttons import PHYSICAL_BUTTONS, LED_CONTROL
from LED_Control_Master_Test import ARDUINO


"""
This is the file which determines which mode of operation we are currently in. The GUI, buttons and input method change depending on which mode we are in.
"""

# MODE MANAGER class
class MODE_MANAGER:
    # Init function
    # Required inputs: GUI class
    #                  |   LED_CONTROL class
    #                  V   V
    def __init__(self,gui,led):
        self.gui = gui
        self.lcd = LCD1602_WRITE()
        self.timer = TIMER(gui)
        self.gyro = LSM6DS3()
        self.led = led

        # List of modes with required inputs
        self.modes = {
            "Menu": MENU_MODE(self.lcd,self.timer,self.gui,self.gyro,self.led),
            "AI Solve": AI_MODE(self.lcd, self.timer,self.gui,self.gyro,self.led),
            "Manual": MANUAL_MODE(self.lcd, self.timer,self.gui,self.gyro,self.led),
            "Start": START_MODE(self.lcd, self.timer,self.gui,self.gyro,self.led),
            "Stop": STOP_MODE(self.lcd, self.timer,self.gui,self.gyro,self.led),
            "Calibrate": CALIBRATE_MODE(self.lcd,self.timer,self.gui,self.gyro,self.led),
            "Start Calibration":START_CALIBRATION(self.lcd,self.timer,self.gui,self.gyro,self.led),
            "Reset": RESET_MODE(self.lcd,self.timer,self.gui,self.gyro,self.led)
        }
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
    def __init__(self, lcd, timer, gui,gyro, led):
        self.lcd = lcd
        self.timer = timer
        self.gui = gui
        self.gyro = gyro
        self.motors = PCA9685()
        self.led = led
        self.led_strip = ARDUINO()

        
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

class AI_MODE(MODE):

    def display(self):
        self.lcd.update_messages("AI Solver", "Start       Menu")
        self.gui.update_label("AI Solver")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(1)

    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

class MANUAL_MODE(MODE):

    def display(self):
        self.lcd.update_messages("Manual Solver", "Start       Menu")
        self.gui.update_label("Manual Solver")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(2)

    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

class CALIBRATE_MODE(MODE):
    
    def display(self):
        self.lcd.update_messages("Calibration Mode", "Start       Menu")
        self.gui.update_label("Calibration Mode")
        self.gui.update_button_text(1,"Start")
        self.gui.update_button_text(2,"")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(1,0,1)
        self.led_strip.write_to_arduino(3)
        
    def handle_input(self, button):
        if button == 1:
            return "Start Calibration"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass

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

    def handle_input(self, button):
        if button == 1:
            pass
        elif button == 2:
            return "Stop"
        elif button == 3:
            pass
        else:
            pass

class STOP_MODE(MODE):

    def display(self):
        self.gui.update_button_text(1,"")
        self.gui.update_button_text(2,"Reset")
        self.gui.update_button_text(3,"Menu")
        self.led.set_led(0,1,1)
        self.timer.stop_timer()
        
    def handle_input(self, button):
        if button == 1:
            pass
        elif button == 2:
            return "Reset"
        elif button == 3:
            return "Menu"
        else:
            pass

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
        while True:
            try:
                self.joystick.read_data()
                x_gyro = self.gyro.read_gyroscope_x()
                y_gyro = self.gyro.read_gyroscope_y()
                z_gyro = self.gyro.read_gyroscope_z()
                self.lcd.update_messages(f"X:{x_gyro} Y:{y_gyro} Z:{z_gyro}", "            Menu")
                self.gui.update_label(f"X:{x_gyro} Y:{y_gyro} Z:{z_gyro}")
                self.gui.update_button_text(1,"Start")
                self.gui.update_button_text(2,"")
                self.gui.update_button_text(3,"Menu")
            except:
                pass
            
    def handle_input(self, button):
        if button == 1:
            return "Start Calibration"
        elif button == 2:
            pass
        elif button == 3:
            return "Menu"
        else:
            pass