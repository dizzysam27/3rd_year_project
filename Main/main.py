from Controller import MODE_SELECTION
from Control_Panel import PHYSICAL_BUTTONS

def main():

    mode_selection = MODE_SELECTION()
    physical_buttons = PHYSICAL_BUTTONS()
    mode_selection.start_program("Menu")
    physical_buttons.event_detect()

    while True:
        pass

if __name__ == "__main__":
    main()
