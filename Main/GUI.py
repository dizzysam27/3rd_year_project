from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys
from Controller import MODE_SELECTION

class GUI:

    def __init__(self):
        self.mode_selection = MODE_SELECTION()
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setWindowTitle("Group 12 Maze Game")

    def run(self):
  
        button1 = QPushButton("Menu")
        button1.clicked.connect(lambda: self.mode_selection.Menu())
        self.layout.addWidget(button1)

        button2 = QPushButton("AI Solver")
        button2.clicked.connect(lambda: self.mode_selection.AI_Solve())
        self.layout.addWidget(button2)

        button3 = QPushButton("Manual")
        button3.clicked.connect(lambda: self.mode_selection.Manual())
        self.layout.addWidget(button3)

        # Set the layout for the main window
        self.window.setLayout(self.layout)

        # Show the window
        self.window.show()
        sys.exit(self.app.exec_())