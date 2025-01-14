import RPi.GPIO as GPIO
import time

# Define GPIO pins connected to the A, B, C, D inputs of CD4511BE
BCD_PINS = {
    "A": 26,  # GPIO17
    "B": 16,  # GPIO27
    "C": 20,  # GPIO22
    "D": 21   # GPIO23
}

def setup():
    """Setup GPIO pins."""
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    for pin in BCD_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def display_digit(digit):
    """
    Display a digit (0-9) on the 7-segment display.

    :param digit: int, the digit to display (0-9).
    """
    if digit < 0 or digit > 9:
        print("Invalid digit: Only 0-9 are supported.")
        return
    
    # Convert digit to 4-bit BCD
    bcd = [int(x) for x in f"{digit:04b}"]
    for i, pin in enumerate(BCD_PINS.values()):
        GPIO.output(pin, bcd[i])

def cleanup():
    """Cleanup GPIO pins."""
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            for i in range(10):  # Cycle through digits 0-9
                display_digit(i)
                time.sleep(1)  # Display each digit for 1 second
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        cleanup()
