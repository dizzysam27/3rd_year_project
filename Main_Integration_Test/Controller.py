import RPi.GPIO as GPIO
from Control_Panel import LCD1602_WRITE
from Timer import Timer
import time

class ModeManager:
    def __init__(self):
        self.lcd = LCD1602_WRITE()
        self.timer = Timer()
        self.modes = {
            "Menu": MenuMode(self.lcd),
            "AI Solve": AISolveMode(self.lcd, self.timer),
            "Manual": ManualMode(self.lcd, self.timer),
            "Start": StartMode(self.lcd, self.timer),
            "Stop": StopMode(self.lcd, self.timer),
            "Calibrate": CalibrateMode(self.lcd)
        }
        self.current_mode = self.modes["Menu"]

    def switch_mode(self, mode_name):
        self.current_mode = self.modes[mode_name]
        self.current_mode.display()

    def handle_input(self, button):
        next_mode_name = self.current_mode.handle_input(button)
        if next_mode_name in self.modes:
            self.switch_mode(next_mode_name)


class Mode:
    def __init__(self, lcd, timer=None):
        self.lcd = lcd
        self.timer = timer

    def handle_input(self, button):
        pass  # To be overridden by subclasses

    def display(self):
        pass  # To be overridden by subclasses

class MenuMode(Mode):
    def display(self):
        self.lcd.update_messages("The Maze Game", "AI    Man    Cal")

    def handle_input(self, button):
        if button == 1:
            return "AI Solve"
        elif button == 2:
            return "Manual"
        elif button == 3:
            return "Calibrate"
        return "Menu"

class AISolveMode(Mode):
    def display(self):
        self.lcd.update_messages("AI Solver", "Start Stop Menu")

    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"

class AISolveMode(Mode):
    def display(self):
        self.lcd.update_messages("AI Solver", "Start Stop Menu")

    def handle_input(self, button):
        if button == 1:
            return "Start"
        elif button == 2:
            return "Stop"
        elif button == 3:
            return "Menu"
        return "AI Solve"



