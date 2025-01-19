from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys
from Controller import MODE_MANAGER

class GUI:

    def __init__(self):
        self.mode_manager = MODE_MANAGER()
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setWindowTitle("Group 12 Maze Game")


        # Add a dynamic label for displaying updates
        self.dynamic_label = QLabel("Welcome to the Maze Game!", self.window)
        self.dynamic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dynamic_label)

    def update_label(self, new_text):
        """Update the dynamic label text."""
        self.dynamic_label.setText(new_text)

    def run(self):
        # Buttons
        button1 = QPushButton("Menu")
        button1.clicked.connect(lambda: [self.mode_manager.handle_input(1), self.update_label("Menu Selected")])
        self.layout.addWidget(button1)

        button2 = QPushButton("AI Solver")
        button2.clicked.connect(lambda: [self.mode_manager.handle_input(2), self.update_label("AI Solver Selected")])
        self.layout.addWidget(button2)

        button3 = QPushButton("Manual")
        button3.clicked.connect(lambda: [self.mode_manager.handle_input(3), self.update_label("Manual Mode Selected")])
        self.layout.addWidget(button3)

        # Set the layout for the main window
        self.window.setLayout(self.layout)

        # Show the window
        self.window.show()
        sys.exit(self.app.exec_())
        