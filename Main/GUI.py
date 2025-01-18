from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys

class GUI:
    def __init__(self):
        self.buttons = B
    def on_button_click(button_number):
        print(f"Button {button_number} clicked!")

    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    window = QWidget()
    window.setWindowTitle("3 Button Example")

    # Create a layout
    layout = QVBoxLayout()

    # Create buttons and add them to the layout
    button1 = QPushButton("Menu")
    button1.clicked.connect(lambda: buttons.Menu())
    layout.addWidget(button1)

    button2 = QPushButton("AI Solver")
    button2.clicked.connect(lambda: buttons.AI_Solve())
    layout.addWidget(button2)

    button3 = QPushButton("Manual")
    button3.clicked.connect(lambda: buttons.Manual())
    layout.addWidget(button3)

    # Set the layout for the main window
    window.setLayout(layout)

    # Show the window
    window.show()
    sys.exit(app.exec_())