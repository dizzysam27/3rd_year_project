from Controller import MODE_SELECTION
from Control_Panel import PHYSICAL_BUTTONS
from GUI import GUI


def main():

    try:
        mode_selection = MODE_SELECTION()
        physical_buttons = PHYSICAL_BUTTONS()
        gui = GUI()
        mode_selection.start_program("Menu")
        physical_buttons.event_detect()
        gui.run()

        while True:
            pass
    
    except KeyboardInterrupt:
        PHYSICAL_BUTTONS.cleanup()

if __name__ == "__main__":
    main()
