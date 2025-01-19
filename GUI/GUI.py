from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys
from controller import MODE_MANAGER

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setWindowTitle("Mode Switcher Demo")

        # Add a dynamic label for displaying updates
        self.dynamic_label = QLabel("Welcome to the Mode Switcher!", self.window)
        self.dynamic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dynamic_label)

        # Initialize the MODE_MANAGER and pass 'self' (GUI instance) to it
        self.mode_manager = MODE_MANAGER(self)  # Pass GUI instance

    def update_label(self, new_text):
        """Update the dynamic label text."""
        self.dynamic_label.setText(new_text)

    def run(self):
        # Buttons to trigger mode changes
        button1 = QPushButton("Switch to Mode 1")
        button1.clicked.connect(lambda: self.mode_manager.switch_mode(1))
        self.layout.addWidget(button1)

        button2 = QPushButton("Switch to Mode 2")
        button2.clicked.connect(lambda: self.mode_manager.switch_mode(2))
        self.layout.addWidget(button2)

        button3 = QPushButton("Switch to Mode 3")
        button3.clicked.connect(lambda: self.mode_manager.switch_mode(3))
        self.layout.addWidget(button3)

        # Set the layout for the main window
        self.window.setLayout(self.layout)

        # Show the window
        self.window.show()
        sys.exit(self.app.exec_())

# Run the GUI application
if __name__ == "__main__":
    gui = GUI()
    gui.run()
