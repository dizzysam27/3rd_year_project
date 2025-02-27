# controller.py

class MODE_MANAGER:
    def __init__(self, gui):
        self.gui = gui  # Store a reference to the GUI
        self.modes = {
            1: Mode1(self.gui),
            2: Mode2(self.gui),
            3: Mode3(self.gui)
        }
        self.current_mode = self.modes[1]  # Start with Mode 1

    def switch_mode(self, mode_number):
        if mode_number in self.modes:
            self.current_mode = self.modes[mode_number]
            self.current_mode.display()  # Display the new mode
            self.gui.update_label(self.current_mode.label)  # Update the label

    def update_gui_label(self, text):
        """This method is called to update the GUI label directly from MODE_MANAGER."""
        self.gui.update_label(text)  # Update the label in the GUI


class Mode:
    def __init__(self, gui, label):
        self.gui = gui  # Store the GUI reference
        self.label = label  # Label for this mode

    def display(self):
        pass  # Placeholder for display logic


class Mode1(Mode):
    def __init__(self, gui):
        super().__init__(gui, "Mode 1 is Active!")

    def display(self):
        print("Displaying Mode 1")
        # Example: Update GUI label from the mode
        self.gui.update_label("Mode 1 is now active!")  # Directly update label in GUI


class Mode2(Mode):
    def __init__(self, gui):
        super().__init__(gui, "Mode 2 is Active!")

    def display(self):
        print("Displaying Mode 2")
        # Example: Update GUI label from the mode
        self.gui.update_label("Mode 2 is now active!")  # Directly update label in GUI


class Mode3(Mode):
    def __init__(self, gui):
        super().__init__(gui, "Mode 3 is Active!")

    def display(self):
        print("Displaying Mode 3")
        # Example: Update GUI label from the mode
        self.gui.update_label("Mode 3 is now active!")  # Directly update label in GUI
