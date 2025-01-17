import time
import threading
from Control_Panel import MODE_SELECTION, LCD1602,LCD1602_WRITE
import tkinter as tk
buttons = MODE_SELECTION()
# Function to be called when buttons are clicked
def on_button_click(button_number):
    print(f"Button {button_number} clicked!")

# Create the main window
root = tk.Tk()
root.title("3 Button Example")

# Create buttons and pack them into the window
button1 = tk.Button(root, text="Menu", command=lambda: buttons.Menu())
button1.pack(padx=10)

button2 = tk.Button(root, text="AI Solve", command=lambda: buttons.AI_Solve())
button2.pack(padx=10)

button3 = tk.Button(root, text="Manual", command=lambda: buttons.Manual())
button3.pack(padx=10)

# Start the main event loop


# Start the application loop




def main():

    buttons = MODE_SELECTION()
    lcd = LCD1602_WRITE()
    buttons.event_detect()
    buttons.Menu()
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
        import sys

        # Function to be called when buttons are clicked
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













    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        buttons.cleanup()
        print("GPIO cleanup completed.")

if __name__ == "__main__":
    main()
