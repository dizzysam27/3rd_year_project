import RPi.GPIO as GPIO
from Control_Panel import LCD1602_WRITE

class MODE_SELECTION:

    def __init__(self):
        self.mode = ""
        self.lcd = LCD1602_WRITE()
        
    def start_program(self,mode):
        self.mode = mode
        self.mode_switcher(None,mode)

    def mode_switcher(self,button,mode):
        print(mode)
        if mode == "Menu":

            if button == 1:
                self.AI_Solve()
            elif button == 2:
                self.Manual()
            elif button == 3:
                self.Calibrate()
            else:
                self.Menu()

        elif mode == "AI Solve":
            
            if button == 1:
                self.Start()
            elif button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.AI_Solve()

        elif mode == "Manual":

            if button == 1:
                self.Start()
            elif button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.Manual()
        
        elif mode == "Calibrate":

            if button == 1:
                pass
            elif button == 2:
                pass
            elif button == 3:
                self.Menu()
            else:
                self.Calibrate()
        
        elif mode == "Start":

            if button == 1:
                pass
            elif button == 2:
                self.Stop()
            elif button == 3:
                self.Menu()
            else:
                self.Start()
        
        elif mode == "Stop":

            if button == 1:
                pass
            elif button == 2:
                pass
            elif button == 3:
                self.Menu()
            else:
                self.Stop()

        else:
            pass  
    
    def Menu(self):
        self.mode = "Menu"
        self.lcd.update_messages("The Maze Game","AI    Man    Cal")
    
    def AI_Solve(self):
        self.mode = "AI Solve"
        self.lcd.update_messages("AI Solver","Start Stop Menu")
    
    def Manual(self):
        self.mode = "Manual"
        self.lcd.update_messages("Manual Solver","Start Stop Menu")
    
    def Start(self):
        self.mode = "Start"
        self.lcd.update_messages("Running","      Stop Menu")
    
    def Stop(self):
        self.mode = "Stop"
        self.lcd.update_messages("Stopped","      Stop Menu")
    
    def Calibrate(self):
        self.mode = "Calibrate"
        self.lcd.update_messages("Calibration Mode","Start Stop Menu")

