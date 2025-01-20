import threading
from datetime import datetime
from LCD_Display import LCD1602_WRITE
import time

class TIMER:

    def __init__(self,gui):

        self.start_time = None
        self.timer_running = threading.Event()  # Event to control timer state
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.daemon = True  # Daemon thread stops with the main program
        self.timer_thread.start()
        self.lcd = LCD1602_WRITE()
        self.gui = gui
        

    def start_timer(self):
    
        self.start_time = datetime.now()
        self.timer_running.set()  # Enable the timer
        self.lcd.update_messages("                ","      Stop      ")

    def stop_timer(self):
        
        self.timer_running.clear()  # Disable the timer
        self.lcd.update_messages(str(self.elapsed_time),"     Reset  Menu")

    def reset_timer(self):
        
        self.start_time = datetime.now()  # Set a new start time
        print("Timer reset.")
        self.lcd.update_messages(str(self.start_time),"Start       Menu")

    def run_timer(self):
        
        while True:
            if self.timer_running.is_set():
                if self.start_time:  # Ensure the timer has been started
                    self.elapsed_time = datetime.now() - self.start_time
                    # print(f"Elapsed time: {self.elapsed_time}", end="\r", flush=True)
                    self.lcd.update_messages(str(self.elapsed_time),"      Stop      ")
                    self.gui.update_label(str(self.elapsed_time)) 
            time.sleep(0.1)  # Reduce CPU usage