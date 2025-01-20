from gpiozero import Button
from signal import pause

# Pin numbers
BUTTON_PIN_1 = Button(4, pull_up=True)
BUTTON_PIN_2 = Button(17, pull_up=True)
BUTTON_PIN_3 = Button(20, pull_up=True)

# Callbacks
def button1_pressed():
    print("Button 1 pressed")

def button2_pressed():
    print("Button 2 pressed")

def button3_pressed():
    print("Button 3 pressed")

# Assign callbacks
BUTTON_PIN_1.when_pressed = button1_pressed
BUTTON_PIN_2.when_pressed = button2_pressed
BUTTON_PIN_3.when_pressed = button3_pressed

print("Press the buttons (Ctrl+C to exit)")
pause()  # Keeps the program running
