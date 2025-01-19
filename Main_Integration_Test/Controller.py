import RPi.GPIO as GPIO
from Control_Panel import LCD1602_WRITE
from Timer import Timer
import time

class MODE_SELECTION:
    
    def __init__(self):
        self.mode = "Menu"  # Default mode
        self.lcd = LCD1602_WRITE()
        self.timer = Timer()
        self.mode_actions = {
            "Menu": self.Menu,
            "AI Solve": self.AI_Solve,
            "Manual": self.Manual,
            "Calibrate": self.Calibrate,
            "Start": self.Start,
            "Stop": self.Stop
        }
    
    def start_program(self, mode):
        # Set the initial mode and update the display
        self.mode = mode
        self.mode_actions.get(self.mode, self.Menu)()

    def mode_switcher(self, button, _):
        # Switch based on the current mode and button
        if self.mode == "Menu":
            if button == 1:
                self.AI_Solve()
            elif button == 2:
                self.Manual()
            elif button == 3:
                self.Calibrate()
            else:
                self.Menu()
        
        elif self.mode == "AI Solve":
            if button == 1:
                self.Start()
            elif button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.AI_Solve()

        elif self.mode == "Manual":
            if button == 1:
                self.Start()
            elif button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.Manual()

        elif self.mode == "Calibrate":
            if button == 1 or button == 2:
                pass 
            elif button == 3:
                self.Menu()
            else:
                self.Calibrate()

        elif self.mode == "Start":
            if button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.Start()

        elif self.mode == "Stop":
            if button == 3:
                self.Menu()
            else:
                self.Stop()

        else:
            self.Menu()  # Default case

    def Menu(self):
        self.mode = "Menu"
        self.lcd.update_messages("The Maze Game", "AI    Man    Cal")


    def AI_Solve(self):
        self.mode = "AI Solve"
        self.lcd.update_messages("AI Solver", "Start Stop Menu")
    
    def Manual(self):
        self.mode = "Manual"
        self.lcd.update_messages("Manual Solver", "Start Stop Menu")
    
    def Start(self):
        self.mode = "Start"
        self.lcd.update_messages("Running", "      Stop Menu")
        self.timer.start_timer()
    
    def Stop(self):
        self.mode = "Stop"
        self.lcd.update_messages("Stopped", "      Stop Menu")
        self.timer.stop_timer()
    
    def Calibrate(self):
        self.mode = "Calibrate"
        self.lcd.update_messages("Calibration Mode", "Start Stop Menu")

