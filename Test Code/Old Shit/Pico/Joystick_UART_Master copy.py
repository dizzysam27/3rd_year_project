import serial
import time

# Start by importing all the details needed for this
import math
import time
import pantilthat

def servo(a):
# This line will create a endless loop
#while True:
    # Get the time in seconds
    #t = time.time()
 
    # Generate an angle using a sine wave (-1 to 1) multiplied by 90 (-90 to 90)
    #a = math.sin(t * 2) * 90
   
    # Cast a to int for v0.0.2

    a = float(a)

    
    # These functions require a number between 90 and -90, then it will snap either the pan or tilt servo to that number in degrees 
    pantilthat.pan(a)
    pantilthat.tilt(a)
 
    # Two decimal places is quite enough!
    print(round(a,2))
 
    # Sleep for a bit so we're not hammering the HAT with updates
    time.sleep(0.1)


# Open UART0 (ttyAMA0) on the Raspberry Pi (ensure UART is enabled)
uart0 = serial.Serial('/dev/serial1', 9600, timeout=1)


# Function to read data from Pico
def read_data_uart0():
    if uart0.in_waiting > 0:
        return uart0.read(uart0.in_waiting).decode('utf-8')
        
    return None

# Example usage
try:
    while True:
        # Read data from Pico
        response_uart0 = read_data_uart0()
        print(f"{response_uart0}")

   
        
        time.sleep(0.01)  # Delay before sending next message

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    uart0.close()
