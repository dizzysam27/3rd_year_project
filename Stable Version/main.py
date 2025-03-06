from Controller import MODE_MANAGER
from Peripherals.Physical_Button_Control import PHYSICAL_BUTTONS, LED_CONTROL
from GUI import GUI

"""
This is the main function which runs the program. This initialises the GUI, MODE MANAGER and PHYSICAL_BUTTONS
"""

def main():
    try:
        # Create instance of LED_CONTROL class
        led_control = LED_CONTROL()
        # Create instance of GUI class (requires LED_CONTROL class to run)
        gui = GUI(led_control)
        # Mode
        mode_manager = MODE_MANAGER(gui, led_control)

        PHYSICAL_BUTTONS(gui, led_control)
        mode_manager.switch_mode("Menu")
        gui.run()

        while True:
            pass

    except KeyboardInterrupt:
        # Cleanup on exit
        PHYSICAL_BUTTONS.cleanup()

if __name__ == "__main__":
    main()