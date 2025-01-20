from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys
from Controller import MODE_MANAGER

class GUI:

    def __init__(self):
        self.mode_manager = MODE_MANAGER(self)  # Pass GUI instance to MODE_MANAGER
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setWindowTitle("Group 12 Maze Game")
        self.window.resize(800, 600)

        self.dynamic_label = QLabel("Welcome to the Maze Game!", self.window)
        self.dynamic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dynamic_label)

        # Store buttons as instance variables
        self.button1 = QPushButton("Menu")
        self.button2 = QPushButton("AI Solver")
        self.button3 = QPushButton("Manual")

    def update_label(self, new_text):
        """Update the dynamic label text."""
        self.dynamic_label.setText(new_text)

    def update_button_text(self, button_id, new_text):
        """Update the text of a specific button."""
        if button_id == 1:
            self.button1.setText(new_text)
        elif button_id == 2:
            self.button2.setText(new_text)
        elif button_id == 3:
            self.button3.setText(new_text)

    def run(self):
        # Connect buttons to controller's handle_input method
        self.button1.clicked.connect(lambda: [self.mode_manager.handle_input(1)])
        self.layout.addWidget(self.button1)

        self.button2.clicked.connect(lambda: [self.mode_manager.handle_input(2)])
        self.layout.addWidget(self.button2)

        self.button3.clicked.connect(lambda: [self.mode_manager.handle_input(3)])
        self.layout.addWidget(self.button3)

        self.window.setLayout(self.layout)
        self.window.show()
        sys.exit(self.app.exec_())

