from LCD_Display import LCD1602_WRITE
from Timer import TIMER

class MODE_MANAGER:
    def __init__(self,gui):
        self.gui = gui
        self.lcd = LCD1602_WRITE()
        self.timer = TIMER(gui)
        self.modes = {
            "Menu": MENU_MODE(self.lcd,self.timer,self.gui),
            "AI Solve": AI_MODE(self.lcd, self.timer,self.gui),
            "Manual": MANUAL_MODE(self.lcd, self.timer,self.gui),
            "Start": START_MODE(self.lcd, self.timer,self.gui),
            "Stop": STOP_MODE(self.lcd, self.timer,self.gui),
            "Calibrate": CALIBRATE_MODE(self.lcd,self.timer,self.gui)
        }
        self.current_mode = self.modes["Menu"]

    def switch_mode(self, mode_name):
        self.current_mode = self.modes[mode_name]
        self.current_mode.display()

    def handle_input(self, button):
        next_mode_name = self.current_mode.handle_input(button)
        if next_mode_name in self.modes:
            self.switch_mode(next_mode_name)

class MODE:
    def __init__(self, lcd, timer, gui):
        self.lcd = lcd
        self.timer = timer
        self.gui = gui

class MENU_MODE(MODE):

    def display(self):
        self.lcd.update_messages("The Maze Game", "AI    Man    Cal")
        self.gui.update_label("Menu")
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
        self.lcd.update_messages("AI Solver", "Start Stop Menu")
        self.gui.update_label("AI Solver")
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"

class MANUAL_MODE(MODE):
    def display(self):
        self.lcd.update_messages("Manual Solver", "Start Stop Menu")
        self.gui.update_label("Manual Solver")
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"


class CALIBRATE_MODE(MODE):
    def display(self):
        self.lcd.update_messages("Calibration Mode", "Start Stop Menu")
        self.gui.update_label("Calibration Mode")
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"

class START_MODE(MODE):
    def display(self):
        self.lcd.update_messages("Start Mode", "Start Stop Menu")
        self.timer.start_timer()
    def handle_input(self, button):
        if button == 1:
            
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"

class STOP_MODE(MODE):
    def display(self):
        self.lcd.update_messages("Stop", "Start Stop Menu")
        self.timer.stop_timer()
    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"


