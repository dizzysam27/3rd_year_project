import time
import threading
from Control_Panel import MODE_SELECTION, LCD1602,LCD1602_WRITE

def main():

    buttons = MODE_SELECTION()
    lcd = LCD1602_WRITE()
    
    try:

        buttons.Menu()
        buttons.event_detect()
        time.sleep(20)
        lcd.update_messages("Hello","AI    Man    Cal")
        while True:
            continue














    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        buttons.cleanup()
        print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()
