from Controller import MODE_MANAGER
from Physical_Buttons import PHYSICAL_BUTTONS
from GUI import GUI


def main():
    try:
    
        gui = GUI()
        mode_manager = MODE_MANAGER(gui)
        physical_buttons = PHYSICAL_BUTTONS(gui)

        mode_manager.switch_mode("Menu")
        physical_buttons
        gui.run()

        while True:
            pass

    except KeyboardInterrupt:
        # Cleanup on exit
        PHYSICAL_BUTTONS.cleanup()

if __name__ == "__main__":
    main()
